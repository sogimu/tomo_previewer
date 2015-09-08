import os
import json

from settings import Settings

class SliceMap():
    path_to_slices = ""

    path_to_cache = ""
    slices_dir_name = ""
    file_name = ""

    done = False
    creation_going = False
    has_error = False
    time = -1

    slice_name_format = ""
    slicemap_name_format = ""
    config_name_format = ""
    
    rows = -1
    cols = -1
    slices_number = -1

    width  = -1
    height = -1

    path_to_slicemaps_config_and_cache = ""

    @property
    def path_to_config_global(self):
        return os.path.join( self.path_to_slicemaps_config_and_cache, self.config_name_format)

    @property
    def path_to_config_relative(self):
        return os.path.join( os.path.relpath( self.path_to_slicemaps_config_and_cache, Settings.IMPORT_PATH ), self.config_name_format)

    def __init__(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height):
        self.path_to_slices = path_to_slices

        self.path_to_cache = os.path.join( 
            os.path.abspath( 
                os.path.join(
                    path_to_slices, 
                    ".."
                )
            ), 
            Settings.CACHE_FOLDER_NAME
        )

        self.slices_dir_name = os.path.relpath(
            path_to_slices,
            os.path.join(
                path_to_slices, 
                ".."
            )
        )

        self.path_to_slicemaps_config_and_cache = os.path.join(
            self.path_to_cache,
            Settings.PROCESSING_CACHE_FOLDER_NAME,
            self.slices_dir_name
        )

        self.file_name = os.path.join(
            self.path_to_slicemaps_config_and_cache,
            Settings.PROCESSING_CONFIG_NAME_FORMAT.format( self.slices_dir_name )
        )

        self.done = False
        self.creation_going = False
        self.has_error = False
        self.time = -1

        self.slice_name_format = slice_name_format
        self.slicemap_name_format = slicemap_name_format
        self.config_name_format = config_name_format
        self.rows = rows
        self.cols = cols
        self.slices_number = self.rows * self.cols
        self.width = width
        self.height = height

    def to_array(self):
        model_python_array = {
            "path_to_slices": self.path_to_slices,
            "path_to_cache": self.path_to_cache,
            "slices_dir_name": self.slices_dir_name,
            "file_name": self.file_name,
            "done": self.done,
            "creation_going": self.creation_going,
            "has_error": self.has_error,
            "time": self.time,
            "slice_name_format": self.slice_name_format,
            "slicemap_name_format": self.slicemap_name_format,
            "config_name_format": self.config_name_format,
            "rows": self.rows,
            "cols": self.cols,
            "slices_number": self.slices_number,
            "width": self.width,
            "height": self.height,
            "path_to_slicemaps_config_and_cache": self.path_to_slicemaps_config_and_cache
        }

        return model_python_array

    def save(self):
        model_python_array = self.to_array()
        model_json_array = json.dumps( model_python_array )

        if( not( os.path.isdir(self.path_to_slicemaps_config_and_cache) ) ):
            os.makedirs( self.path_to_slicemaps_config_and_cache )

        cache_config_file = open( self.file_name, "w" );
        cache_config_file.write( model_json_array )
        cache_config_file.close()

    def refresh(self):
        cache_config_file = open( self.file_name, "r" );
        cache_config_file_python_array = json.loads( cache_config_file.read() )

        self.path_to_slices = cache_config_file_python_array["path_to_slices"]

        self.path_to_cache = cache_config_file_python_array["path_to_cache"]
        self.slices_dir_name = cache_config_file_python_array["slices_dir_name"]
        self.file_name = cache_config_file_python_array["file_name"]

        self.done = cache_config_file_python_array["done"]
        self.creation_going = cache_config_file_python_array["creation_going"]
        self.has_error = cache_config_file_python_array["has_error"]
        self.time = cache_config_file_python_array["time"]

        self.slice_name_format = cache_config_file_python_array["slice_name_format"]
        self.slicemap_name_format = cache_config_file_python_array["slicemap_name_format"]
        self.config_name_format = cache_config_file_python_array["config_name_format"]
        
        
        self.rows = cache_config_file_python_array["rows"]
        self.cols = cache_config_file_python_array["cols"]
        self.slices_number = cache_config_file_python_array["slices_number"]

        self.width  = cache_config_file_python_array["width"]
        self.height = cache_config_file_python_array["height"]

        self.path_to_slicemaps_config_and_cache = cache_config_file_python_array["path_to_slicemaps_config_and_cache"]

        cache_config_file.close()

    def __repr__(self):
        return '<SliceMap path_to_slices={}, path_to_cache={}, slices_dir_name={}, file_name={}, done={}, creation_going={}, has_error={}, width={}, height={}, time={}, slice_name_format={}, slicemap_name_format={}, config_name_format={}>. rows={}, cols={}, slices_number={}, path_to_slicemaps_config_and_cache={}'.format(self.path_to_slices, self.path_to_cache, self.slices_dir_name, self.file_name, self.done, self.creation_going, self.has_error, self.width, self.height, self.time, self.slice_name_format, self.slicemap_name_format, self.config_name_format, self.rows, self.cols, self.slices_number, self.path_to_slicemaps_config_and_cache)