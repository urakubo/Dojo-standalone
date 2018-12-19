###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


from os import path, pardir
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QInputDialog, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

main_dir    = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

from Params import Params
from ImportImgSeg import ImportImgSeg
# import UndoRedo


class ImportDialog(QWidget):
 
    def __init__(self, u_info, parent):
        super().__init__()
        self.title = 'Import Images & Segments'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 150

        self.u_info = u_info
        self.parent = parent
        self.initUI()

    def initUI(self):

        # Labels
        lbl1 = QLabel('Source Image Folder:<BR>(TIFF/PNG)')
        lbl2 = QLabel('Source Segmentation Folder:<BR>(TIFF/PNG)')
        lbl3 = QLabel('Destination Dojo Folder:')

        self.edit1=QLineEdit()
        self.edit2=QLineEdit()
        self.edit3=QLineEdit()

        self.edit1.setText( self.u_info.files_path )
        self.edit2.setText( self.u_info.files_path )
        self.edit3.setText( self.u_info.files_path )

        btn1=QPushButton("Browse...")
        btn2=QPushButton("Browse...")
        btn3=QPushButton("Browse...")

        btn1.clicked.connect(self._dir1_img)
        btn2.clicked.connect(self._dir2_seg)
        btn3.clicked.connect(self._dir3_dst)

        ok_import = QPushButton("OK")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ok_import.clicked.connect(self._ExecuteImport)
        cl_import.clicked.connect(self._Cancel)


        layout = QGridLayout()
        layout.addWidget(lbl1, 0, 0)
        layout.addWidget(lbl2, 1, 0)
        layout.addWidget(lbl3, 2, 0)

        layout.addWidget(self.edit1, 0, 1)
        layout.addWidget(self.edit2, 1, 1)
        layout.addWidget(self.edit3, 2, 1)

        layout.addWidget(btn1, 0, 2)
        layout.addWidget(btn2, 1, 2)
        layout.addWidget(btn3, 2, 2)

        layout.addWidget(ok_import, 3, 1, alignment=(Qt.AlignRight))
        layout.addWidget(cl_import, 3, 2)

        self.setLayout(layout)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()


    def _dir1_img(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Image Folder", self.edit1.text())
        if len(fname) == 0:
            return
        fname = fname.replace('/', os.sep)
        self.edit1.setText(fname)

    def _dir2_seg(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Segmentation Folder", self.edit2.text())
        if len(fname) == 0:
            return
        fname = fname.replace('/', os.sep)
        self.edit2.setText(fname)

    def _dir3_dst(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Dojo Folder", self.edit3.text())
        if len(fname) == 0:
            return
        fname = fname.replace('/', os.sep)
        self.edit3.setText(fname)



    def _ExecuteImport(self):  # wxGlade: ImportImagesSegments.<event_handler>
        dir_input_images = self.edit1.text()
        dir_input_ids = self.edit2.text()
        self.u_info.SetUserInfo(self.edit3.text())

        im = ImportImgSeg(self.u_info)
        Flag1 = im.images(dir_input_images)  ###
        Flag2 = im.ids(dir_input_ids)        ###
        print(Flag1)
        print(Flag2)
        if Flag1 == False or Flag2 == False:
            print('Error! Dojo files were not created.')
            self.close()
            return False
        print('Dojo files were successfully created.')
        self.u_info.files_found = True
        self.close()
        statusbar = ["Target Dojo folder: " + self.u_info.files_path]
        for i in range(len(statusbar)):
            self.parent.frame_statusbar.SetStatusText(statusbar[i], i)

        self.parent.LaunchDojo()
        self.close()
        return True

    def _Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        return False

