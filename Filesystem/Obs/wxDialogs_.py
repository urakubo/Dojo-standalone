import wx
import os
import os.path
import DefaultParams
import copy
#import shutil
from distutils.dir_util import copy_tree
import subprocess
import ImportImgSeg
    #----------------------------------------------------------------------
def ImportFiles(self, event, UserInfo):
    dpath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
    dpath = "C:\\Users\\urakubo\\Desktop\\Mojo\\ac3x75_ImagesPanels"
    openFileDialog = wx.DirDialog(self, "Select Images Folder", dpath, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    openFileDialog.ShowModal()
    dir_input_images = openFileDialog.GetPath()
    openFileDialog.Destroy()
    print 'Image files folder: ', dir_input_images

    # Input segment dir
    openFileDialog = wx.DirDialog(self, "Select Segmentation Folder", dir_input_images, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    openFileDialog.ShowModal()
    dir_input_ids = openFileDialog.GetPath()
    openFileDialog.Destroy()
    print 'Segmentation files folder: ', dir_input_ids


    # Import Mojo dir
    openFileDialog = wx.DirDialog(self, "Select/create Mojo Import Folder", dir_input_ids, wx.DD_DEFAULT_STYLE)
    openFileDialog.ShowModal()
    dir_mojo = openFileDialog.GetPath()
    openFileDialog.Destroy()
    print 'Import Mojo folder: ', dir_mojo
    UserInfo.mojo_files_found = True
    UserInfo.SetMojoPath(dir_mojo)
    MojoControlPanel_statusbar_fields = ["Target Mojo Folder: " + UserInfo.mojo_files_path]
    for i in range(len(MojoControlPanel_statusbar_fields)):
        self.MojoControlPanel_statusbar.SetStatusText(MojoControlPanel_statusbar_fields[i], i)

    ImportImgSeg.images( UserInfo, dir_input_images )
    ImportImgSeg.ids( UserInfo, dir_input_ids )

    # ----------------------------------------------------------------------
def SelectMojoFolder(self, event, UserInfo):
    dpath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
    # dpath = "C:\\Users\\urakubo\\Desktop\\Mojo\\ac3x75\\mojo"
    selectFileDialog = wx.DirDialog(self, "Select Mojo folder", dpath, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    selectFileDialog.ShowModal()
    dir = selectFileDialog.GetPath()
    selectFileDialog.Destroy()

    tmp_info = copy.deepcopy(UserInfo)
    tmp_info.SetMojoPath(dir)

    # Check file existence
    if os.path.exists(tmp_info.mojo_files_path) and \
        os.path.exists(tmp_info.mojo_ids_path) and \
        os.path.exists(tmp_info.mojo_tile_ids_path) and \
        os.path.isfile(tmp_info.mojo_tile_ids_volume_file) and \
        os.path.isfile(tmp_info.mojo_color_map_file) and \
        os.path.isfile(tmp_info.mojo_segment_info_db_file) and \
        os.path.exists(tmp_info.mojo_images_path) and \
        os.path.exists(tmp_info.mojo_tile_images_path) and \
        os.path.isfile(tmp_info.mojo_tile_images_volume_file) :
        print 'All Mojo files are found. Applying ...'
        UserInfo.mojo_files_found = True
        UserInfo.SetMojoPath(dir)
    else:
        print 'Some Mojo files are missing.'
        return

    # Change statusbar
    MojoControlPanel_statusbar_fields = ["Target Mojo Folder: " + UserInfo.mojo_files_path]
    for i in range(len(MojoControlPanel_statusbar_fields)):
        self.MojoControlPanel_statusbar.SetStatusText(MojoControlPanel_statusbar_fields[i], i)

    print UserInfo.mojo_files_path
    print UserInfo.mojo_ids_path
    print UserInfo.mojo_tile_ids_path
    print UserInfo.mojo_tile_ids_volume_file
    print UserInfo.mojo_color_map_file
    print UserInfo.mojo_segment_info_db_file
    print UserInfo.mojo_images_path
    print UserInfo.mojo_tile_images_path
    print UserInfo.mojo_tile_images_volume_file


    # ----------------------------------------------------------------------
def SelectMojoExportFolder(self, event, UserInfo):
    if not  UserInfo.mojo_files_found :
        print 'Mojo files are not validated.'
        print 'Select Mojo files folder.'
        return False
    dpath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
    selectFileDialog = wx.DirDialog(self, "Select Export Folder", dpath, wx.DD_DEFAULT_STYLE )
    selectFileDialog.ShowModal()
    dir = selectFileDialog.GetPath()
    selectFileDialog.Destroy()
    dir = dir + '\\mojo'
    print 'Export folder: ', dir
    tmp_info = copy.deepcopy(UserInfo)
    tmp_info.SetMojoPath(dir)

    print tmp_info.mojo_files_path
    print tmp_info.mojo_ids_path
    print tmp_info.mojo_tile_ids_path
    print tmp_info.mojo_tile_ids_volume_file
    print tmp_info.mojo_color_map_file
    print tmp_info.mojo_segment_info_db_file
    print tmp_info.mojo_images_path
    print tmp_info.mojo_tile_images_path
    print tmp_info.mojo_tile_images_volume_file

    os.mkdir(tmp_info.mojo_files_path)
    copy_tree(UserInfo.mojo_ids_path, tmp_info.mojo_ids_path)
    copy_tree(UserInfo.mojo_images_path, tmp_info.mojo_images_path)


    # ----------------------------------------------------------------------
def SelectImageExportFolder(self, event, UserInfo, file_type):
    if not  UserInfo.mojo_files_found :
        print 'Mojo files are not validated.'
        print 'Select Mojo files folder.'
        return False
    selectFileDialog = wx.DirDialog(self, "Select Image Export Folder", \
                        UserInfo.mojo_files_path, wx.DD_DEFAULT_STYLE )
    selectFileDialog.ShowModal()
    dir = selectFileDialog.GetPath()
    selectFileDialog.Destroy()
    dir = dir + '\\Images'


    # ----------------------------------------------------------------------
def SelectIdsExportFolder(self, event, UserInfo, file_type):
    if not  UserInfo.mojo_files_found :
        print 'Mojo files are not validated.'
        print 'Select Mojo files folder.'
        return False
    selectFileDialog = wx.DirDialog(self, "Select Segmentation Export Folder", \
                        UserInfo.mojo_files_path, wx.DD_DEFAULT_STYLE )
    selectFileDialog.ShowModal()
    dir = selectFileDialog.GetPath()
    selectFileDialog.Destroy()
    dir = dir + '\\Ids'

# (None, "Choose input directory", "",
#                     wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
