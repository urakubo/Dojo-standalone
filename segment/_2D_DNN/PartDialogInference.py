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


from MiscellaneousSegment import MiscellaneousSegment

class PartDialogInference(MiscellaneousSegment):
    def InferenceSetParams(self, tab):

        tips = [
                        'Path to folder containing images',
                        'Path to folder for storing segmentation',
                        'Directory with checkpoint for training data',
                        'Save Parameters ',
                        'Load Parameters '
                        ]

        datadir = self.parent.u_info.data_path
        imgpath =  os.path.join(datadir, "_2DNN_test_images")
        outpath =  os.path.join(datadir, "_2DNN_inference")
        modelpath =  os.path.join(datadir, "_2DNN_model_tensorflow")
        paramfile = os.path.join(datadir, "parameters", "Inference_2D.pickle")
        args = [
                        ['Image Folder',    'LineEdit', imgpath, 'BrowseDirImg'],
                        ['Output Segmentation Folder',   'LineEdit', outpath, 'BrowseDirImg'],
                        ['Checkpoint Folder',      'LineEdit', modelpath, 'BrowseDir'],
                        ['Save Parameters', 'LineEdit',paramfile, 'BrowseFile'],
                        ['Load Parameters', 'LineEdit',paramfile, 'BrowseFile']
                        ]
        self.args_inference_title = [args[i][0] for i in range(len(args))]

        filter_name = 'Inference'

        ## Labels
        lbl   = []
        obj_args = []
        require_browse_dir = []
        require_browse_dir_img = []
        require_browse_file = []
        ##
        ##
        for i in range(len(args)):
        ##
            arg = args[i][0]
            if arg == 'Save Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.save_params(obj_args, args, filter_name))
            elif arg == 'Load Parameters':
                lbl.append(QPushButton(arg))
                lbl[-1].clicked.connect(lambda: self.load_params(obj_args, args, filter_name))
            else :
                lbl.append(QLabel(args[i][0] + ' :'))
                lbl[-1].setToolTip(tips[i])

        ##
        for i in range(len(args)):
        ##
            if  args[i][1] == 'LineEdit':
                obj_args.append( QLineEdit() )
                obj_args[-1].setText( args[i][2] )
                if args[i][3] == 'BrowseDir':
                    require_browse_dir.append(i)
                if args[i][3] == 'BrowseDirImg':
                    require_browse_dir_img.append(i)
                if args[i][3] == 'BrowseFile':
                    require_browse_file.append(i)
            elif args[i][1] == 'SpinBox':
                obj_args.append(QSpinBox())
                obj_args[-1].setMinimum( args[i][2][0] )
                obj_args[-1].setMaximum( args[i][2][2] )
                obj_args[-1].setValue( args[i][2][1] )
            elif args[i][1] == 'ComboBox':
                obj_args.append(QComboBox(self))
                items = args[i][2]
                for item in items:
                    obj_args[-1].addItem(item)
            else:
                print('Internal error. No fucntion.')

        self.obj_args_inference = obj_args
        self.args_inference = args

        # Organize tab widget
        display_order = [0,1,2,3,4]
        self.OrganizeTab(tab, lbl, obj_args, display_order, require_browse_dir,require_browse_dir_img, require_browse_file, self.ExecuteInference)


    def _save_inference_params_2D(self):
        self.save_params(self.obj_args_inference, self.args_inference, 'Inference')
        return True

    def _load_inference_params_2D(self):
        self.load_params(self.obj_args_inference, self.args_inference, 'Inference')
        return True




