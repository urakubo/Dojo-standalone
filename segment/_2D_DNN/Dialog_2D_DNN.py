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


from PartDialogTraining  import PartDialogTraining
from PartDialogTrainingExecutor  import PartDialogTrainingExecutor
from PartDialogInference  import PartDialogInference
from PartDialogInferenceExecutor  import PartDialogInferenceExecutor

class Dialog_2D_DNN(QWidget, PartDialogTraining, PartDialogTrainingExecutor, PartDialogInference, PartDialogInferenceExecutor, MiscellaneousSegment):
    def __init__(self, parent):
        super().__init__()
        self.left   = 200
        self.top    = 200
        self.width  = 800
        self.height = 250
        self.comboText = None
        self.u_info = parent.u_info
        self.parent = parent
        self.title  = "2D DNN"
        self.initUI()


    def initUI(self):


        ##
        ## Define tab
        ##
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 500)

        # Add tabs
        self.tabs.addTab(self.tab1,"Training")
        self.tabs.addTab(self.tab2,"Inference")

        self.TrainingSetParams(self.tab1)
        self.InferenceSetParams(self.tab2)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(path.join(icon_dir, 'Mojo2_16.png')))
        self.show()

    ##
    ##
    ##
    def ObtainUIParams(self, obj_args, args):
        args_header = [args[i][0] for i in range(len(args))]
        params = []
        for i, arg in enumerate(args_header):
            param = []
            if   args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
            params.append(param)

        return params


    ##
    ##
    ##
    def ObtainUIParamsStr(self, obj_args, args):
        args_header = [args[i][0] for i in range(len(args))]
        params = []
        for i, arg in enumerate(args_header):
            param = []
            if   args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
                param = ' ' + str(param) + ' '
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
                param = self.obj_args_training[i].tabText(param)
            params.append(param)

        return params



    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        print('2D DNN was not executed.')
        return False


    def OrganizeTab(self, tab,  lbl, obj_args, display_order, require_browse_dir, require_browse_dir_img, require_browse_file, Execute):
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        for i, id in enumerate(display_order):
            tab.layout.addWidget(lbl[id], i + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol - 1)
            if id in require_browse_dir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_dir_img:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir_img(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browse_file:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda  state, x=id: self.browse_file(obj_args[x]))
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))


                # addWidget(*Widget, row, column, rowspan, colspan)

        ## Execute & cancel buttons
        ok_import = QPushButton("Execute")
        cl_import = QPushButton("Cancel")
        ok_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cl_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        ok_import.clicked.connect(Execute)
        cl_import.clicked.connect(self.Cancel)
        tab.layout.addWidget(ok_import, i + 2, 1, alignment=(Qt.AlignRight))
        tab.layout.addWidget(cl_import, i + 2, 2)
        tab.layout.setRowStretch(10, 1) # I do not understand why >(5, 1) produces top aligned rows.
        tab.setLayout(tab.layout)

        return