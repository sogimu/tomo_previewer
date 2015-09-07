import os
import re

import cherrypy

from settings import Settings
from proc import SlicemapFactory

class Utils():
    @staticmethod
    def get_slices_dirs(path_to_data, slice_name_format):
        def get_slices_dirs_recurs(path_to_data, slice_name_format, pathes):
            files_names = sorted( os.listdir(path_to_data) )

            is_dir_with_slices = False
            for file_name in files_names:
                if os.path.isdir( os.path.join(path_to_data, file_name) ):
                    get_slices_dirs_recurs( os.path.join(path_to_data, file_name), slice_name_format, pathes)

                else:
                    if re.match(slice_name_format, file_name):
                        is_dir_with_slices = True
                        break
                    
            if(is_dir_with_slices):
                pathes.append( path_to_data )

        pathes = []
        get_slices_dirs_recurs(path_to_data, slice_name_format, pathes)
        return pathes

    @staticmethod
    def get_slices_dirs_for_processing(path_to_data, slice_name_format):
        potential_paths_for_processing = Utils.get_slices_dirs(path_to_data, slice_name_format)

        sf = SlicemapFactory()

        paths_for_processing = []

        for potential_path in potential_paths_for_processing:
            if( sf.isExist( potential_path ) == True):
                slicemap_obj = sf.get( potential_path )
                if( (slicemap_obj.done == False or os.path.isdir( slicemap_obj.path_to_slicemaps_config_and_cache ) == False) and slicemap_obj.creation_going == False ):
                    paths_for_processing.append( potential_path )

            else:
                slicemap_obj = sf.init(potential_path, Settings.SLICE_NAME_FORMAT, Settings.SLICEMAP_NAME_FORMAT, Settings.VISUALIZATION_CONFIG_NAME_FORMAT, Settings.SLICEMAP_ROWS, Settings.SLICEMAP_COLS, Settings.SLICEMAP_SIZE_WIDTH, Settings.SLICEMAP_SIZE_HEIGHT)
                paths_for_processing.append( potential_path )

        return paths_for_processing

    @staticmethod
    def create_link_for_preview(path_to_slices):
        return Settings.URL_PREFIX + Settings.URL + ":" + str(Settings.PORT) + "/show_preview?path_to_slices=" + path_to_slices

    @staticmethod
    def get_slicemaps(path_to_data, slice_name_format):
        potential_paths_for_processing = Utils.get_slices_dirs(path_to_data, slice_name_format)

        sf = SlicemapFactory()

        processed_slicedmaps = []

        for potential_path in potential_paths_for_processing:
            if( sf.isExist( potential_path ) == True):
                slicemap_obj = sf.get( potential_path )
                processed_slicedmaps.append( slicemap_obj )

        return processed_slicedmaps