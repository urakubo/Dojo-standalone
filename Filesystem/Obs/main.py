#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
import sys
import wx
# sys.path.append('MojoControlPanel/')
import wxglade_mojo as wxg
import DefaultParams

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):

        self.MojoControlPanel = wxg.MojoControlPanel(None, wx.ID_ANY, "")
        self.SetTopWindow(self.MojoControlPanel)
        self.MojoControlPanel.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

