###
###
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import sys, os, time, errno
import numpy as np
import copy
#import shutil
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket
import time

from wxExportDialog import wxExportDialog
from wxImportDialog import wxImportDialog
from DojoStandalone import ServerLogic
# from wxDojo import ServerLogic

from os import path, pardir
current_dir = path.abspath(path.dirname(__file__))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
sys.path.append(path.join(parent_dir, "Filesystem"))
from Params import Params
from SaveChanges import SaveChanges
import ExportImgSeg

if sys.version_info.major == 3:
    import asyncio

class wxFileIO():

#    def StartThreadDojo(self):
#
#        self.p = s.Popen('python -u DojoStandalone.py u_info.pickle', stdout=s.PIPE, stderr=s.PIPE)
#
#        self.sentinel = True
#        while self.sentinel:
#            line = self.p.stdout.readline()
#            if line.strip() == "":
#                pass
#            else:
#                sys.stdout.write(line)
#                sys.stdout.flush()


    def StartThreadDojo(self):

        logic = ServerLogic()
        logic.run(self.u_info)


    def RestartDojo(self):

        print("Asked tornado to exit\n")
        if sys.version_info.major == 2:
        	ioloop = tornado.ioloop.IOLoop.instance()
        	ioloop.add_callback(ioloop.stop)
        if sys.version_info.major == 3:
            self.u_info.worker_loop.stop()
            time.sleep(1)
            self.u_info.worker_loop.close()
            
        time.sleep(1)
        print('Restart dojo server.')

        if sys.version_info.major == 2:
            self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
            self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
            self.u_info.dojo_thread.start()
        if sys.version_info.major == 3:
            self.u_info.worker_loop = asyncio.new_event_loop()
            self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
            self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
            self.u_info.dojo_thread.start()


    def TerminateDojo(self):

        print("Asked tornado to exit\n")
        if sys.version_info.major == 2:
        	ioloop = tornado.ioloop.IOLoop.instance()
        	ioloop.add_callback(ioloop.stop)

        if sys.version_info.major == 3:

            self.u_info.worker_loop.stop()
            time.sleep(1)
            self.u_info.worker_loop.close()
            #self.u_info.worker_loop.stop()
            #self.u_info.worker_loop.call_soon_threadsafe(self.u_info.worker_loop.close)


        # if self.u_info.dojo_thread != None:

        self.u_info.dojo_thread = None
        self.u_info.files_found = False

        self.import_mojo.Enable(enable=True)
        self.select_dojo.Enable(enable=True)
        self.copy_dojo.Enable(enable=False)
        self.save_dojo.Enable(enable=False)
        self.close_dojo.Enable(enable=False)
        self.export_image.Enable(enable=False)
        self.export_ids.Enable(enable=False)
        self.panel_URL.Hide()
        self.Layout()
        self.Refresh()
        self.Update()

    def LaunchDojo(self):  # wxGlade: ControlPanel.<event_handler>

        # Launch Dojo server as subprocess.
        with open(path.join(parent_dir, "u_info.pickle"), 'wb') as f:
            pickle.dump(self.u_info, f,protocol=2)


        if sys.version_info.major == 2:
            self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
            self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
            self.u_info.dojo_thread.start()
        if sys.version_info.major == 3:
            self.u_info.worker_loop = asyncio.new_event_loop()
            self.u_info.dojo_thread = threading.Thread(target=self.StartThreadDojo)
            self.u_info.dojo_thread.setDaemon(True) # Stops if control-C
            self.u_info.dojo_thread.start()

        print(self.u_info.url)

        self.DojoHTTP.SetURL(self.u_info.url)
        # self.DojoHTTP.SetLabel(self.u_info.url)
        self.DojoHTTP.SetLabel('Please click here!')

        ##self.panel_URL = wx.Panel(self, wx.ID_ANY)
        ##self.DojoHTTP = wx.adv.HyperlinkCtrl(self.panel_URL, wx.ID_ANY, 'Please click here.', "")

        ## self.ss1 = wx.BoxSizer(wx.HORIZONTAL)

        ##self.ss1.Replace(0, self.DojoHTTP, 0, wx.ALL, 4)
        ##self.ss1.Remove(0)
        ##URL_Text = wx.StaticText(self.panel_URL, wx.ID_ANY, "URL")

        ##self.ss1.Add(URL_Text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        ##self.ss1.Add(self.DojoHTTP, 0, wx.ALL, 4)
        ##self.panel_URL.SetSizer(self.ss1)

        self.panel_URL.Show()
        self.import_mojo.Enable(enable=False)
        self.select_dojo.Enable(enable=False)
        self.close_dojo.Enable(enable=True)
        self.copy_dojo.Enable(enable=True)
        self.save_dojo.Enable(enable=True)
        self.export_image.Enable(enable=True)
        self.export_ids.Enable(enable=True)
        self.Layout()
        self.Refresh()
        self.Update()


    def Import(self, event):  # wxGlade: ControlPanel.<event_handler>
        self.ImportImagesSegments = wxImportDialog(self, wx.ID_ANY, "",sim_name=[self, self.u_info])
        self.ImportImagesSegments.Show()


    def SelectDojoFile(self, event):
        dpath = self.u_info.files_path
        dialog = wx.DirDialog(self, "Select Dojo folder", dpath, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            dir = dialog.GetPath()
        except Exception:
            wx.LogError('Failed to open directory!')
            raise
        finally:
            dialog.Destroy()

        tmp_info = copy.deepcopy(self.u_info)
        tmp_info.SetUserInfo(dir)

        # Check file existence
        if os.path.exists(tmp_info.files_path) and \
            os.path.exists(tmp_info.ids_path) and \
            os.path.exists(tmp_info.tile_ids_path) and \
            os.path.isfile(tmp_info.tile_ids_volume_file) and \
            os.path.isfile(tmp_info.color_map_file) and \
            os.path.isfile(tmp_info.segment_info_db_file) and \
            os.path.exists(tmp_info.images_path) and \
            os.path.exists(tmp_info.tile_images_path) and \
            os.path.isfile(tmp_info.tile_images_volume_file) :
            print('All Dojo files are found. Applying..')
            self.u_info.files_found = True
            self.u_info.SetUserInfo(dir)
        else:
            print('Some Dojo files are missing.')
            return

        # Change statusbar
        frame_statusbar_fields = ["Target Dojo Folder: " + self.u_info.files_path]
        for i in range(len(frame_statusbar_fields)):
            self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)

        print(self.u_info.files_path)
        print(self.u_info.ids_path)
        print(self.u_info.tile_ids_path)
        print(self.u_info.tile_ids_volume_file)
        print(self.u_info.color_map_file)
        print(self.u_info.segment_info_db_file)
        print(self.u_info.images_path)
        print(self.u_info.tile_images_path)
        print(self.u_info.tile_images_volume_file)

        self.LaunchDojo()

    def CloseDojoFiles(self, event):  # wxGlade: ControlPanel.<event_handler>

        dlg = wx.MessageDialog(None,'Do you want to save changes?','Closing Dojo File',wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
        	self.SaveChanges = SaveChanges()
        	self.SaveChanges.run(self.u_info)
        	self.TerminateDojo()
        else:
        	self.TerminateDojo()
        
        #Save changes?
        #print("Save changes.")
        #self.SaveChanges = SaveChanges()
        #self.SaveChanges.run(self.u_info)

        #self.TerminateDojo()


    def SaveDojoFiles(self, event):  # wxGlade: ControlPanel.<event_handler>
        #if not  self.u_info.files_found :
        #    print('Dojo files are not validated.')
        #    print('Select Mojo files folder.')
        #    return False

        self.SaveChanges = SaveChanges()
        self.SaveChanges.run(self.u_info)
        self.RestartDojo()
        
        # ----------------------------------------------------------------------
    def ExportDojoFiles(self, event):
        #if not  self.u_info.files_found :
        #    print('Dojo files are not validated.')
        #    print('Select Dojo files folder.')
        #    return False

        ##
        dialog = wx.DirDialog(self, "Select Export Folder", self.u_info.files_path, wx.DD_DEFAULT_STYLE )
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            dir = dialog.GetPath()
        except Exception:
            wx.LogError('Failed to open directory!')
            raise
        finally:
            dialog.Destroy()

        ##
        dir = dir + os.sep + 'dojo'
        print('Export folder: ', dir)
        tmp_info = copy.deepcopy(self.u_info)
        tmp_info.SetUserInfo(dir)

        print(tmp_info.files_path)
        print(tmp_info.ids_path)
        print(tmp_info.tile_ids_path)
        print(tmp_info.tile_ids_volume_file)
        print(tmp_info.color_map_file)
        print(tmp_info.segment_info_db_file)
        print(tmp_info.images_path)
        print(tmp_info.tile_images_path)
        print(tmp_info.tile_images_volume_file)

        os.mkdir(tmp_info.files_path)
        copy_tree(self.u_info.ids_path, tmp_info.ids_path)
        copy_tree(self.u_info.images_path, tmp_info.images_path)

        # ----------------------------------------------------------------------

    def ExportImages(self, event):
        #if not  self.u_info.files_found :
        #    print('Dojo files are not validated.')
        #    print('Select Mojo files folder.')
        #    return False

        self.ImportImagesSegments = wxExportDialog(self, wx.ID_ANY, "",sim_name=[self, self.u_info, 'images'])
        self.ImportImagesSegments.Show()


        # ----------------------------------------------------------------------
    def ExportSegmentation(self, event):
        #if not  self.u_info.files_found :
        #    print('Dojo files are not validated.')
        #    print('Select Dojo files folder.')
        #    return False

        self.ImportImagesSegments = wxExportDialog(self, wx.ID_ANY, "",sim_name=[self, self.u_info, 'ids'])
        self.ImportImagesSegments.Show()

        # ----------------------------------------------------------------------


    def Exit(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.Close()
