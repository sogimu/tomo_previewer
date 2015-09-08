#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import sys
import os
import argparse
import json
import cherrypy

from app.settings import Settings
from app.proc import SlicemapFactory
from app.utils import Utils

version = "0.9.0"

def input_path(filePath):
    if not(bool(os.path.isdir(filePath))):
        msg = "%r bad path " % filePath
        raise argparse.ArgumentTypeError(msg)
    return filePath

def createParser ():
    # Создаем класс парсера
    parser = argparse.ArgumentParser(
            prog = 'Trigger slicemap creation',
            description = '''Application for triggering creation slicemaps from slices of tomographic data''',
            epilog = '''Lizin Aleksandr Sergeevich aka Sogimu, email: sogimu@nxt.ru, 2015.''',
            add_help = False
            )
 
    # Создаем группу параметров для родительского парсера,
    # ведь у него тоже должен быть параметр --help / -h
    parent_group = parser.add_argument_group (title='Settings')
 
    parent_group.add_argument ('--help', '-h', action='help', help='Help')

    parent_group.add_argument ('--version', '-v',
                action='version',
                help = 'Print version',
                version='%(prog)s {}'.format (version))

    # Создаем группу подпарсеров
    subparsers = parser.add_subparsers (dest = 'command',
            title = 'Commands',
            description = 'Commands for first param %(prog)s')

    # Создаем парсер для команды run
    create_parser = subparsers.add_parser ('run',
            add_help = False,
            help = 'Run command "Trigger_slicemap_creation"',
            description = '''Command for triggering slicemaps creation.''')
 
    # Создаем новую группу параметров
    create_group = create_parser.add_argument_group (title='Settings')
 
    # Добавляем параметры
    create_group.add_argument ('-ip', '--import-path', type=input_path, default=Settings.IMPORT_PATH,
            help = 'Path to directory with tomographic data (slices, images).')

    create_group.add_argument ('-snf', '--slice-path-format', type=str, default=Settings.SLICE_PATH_FORMAT,
            help = r'Format of slices(images) path. Example: [\D,\d]*?(tomo_data.*slices[\D,\d]*?/[^/]+\d+.tif)')

    create_group.add_argument ('-f', '--force', type=bool, default=False,
            help = r'Force creation even slicemaps already created')

    create_group.add_argument ('--help', '-h', action='help', help='Help')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    if namespace.command   == "run":
        if( namespace.force == False ):
            paths_for_processing = Utils.get_slices_dirs_for_processing( namespace.import_path, namespace.slice_path_format )
        else:
            paths_for_processing = Utils.get_slices_dirs( namespace.import_path, namespace.slice_path_format )

        sf = SlicemapFactory()
        sf.processMany( paths_for_processing )

        cherrypy.log( "triggered: %s, number_of_new_volumes: %s, paths_to_the_new_volumes: %s" % (True, len(paths_for_processing), paths_for_processing) )

    else:
        parser.print_help()