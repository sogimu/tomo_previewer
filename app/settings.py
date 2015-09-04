import sys
import os

class Settings():
	# @staticmethod
	IMPORT_PATH = "/home/sogimu/data/"
	EXPORT_PATH = "/home/sogimu/slicemaps"
	# SLICEMAP_FOLDER_NAME = "slicemaps"
	SLICE_NAME_FORMAT = "^([\D,\d]+\d+.tif)$"
	SLICEMAP_NAME_FORMAT = "slicemap{0}.jpeg"
	CONFIG_NAME_FORMAT = "slicemap_config.json"
	SLICEMAP_ROWS = 10
	SLICEMAP_COLS = 10
	SLICEMAP_SIZE_WIDTH = 4096
	SLICEMAP_SIZE_HEIGHT = 4096
	SLICEMAP_PROCESSING_THREADS_NUMBER = 4
	