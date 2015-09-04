import os

from sqlalchemy import Column, DateTime, String, Integer, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SliceMap(Base):
    __tablename__ = 'slice_map'
    path_to_slices = Column(String, primary_key=True)

    done = Column(Boolean)
    creation_going = Column(Boolean)
    has_error = Column(Boolean)
    time = Column(Float)

    slice_name_format = Column(String)
    slicemap_name_format = Column(String)
    config_name_format = Column(String)
    
    
    rows = Column(Integer)
    cols = Column(Integer)
    slices_number = Column(Integer)

    width  = Column(Integer)
    height = Column(Integer)

    path_to_slicemaps_and_config = Column(String)

    @property
    def path_to_config(self):
        return os.path.join( self.path_to_slicemaps_and_config, self.config_name_format)

    def __init__(self, path_to_slices, slice_name_format, slicemap_name_format, config_name_format, rows, cols, width, height, path_to_slicemaps_and_config):
        self.done = False
        self.creation_going = False
        self.has_error = False
        self.time = -1

        self.path_to_slices = path_to_slices
        self.slice_name_format = slice_name_format
        self.slicemap_name_format = slicemap_name_format
        self.config_name_format = config_name_format
        self.rows = rows
        self.cols = cols
        self.slices_number = self.rows * self.cols
        self.width = width
        self.height = height
        self.path_to_slicemaps_and_config = path_to_slicemaps_and_config
        

    # def __repr__(self):
    #     return '<SliceMap path_to_dir={}, slices_number={}, resize_factor={}, original_slice_width={}, original_slice_height={}, slice_width={}, slice_height={}, width={}, height={}, slices_per_row={}, slices_per_col={}, time={}>'.format(self.path_to_dir, self.slices_number, self.resize_factor, self.original_slice_width, self.original_slice_height, self.slice_width, self.slice_height, self.width, self.height, self.slices_per_row, self.slices_per_col, self.time)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.sqlite')
Base.metadata.create_all(engine)