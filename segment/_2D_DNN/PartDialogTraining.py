###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


class PartDialogTraining():
    def TrainingSetParams(self, tab):


        tips = [
                        'Path to folder containing images',
                        'Number of images in batch',
                        'Path to folder containing segmentation',
                        'Output Filetype',
                        'Directory with checkpoint to resume training from or use for testing',
                        'Model',
                        'Discriminator on target vs output or paired with input',
                        'Generator',
                        'Number of training epochs',
                        'Write current training images every display frequency steps',
                        'X Loss Function',
                        'X Loss Function',
                        'Dimensions for Augmentation',
                        'Save Parameters ',
                        'Load Parameters ',
                        'Depth of U-net (maximum 8)',
                        'Number of residual blocks in res net',
                        'Number of highway units in highway net',
                        'Number of dense blocks in dense net',
                        'Number of dense connected layers in each block of the dense net'
                        ]

        datadir = self.parent.u_info.segmentation_data_path
        imgpath =  os.path.join(datadir, "segment_2DNN_img")
        segpath =  os.path.join(datadir, "segment_2DNN_seg")
        paramfile = os.path.join(datadir, "Training_Params_2D.pickle")
        self.args_training = [
                        ['Image Folder',    'LineEdit', imgpath, 'Browsedir'],
                        ['Batch Size',      'SpinBox', [1,1, 65535]],
                        ['Segmentation Folder',   'LineEdit', segpath, 'Browsedir'],
                        ['Output Filetype', 'ComboBox', ['png','jpeg']],
                        ['Checkpoint',      'LineEdit', datadir, 'Browsedir'],
                        ['Model', 'ComboBox',   ['pix2pix','pix2pix2','CycleGAN']],
                        ['Discriminator (CycleGAN only)', 'ComboBox', ['', 'paired', 'unpaired']],
                        ['Maximal Epochs', 'SpinBox', [1, 2000, 65535]],
                        ['Display Frequency', 'SpinBox', [0, 200, 65535]],
                        ['X Loss Function', 'ComboBox',   ["hinge", "square", "softmax", "approx", "dice", "logistic"]],
                        ['Y Loss Function', 'ComboBox',   ["square", "hinge", "softmax", "approx", "dice", "logistic"]],
                        ['Augmentation',    'ComboBox', ["fliplr, flipud, transpose", "fliplr, flipud", "fliplr", "flipud", "None"]],
                        ['Save Parameters', 'LineEdit',paramfile, 'Browsefile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'Browsefile'],
                        ['U depth','SpinBox',[1,8,8]],
                        ['N res blocks','SpinBox',[1,9,255]],
                        ['N highway units','SpinBox',[1,9,255]],
                        ['N dense blocks','SpinBox',[1,5,255]],
                        ['N dense layers','SpinBox',[1,5,255]],
                        ['Generator', 'Tab', ['unet', 'resnet', 'highwaynet', 'densenet']]
                        ]
        self.args_training_title = [self.args_training[i][0] for i in range(len(self.args_training))]


        ## Labels
        lbl   = []
        self.obj_args_training = []
        require_browsedir = []
        require_browsefile = []
        ##
        for i in range(len(self.args_training)):
        ##
            arg = self.args_training[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self._save_training_params_2D)
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(self._load_training_params_2D)
            else :
                lbl.append(QLabel(self.args_training_title[i] + ' :'))
                lbl[-1].setToolTip(tips[i])
        ##
        for i in range(len(self.args_training)):
        ##
            if  self.args_training[i][1] == 'LineEdit':
                self.obj_args_training.append( QLineEdit() )
                self.obj_args_training[-1].setText( self.args_training[i][2] )
                if self.args_training[i][3] == 'Browsedir':
                    require_browsedir.append(i)
                if self.args_training[i][3] == 'Browsefile':
                    require_browsefile.append(i)
            elif self.args_training[i][1] == 'SpinBox':
                self.obj_args_training.append(QSpinBox())
                self.obj_args_training[-1].setMinimum( self.args_training[i][2][0] )
                self.obj_args_training[-1].setMaximum( self.args_training[i][2][2] )
                self.obj_args_training[-1].setValue( self.args_training[i][2][1] )
            elif self.args_training[i][1] == 'ComboBox':
                self.obj_args_training.append(QComboBox(self))
                items = self.args_training[i][2]
                for item in items:
                    self.obj_args_training[-1].addItem(item)
            elif self.args_training[i][1] == 'Tab':
                # Add tabs
                self.obj_args_training.append(QTabWidget(self))
                ttab = []
                for ttab_title in self.args_training[i][2]:
                    ttab.append( QWidget() )
                    self.obj_args_training[-1].addTab(ttab[-1], ttab_title)
                self._Training2D_Unet(ttab[0], lbl)
                self._Training2D_Resnet(ttab[1], lbl)
                self._Training2D_Highwaynet(ttab[2], lbl)
                self._Training2D_Densenet(ttab[3], lbl)

            else:
                print('Internal error. No fucntion.')


        # Organize tab widget
        display_order = [0,1,2,3,4,5,6,-1,7,8,9,10,11,12,13]
        self.OrganizeTab(tab, lbl, self.obj_args_training, display_order, require_browsedir, require_browsefile, self.ExecuteTraining)


    def _Training2D_Unet(self, ttab, lbl):
        id = self.args_training_title.index('U depth')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args_training[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Resnet(self, ttab, lbl):
        id = self.args_training_title.index('N res blocks')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args_training[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Highwaynet(self, ttab, lbl):
        id = self.args_training_title.index('N highway units')
        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args_training[id], 1, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _Training2D_Densenet(self, ttab, lbl):
        id1 = self.args_training_title.index('N dense blocks')
        id2 = self.args_training_title.index('N dense layers')

        ttab.layout = QGridLayout(ttab)
        ttab.layout.addWidget(lbl[id1], 1, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args_training[id1], 1, 1, 1, 4)
        ttab.layout.addWidget(lbl[id2], 2, 0, alignment=(Qt.AlignRight))
        ttab.layout.addWidget(self.obj_args_training[id2], 2, 1, 1, 4)
        ttab.setLayout(ttab.layout)


    def _save_training_params_2D(self):
        self.save_params_2D(self.obj_args_training, self.args_training, self.args_training_title, 'Training')
        return True

    def _load_training_params_2D(self):
        self.load_params_2D(self.obj_args_training, self.args_training, self.args_training_title, 'Training')
        return True

