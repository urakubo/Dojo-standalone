#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##
## Smart merge
##

import os
import math
import numpy as np
import h5py
import lxml
import lxml.etree
import shutil

from itertools import chain

import UpdateDB
from typing import Any

import DefaultParams
from np2sego import Sego

# import sys
# import string
# import math
# import mahotas
# import PIL
# import PIL.Image
# import scipy
# import scipy.io
##
##
##
def save_hdf5( file_path, dataset_name, array ):
    hdf5             = h5py.File( file_path, 'w' )
    dataset          = hdf5.create_dataset( dataset_name, data=array )
    hdf5.close()


def load_hdf5( file_path, dataset_name):
    hdf5			= h5py.File( file_path, 'r' )
    array			= hdf5[dataset_name].value
    hdf5.close()
    return array


def ObtainFullSizeIds( current_tile_path,  numTilesY, numTilesX, numVoxelsY, numVoxelsX, numVoxelsPerTileY, numVoxelsPerTileX ):
    merged_ids = np.zeros((numVoxelsY, numVoxelsX), np.uint32)  # type: Any
    for tile_index_y in range(numTilesY):
        for tile_index_x in range(numTilesX):
            ## Load panels
            tmp = os.sep + 'y=' + '%08d' % (tile_index_y) + ',' + 'x=' + '%08d' % (tile_index_x) + '.hdf5'
            current_tile_name = current_tile_path + tmp
            tile_ids = load_hdf5(current_tile_name, 'IdMap')

            ## Obtain merged ids
            y = tile_index_y * numVoxelsPerTileY
            x = tile_index_x * numVoxelsPerTileX
            merged_ids[y: y + numVoxelsPerTileY, x: x + numVoxelsPerTileX] = tile_ids
    return  merged_ids

###
###
def main( MergeIDs, UserInfo ):
    #
    output_tile_ids_path          = UserInfo.mojo_tile_ids_path
    output_tile_volume_file       = UserInfo.mojo_tile_ids_volume_file
    output_color_map_file         = UserInfo.mojo_color_map_file
    output_segment_info_db_file   = UserInfo.mojo_segment_info_db_file
    undo_segment_info_db_file     = UserInfo.mojo_segment_info_db_undo_file
###
###
    with open( output_tile_volume_file, 'r' ) as file:
        idTiledVolDesc = lxml.etree.parse(file).getroot()
    # "root.tag" and "root.attrib" to check them
    numTilesW 			= int( idTiledVolDesc.get('numTilesW') )			# 1
    numTilesX 			= int( idTiledVolDesc.get('numTilesX') )			# 1
    numTilesY 			= int( idTiledVolDesc.get('numTilesY') )			# 1
    numTilesZ 			= int( idTiledVolDesc.get('numTilesZ') )			# 100
    numVoxelsPerTileX	= int( idTiledVolDesc.get('numVoxelsPerTileX') )	# 512
    numVoxelsPerTileY	= int( idTiledVolDesc.get('numVoxelsPerTileY') )	# 512
    numVoxelsPerTileZ	= int( idTiledVolDesc.get('numVoxelsPerTileZ') )	# 1
    numVoxelsX			= int( idTiledVolDesc.get('numVoxelsX') )			# 512
    numVoxelsY			= int( idTiledVolDesc.get('numVoxelsY') )			# 512
    numVoxelsZ			= int( idTiledVolDesc.get('numVoxelsZ') )			# 100
    ###
    ### Edit IDs
    ###

    flattenMergeIDs = set(chain.from_iterable(MergeIDs))  ## To check whether ids should be updated.
    print flattenMergeIDs
    ids_files_undo  = []

    outfile = Sego(UserInfo)
    tile_index_w = 0
    UserInfo.ids_files_undo = []

    for tile_index_z in range(numTilesZ):
        tmp = os.sep + 'w=' + '%08d' % (tile_index_w) + os.sep + 'z=' + '%08d' % (tile_index_z)
        current_tile_path = UserInfo.mojo_tile_ids_path + tmp

        ## Obtain a whole image
        merged_ids = ObtainFullSizeIds( current_tile_path,  numTilesY, numTilesX,
                                        numVoxelsY, numVoxelsX, numVoxelsPerTileY, numVoxelsPerTileX )

        ## Check whether ids should be updated.
        unique_tile_ids = np.unique(merged_ids)
        if bool(flattenMergeIDs.intersection(set(unique_tile_ids))):

        ## Target components for smart connection
            for IDs in MergeIDs:
                TargetID = IDs[0]
                for i in IDs:
                    merged_ids[merged_ids == i] = TargetID

            ##
            ## Change id files at the specified Z
            ##
            outfile.run( merged_ids, tile_index_z )
            ##

            # Add the Undo functionality
            # print 'Save: ', current_tile_path
            # ids_files_undo.extend(filenames_undo)  ## Filename for undo


    ##
    ## Update database
    ##
    id_tile_list	= []
    id_max 			= 0
    id_counts       = np.zeros( 0, dtype=np.int64 )
    for tile_index_z in range(numTilesZ):
        tmp = os.sep + 'w=' + '%08d' % (tile_index_w) + os.sep + 'z=' + '%08d' % (tile_index_z)
        current_tile_ids_path = output_tile_ids_path + tmp
        for tile_index_y in range(numTilesY):
            for tile_index_x in range(numTilesX):
                tile_index_w = 0
                tmp = os.sep + 'y=' + '%08d' % (tile_index_y) + ',' + 'x=' + '%08d' % (tile_index_x) + '.hdf5'
                current_tile_ids_name = current_tile_ids_path + tmp
                tile_ids = load_hdf5(current_tile_ids_name, 'IdMap')

                ## Update database
                # Max id
                current_max = np.max(unique_tile_ids)
                if id_max < current_max:
                    id_max = current_max
                    id_counts.resize(id_max + 1)

                # id list
                unique_tile_ids = np.unique(tile_ids)
                for unique_tile_id in unique_tile_ids:
                    id_tile_list.append((unique_tile_id, tile_index_w, tile_index_z, tile_index_y, tile_index_x));

                # Pixel number of each id
                current_image_counts = np.bincount(tile_ids.ravel())
                current_image_counts_ids = np.nonzero(current_image_counts)[0]
                current_max = np.max(current_image_counts_ids)
                id_counts[current_image_counts_ids] = id_counts[current_image_counts_ids] + np.int64(current_image_counts[current_image_counts_ids])


    ## print id_counts

    ## Sort the tile list so that the same id appears together
    id_tile_list = np.array( sorted( id_tile_list ), np.uint32 )

    ## For Undo
    UserInfo.ids_files_undo = ids_files_undo
    UpdateDB.backup( UserInfo, UserInfo.mojo_segment_info_db_undo_file )
    UserInfo.flag_undo      = 1
    UserInfo.flag_redo      = 0

    ## Update database
    UpdateDB.main( output_segment_info_db_file, id_tile_list, id_max, id_counts )

    # print files_ids_undo


# Make a color map
#	ncolors  = id_max + 1
#	color_map = np.zeros( (ncolors + 1, 3), dtype=np.uint8 );
#	for color_i in xrange( 1, ncolors + 1 ):
#		rand_vals = np.random.rand(3);
#		color_map[ color_i ] = [ rand_vals[0]*255, rand_vals[1]*255, rand_vals[2]*255 ];
#
#	print 'Writing colorMap file (hdf5)'
#	hdf5               = h5py.File( output_color_map_file, 'w' )
#	hdf5['idColorMap'] = color_map
#	hdf5.close()


###
###


