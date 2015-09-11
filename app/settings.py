import sys
import os

class Settings():
	URL_PREFIX = "http://"

	URL = "ipecluster7.ipe.kit.edu"
	# URL = "ankaastor2.anka.kit.edu"
	PORT = 8080
	IMPORT_PATH = "./data"
	CACHE_FOLDER_NAME = "cache"
	PREVIEWS_CACHE_FOLDER_NAME = "previews"
	PREVIEW_CONFIG_NAME = "preview_config.json"
	SLICEMAPS_CONFIG_NAME = "slicemaps_config.json"
	VISUALIZATION_CONFIG_NAME = "visualization_config.json"
	SLICE_NAME_FORMAT = "^(.*\d+.tif)$"
	SLICE_PATH_FORMAT = ".*\/tomo_data\/.*slices.*\/(.*\d+.tif)"
	SLICEMAP_NAME_FORMAT = "slicemap{0}.jpeg"
	PREVIEW_SLICEMAPS_NUMBERS = [2, 6, 14]
	PREVIEW_SLICEMAPS_SIZES =   ["2048x2048", "4096x4096"]
	PREVIEW_PROCESSING_THREADS_NUMBER = 3