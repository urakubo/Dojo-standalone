###
###
###

import sys, os, time, errno

import numpy as np
import copy
from itertools import chain
import subprocess as s
import time


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

        inference_params = self.ObtainUIParamsStr(self.obj_args_inference, self.args_inference, self.args_inference_title)

        def DerivParam(param_name):
            id = self.args_inference_title.index(param_name)
            return inference_params[id]

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
                + ' --input_dir ' + DerivParam('Image Folder') + ' ' \
                + ' --output_dir ' + DerivParam('Output Segmentation Folder') + ' ' \
                + ' --checkpoint ' + DerivParam('Checkpoint') + ' ' \
                + ' --image_height ' + DerivParam('Image Height') + ' ' \
                + ' --image_width ' + DerivParam('Image Width')
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

