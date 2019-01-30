###
###
###

import sys, os, time, errno

import numpy as np
import copy
from itertools import chain
import subprocess as s
import time

import glob     # Wild card
import cv2

from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "segment"))
sys.path.append(os.path.join(main_dir, "filesystem"))

_2D_DNN_dir = os.path.join(main_dir, 'segment', '_2D_DNN')

class PartDialogInferenceExecutor():

    def ExecuteInference(self):  # wxGlade: ImportImagesSegments.<event_handler>
        #
        # Dialog to specify directory
        #

        params = self.ObtainParams(self.obj_args_inference, self.args_inference)

        image_width, image_height = self.ObtainFirstImageSize(params['Image Folder'])

        if getattr(sys, 'frozen', False):
            print('Run on pyinstaller.')
            execfile = os.path.join(main_dir, 'translate.exe')
        # running in a bundle
        else:
            print('Run on live python.')
            execfile = 'python ' +  os.path.join(_2D_DNN_dir, 'translate.py')
        # running live


        comm = execfile +' ' \
                + ' --mode test ' \
                + ' --model pix2pix ' \
                + ' --save_freq 0 ' \
                + ' --input_dir ' + params['Image Folder'] + ' ' \
                + ' --input_dir_B ' + params['Image Folder'] + ' ' \
                + ' --output_dir ' + params['Output Segmentation Folder'] + ' ' \
                + ' --checkpoint ' + params['Checkpoint Folder'] + ' ' \
                + ' --image_height ' + str(image_height) + ' ' \
                + ' --image_width ' + str(image_width)
        # - -image_height 1024
        # - -image_width 1024


        try:
            print(comm)
            print('Start inference.')
            s.Popen(comm.split())
        except subprocess.CalledProcessError as e:
            print("Inference was not executed.")
            self.Cancel()
            return False

        QMessageBox.about(self, '2D DNN', 'Inference runs on a different process.\nLaunch Tensorboard to monitor the progress.')

        self.close()
        return True


    def ObtainFirstImageSize(self, input_path):

        ## Obtain parameters
        #
        search1 = os.path.join(input_path, '*.png')
        search2 = os.path.join(input_path, '*.tif')
        filestack = sorted(glob.glob(search1))
        filestack.extend(sorted(glob.glob(search2)))

        input_image = cv2.imread(filestack[0], cv2.IMREAD_GRAYSCALE)
        image_width, image_height = input_image.shape
        print(input_image.shape)
        return image_width, image_height

