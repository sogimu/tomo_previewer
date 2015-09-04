import os
import glob
import json
import subprocess
import re

import cherrypy
from cherrypy.lib import static

from app import load_template, render_template

from models import SliceMap
from settings import Settings
from proc import SlicemapFactory
from utils import Utils

class App(object):
    @cherrypy.expose
    def index(self):
        slicemaps = Utils.get_slicemaps( Settings.IMPORT_PATH, Settings.SLICE_NAME_FORMAT )
        return render_template('index.html', {'slicemaps': slicemaps})

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def is_preview_exist(self, path_to_slices):
        sf = SlicemapFactory()

        if( sf.isExist( path_to_slices ) == True):
            slicemap_obj = sf.get( path_to_slices )
            status = {
                "exist": True,
                "done": slicemap_obj.done,
                "creation_going": slicemap_obj.creation_going,
                "has_error": slicemap_obj.has_error,
                "link": Utils.create_link_for_preview( path_to_slices )
            }
        else:
            status = {
                "exist": False,
            }

        return status

    @cherrypy.expose
    def show_preview(self, path_to_slices):
        sf = SlicemapFactory()

        if( sf.isExist( path_to_slices ) == True):
            slicemap_obj = sf.get( path_to_slices )
            if(slicemap_obj.done == True and slicemap_obj.has_error == False):
                return render_template('show_preview.html', {'slicemap_obj': slicemap_obj})
            if(slicemap_obj.done == False and slicemap_obj.creation_going == True):
                return "Processing slices still going..."
        else:
            return "Preview for volume on the path: %s not found." % path_to_slices