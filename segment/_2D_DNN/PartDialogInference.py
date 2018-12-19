###
###
###
import sys, os, time, errno

import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import subprocess as s
import tornado
import tornado.websocket
import time


from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox,  \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))


class PartDialogInference():
    def InferenceSetParams(self, tab):

        tips = [
                        'Path to folder containing images',
                        'Path to folder for storing segmentation',
                        'Directory with checkpoint for training data',
                        'Target image height ',
                        'Target image width ',
                        'Save Parameters ',
                        'Load Parameters '
                        ]

        datadir = self.parent.u_info.segmentation_data_path
        imgpath =  os.path.join(datadir, "segment_2DNN_img")
        outpath =  os.path.join(datadir, "segment_2DNN_out")
        paramfile = os.path.join(datadir, "Inference_Params_2D.pickle")
        self.args_inference = [
                        ['Image Folder',    'LineEdit', imgpath, 'Browsedir'],
                        ['Output Segmentation Folder',   'LineEdit', outpath, 'Browsedir'],
                        ['Checkpoint',      'LineEdit', datadir, 'Browsedir'],
                        ['Image Height', 'SpinBox', [0, 1024, 65535]],
                        ['Image Width',  'SpinBox', [0, 512, 65535]],
                        ['Save Parameters', 'LineEdit',paramfile, 'Browsefile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'Browsefile']
                        ]
        self.args_inference_title = [self.args_inference[i][0] for i in range(len(self.args_inference))]


        ## Labels
        lbl   = []
        self.obj_args_inference = []
        require_browsedir = []
        require_browsefile = []
        ##
        for i in range(len(self.args_inference)):
        ##
            arg = self.args_inference[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self._save_inference_params_2D)
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self._load_inference_params_2D)
            else :
                lbl.append(QLabel(self.args_inference_title[i] + ' :'))
                lbl[-1].setToolTip(tips[i])
        ##
        for i in range(len(self.args_inference)):
        ##
            if  self.args_inference[i][1] == 'LineEdit':
                self.obj_args_inference.append( QLineEdit() )
                self.obj_args_inference[-1].setText( self.args_inference[i][2] )
                if self.args_inference[i][3] == 'Browsedir':
                    require_browsedir.append(i)
                if self.args_inference[i][3] == 'Browsefile':
                    require_browsefile.append(i)
            elif self.args_inference[i][1] == 'SpinBox':
                self.obj_args_inference.append(QSpinBox())
                self.obj_args_inference[-1].setMinimum( self.args_inference[i][2][0] )
                self.obj_args_inference[-1].setMaximum( self.args_inference[i][2][2] )
                self.obj_args_inference[-1].setValue( self.args_inference[i][2][1] )
            elif self.args_inference[i][1] == 'ComboBox':
                self.obj_args_inference.append(QComboBox(self))
                items = self.args_inference[i][2]
                for item in items:
                    self.obj_args_inference[-1].addItem(item)
            else:
                print('Internal error. No fucntion.')

        # Organize tab widget
        display_order = [0,1,2,3,4]
        self.OrganizeTab(tab, lbl, self.obj_args_inference, display_order, require_browsedir, require_browsefile, self.ExecuteInference)


    def _save_inference_params_2D(self):
        self.save_params_2D(self.obj_args_inference, self.args_inference, self.args_inference_title, 'Inference')
        return True

    def _load_inference_params_2D(self):
        self.load_params_2D(self.obj_args_inference, self.args_inference, self.args_inference_title, 'Inference')
        return True


