#
#
#
import os

class User:
    def __init__(self):
        desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")    + os.sep + "Desktop"
        mydocument_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + os.sep + "Documents"
        user_path    = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
        user_path = "C:\\Users\\urakubo\\Desktop\\ffn\\180620Laxmi"
        # dpath = "C:\\Users\\urakubo\\Desktop\\Mojo\\mojo_data_subvolume\mojo"
        # C:\Users\urakubo\Desktop\Mojo\ac3x75_ImagesPanels
        # C:\Users\urakubo\Desktop\Mojo\examples\Laxmi_ImagePanelData
        # C:\Users\urakubo\Desktop\Mojo\examples\FlyBrainOrg

    # Mojo unit image size for import
        self.tile_num_pixels_y = 512
        self.tile_num_pixels_x = 512
        #self.tile_num_pixels_y = 256
        #self.tile_num_pixels_x = 256
        self.ncolors           = 16383 ## Must be smaller than 16384 = console.log( gl.getParameter(gl.MAX_TEXTURE_SIZE) )

    # Mojo file paths
        self.mojo_files_found = False
        self.mojo_files_path = user_path
        self.mojo_ids_path              = self.mojo_files_path  + os.sep + 'ids'
        self.mojo_tile_ids_path         = self.mojo_ids_path    + os.sep + 'tiles'
        self.mojo_tile_ids_volume_file  = self.mojo_ids_path    + os.sep + 'tiledVolumeDescription.xml'
        self.mojo_color_map_file        = self.mojo_ids_path    + os.sep + 'colorMap.hdf5'
        self.mojo_segment_info_db_file  = self.mojo_ids_path    + os.sep + 'segmentInfo.db'
        self.mojo_segment_info_db_undo_file  = self.mojo_ids_path    + os.sep + 'segmentInfo_undo.pickle'
        self.mojo_segment_info_db_redo_file  = self.mojo_ids_path    + os.sep + 'segmentInfo_redo.pickle'

        self.mojo_images_path           = self.mojo_files_path  + os.sep + 'images'
        self.mojo_tile_images_path      = self.mojo_images_path + os.sep + 'tiles'
        self.mojo_tile_images_volume_file = self.mojo_images_path + os.sep + 'tiledVolumeDescription.xml'
        self.mojo_image_extension       = '.tif'

        self.backup_db_name             = 'idTileIndex'
        self.ids_files_undo             = []
        self.ids_files_redo             = []
        self.flag_undo                  = 0
        self.flag_redo                  = 0


        self.export_images_dir          = 'export_images'
        self.export_ids_dir             = 'export_ids'
        self.export_images_name         = 'z%08d'
        self.export_ids_name            = 'z%08d'
        self.export_col_name            = 'colormap'
        self.export_db_name             = 'segmentInfo'
        self.export_db_ids              = ['id', 'name', 'size','confidence','type','subtype']
        self.hdf_color_name = 'idColorMap'

    def SetMojoPath(self, user_path):
        self.mojo_files_path                = user_path
        self.mojo_ids_path                  = self.mojo_files_path  + os.sep + 'ids'
        self.mojo_tile_ids_path             = self.mojo_ids_path    + os.sep + 'tiles'
        self.mojo_tile_ids_volume_file      = self.mojo_ids_path    + os.sep + 'tiledVolumeDescription.xml'
        self.mojo_color_map_file            = self.mojo_ids_path    + os.sep + 'colorMap.hdf5'
        self.mojo_segment_info_db_file      = self.mojo_ids_path    + os.sep + 'segmentInfo.db'
        self.mojo_segment_info_db_undo_file  = self.mojo_ids_path    + os.sep + 'segmentInfo_undo.pickle'
        self.mojo_segment_info_db_redo_file  = self.mojo_ids_path    + os.sep + 'segmentInfo_redo.pickle'

        self.mojo_images_path               = self.mojo_files_path  + os.sep + 'images'
        self.mojo_tile_images_path          = self.mojo_images_path + os.sep + 'tiles'
        self.mojo_tile_images_volume_file   = self.mojo_images_path + os.sep + 'tiledVolumeDescription.xml'
