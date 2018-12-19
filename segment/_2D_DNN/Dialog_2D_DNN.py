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

from PartDialogTraining  import PartDialogTraining
from PartDialogTrainingExecutor  import PartDialogTrainingExecutor
from PartDialogInference  import PartDialogInference
from PartDialogInferenceExecutor  import PartDialogInferenceExecutor

class Dialog_2D_DNN(QWidget, PartDialogTraining, PartDialogTrainingExecutor, PartDialogInference, PartDialogInferenceExecutor):
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
    def ObtainUIParams(self, obj_args, args, args_title):

        params = []
        for i, arg in enumerate(args_title):
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
    def ObtainUIParamsStr(self, obj_args, args, args_title):

        params = []
        for i, arg in enumerate(args_title):
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



    def save_params_2D(self, obj_args, args, args_title, TrainOrInf):

        print('')

        params = self.ObtainUIParams(obj_args, args, args_title)

        id = args_title.index('Save Parameters')
        filename = obj_args[id].text()
        print('')
        print('Save file : ', filename)
        self.print_current_states(obj_args, args, args_title)
        print('')
        try:
            with open(filename, mode='wb') as f:
                pickle.dump(params, f)
            print(TrainOrInf, 'parameter file for 2D DNN was saved.')
        except :
            print(TrainOrInf, 'parameter file for 2D DNN cannot be saved.')
            return False

        return True


    def load_params_2D(self, obj_args, args, args_title, TrainOrInf):
        #
        id = args_title.index('Load Parameters')
        filename = obj_args[id].text()
        print('')
        print('Load file : ', filename)
        try:
            with open(filename, mode='rb') as f:
                params = pickle.load(f)
        except :  # parent of IOError, OSError *and* WindowsError where available
            print(TrainOrInf, ' parameter file for 2D DNN cannot be open.')
            return False

        for i, arg in enumerate(args_title):
            if   args[i][1] == 'LineEdit':
                obj_args[i].setText( params[i] )
            elif args[i][1] == 'SpinBox':
                obj_args[i].setValue( params[i] )
            elif args[i][1] == 'ComboBox':
                id = obj_args[i].findText( params[i] )
                obj_args[i].setCurrentIndex( id )
            elif args[i][1] == 'Tab':
                obj_args[i].setCurrentIndex( params[i] )

        self.print_current_states(obj_args, args, args_title)
        return True


    def print_current_states(self, obj_args, args, args_title):
        for i, arg in enumerate(args_title):
            if   args[i][1] == 'LineEdit':
                param = obj_args[i].text()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
                print("{0:>20} : {1:d}".format(arg, param))
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
                print("{0:>20} : {1:s}".format(arg, param))
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
                print("{0:>20} : {1:s}".format(arg, obj_args[i].tabText(param)))


    def browse_dir(self, lineedit_obj):
        currentdir = lineedit_obj.text()
        newdir = QFileDialog.getExistingDirectory(self, "Select Folder", currentdir)
        if len(newdir) == 0:
            return False
        newdir = newdir.replace('/', os.sep)
        lineedit_obj.setText(newdir)
        return True


    def browse_file(self, lineedit_obj):
        currentfile = lineedit_obj.text()
        newf = QFileDialog.getOpenFileName(self, "Select Folder", currentfile)
        newfile = newfile[0]
        if len(newfile) == 0:
            return False
        newfile = newfile.replace('/', os.sep)
        lineedit_obj.setText(newfile)
        return True


    def Cancel(self):  # wxGlade: ImportImagesSegments.<event_handler>
        self.close()
        print('2D DNN was not executed.')
        return False


    def OrganizeTab(self, tab,  lbl, obj_args, display_order, require_browsedir, require_browsefile, Execute):
        tab.layout = QGridLayout(tab)
        ncol = 8
        browse_button = []
        for i, id in enumerate(display_order):
            tab.layout.addWidget(lbl[id], i + 1, 0, alignment=Qt.AlignRight)  # (Qt.AlignRight | Qt.AlignTop)
            if id in require_browsedir:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_dir(obj_args[x]))
                tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol - 1)
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            elif id in require_browsefile:
                browse_button.append(QPushButton("Browse..."))
                browse_button[-1].clicked.connect(lambda state, x=id: self.browse_file(obj_args[x]))
                tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol - 1)
                tab.layout.addWidget(browse_button[-1], i + 1, ncol, 1, 1, alignment=(Qt.AlignRight))
            else:
                tab.layout.addWidget(obj_args[id], i + 1, 1, 1, ncol)
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