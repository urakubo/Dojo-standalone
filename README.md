[Japanese version here](README.ja.md)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This software is under development!

# A unified environment for DNN-based automated segmentation of neuronal EM images

- [Introduction](#Introduction)
- [System requirements](#System-requirements)
- [Installation](#Installation)
- [How to use: Dojo proofreader](#Dojo-proofreader)
- [How to use: 3D annotator](#3D-annotator)
- [How to use: 2D DNN](#2D-DNN)
- [How to use: 3D FFN](#3D-FFN)
- [How to use: 2D and 3D filters](#2D-and-3D-filters)
- [Example workflow1: Mitochondria segmentation by use of 2D DNN](Workflow1.md)
- [Example workflow2: Membrane segmentation by use of 3D FFN](Workflow2.md) 
- [About copyrights](#About-copyrights)


## Introduction
Recent years have seen a rapid expansion in the field of micro-connectomics, which targets 3D reconstruction of neuronal networks from a stack of 2D electron microscopic (EM). The spatial scale of the 3D reconstruction grows rapidly over 1 mm3, thank to deep neural networks (DNN) that enable automated neuronal segmentation. Advanced research teams have developed their own pipelines for the DNN-based large-scale segmentation (Informatics 2017, 4:3, 29). Those pipelines are typically a series of client-server software for alignment, segmentation, proofreading, etc., each of which requires specific PC configuration. Because of such complexity, it is difficult even for computer experts to use them, and impossible for experimentalists. This makes a serious divide between the advanced and general experimental laboratories.
   To bridge this divide, we are now trying to unify pieces of software for automated EM segmentation.

1.	We built a desktop version of the proofreading software Dojo (IEEE Trans. Vis. Comput. Graph. 20, 2466–2475) on Microsoft Windows 10, 64 bit.
2.	We merged it with a DNN framework: Google Tensorflow/tensorboard. 
3.	We then incorporated two types of DNN-based segmentation programs: 2D U-net/Resnet (https://github.com/tbullmann/imagetranslation-tensorflow) and flood-filling networks (https://github.com/google/ffn).
4.	A 3D annotator was equipped for visual inspection and annotation (based on Three.js).
5.	2D/3D filtration functions were incorporated for the postprocessing of DNN-generated segmentation images (based on skimage and opencv3).

Multiple users can simultaneously use it through web browsers. The goal is to develop a unified software environment for DNN-based segmentation, postprocessing, proofreading, annotation, and visualization of EM images. The VAST Lite is recommended for ground truth generation for DNNs (https://software.rc.fas.harvard.edu/lichtman/vast/ ).

## System requirements
Operating system: Microsoft Windows 10 (64 bit). Linux and macOS versions will be built in future.
Recommendation: High-performance NVIDIA graphics card such as GeForce GTX 1080ti.

## Installation
We provide standalone versions (pyinstaller version) and Python source codes.

### Pyinstaller version 
1.	Download one of the following two versions, and unzip it:
	- CPU version (Ver0.62: 340 MB): https://www.dropbox.com/s/a8aepoikrpsmgob/UNI_EM0.62_Pyinstaller.zip?dl=0
   	- GPU version (Ver0.62: XXX MB): Under construction.

	The GPU version can be used if the PC-equipped NVIDIA GPU has over 3.5 compute capability:

	- https://developer.nvidia.com/cuda-gpus

2.	Download sample EM/segmentation data from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0

3.	Please click the link "main.exe" in Dojo_StandaloneX.XX to launch the control panel.


### Python version 
1. Install Python 3.5 or 3.6 in a Microsoft Windows PC, 64 bit.
2. Install cuda 9.0 and cuDNN v7 for Tensorflow 1.12 (latest combination on 2018/12/20) if your PC has a NVIDIA-GPU.
3. Download the source codes from the github site:
   	- git clone https://github.com/urakubo/Dojo-standalone
4. Install the following modules of Python: Tensorflow-gpu, PyQt5, openCV3, pypng, tornado, pillow, libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl. Check also "requirements.txt". 
5. Copy Dojo_StandaloneX.XX/Marching_cube/marching_cubes.cp3X-win_amd64.pyd and paste it to {$INSTALL_PYTHON}\Lib\site-packages.

	- This marching cube program is obtained from the ilastik: https://github.com/ilastik/marching_cubes

6. Execute "python main.py" in the Dojo_StandaloneX.XX/ folder. The control panel will appear.

7. Download sample EM/segmentation data from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0
	- https://www.dropbox.com/s/6nvu8o6she6rx9v/ISBI_Dojo.zip?dl=0


## How to use
### Dojo proofreader
This is a proofreading software as a part of Rhoana pipeline (Copyright, Lichtman/Pfister lab, Harvard, USA).

	- https://www.rhoana.org/dojo/

1. Select Dojo → Open Dojo Folder from the dropdown menu, and specify the folder of the sample EM/segmentation dojo files. Dojo will be launched as a web application.
2. Please push the "Reload" button first if the Dojo seems to be in trouble. The Dojo can also be seen in the other web browser if users copy and paste the URL [ http://X.X.X.X:8888/dojo/ ] . Users can also use Dojo through the web browsers of other PCs within the same LAN.
3.	The usage of Dojo is described in the original web page [ https://www.rhoana.org/dojo/ ] . For example, users can move the layers by pressing w/s keys, and change the opacity of segmentation by pressing c/d keys.
4.	Users can import pairs of new EM images and segmentation by selecting Dojo → Import EM Stack/Segmentation. Specify the folders containing a stack of EM images and a stack of segmentation images through the dialog (sequentially numbered, gray-scale png/tiff files). 
5.	The edited segmentation images can be exported as sequentially numbered, gray-scale png/tiff files, by selecting Dojo → Export EM Stack / Export. 

<BR>
<p align="center">
  <img src="Images/Dojo.png" alt="Dojo Proofreading software" width="600">
</p>
<BR>

### 3D annotator
Select Annotator → Open in the dropdown menu. The 3D Annotator will be launched.

1.	Check red crosses in the object table of the right side. The checked objects will appear in the left side. Objects in the object table can be re-ordered by size, and users can see visible big objects by clicking the red crosses of large size objects.
2.	The appeared objects can be rotated, panned, zoomed in/out with the mouse, and their names and colors (RGB) can be changed though the object table.
3.	Users can control the background color, bounding box, and light projection through the accordion menu "Appearance".
4.	The edited contents of the object table can be saved by clicking the button under the object table (CSV).

Turn on the toggle switch in the accordion menu 'Marker label' (right side), then click on any appeared objects. Users will see red markers at the clicked surface location. 

1.	The appeared markers are registered in the marker table. Their colors (RGB), names, radiuses, and deletion can be controlled through the marker table.
2.	Users can also define the colors, names, and numbers of next makers through the accordion menu "Marker label" (right side).
3.	The edited contents of the marker table can be saved by clicking the download button under the marker table (CSV).

Click the "Save image" button at the right side. A screenshot of the scene will be saved as "Screenshot.png".

<BR>
<p align="center">
  <img src="Images/Annotator.png" alt="3D Annotator" width="600">
</p>
<BR>

### 2D DNN
We implemented 2D CNN (Resnet/U-net/Highwaynet/Densenet)-based segmentation programs on Tensorflow V1.12. Programmed by Dr. Torsten Bullmann.

	- https://github.com/tbullmann/imagetranslation-tensorflow

#### Requirements. 
1.	one-page ground truth with 512 x 512 xy-pixels.
2.	Six min training period with a NVIDIA-GPU card (in the case of GTX1070).

The VAST Lite is recommended for the ground truth generation (https://software.rc.fas.harvard.edu/lichtman/vast/ ).


#### Procedure:
1.	Select Segmentation → 2D DNN in the pulldown menu. A dialog that has the two tabs appears: training and inference.
2.	Select the training tab and specify parameters:
	- Image Folder:	Folder containing EM images (tiff/png images).
	- Segmentation Folder: Folder containing ground truth segmentation (tiff/png images).
	- Checkpoint:	DNN connectivity will be stored.
	- X loss:	"hinge", "square", "softmax", "approx", "dice", "logistic"
	- Y loss:	"hinge", "square", "softmax", "approx", "dice", "logistic"
	- Model:	"pix2pix", "pix2pix2", "CycleGAN"
	- Generator:	"unet", "resnet", "highwaynet", "densenet"
	- Augmentation:	{fliplr  ,flipud, transpose} 
	- Maximal epochs
	- Display Frequency
	- Save Parameters
	- Load Parameters
3. Execute training. The default parameters target a sample EM image "Dojo_Standalone/data/_2DNN_ground_truth/0049.png" and segmentation image "Dojo_Standalone/data/_2DNN_training_images/49_memb.png".
4. Select Segmentation → Tensorboard to inspect the progression of training. It took 5 min for the training of sample data by use of NVIDIA GeForce GTX 1070.
5. The console window shows the end of training as "saving model".
6. Confirm the connectivity file "model-XXXXX.data-XXXXX-of-XXXXX" (800 MB) in the checkpoint folder. 
9. Select Segmentation → 2D DNN, and set the parameters of the inference tab.
	- Image Folder:	Folder containing EM images (tiff/png images).
   	- Output Segmentation Folder 
	- Checkpoint 
10. Execute inference.
11. Check that the inference results are stored in the Output Segmentation Folder (Dojo_Standalone/data/_2DNN_inference by default).

<BR>
<p align="center">
  <img src="Images/_2DNN.png" alt="2D DNN" width="600">
</p>
<BR>

### 3D FFN
Here, we wrapped an excellent membrane segmentation program that was developed by Dr. Michał Januszewski et al. : flood filling networks (FFN, Nature Methods, vol. 15 (2018), pp. 605-610 ; https://github.com/google/ffn ). The FFN, which is a recurrent 3D convolutional network, directly produce 3D volume segmentation with high precision. 

#### Requirements. 
1.	3D ground truth of 512 x 512 xy-pixels and over 50 Z-slices.
2.	Long training period (-1 weeks) with a high-performance NVIDIA-GPU card (GTX1080ti or higher).

The VAST Lite is recommended for the ground truth generation (https://software.rc.fas.harvard.edu/lichtman/vast/ ).


#### Procedure:
1.	Select Segmentation → 3D FFN in the pulldown menu. A dialog that has the four tabs appears: Preprocessing, Training, Inference, and Postprocessing.
2.	Select the preprocessing tab and specify parameters:
	- Image Folder:	Folder containing EM images (grayscale sequential tiff/png images).
	- Ground Truth Folder: Folder containing ground truth segmentation (grayscale sequential tiff/png images).
	- FFN File Folder: 	Folder storing generated files for training.
	- Save Parameters
	- Load Parameters

	By default, users will see an example EM image volume and their segmentation (kasthuri15) those of which are stored in Dojo-standalone/data/_3DNN_training_images and Dojo-standalone/data/_3DNN_ground_truth, respectively.
3.	Execute the preprocessing. It takes 5 to 60 min depending on the target image volume and machine speed. It produces the three files in the FFN file folder: af.h5, groundtruth.h5, and tf_record_file .
4.	Select the training tab and specify parameters:
	- Max Training Steps: 	The number of training FFN, a key parameter.
	- Sparse Z:	Check it if the target EM-image stack is anisotropic. Internally, 
	- Training Image h5 File:	Generated file
	- Ground truth h5 File:		Generated file.
	- Tensorflow Record File:	Generated file.
	- Tensorflow Model Folder:	Folder storing training results.
5.	Execute the training. It requires over a few days depending on the target image volume, machine speed, and the Max Training Steps. A few million training steps are required for minimal quality inference. Users can execute additive training by specifying the same parameter settings with the increasing number of "Max Training Steps".
6.	Select the inference tab and specify parameters:
	- Target Image Folder:	Folder containing EM images (sequential grayscale tiff/png images).
	- Output Inference Folder: Folder that will store the inference result.
	- Tensorflow Model Files: Specify the trained model files. Please remove their suffix, and just specify the prefix such as "model.ckpt-2000000."
	- Sparse Z:	Check if it was checked it at the training process.
	- Checkpoint interval: Checkpoint interval.
	- FFN File Folder: Folder storing generated files for inference "inference_params.pbtxt."
	- Save Parameters
	- Load Parameters
7.  Execute the inference. It requires 5-60 min depending on the target image volume and machine speed. It produces the inference results "0/0/seg-0_0_0.npz " and " seg-0_0_0.prob " in the Output Inference Folder. It also produces "inference_params.pbtxt" in the FFN file folder.
8.  Select the postprocessing tab and specify parameters:
	- Target Inference File: Specify inferred segmentation file such as seg-0_0_0.npz.
	- Output Inference Folder: Folder storing generated sequential image files.
	- OUtput Filetype: Please select one of them. 16 bit images are recommended.
	- Save Parameters
	- Load Parameters
9.  Execute the postprocessing. It generally requires less than 5 min. It produces the inference result in the Output Inference Folder.
10. Check the quality of segmentation (inference) by use of colored images or Dojo proofreader.


### 2D and 3D filters
We equipped a variety of 2D and 3D image filters. Select Plugins → 2D/3D Filters. Those filters are intended to use a postprocessing of 2D DNN segmentation. I will soon describe how to use them.

## Authors

* **Hidetoshi Urakubo** - *Initial work* - [Webpage](https://researchmap.jp/urakubo/?lang=english)
* **Ryoji Miyamoto** - *Frontend programming* - [Webpage](https://polygonpla.net/)
* **Torsten Bullmann** - *2D convolutional neural networks* - [Webpage](https://www.cb.hs-mittweida.de/en/mitarbeiterinnen-mitarbeiter-in-ihren-fachgruppen/bullmann-torsten.html)

## License

This project is licensed under the GNU General Public License (GPLv3) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
This software relies on many excellent free and copyrighted software packages. We obey policies of those software packages.

	- Flood-filling networks (Apache License 2.0)
	- Imagetranslation-tensorflow (MIT)
	- Tensorflow, Tensorboard (Apache License 2.0)
	- PyQT5 (GPLv3)
	- Rhoana Dojo (MIT)
	- Open CV3 (3-clause BSD License, https://opencv.org/license.html)
	- Scikit image (http://scikit-image.org/docs/dev/license.html)
	- Three.js (MIT)
	- Tabulator (MIT) https://github.com/olifolkerd/tabulator/blob/master/LICENSE
	- Bootstrap (MIT) https://getbootstrap.com/docs/4.0/about/license/

Hidetoshi Urakubo
2019/2/1
