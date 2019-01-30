import sys, os, time, errno


import numpy as np
import copy
from distutils.dir_util import copy_tree
from itertools import chain
import pickle
import threading
import tornado
import tornado.websocket
import glob     # Wild card
import cv2
import threading

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QTabWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, QSpinBox, QSlider, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, \
    QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSlot


import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
from Executor  import Executor

H = 256
W = 256
MAXSLIDER = 100

class ThumbnailGeneratorFFN():

    def __init__(self, parent):
        self.parent = parent

    def _ChangeZ(self):
        params = self.ObtainParams()
        self.training_file_stack = self.ObtainImageFiles( params['Training Image Folder'] )
        self.ground_truth_file_stack = self.ObtainImageFiles( params['Ground Truth Folder'] )
        sz = self.control_thumbnail[0].value()  # Z 0:99
        if len(self.training_file_stack) > 0 and len(self.ground_truth_file_stack) > 0 :
            znum = len( self.training_file_stack )
            id = np.floor(znum * sz / MAXSLIDER).astype(np.uint16)
            self.training_image = cv2.imread(self.training_file_stack[id], cv2.IMREAD_GRAYSCALE)
            znum = len( self.ground_truth_file_stack )
            id = np.floor(znum * sz / MAXSLIDER).astype(np.uint16)
            self.ground_truth = cv2.imread(self.ground_truth_file_stack[id], -1).astype(np.uint8)
            self._ChangeXY()

    def _ChangeXY(self):
        sx = self.control_thumbnail[1].value() # X 0:99
        sy = self.control_thumbnail[2].value() # y 0:99

        if len(self.training_image) > 0 and len(self.ground_truth) > 0:
            imgy, imgx = self.training_image.shape
            onset_x = (imgx - W) * sx / MAXSLIDER
            onset_y = (imgy - H) * sy / MAXSLIDER
            onset_x = int(onset_x)
            onset_y = int(onset_y)
            onset_x = (onset_x > 0) * onset_x
            onset_y = (onset_y > 0) * onset_y
            self.training_image_cropped = self.training_image[ onset_y : onset_y + H, onset_x : onset_x + W].copy()

            if self.normal_training_image.isChecked() == True:
                normal_factor = (255 / np.max(self.training_image_cropped) ).astype(np.float)
                training_cropped_normalized = (self.training_image_cropped * normal_factor).astype(np.uint8)
            else:
                training_cropped_normalized = self.training_image_cropped


            imgy, imgx = self.ground_truth.shape
            onset_x = (imgx - W) * sx / MAXSLIDER
            onset_y = (imgy - H) * sy / MAXSLIDER
            onset_x = int(onset_x)
            onset_y = int(onset_y)
            onset_x = (onset_x > 0) * onset_x
            onset_y = (onset_y > 0) * onset_y
            self.ground_truth_cropped = self.ground_truth[ onset_y : onset_y + H, onset_x : onset_x + W].copy()

            if self.normal_ground_truth.isChecked() == True:
                normal_factor = (255 / np.max(self.ground_truth_cropped) ).astype(np.float)
                truth_cropped_normalized = (self.ground_truth_cropped * normal_factor).astype(np.uint8)
            else:
                truth_cropped_normalized = self.ground_truth_cropped


            qimage1 = QtGui.QImage(training_cropped_normalized, W, H,
                           QtGui.QImage.Format_Grayscale8)
            pixmap1 = QtGui.QPixmap.fromImage(qimage1)
            self.canvas1.setPixmap(pixmap1)

            qimage2 = QtGui.QImage(truth_cropped_normalized, W, H,
                           QtGui.QImage.Format_Grayscale8)
            pixmap2 = QtGui.QPixmap.fromImage(qimage2)
            self.canvas2.setPixmap(pixmap2)


    def GenerateThumbnailObject(self, filter, obj_args, args):
        ##
        ## Canvas
        ##
        self.training_image_cropped = []
        self.truth_image_cropped = []
        self.filter   = filter
        self.obj_args = obj_args
        self.args     = args

        image1 = (np.ones((H, W))*128).astype(np.uint8)
        image2 = (np.ones((H, W))*128).astype(np.uint8)

        qimage1 = QtGui.QImage(image1.data, image1.shape[1], image1.shape[0],
                              QtGui.QImage.Format_Grayscale8)
        pixmap1 = QtGui.QPixmap.fromImage(qimage1)

        qimage2 = QtGui.QImage(image2.data, image2.shape[1], image2.shape[0],
                              QtGui.QImage.Format_Grayscale8)
        pixmap2 = QtGui.QPixmap.fromImage(qimage2)

        self.canvas1 = QLabel()
        self.canvas1.setPixmap(pixmap1)

        self.canvas2 = QLabel()
        self.canvas2.setPixmap(pixmap2)


        slider_names    = ['Target Z', 'Target X', 'Target Y']
        slider_events   = [ self._ChangeZ, self._ChangeXY, self._ChangeXY ]

        self.control_thumbnail  = []
        s = []
        vbox = QVBoxLayout()
        for i in range(len(slider_names)) :
            vbox.addWidget(QLabel(slider_names[i]))
            s.append(QSlider(Qt.Horizontal))
            s[-1].setFocusPolicy(QtCore.Qt.NoFocus)
            s[-1].setTickPosition(QSlider.TicksBothSides)
            s[-1].setMinimum(0)
            s[-1].setMaximum(MAXSLIDER-1)
            s[-1].setValue(0)
            s[-1].setTickInterval(20)
            s[-1].setSingleStep(1)
            vbox.addWidget(s[-1])
            s[-1].valueChanged.connect(slider_events[i])
            self.control_thumbnail.append(s[-1])
        ##
        ##
        self.normal_training_image = QCheckBox('Training image normalized')
        self.normal_training_image.move(20, 20)
        self.normal_training_image.stateChanged.connect( self._ChangeZ )
        vbox.addWidget(self.normal_training_image)
        self.normal_ground_truth = QCheckBox('Ground truth normalized')
        self.normal_ground_truth.move(20, 20)
        self.normal_ground_truth.stateChanged.connect( self._ChangeZ )
        vbox.addWidget(self.normal_ground_truth)
        ##
        ##
        self.norm_sample = QCheckBox('Dummy')
        self.norm_sample.move(2, 2)
        self.norm_sample.stateChanged.connect(lambda: self._ChangeXY)
        vbox.addWidget(self.norm_sample)

        ### Initial sample image
        self._ChangeZ()

        ### Generate objects
        thumb = QWidget()
        thumb.layout = QGridLayout(thumb)

        thumb.layout.addWidget(QLabel('Training image'), 0, 0, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(QLabel('Ground truth'), 0, 1, alignment=Qt.AlignCenter)

        thumb.layout.addWidget(self.canvas1, 1, 0, 1, 1, alignment=Qt.AlignCenter)
        thumb.layout.addWidget(self.canvas2, 1, 1, 1, 1, alignment=Qt.AlignCenter)

        thumb.layout.addLayout(vbox, 0, 2, -1, 1, alignment=Qt.AlignCenter)

        thumb.layout.setRowStretch(3, 2) # I do not understand why >(5, 1) produces top aligned rows.
        thumb.setLayout(thumb.layout)

        return thumb

    def ObtainImageFiles(self, input_path):
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        search3 = os.path.join(input_path, '*.tiff')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))
        filestack.extend(sorted(glob.glob(search3)))
        return filestack


    def ObtainParams(self):

        obj_args = self.obj_args
        args     = self.args

        args_header = [args[i][0] for i in range(len(args))]
        params = {}
        for i, arg in enumerate(args):
            param = {}
            if   args[i][1] == 'LineEdit':
                param = obj_args[i].text()
            elif args[i][1] == 'SpinBox':
                param = obj_args[i].value()
            elif args[i][1] == 'ComboBox':
                param = obj_args[i].currentText()
            elif args[i][1] == 'Tab':
                param = obj_args[i].currentIndex()
            elif args[i][1] == 'CheckBox':
                param = obj_args[i].checkState()
            params[args_header[i]] = param
        return params
