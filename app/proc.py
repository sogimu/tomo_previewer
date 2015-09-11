import os
import multiprocessing
import subprocess
import math

import cherrypy

from settings import Settings
from models import SliceMap, Preview

class SlicemapProcess(multiprocessing.Process):
    def __init__(self, path):
        super(SlicemapProcess, self).__init__()
        self.path = path

    def run(self):
        import time
        self.sf = SlicemapFactory()
        print( self.path )
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
                slicemapsProc = SlicemapProcess( path )
                slicemapsProc.start()
                slicemapProcess_pull.append( slicemapsProc )

            for slicemapProc in slicemapProcess_pull:
                slicemapProc.join()

        begin = 0
        end = 0

        while True:
            begin = end
            if( begin + Settings.PREVIEW_PROCESSING_THREADS_NUMBER > len(self.paths_for_processing) ):
                end = len(self.paths_for_processing)
            else:
                end = begin + Settings.PREVIEW_PROCESSING_THREADS_NUMBER

            group_of_paths_for_processing = self.paths_for_processing[ begin : end ]
            processPaths( group_of_paths_for_processing )

            if end == len(self.paths_for_processing):
                break
        cherrypy.log("SlicemapsProcess: Stop(): %s. " % self.paths_for_processing)


class SlicemapFactory():
    def __init__(self):
        pass

    def init(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_number, width, height):
        slicemap_obj = SliceMap(path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_number, width, height)
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

    def get(self, path_to_object):
        slicemap_obj = SliceMap.getEmpty()
        slicemap_obj.read(path_to_object)

        return slicemap_obj

    def isExist(self, path_to_config):
        return os.path.isfile( path_to_config )

class PreviewFactory():
    def __init__(self):
        pass

    def init(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_numbers, slicemaps_sizes):
        preview_obj = Preview(path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_numbers, slicemaps_sizes, [])

        sf = SlicemapFactory()
        for i in range( 0, len(slicemaps_sizes) ):
            for j in range( 0, len(slicemaps_numbers) ):
                slicemaps_size   = slicemaps_sizes[i]
                slicemaps_number = slicemaps_numbers[j]
                width = slicemaps_size.split("x")[0]
                height = slicemaps_size.split("x")[1]
                slicemap_obj = sf.init( preview_obj.path_to_slices, preview_obj.slice_name_format, preview_obj.slicemap_name_format, Settings.VISUALIZATION_CONFIG_NAME, slicemaps_number, width, height )
                slicemap_obj.save()

                preview_obj.slicemaps_info.append( {"slicemaps_number": slicemaps_number, "slicemaps_size": slicemaps_size, "path_to_processing_config": slicemap_obj.path_to_file, "path_to_visualization_config": slicemap_obj.path_to_visualization_config_relative})

        preview_obj.save()

        return preview_obj

    # def processOne(self, path_for_processing, slicemaps_number, slicemaps_size):
    #     slicemapProc = SlicemapProcess(path_for_processing)
    #     slicemapProc.start()

    def processMany(self, previews):
        if len(previews) > 0:
            pf = PreviewFactory()

            paths_to_slicemaps = []
            for preview in previews:
                paths_to_slicemaps = paths_to_slicemaps + [ slicemap_info["path_to_processing_config"] for slicemap_info in preview.slicemaps_info ]

            slicemapsProc = SlicemapsProcess( paths_to_slicemaps )
            slicemapsProc.start()

    def remove(self, path_to_slices):
        pass

    def get(self, path_to_slices):
        preview_obj = Preview(path_to_slices, "", "", "", [], [], [])
        preview_obj.refresh()

        return preview_obj

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

        path_to_preview = os.path.join(
            path_to_cache,
            Settings.PREVIEWS_CACHE_FOLDER_NAME,
            slices_dir_name
        )

        path_to_file = os.path.join(
            path_to_preview,
            Settings.PREVIEW_CONFIG_NAME.format( slices_dir_name )
        )

        return os.path.isfile(path_to_file)