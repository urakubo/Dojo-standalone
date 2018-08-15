#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import wx.adv
import wx.grid
import sys
import os

sys.path.append("./wxMain")
sys.path.append("./Filesystem")

if os.name == 'nt':
  try:
    import win32api
  except Exception:
    print('No win32api module.')


import wxMain8 as wxg
from Params import Params

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):

        self.u_info = Params()
        self.control_panel = wxg.ControlPanel(None, wx.ID_ANY, "",sim_name=[self, self.u_info])
        self.SetTopWindow(self.control_panel)
        self.control_panel.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

