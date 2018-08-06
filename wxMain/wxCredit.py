##
##
##

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import wx.adv
import os

from os import path, pardir
current_dir = path.abspath(path.dirname(__file__))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
icon_dir    = path.join(parent_dir, "icons")

class wxCredit():

    def AboutDojo(self, event):
        description = 'This is a test'

        about = wx.adv.AboutDialogInfo()
        about.SetIcon(   wx.Icon(  path.join(icon_dir, "Mojo2_128.png") , wx.BITMAP_TYPE_PNG) )
        about.SetName('Dojo Standalone')
        about.SetVersion('1.0')
        about.SetDescription(description)
        about.SetCopyright('(C) 2018 Hidetoshi Urakubo')
        about.SetWebSite('http://www.rhoana.org/dojo/')
        about.AddDeveloper('Hideotshi Urakubo')
        about.AddDeveloper('Torsten Bullmann')
        about.AddDocWriter('Hideotshi Urakubo')
        about.AddDocWriter('Torsten Bullmann')
        about.AddDocWriter('Shin Ishii')
        wx.adv.AboutBox(about)
