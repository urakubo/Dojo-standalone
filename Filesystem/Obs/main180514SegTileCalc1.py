##
##
##

import os
import numpy as np
import h5py
import lxml
import lxml.etree
import UpdateDB
import DefaultParams

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
    print 'Save: ', file_path



def load_hdf5( file_path, dataset_name):
    
    hdf5			= h5py.File( file_path, 'r' )
    array			= hdf5[dataset_name].value
    hdf5.close()
#    print 'Load: ', file_path
    return array


# def save_image( file_path, image ):
#    image.save( file_path )
#    print file_path

###
###
def main( MergeIDs ):
###
###
	p = defaultparams()
	output_path                   = 'C:\Users\urakubo\Desktop\Bullmann\Mojo\mojo_data_subvolume\z=0000-0099\mojo'
###

	output_ids_path               = output_path     + '\\ids'
	output_tile_ids_path          = output_ids_path + '\\tiles'
	output_tile_volume_file       = output_ids_path + '\\tiledVolumeDescription.xml'
	output_color_map_file         = output_ids_path + '\\colorMap.hdf5'
	output_segment_info_db_file   = output_ids_path + '\\segmentInfo.db'

###
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
###    id_counts            = np.zeros( 0, dtype=np.int64 )
###    tile_index_z         = 0
###
	id_tile_list	= []
	id_max 			= 0
	id_counts       = np.zeros( 0, dtype=np.int64 )
###
###
###
	for tile_index_w in range( numTilesW ):
		for tile_index_z in range( numTilesZ ):
			tmp = '\\' + 'w=' + '%08d' % ( tile_index_w ) + '\\' + 'z=' + '%08d' % ( tile_index_z )
			current_tile_ids_path    = output_tile_ids_path + tmp
			for tile_index_y in range( numTilesY ):
				for tile_index_x in range( numTilesX ):
					tmp = '\\' + 'y=' + '%08d' % ( tile_index_y ) + ','  + 'x=' + '%08d' % ( tile_index_x ) + '.hdf5'
					current_tile_ids_name = current_tile_ids_path + tmp

					##
					## tile_ids:
					## np.zeros( ( tile_num_pixels_y, tile_num_pixels_x ), np.uint32 )
					##
					tile_ids = load_hdf5( current_tile_ids_name, 'IdMap')
					
					for IDs in MergeIDs:
						TargetID = IDs[0]
						for i in IDs:
							tile_ids[ tile_ids == i ] = TargetID

					## Remove correspondent ID info!
					
					save_hdf5( current_tile_ids_name, 'IdMap', tile_ids )
					##
					##



				### Max id
					unique_tile_ids = np.unique( tile_ids )
					current_max = np.max( unique_tile_ids )
        			if id_max < current_max:
						id_max = current_max
						id_counts.resize( id_max + 1 )

				### id list
        			unique_tile_ids = np.unique( tile_ids )
        			for unique_tile_id in unique_tile_ids:
        				id_tile_list.append( (unique_tile_id, tile_index_w, tile_index_z, tile_index_y, tile_index_x ) );

				### Pixel number of each id
        			current_image_counts = np.bincount( tile_ids.ravel() )
        			current_image_counts_ids = np.nonzero( current_image_counts )[0]
        			current_max = np.max( current_image_counts_ids )
        			id_counts[ current_image_counts_ids ] = \
        				id_counts[ current_image_counts_ids ] + np.int64( current_image_counts [ current_image_counts_ids ] )
        

	## print id_counts

	## Sort the tile list so that the same id appears together
	id_tile_list = np.array( sorted( id_tile_list ), np.uint32 )
	UpdateDB.main( output_segment_info_db_file, id_tile_list, id_max, id_counts, numTilesZ )




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
if __name__ == '__main__':
	MergeIDs = []
	main( MergeIDs )

###
###


