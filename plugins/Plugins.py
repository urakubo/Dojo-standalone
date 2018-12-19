
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

import socket
import sys
import os
from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)


# ----------------------------------------------------------------------
# Interface of plugins to Control Panel
# Please add user defined functions
# Also please edit "menu.json" for a plugins pulldown menu.
# ----------------------------------------------------------------------

sys.path.append(path.join(plugins_dir, "superpixel"))
sys.path.append(path.join(plugins_dir, "export_stl"))
sys.path.append(path.join(plugins_dir, "stl_viewer"))
from StlViewer import StlViewer

# import wxglade_superpixel

class Plugins():

    def ExportStl_(self):
        print("'Export Stl' not implemented!")


    def StlViewer_(self):

        ## Dialog: Is Dojo activated?
        if self.u_info.files_found == False:
            QMessageBox.information(self, "3D Viewer", "Please Open Dojo File!")
            return

        ## Dialog: Is the 3D Viewer already launched?
        if 2 in self.table_widget.appl:
            QMessageBox.information(self, "3D Viewer", "3D Viewer Has Already Been Launched!")
            return

        ## Initialize
        self.stl_viewer = StlViewer(self)
        IDs = self.stl_viewer.ObtainIDs()
        if (IDs == False) or (len(IDs)==0):
            print('No Valid Number is Specified.')
            return

        ## Generate Stl
        self.stl_viewer.GenerateStls(IDs)

        ## Call StlViewer
        self.table_widget.addTab(2, '3D Viewer', self.u_info.url+'stl/index.html' )



    def StlViewer2_(self):

        ## Dialog: Is Dojo activated?
        if self.u_info.files_found == False:
            QMessageBox.information(self, "3D Viewer", "Please Open Dojo File!")
            return

        ## Dialog: Is the 3D Viewer already launched?
        if 2 in self.table_widget.appl:
            QMessageBox.information(self, "3D Viewer", "3D Viewer Has Already Been Launched!")
            return

        ## Initialize
        self.stl_viewer = StlViewer(self)
        IDs = self.stl_viewer.ObtainIDs2()
        if (IDs == False) or (len(IDs)==0):
            print('No Valid Number is Specified.')
            return

        ## Generate Stl
        self.stl_viewer.GenerateStls(IDs)

        ## Call StlViewer
        self.table_widget.addTab(2, '3D Viewer', self.u_info.url + 'stl/index.html')

#    def Tensorboard_(self):
#        tmp = Tensorboard(self)
#        self.table_widget._addTab(0, 'Tensorboard', 'http://' + socket.gethostbyname(socket.gethostname()) + ':6006' )

    def SuperPixel_(self):
        #import wx
        # self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "",sim_name=[self, self.UserInfo])
    	#self.superpix = wxglade_superpixel.SuperPixel(self, wx.ID_ANY, "")
        #self.superpix.Show()
        #event.Skip()
        pass

    def UserDefined_(self):
        print("'User Defined' is not implemented!")
        # event.Skip()

# ----------------------------------------------------------------------

