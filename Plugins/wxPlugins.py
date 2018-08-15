
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import os
import sys
from os import path, pardir

# ----------------------------------------------------------------------
# Interface of plugins to Control Panel
# Please add user defined functions
# Also please edit "menu.json" for a plugins pulldown menu.
# ----------------------------------------------------------------------

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
Plugins_dir  = path.abspath(path.join(main_dir, "Plugins"))
sys.path.append(path.join(Plugins_dir, "superpixel"))
sys.path.append(path.join(Plugins_dir, "export_stl"))


import wxglade_superpixel
#from ExportStl import ExportStl

class wxPlugins():

    def ExportStl_(self, event):
        print("'Export Stl' not implemented!")
        event.Skip()
        # func = ExportStl(self.u_info)
        # func.Run()



    def SuperPixel_(self, event):
    
        # self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "",sim_name=[self, self.UserInfo])
    	self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "")
    	self.superpix.Show()
        #event.Skip()


    def UserDefined_(self, event):
        print("'User Defined' not implemented!")
        event.Skip()

# ----------------------------------------------------------------------

