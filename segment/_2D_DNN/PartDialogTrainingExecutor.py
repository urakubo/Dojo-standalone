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

class PartDialogTrainingExecutor():

    def ExecuteTraining(self):  # wxGlade: ImportImagesSegments.<event_handler>
        #
        # Dialog to specify directory
        #

        if getattr(sys, 'frozen', False):
            print('Run on pyinstaller.')
            execfile = os.path.join(main_dir, 'translate.exe')
        # running in a bundle
        else:
            print('Run on live python.')
            execfile = 'python ' +  os.path.join(_2D_DNN_dir, 'translate.py')
        # running live


        training_params = self.ObtainUIParamsStr(self.obj_args_training, self.args_training, self.args_training_title)

        def DerivParam(param_name):
            id = self.args_training_title.index(param_name)
            return training_params[id]

        id = self.args_training_title.index('Augmentation')
        aug = training_params[id]
        if   aug == "fliplr, flipud, transpose":
            augmentation = '--fliplr --flipud --transpose'
        elif aug == "fliplr, flipud":
            augmentation = '--fliplr --flipud --no_transpose'
        elif aug == "fliplr":
            augmentation = '--fliplr --no_flipud --no_transpose'
        elif aug == "flipud":
            augmentation = '--no_fliplr --flipud --no_transpose'
        elif aug == "None":
            augmentation = '--no_fliplr --no_flipud --no_transpose'
        else :
            print("Internal error at Augumentation of PartDialogTrainingExecutor.")
            self._Cancel()
            return False
        #
        print('Images and segmentation were merged.')
        #
        comm = execfile +' ' \
                + ' --mode train ' \
                + ' --input_dir ' + DerivParam('Image Folder') + ' ' \
                + ' --input_dir_B ' + DerivParam('Segmentation Folder') + ' ' \
                + ' --output_dir ' + DerivParam('Checkpoint') + ' ' \
                + ' --which_direction AtoB ' +  ' ' \
                + ' --X_loss ' + DerivParam('X Loss Function') + ' ' \
                + ' --Y_loss ' + DerivParam('Y Loss Function') + ' ' \
                + ' --model ' + DerivParam('Model') + ' ' \
                + ' --generator ' + DerivParam('Generator') + ' ' \
                + ' ' + augmentation + ' ' \
                + ' --max_epochs ' + DerivParam('Maximal Epochs') + ' ' \
                + ' --display_freq ' +  DerivParam('Display Frequency') + ' ' \
                + ' --u_depth ' + DerivParam('U depth') + ' ' \
                + ' --n_res_blocks ' + DerivParam('N res blocks') + ' ' \
                + ' --n_highway_units ' + DerivParam('N highway units') + ' ' \
                + ' --n_dense_blocks ' + DerivParam('N dense blocks') + ' ' \
                + ' --n_dense_layers ' + DerivParam('N dense layers') + ' '



        print(comm)
        print('Start training.')
        try:
            s.Popen(comm.split())
        except s.CalledProcessError as e:
            print("Merger was not executed.")
            self.Cancel()
            return False


        QMessageBox.about(self, '2D DNN', 'Training runs on a different process.\nLaunch Tensorboard to monitor the progress.')

        self.close()
        return True


