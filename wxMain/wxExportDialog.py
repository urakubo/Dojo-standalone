#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.1 on Wed Jul 11 04:59:13 2018
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import os
import os.path
import sys
import numpy as np


from os import path, pardir
current_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
icon_dir    = path.join(parent_dir, "icons")
sys.path.append(path.join(parent_dir, "Filesystem"))
from Params import Params
from ExportImgSeg import ExportImgSeg

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxExportDialog(wx.Frame):
    def __init__(self, *args, **kwds):

        ##
        ##
        [self.parent, self.u_info, self.flag] = kwds.pop('sim_name')
        ##
        ##
        if(self.flag == 'images'):
            title = "Export Images"
            choice = ["PNG, 16bit, Grayscale", "PNG, 8bit, Grayscale",
                      "TIFF, 16bit, Grayscale", "TIFF, 8bit, Grayscale",
                      "Multi-TIFF, 16bit, Grayscale", "Multi-TIFF, 8bit, Grayscale",
                      "NUMPY, 32bit, uint (npy)", "NUMPY, 32bit, uint (npz), 'stack'", "HDF, 64bit, int, 'stack'"]
            self.table = ["PNG16G", "PNG8G",
                      "TIF16G", "TIF8G",
                      "MTIF16G", "MTIF8G",
                      "NUMPY32", "NUMPY32C", "HDF64"]
        elif(self.flag == 'ids'):
            title = "Export Ids"
            choice = ["PNG, 16bit, Grayscale", "PNG, 8bit, Grayscale", "PNG, 8bit, Color",
                      "TIFF, 16bit, Grayscale", "TIFF, 8bit, Grayscale", "TIFF, 8bit, Color",
                      "Multi-TIFF, 16bit, Grayscale", "Multi-TIFF, 8bit, Grayscale", "Multi-TIFF, 8bit, Color",
                      "NUMPY, 32bit, uint (npy)", "NUMPY, 32bit, uint (npz), 'stack'",
                      "HDF, 64bit, int, 'stack'"]
            self.table = ["PNG16G", "PNG8G", "PNG8C",
                      "TIF16G", "TIF8G", "TIF8C",
                      "MTIF16G", "MTIF8G", "MTIF8C",
                      "NUMPY32", "NUMPY32C",
                      "HDF64"]

        # begin wxGlade: TemplateExporter.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.p1 = wx.Panel(self, wx.ID_ANY)
        self.Filetype = wx.ComboBox(self.p1, 1, choices=choice, style=wx.CB_DROPDOWN)
        self.Filename = wx.TextCtrl(self.p1, 2, "")
        self.StartID = wx.SpinCtrl(self.p1, 3, "0", min=0, max=100000)
        self.NumDigits = wx.SpinCtrl(self.p1, 4, "4", min=4, max=8)
        self.p2 = wx.Panel(self, wx.ID_ANY)
        self.panel_3 = wx.Panel(self.p2, wx.ID_ANY)
        self.button1 = wx.Button(self.p2, wx.ID_OK, "")
        self.button2 = wx.Button(self.p2, 2, "Cancel")

        self.SetTitle(title)
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(  path.join(icon_dir, "Mojo2_16.png")  , wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.Filetype.SetSelection(0)
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.SpecifyDIR, self.button1)
        self.Bind(wx.EVT_BUTTON, self.Cancel, id=2)
        # end wxGlade


    def __do_layout(self):
        # begin wxGlade: TemplateExporter.__do_layout
        s0 = wx.BoxSizer(wx.HORIZONTAL)
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_s = wx.FlexGridSizer(4, 2, 0, 0)
        label1 = wx.StaticText(self.p1, wx.ID_ANY, "Format:")
        grid_s.Add(label1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        grid_s.Add(self.Filetype, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        label2 = wx.StaticText(self.p1, wx.ID_ANY, "Filename:")
        grid_s.Add(label2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        grid_s.Add(self.Filename, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        label3 = wx.StaticText(self.p1, wx.ID_ANY, "Start At:")
        grid_s.Add(label3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        grid_s.Add(self.StartID, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        label4 = wx.StaticText(self.p1, wx.ID_ANY, "Digits (1-8):")
        grid_s.Add(label4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        grid_s.Add(self.NumDigits, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        self.p1.SetSizer(grid_s)
        s1.Add(self.p1, 0, wx.EXPAND, 0)
        s2.Add(self.panel_3, 1, wx.EXPAND, 0)
        s2.Add(self.button1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        s2.Add(self.button2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 4)
        self.p2.SetSizer(s2)
        s1.Add(self.p2, 1, wx.EXPAND, 0)
        s0.Add(s1, 1, wx.EXPAND, 0)
        self.SetSizer(s0)
        s0.Fit(self)
        self.Layout()
        # end wxGlade


    def SpecifyDIR(self, event):  # wxGlade: TemplateExporter.<event_handler>
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

        fname     = self.Filename.GetLineText(0)
        ftype     = self.table[self.Filetype.GetSelection()]
        startid   = self.StartID.GetValue()
        numdigit  = self.NumDigits.GetValue()

        print(self.flag)
        print('Filedir:    ', dir)
        print('Filename:   ', fname )
        print('Filetype:   ', ftype )
        print('Init ID:    ', startid )
        print('Num Digits: ', numdigit )

        exports = ExportImgSeg()
        exports.run(self.u_info, dir, fname, ftype, startid, numdigit, self.flag)

        self.Close()
        return True

    def Cancel(self, event):  # wxGlade: TemplateExporter.<event_handler>
        self.Close()
        return False




# end of class TemplateExporter

class MyApp(wx.App):
    def OnInit(self):
        self.frame = TemplateExporter(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
