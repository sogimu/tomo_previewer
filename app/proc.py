import os
import multiprocessing
import subprocess

import cherrypy

from settings import Settings
from models import SliceMap

class SlicemapProcess(multiprocessing.Process):
    def __init__(self, path):
        super(SlicemapProcess, self).__init__()
        self.path = path

    def run(self):
        import time
        self.sf = SlicemapFactory()
        self.slicemap_obj = self.sf.get( self.path )

        cherrypy.log("SlicemapProcess: Start(): %s. " % self.slicemap_obj.path_to_slices)
        slicemap_creator_process = "python slice_map_creator/run.py create -sp '%s' -rc '%s' -sms '%s' -smpg '%s' -smpr '%s' -cp '%s' -snf '%s' -smnf '%s' -cnf '%s'" % (
            self.slicemap_obj.path_to_slices, 
            "%sx%s" % (self.slicemap_obj.rows, self.slicemap_obj.cols), 
            "%sx%s" % (self.slicemap_obj.width, self.slicemap_obj.height), 
            self.slicemap_obj.path_to_slicemaps_config_and_cache,
            os.path.relpath( self.slicemap_obj.path_to_slicemaps_config_and_cache, Settings.IMPORT_PATH ),
            self.slicemap_obj.path_to_slicemaps_config_and_cache,
            self.slicemap_obj.slice_name_format,
            self.slicemap_obj.slicemap_name_format,
            self.slicemap_obj.config_name_format
        )
        cherrypy.log(slicemap_creator_process)

        start_time = time.time()

        self.slicemap_obj.done = False
        self.slicemap_obj.creation_going = True
        self.slicemap_obj.save()

        try:
            subprocess.call(slicemap_creator_process, shell=True)
        except:
            self.slicemap_obj.has_error = True
            self.slicemap_obj.save()

        finally:
            self.slicemap_obj.done = True
            self.slicemap_obj.creation_going = False
            self.slicemap_obj.time = time.time() - start_time

            self.slicemap_obj.save()

        cherrypy.log("SlicemapProcess: Stop(): %s. " % self.slicemap_obj.path_to_slices)

class SlicemapsProcess(multiprocessing.Process):
    def __init__(self, paths_for_processing):
        super(SlicemapsProcess, self).__init__()
        self.paths_for_processing = paths_for_processing

    def run(self):
        cherrypy.log("SlicemapsProcess: Start(): %s. " % self.paths_for_processing)

        def processPaths(paths):
            slicemapProcess_pull = []
            for path in paths:
                slicemapsProc = SlicemapProcess(path)
                slicemapsProc.start()
                slicemapProcess_pull.append(slicemapsProc)

            for slicemapProc in slicemapProcess_pull:
                slicemapProc.join()

        begin = 0
        end = 0

        while True:
            begin = end
            if( begin + Settings.SLICEMAP_PROCESSING_THREADS_NUMBER > len(self.paths_for_processing) ):
                end = len(self.paths_for_processing)
            else:
                end = begin + Settings.SLICEMAP_PROCESSING_THREADS_NUMBER

            group_of_paths_for_processing = self.paths_for_processing[ begin : end ]
            processPaths( group_of_paths_for_processing )

            if end == len(self.paths_for_processing):
                break
        cherrypy.log("SlicemapsProcess: Stop(): %s. " % self.paths_for_processing)


class SlicemapFactory():
    def __init__(self):
        pass

    def init(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height):
        slicemap_obj = SliceMap(path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height)
        slicemap_obj.save()
        return slicemap_obj

    def processOne(self, path_for_processing):
        slicemapProc = SlicemapProcess(path_for_processing)
        slicemapProc.start()

    def processMany(self, paths_for_processing):
        if len(paths_for_processing) > 0:
            slicemapsProc = SlicemapsProcess(paths_for_processing)
            slicemapsProc.start()

    def remove(self, path_to_slices):
        pass

    def get(self, path_to_slices):
        slicemap_obj = SliceMap(path_to_slices,"","","",0,0,0,0)
        slicemap_obj.refresh()

        return slicemap_obj

    def isExist(self, path_to_slices):
        path_to_cache = os.path.join( 
            os.path.abspath( 
                os.path.join(
                    path_to_slices, 
                    ".."
                )
            ), 
            Settings.CACHE_FOLDER_NAME
        )

        slices_dir_name = os.path.relpath(
            path_to_slices,
            os.path.join(
                path_to_slices, 
                ".."
            )
        )

        path_to_slicemaps_config_and_cache = os.path.join(
            path_to_cache,
            Settings.PROCESSING_CACHE_FOLDER_NAME,
            slices_dir_name
        )

        file_name = os.path.join(
            path_to_slicemaps_config_and_cache,
            Settings.PROCESSING_CONFIG_NAME_FORMAT.format( slices_dir_name )
        )

        return os.path.isfile(file_name)