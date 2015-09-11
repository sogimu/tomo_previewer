import os
import json
import re
import math

from settings import Settings

import proc

class SliceMap():
    path_to_slices = ""

    path_to_cache = ""
    slices_dir_name = ""
    path_to_file = ""

    done = False
    creation_going = False
    has_error = False
    time = -1

    slice_name_format = ""

    slicemap_name_format = ""
    config_name_format = ""
    
    slices_number = -1
    slicemaps_number = -1

    rows = -1
    cols = -1

    width  = -1
    height = -1

    path_to_slicemaps_config_and_cache = ""

    @property
    def path_to_visualization_config_global(self):
        return os.path.join( self.path_to_slicemaps_config_and_cache, self.config_name_format)

    @property
    def path_to_visualization_config_relative(self):
        return os.path.join( os.path.relpath( self.path_to_slicemaps_config_and_cache, Settings.IMPORT_PATH ), self.config_name_format)

    def __init__(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_number, width, height):
        self.path_to_slices = path_to_slices

        self.done = False
        self.creation_going = False
        self.has_error = False
        self.time = -1

        self.slice_name_format = slice_name_format
        self.slicemap_name_format = slicemap_name_format
        self.config_name_format = config_name_format

        slices_number = 0
        for path_to_file in os.listdir( path_to_slices ):
            if( re.match( slice_name_format, path_to_file ) ):
                slices_number = slices_number + 1
        self.slices_number = slices_number

        self.slicemaps_number = slicemaps_number

        self.rows = int( math.ceil( math.sqrt( math.ceil( float(self.slices_number) / float(self.slicemaps_number) ) ) ) )
        self.cols = self.rows

        self.width = width
        self.height = height

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
            Settings.PREVIEWS_CACHE_FOLDER_NAME,
            self.slices_dir_name,
            str(int(self.width)) + "x" + str(int(self.width)) + "_" + str(int(self.slicemaps_number))

        )

        self.path_to_file = os.path.join(
            self.path_to_slicemaps_config_and_cache,
            Settings.SLICEMAPS_CONFIG_NAME
        )

    @staticmethod
    def getEmpty():
        return SliceMap("/", "", "", "", 1, 1, 1)

    def to_array(self):
        model_python_array = {
            "path_to_slices": self.path_to_slices,
            "path_to_cache": self.path_to_cache,
            "slices_dir_name": self.slices_dir_name,
            "path_to_file": self.path_to_file,
            "done": self.done,
            "creation_going": self.creation_going,
            "has_error": self.has_error,
            "time": self.time,
            "slice_name_format": self.slice_name_format,
            "slicemap_name_format": self.slicemap_name_format,
            "config_name_format": self.config_name_format,
            "rows": self.rows,
            "cols": self.cols,
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

        config_file = open( self.path_to_file, "w" );
        config_file.write( model_json_array )
        config_file.close()

    def refresh(self):
        self.read( self.path_to_file )

    def read(self, path):
        config_file = open( path, "r" );
        config_file_python_array = json.loads( config_file.read() )

        self.path_to_slices = config_file_python_array["path_to_slices"]

        self.path_to_cache = config_file_python_array["path_to_cache"]
        self.slices_dir_name = config_file_python_array["slices_dir_name"]
        self.path_to_file = config_file_python_array["path_to_file"]

        self.done = config_file_python_array["done"]
        self.creation_going = config_file_python_array["creation_going"]
        self.has_error = config_file_python_array["has_error"]
        self.time = config_file_python_array["time"]

        self.slice_name_format = config_file_python_array["slice_name_format"]
        self.slicemap_name_format = config_file_python_array["slicemap_name_format"]
        self.config_name_format = config_file_python_array["config_name_format"]
        
        
        self.rows = config_file_python_array["rows"]
        self.cols = config_file_python_array["cols"]

        self.width  = config_file_python_array["width"]
        self.height = config_file_python_array["height"]

        self.path_to_slicemaps_config_and_cache = config_file_python_array["path_to_slicemaps_config_and_cache"]

        config_file.close()


    def __repr__(self):
        return '<SliceMap path_to_slices={}, path_to_cache={}, slices_dir_name={}, path_to_file={}, done={}, creation_going={}, has_error={}, width={}, height={}, time={}, slice_name_format={}, slicemap_name_format={}, config_name_format={}>. rows={}, cols={}, path_to_slicemaps_config_and_cache={}'.format(self.path_to_slices, self.path_to_cache, self.slices_dir_name, self.path_to_file, self.done, self.creation_going, self.has_error, self.width, self.height, self.time, self.slice_name_format, self.slicemap_name_format, self.config_name_format, self.rows, self.cols, self.slices_number, self.path_to_slicemaps_config_and_cache)

class Preview():
    path_to_slices = ""

    path_to_cache = ""
    slices_dir_name = ""
    path_to_file = ""
    path_to_dir = ""

    config_name_format = ""

    slices_number = -1

    slicemaps_numbers = []
    slicemaps_sizes = []
    slicemaps_info = []

    @property
    def done(self):
        sf = proc.SlicemapFactory()

        slicemaps_done_number = 0

        for slicemap_info in self.slicemaps_info:
            if( sf.isExist( slicemap_info["path_to_processing_config"] ) ):
                slicemap_obj = sf.get( slicemap_info["path_to_processing_config"] )
                if(slicemap_obj.done == True):
                    slicemaps_done_number = slicemaps_done_number + 1

        return slicemaps_done_number == len(self.slicemaps_info) if True else False

    @property
    def creation_going(self):
        sf = proc.SlicemapFactory()

        is_creation_going = False

        for slicemap_info in self.slicemaps_info:
            if( sf.isExist( slicemap_info["path_to_processing_config"] ) ):
                slicemap_obj = sf.get( slicemap_info["path_to_processing_config"] )
                if(slicemap_obj.creation_going == True):
                    is_creation_going = True
                    break

        return is_creation_going

    @property
    def has_error(self):
        sf = proc.SlicemapFactory()

        has_error = False

        for slicemap_info in self.slicemaps_info:
            if( sf.isExist( slicemap_info["path_to_processing_config"] ) ):
                slicemap_obj = sf.get( slicemap_info["path_to_processing_config"] )
                if(slicemap_obj.creation_going == True):
                    has_error = True
                    break

        return has_error

    @property
    def time(self):
        sf = proc.SlicemapFactory()

        sum_time = 0

        for slicemap_info in self.slicemaps_info:
            if( sf.isExist( slicemap_info["path_to_processing_config"] ) ):
                slicemap_obj = sf.get( slicemap_info["path_to_processing_config"] )
                if(slicemap_obj.done == True):
                    sum_time = sum_time + slicemap_obj.time

        return sum_time

    @property
    def path_to_config_global(self):
        return os.path.join( self.path_to_dir, self.config_name_format)

    @property
    def path_to_config_relative(self):
        return os.path.join( os.path.relpath( self.path_to_dir, Settings.IMPORT_PATH ), self.config_name_format)

    def __init__(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, slicemaps_numbers, slicemaps_sizes, slicemaps_info):
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

        self.path_to_dir = os.path.join(
            self.path_to_cache,
            Settings.PREVIEWS_CACHE_FOLDER_NAME,
            self.slices_dir_name
        )

        self.path_to_file = os.path.join(
            self.path_to_dir,
            Settings.PREVIEW_CONFIG_NAME
        )

        # self.done = False
        # self.creation_going = False
        # self.has_error = False
        # self.time = -1

        self.slice_name_format = slice_name_format
        self.slicemap_name_format = slicemap_name_format
        self.config_name_format = config_name_format

        slices_number = 0
        for path_to_file in os.listdir( path_to_slices ):
            if( re.match( slice_name_format, path_to_file ) ):
                slices_number = slices_number + 1
        self.slices_number = slices_number
         
        self.slicemaps_numbers = slicemaps_numbers
        self.slicemaps_sizes = slicemaps_sizes
        self.slicemaps_info = slicemaps_info

    def to_array(self):
        model_python_array = {
            "path_to_slices": self.path_to_slices,
            "path_to_cache": self.path_to_cache,
            "slices_dir_name": self.slices_dir_name,
            "path_to_dir": self.path_to_dir,
            "path_to_file": self.path_to_file,
            "done": self.done,
            "creation_going": self.creation_going,
            "has_error": self.has_error,
            "time": self.time,

            "slice_name_format": self.slice_name_format,
            "slicemap_name_format": self.slicemap_name_format,
            "config_name_format": self.config_name_format,
            "slicemaps_numbers": self.slicemaps_numbers,
            "slicemaps_sizes": self.slicemaps_sizes,
            "slicemaps_info": self.slicemaps_info
        }

        return model_python_array

    def save(self):
        model_python_array = self.to_array()
        model_json_array = json.dumps( model_python_array )

        if( not( os.path.isdir(self.path_to_dir) ) ):
            os.makedirs( self.path_to_dir )

        config_file = open( self.path_to_file, "w" );
        config_file.write( model_json_array )
        config_file.close()

    def refresh(self):
        config_file = open( self.path_to_file, "r" );
        config_file_python_array = json.loads( config_file.read() )

        self.path_to_slices = config_file_python_array["path_to_slices"]
        self.path_to_cache = config_file_python_array["path_to_cache"]
        self.slices_dir_name = config_file_python_array["slices_dir_name"]
        self.path_to_dir = config_file_python_array["path_to_dir"]
        self.path_to_file = config_file_python_array["path_to_file"]
        # self.done = config_file_python_array["done"]
        # self.creation_going = config_file_python_array["creation_going"]
        # self.has_error = config_file_python_array["has_error"]
        # self.time = config_file_python_array["time"]

        self.slice_name_format = config_file_python_array["slice_name_format"]
        self.slicemap_name_format = config_file_python_array["slicemap_name_format"]
        self.config_name_format = config_file_python_array["config_name_format"]
        self.slicemaps_numbers = config_file_python_array["slicemaps_numbers"]
        self.slicemaps_sizes = config_file_python_array["slicemaps_sizes"]
        self.slicemaps_info = config_file_python_array["slicemaps_info"]

        config_file.close()

    # def __repr__(self):
        # return '<Preview path_to_slices={}, path_to_cache={}, slices_dir_name={}, path_to_file={}, done={}, creation_going={}, has_error={}, width={}, height={}, time={}, slice_name_format={}, slicemap_name_format={}, config_name_format={}>. rows={}, cols={}, path_to_slicemaps_config_and_cache={}'.format(self.path_to_slices, self.path_to_cache, self.slices_dir_name, self.path_to_file, self.done, self.creation_going, self.has_error, self.width, self.height, self.time, self.slice_name_format, self.slicemap_name_format, self.config_name_format, self.rows, self.cols, self.slices_number, self.path_to_slicemaps_config_and_cache)