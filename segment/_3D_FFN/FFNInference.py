###
###
###
import sys, os, time, errno
import numpy as np
import copy
from itertools import chain
import subprocess as s
import time
import cv2
import h5py
import threading

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)
icon_dir = path.join(main_dir, "icons")
segmentation_dir = path.join(main_dir, "segment")
sys.path.append(segmentation_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))


#######
ffn_dir = path.join(main_dir, "segment","_3D_FFN", "ffn")
sys.path.append(ffn_dir)
from google.protobuf import text_format
from absl import app
from absl import flags
from tensorflow import gfile

from ffn.utils import bounding_box_pb2
from ffn.inference import inference
from ffn.inference import inference_flags
from ffn.inference import inference_pb2

#######

from MiscellaneousSegment import MiscellaneousSegment

if getattr(sys, 'frozen', False):
    #print('Run on pyinstaller.')
    exec_run_inference = os.path.join(main_dir, 'run_inference.exe')
#
else:
    #print('Run on live python.')
    exec_dir = os.path.join(main_dir, 'segment', '_3D_FFN', 'ffn')
    exec_run_inference = 'python ' + os.path.join(exec_dir, 'run_inference.py')

# running live


class FFNInference(MiscellaneousSegment):

    def write_text(self, f, key, value, t):
        if isinstance(value, str):
            f.write(' {0}{1}: "{2}" \n'.format(t, key, value ) )
        else:
            f.write(' {0}{1}: {2} \n'.format(t, key, value))

    def write_call(self, f, request, t):
        for key, value in request.items():
            if isinstance(request[key], dict):
                f.write('{} {{\n'.format(key))
                tid = t + "  "
                self.write_call(f, request[key], tid)
                f.write('}\n')
            else:
                self.write_text(f, key, value, t)

    def _Run(self, parent, params, comm_title):

        ##
        ## h5 file (target image file) generation.
        ##
        target_image_file_h5 = os.path.join(params['FFN File Folder'], "grayscale_inf.h5")

        try:
            target_image_files = self.ObtainImageFiles(params['Target Image Folder'])
            images = [cv2.imread(i, cv2.IMREAD_GRAYSCALE) for i in target_image_files]
            images = np.array(images)
            image_x    = images.shape[0]
            image_y    = images.shape[1]
            image_z    = images.shape[2]
            image_mean = np.mean(images).astype(np.int16)
            image_std  = np.std(images).astype(np.int16)
            with h5py.File( target_image_file_h5 , 'w') as f:
                f.create_dataset('raw', data=images, compression='gzip')
            print('h5 file (target image) was generated.')
        except:
            print("Error: Target Image h5 was not generated.")
            return False

        ##
        ## Inference configration file generation
        ##
        request = {}
        request['image'] = {"hdf5": "{}@raw".format(target_image_file_h5).replace('\\', '/') }
        request['image_mean'] = image_mean
        request['image_stddev'] = image_std
        request['checkpoint_interval'] = int(params['Checkpoint Interval'])
        request['seed_policy'] = "PolicyPeaks"
        request['model_checkpoint_path'] = params['Tensorflow Model File'].replace('\\', '/')
        request['model_name'] = "convstack_3d.ConvStack3DFFNModel"

        print("params['Sparse Z']", params['Sparse Z'])
        if params['Sparse Z'] != Qt.Unchecked:
            request['model_args'] = "{\\\"depth\\\": 9, \\\"fov_size\\\": [33, 33, 17], \\\"deltas\\\": [8, 8, 4]}"
            #request['model_args'] = ' {"depth":9,"fov_size":[33,33,17],"deltas":[8,8,4]} '
        else :
            request['model_args'] = "{\\\"depth\\\": 12, \\\"fov_size\\\": [33, 33, 33], \\\"deltas\\\": [8, 8, 8]}"
            #request['model_args'] = ' {"depth":12,"fov_size":[33,33,33],"deltas":[8,8,8]} '

        request['segmentation_output_dir'] = params['Output Inference Folder'].replace('\\', '/')
        inference_options = {}
        inference_options['init_activation'] = 0.95
        inference_options['pad_value'] = 0.05
        inference_options['move_threshold'] = 0.9
        inference_options['min_boundary_dist'] = {"x": 1, "y": 1, "z": 1}
        inference_options['segment_threshold'] = 0.6
        inference_options['min_segment_size'] = 1000
        request['inference_options'] = inference_options

        config_file = os.path.join(params['FFN File Folder'], "inference_params.pbtxt")
        with open(config_file, "w", encoding='utf-8') as f:
            self.write_call(f, request, "")

        print('Configuration file was saved at :')
        print(config_file)

        ##
        ## Inference start (I gave up the use of run_inference because of the augment parsing problem)
        ##
        request = inference_pb2.InferenceRequest()
        with open(config_file, mode='r') as f:
            text_list = f.readlines()
        text = ' '.join(text_list)
        text_format.Parse(text, request)

        if not gfile.Exists(request.segmentation_output_dir):
            gfile.MakeDirs(request.segmentation_output_dir)
        runner = inference.Runner()
        runner.start(request)
        #  runner.run((bbox.start.z, bbox.start.y, bbox.start.x),
        #             (bbox.size.z, bbox.size.y, bbox.size.x))
        runner.run((0, 0, 0),
                   (image_z, image_y, image_x))

        counter_path = os.path.join(request.segmentation_output_dir, 'counters.txt')
        if not gfile.Exists(counter_path):
            runner.counters.dump(counter_path)
        ##
        ##
        print(comm_title, 'was finished.')
        ##
        return True
        ##

    def __init__(self, u_info):
        ##
        datadir = u_info.data_path
        Inference_image_path = os.path.join(datadir, "_3DNN_training_images")
        ffn_file_path        = os.path.join(datadir, "ffn")
        tensorflow_file      = os.path.join(datadir, "_3DNN_model_tensorflow", "model.ckpt-2000000.data-00000-of-00001")
        self.paramfile = os.path.join(datadir, "parameters", "FFN_Inference.pickle")

        self.filter_name = 'FFN Inference'

        self.tips = [
                        'Path to folder containing target images',
                        'Output inference folder',
                        'Tensorflow model File',
                        'Click it if you used in the training process',
                        'Checkpoint Interval',
                        'FFN File Folder',
                        ]

        self.args = [
                        ['Target Image Folder',  'LineEdit', Inference_image_path, 'BrowseDirImg'],
                        ['Output Inference Folder',  'LineEdit', ffn_file_path, 'BrowseDir'],
                        ['Tensorflow Model File', 'LineEdit', tensorflow_file, 'BrowseFile'],
                        ['Sparse Z', 'CheckBox', False],
                        ['Checkpoint Interval', 'SpinBox', [100, 1800, 65535]],
                        ['FFN File Folder',   'LineEdit', ffn_file_path, 'BrowseDir'],
            ]


    def Execute(self, parent, comm_title, obj_args, args):
        params = self.ObtainParams(obj_args, args)
        thread = threading.Thread(target=self._Run, args=( parent, params, comm_title ) )
        thread.daemon = True
        thread.start()
        QMessageBox.about(parent, 'FFN',  comm_title + ' runs on a different process.')
        # parent.close()
        return

