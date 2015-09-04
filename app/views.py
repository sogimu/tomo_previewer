import os
import glob
import json
import subprocess
import re

import cherrypy
from cherrypy.lib import static

from models import SliceMap
from settings import Settings
from proc import SlicemapFactory

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader( os.path.join('app', 'templates') ))


def load_template(template_name):
    """
    load template
    """
    template_path = os.path.join(template_name)
    template = env.get_template(template_path)
    return template

def render_template(template_name, context):
    """
    open template and render using context
    """
    template = load_template(template_name)
    return template.render(context)

class App(object):
    @cherrypy.expose
    def index(self):
        return render_template('index.html', {'salutation': 'Hello', 'target': 'World'})

    @cherrypy.expose
    def render(self, filepath):
        sf = SlicemapFactory()

        if( sf.isExist( filepath ) == True):
            smo = sf.get( filepath )
            print(smo)
            return render_template('render.html', {'slicemap_obj': smo})
        else:
            return render_template('404.html', {'info': "Preview for volume on the path: %s not found." % filepath})


    @cherrypy.expose
    def trigger_slicemap_creation(self):
        def get_slices_dirs(start_path, slice_name_format, pathes):
            files_names = sorted( os.listdir(start_path) )

            is_dir_with_slices = False
            for file_name in files_names:
                if os.path.isdir( os.path.join(start_path, file_name) ):
                    # if( Settings.SLICEMAP_FOLDER_NAME not in os.listdir( os.path.join(start_path, file_name) ) ):
                    get_slices_dirs( os.path.join(start_path, file_name), slice_name_format, pathes)

                else:
                    if re.match(slice_name_format, file_name):
                        is_dir_with_slices = True
                        break
                    
            if(is_dir_with_slices):
                print("get_slices_dirs: Dir have slices: %s" % start_path)
                pathes.append( start_path )

        potential_paths_for_processing = []
        paths_for_processing = []
        get_slices_dirs(Settings.IMPORT_PATH, Settings.SLICE_NAME_FORMAT, potential_paths_for_processing)

        print("potential_paths_for_processing: ", potential_paths_for_processing)

        slicemaps_objects_for_processing = []

        sf = SlicemapFactory()

        for potential_path in potential_paths_for_processing:
            path_to_slicemaps_and_config = os.path.join(Settings.EXPORT_PATH, potential_path)

            # if(potential_path == "/home/sogimu/data/sample-001/slices_8bit"):
            #     import pdb
            #     pdb.set_trace()

            if( sf.isExist( potential_path ) == True):
                smo = sf.get( potential_path )        
                if( (smo.done == False or os.path.isdir(path_to_slicemaps_and_config) == False) and smo.creation_going == False ):
                    slicemaps_objects_for_processing.append( smo )
                    paths_for_processing.append( potential_path )

            else:
                smo = sf.init(potential_path, Settings.SLICE_NAME_FORMAT, Settings.SLICEMAP_NAME_FORMAT, Settings.CONFIG_NAME_FORMAT, Settings.SLICEMAP_ROWS, Settings.SLICEMAP_COLS, Settings.SLICEMAP_SIZE_WIDTH, Settings.SLICEMAP_SIZE_HEIGHT, path_to_slicemaps_and_config)
                slicemaps_objects_for_processing.append( smo )
                paths_for_processing.append( potential_path )

        print("paths_for_processing: ", paths_for_processing)

        sf.processMany( paths_for_processing )

        jsonDump = json.dumps({
            'triggered': True,
            'number_of_new_volumes': len(paths_for_processing),
            'paths_to_the_new_volumes': paths_for_processing
        })

        return render_template('trigger_slicemap_creation.html', {'status': jsonDump})