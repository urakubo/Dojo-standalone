##
##
##

import os
import numpy as np
import h5py
import lxml
import lxml.etree
import save_db as s
import PIL
import PIL.Image
import png
import DefaultParams

##

# Not yet
def save_u16_to_tiff(u16in, size, filename):
    """
    Since Pillow has poor support for 16-bit TIFF,
    we make our own save function to properly save a 16-bit TIFF.
    http://blog.itsayellow.com/index.php/2017/09/21/saving-16-bit-tiff-images-with-pillow-in-python/
    """
    # PIL interprets mode 'I;16' as "uint16, little-endian"
    img_out = Image.new('I;16', size)

    # make sure u16in little-endian, output bytes
    outpil = u16in.astype(u16in.dtype.newbyteorder("<")).tobytes()
    img_out.frombytes(outpil)
    img_out.save(filename)


def save_u16_to_png(id_data, filename):
    # Use pypng to write zgray as a grayscale PNG.
    with open(filename, 'wb') as f:
        writer = png.Writer(width=id_data.shape[1], height=id_data.shape[0], bitdepth=16, greyscale=True)
        id_data_list = id_data.astype('uint16').tolist()
        writer.write(f, id_data_list)


def save_u8_to_png(id_data, filename):
    # Use pypng to write zgray as a grayscale PNG.
    with open(filename, 'wb') as f:
        writer = png.Writer(width=id_data.shape[1], height=id_data.shape[0], bitdepth=8, greyscale=True)
        id_data_list = id_data.astype('uint8').tolist()
        writer.write(f, id_data_list)

# Not yet
def save_col_to_png(u16in, size, filename):
    # Use pypng to write z as a color PNG.
    with open('foo_color.png', 'wb') as f:
        writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
        # Convert z to the Python list of lists expected by
        # the png writer.
        z2list = z.reshape(-1, z.shape[1] * z.shape[2]).tolist()
        writer.write(f, z2list)


def mkdir_safe( dir_to_make ):
    if not os.path.exists( dir_to_make ):
        execute_string = 'mkdir ' + '"' + dir_to_make + '"'
        print execute_string
        print
        os.system( execute_string )

def load_hdf5(file_path, dataset_name):
    hdf5 = h5py.File(file_path, 'r')
    array = hdf5[dataset_name].value
    hdf5.close()
    return array


###
###
def main(p):
    #
    p = DefaultParams.Params()
    mojo_tile_path          = p.mojo_tile_images_path
    mojo_tile_volume_file   = p.mojo_tile_images_volume_file
    input_color_map_file    = p.mojo_color_map_file
    export_path             = p.export_images_path
    export_name             = p.export_images_name

    #
    with open(mojo_tile_volume_file, 'r') as file:
        idTiledVolDesc = lxml.etree.parse(file).getroot()
    num_tiles_x = int(idTiledVolDesc.get('numTilesX'))  # 1
    num_tiles_y = int(idTiledVolDesc.get('numTilesY'))  # 1
    num_tiles_z = int(idTiledVolDesc.get('numTilesZ'))  # 100
    num_pixels_per_tile_x = int(idTiledVolDesc.get('numVoxelsPerTileX'))  # 512
    num_pixels_per_tile_y = int(idTiledVolDesc.get('numVoxelsPerTileY'))  # 512
    num_pixels_original_image_x = int(idTiledVolDesc.get('numVoxelsX'))  # 512
    num_pixels_original_image_y = int(idTiledVolDesc.get('numVoxelsY'))  # 512


    #
    mkdir_safe( p.export_images_path )

    #
    tile_index_w = 0
    for tile_index_z in range(num_tiles_z):
        tmp = '\\' + 'w=' + '%08d' % (tile_index_w) + '\\' + 'z=' + '%08d' % (tile_index_z)
        current_tile_path = mojo_tile_path + tmp
        merged_ids = np.zeros( ( num_pixels_original_image_y, num_pixels_original_image_x ), np.uint32 )
        for tile_index_y in range(num_tiles_y):
            for tile_index_x in range(num_tiles_x):

                # Load and merge panels
                tmp = '\\' + 'y=' + '%08d' % (tile_index_y) + ',' + 'x=' + '%08d' % (tile_index_x) + '.tif'
                current_tile_name = current_tile_path + tmp

                # tile_ids = load_hdf5(current_tile_name, 'IdMap')
                tile_image = PIL.Image.open( current_tile_name )

                y = tile_index_y * num_pixels_per_tile_y
                x = tile_index_x * num_pixels_per_tile_x
                merged_ids[  y : y + num_pixels_per_tile_y, x : x + num_pixels_per_tile_x ] = tile_image

        # Save a merged image
        current_export_name = export_path + '\\' + export_name + '_z%08d' % (tile_index_z) + '.png'
        print current_export_name
        save_u16_to_png(merged_ids, current_export_name)
        # save_u8_to_png(merged_ids, current_export_name)



###
###
if __name__ == '__main__':
    p = []
    main(p)

###
###
