import sys
import os

class Settings():
	URL_PREFIX = "http://"

	URL = "ipecluster7.ipe.kit.edu"
	# URL = "0.0.0.0"
	PORT = 8080
	IMPORT_PATH = "./data"
	CACHE_FOLDER_NAME = "cache"
	PROCESSING_CACHE_FOLDER_NAME = "slicemaps"
	PROCESSING_CONFIG_NAME_FORMAT = "processing_config.json"
	SLICE_NAME_FORMAT = "^(.*\d+.tif)$"
	SLICE_PATH_FORMAT = ".*\/tomo_data\/.*slices.*\/(.*\d+.tif)"
	SLICEMAP_NAME_FORMAT = "slicemap{0}.jpeg"
	VISUALIZATION_CONFIG_NAME_FORMAT = "visualization_config.json"
	SLICEMAP_ROWS = 10
	SLICEMAP_COLS = 10
	SLICEMAP_SIZE_WIDTH = 4096
	SLICEMAP_SIZE_HEIGHT = 4096
	SLICEMAP_PROCESSING_THREADS_NUMBER = 4