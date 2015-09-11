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
from proc import PreviewFactory, SlicemapFactory
from utils import Utils

class App(object):
    @cherrypy.expose
    def index(self):
        slicemaps = Utils.get_previews( Settings.IMPORT_PATH, Settings.SLICE_NAME_FORMAT )
        return render_template('index.html', {'slicemaps': slicemaps})

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def is_preview_exist(self, path_to_slices):
        pf = PreviewFactory()

        if( pf.isExist( path_to_slices ) == True):
            preview_obj = pf.get( path_to_slices )
            status = {
                "exist": True,
                "done": preview_obj.done,
                "creation_going": preview_obj.creation_going,
                "has_error": preview_obj.has_error,
                "link": Utils.create_link_for_preview( path_to_slices )
            }
        else:
            status = {
                "exist": False,
            }

        return status

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_previews(self):
        previews = Utils.get_previews( Settings.IMPORT_PATH, Settings.SLICE_NAME_FORMAT )
        
        previews_python_array = []
        for preview in previews:
            previews_python_array.append( preview.to_array() )

        return previews_python_array

    @cherrypy.expose
    def show_preview(self, path_to_slices):
        pf = PreviewFactory()

        if( pf.isExist( path_to_slices ) == True):
            preview_obj = pf.get( path_to_slices )
            if(preview_obj.done == True and preview_obj.has_error == False):
                return render_template('show_preview.html', {'preview_obj': preview_obj})
            if(preview_obj.done == False and preview_obj.creation_going == True):
                return "Processing still going ..."
        else:
            return "Preview for volume on the path: %s not found." % path_to_slices