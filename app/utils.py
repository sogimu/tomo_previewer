import os
import re

import cherrypy

from settings import Settings
from proc import SlicemapFactory, PreviewFactory

class Utils():
    @staticmethod
    def get_slices_dirs(path_to_data, slice_path_format):
        def get_slices_dirs_recurs(path_to_data, slice_name_format, pathes):
            files_names = sorted( os.listdir(path_to_data) )

            is_dir_with_slices = False
            for file_name in files_names:
                if os.path.isdir( os.path.join(path_to_data, file_name) ):
                    get_slices_dirs_recurs( os.path.join(path_to_data, file_name), slice_name_format, pathes)

                else:
                    file_path_absolute = os.path.join( path_to_data, file_name )
                    if re.match(slice_path_format, file_path_absolute):
                        is_dir_with_slices = True
                        break
                    
            if(is_dir_with_slices):
                pathes.append( path_to_data )

        pathes = []
        get_slices_dirs_recurs(path_to_data, slice_path_format, pathes)
        return pathes

    @staticmethod
    def get_previews_for_processing(path_to_data, slice_path_format, process_all=False):
        potential_paths_for_processing = Utils.get_slices_dirs(path_to_data, slice_path_format)

        pf = PreviewFactory()

        previews_for_processing = []

        for potential_path in potential_paths_for_processing:
            if( pf.isExist( potential_path ) == True):
                preview_obj = pf.get( potential_path )
                if( preview_obj.done == False and preview_obj.creation_going == False or process_all ):
                    previews_for_processing.append( preview_obj )

            else:
                preview_obj = pf.init( potential_path, Settings.SLICE_NAME_FORMAT, Settings.SLICEMAP_NAME_FORMAT, Settings.PREVIEW_CONFIG_NAME, Settings.PREVIEW_SLICEMAPS_NUMBERS, Settings.PREVIEW_SLICEMAPS_SIZES )
                previews_for_processing.append( preview_obj )

        return previews_for_processing

    @staticmethod
    def create_link_for_preview(path_to_slices):
        return Settings.URL_PREFIX + Settings.URL + ":" + str(Settings.PORT) + "/show_preview?path_to_slices=" + path_to_slices

    @staticmethod
    def get_previews(path_to_data, slice_path_format):
        potential_paths_for_processing = Utils.get_slices_dirs(path_to_data, slice_path_format)

        pf = PreviewFactory()

        processed_slicemaps = []

        for potential_path in potential_paths_for_processing:
            if( pf.isExist( potential_path ) == True):
                slicemap_obj = pf.get( potential_path )
                processed_slicemaps.append( slicemap_obj )

        return processed_slicemaps