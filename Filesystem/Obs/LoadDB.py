##
## Simple merger
##

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import itertools
import math
import numpy as np
import h5py
import lxml
import lxml.etree


from itertools import chain

import UpdateDB
import Params

###
###
class LoadDB:

    def save_hdf5( self, file, dataset_name, array ):
        hdf5             = h5py.File( file, 'w' )
        hdf5.create_dataset( dataset_name, data=array )
        hdf5.flush()
        hdf5.close()

    def load_hdf5( self, file_path, dataset_name):
        hdf5			= h5py.File( file_path, 'r' )
        array			= hdf5[dataset_name].value
        hdf5.close()
        return array

        ###
        ###

