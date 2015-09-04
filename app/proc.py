import os
import multiprocessing
import subprocess

from settings import Settings

from models import engine
from models import SliceMap

class SlicemapProcess(multiprocessing.Process):
    def __init__(self, path):
        super(SlicemapProcess, self).__init__()
        self.path = path

    def run(self):
        import time
        self.sf = SlicemapFactory()
        self.slicemap_obj = self.sf.get( self.path )
        self.session = self.sf.getSession()

        print("SlicemapProcess: Start(): %s. " % self.slicemap_obj.path_to_slices)
        slicemap_creator_process = "python slice_map_creator/run.py create -sp '%s' -rc '%s' -sms '%s' -smpg '%s' -smpr '%s' -cp '%s' -snf '%s' -smnf '%s' -cnf '%s'" % (
            self.slicemap_obj.path_to_slices, 
            "%sx%s" % (self.slicemap_obj.rows, self.slicemap_obj.cols), 
            "%sx%s" % (self.slicemap_obj.width, self.slicemap_obj.height), 
            self.slicemap_obj.path_to_slicemaps_and_config, 
            self.slicemap_obj.path_to_slicemaps_and_config, 
            self.slicemap_obj.path_to_slicemaps_and_config, 
            self.slicemap_obj.slice_name_format,
            self.slicemap_obj.slicemap_name_format,
            self.slicemap_obj.config_name_format
        )
        print(slicemap_creator_process)

        start_time = time.time()

        self.slicemap_obj.done = False
        self.slicemap_obj.creation_going = True
        self.session.commit()
        try:
            subprocess.call(slicemap_creator_process, shell=True)
        except:
            self.slicemap_obj.has_error = True
            self.session.commit()

        finally:
            self.slicemap_obj.done = True
            self.slicemap_obj.creation_going = False
            self.slicemap_obj.time = time.time() - start_time

            self.session.commit()

        print("SlicemapProcess: Stop(): %s. " % self.slicemap_obj.path_to_slices)

class SlicemapsProcess(multiprocessing.Process):
    def __init__(self, paths_for_processing):
        super(SlicemapsProcess, self).__init__()
        self.paths_for_processing = paths_for_processing

    def run(self):
        print("SlicemapsProcess: Start(): %s. " % self.paths_for_processing)

        def processPaths(paths):
            print(paths)
            slicemapProcess_pull = []
            for path in paths:
                slicemapsProc = SlicemapProcess(path)
                slicemapsProc.start()
                slicemapProcess_pull.append(slicemapsProc)

            for slicemapProc in slicemapProcess_pull:
                slicemapProc.join()

        begin = 0
        end = 0

        while True:
            begin = end
            if( begin + Settings.SLICEMAP_PROCESSING_THREADS_NUMBER > len(self.paths_for_processing) ):
                end = len(self.paths_for_processing)
            else:
                end = begin + Settings.SLICEMAP_PROCESSING_THREADS_NUMBER

            group_of_paths_for_processing = self.paths_for_processing[ begin : end ]
            processPaths( group_of_paths_for_processing )

            if end == len(self.paths_for_processing):
                break
        print("SlicemapsProcess: Stop(): %s. " % self.paths_for_processing)


class SlicemapFactory():
    def __init__(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
 
        self.engine = create_engine('sqlite:///database.sqlite')
        self.session = sessionmaker(bind=engine)()


    def init(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height, path_to_slicemaps_and_config):
        slicemap_obj = SliceMap(path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height, path_to_slicemaps_and_config)
        self.session.add(slicemap_obj)
        self.session.commit()
        return slicemap_obj

    def processOne(self, path_for_processing):
        slicemapProc = SlicemapProcess(path_for_processing)
        slicemapProc.start()

    def processMany(self, paths_for_processing):
        slicemapsProc = SlicemapsProcess(paths_for_processing)
        slicemapsProc.start()

    def remove(self, path_to_slices):
        slicemap_obj = self.session.query( SliceMap ).filter_by( path_to_slices = path_to_slices ).delete()
        return slicemap_obj

    def get(self, path_to_slices):
        slicemap_obj = self.session.query( SliceMap ).filter_by( path_to_slices = path_to_slices ).first()
        return slicemap_obj

    def isExist(self, path_to_slices):
        is_exist = self.session.query( SliceMap ).filter_by( path_to_slices = path_to_slices ).first() != None if True else False
        return is_exist

    def getSession(self):
        return self.session
