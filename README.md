Japanese version here
<https://github.com/urakubo/Dojo-standalone/blob/main0.2/README.ja.md>

This software is under development!

# A unified environment for automated neuronal network reconstruction from EM images

## Introduction
Recent years have seen a rapid expansion in the field of micro-connectomics, which targets 3D reconstruction of neuronal networks from a stack of 2D electron microscopic (EM). Thanks to deep neural networks (DNN) that enable automated neuronal segmentation, the spatial scale of the 3D reconstruction grows rapidly over 1 mm3. Advanced research teams have developed their own pipelines for large-scale segmentation (Informatics 2017, 4:3, 29). Those pipelines are series of client-server software for alignment, segmentation, proofreading, etc., each of which requires specific PC environments. Because of such complexity, it is difficult even for computer experts to use them, and impossible for experimentalists. This makes a serious divide between the advanced and general experimental laboratories.
   To bridge this divide, we are now trying to unify pieces of software for automated EM segmentation. 
1.	We built a desktop version of the proofreading software Dojo (IEEE Trans. Vis. Comput. Graph. 20, 2466–2475) with permission of Dr. Daniel Haehn.
2.	We merged it with Tensorflow/tensorboard (DNN framework by google) and 2D/3D DNN-based segmentation programs. 
3.	A 3D viewer was equipped for visual inspection. 

Multiple users can simultanously use it through web browsers. The final goal is to develop unified softwre for alignment, ground-truth preparation, DNN-based segmentation, and proofreading for EM experimentalists.

## System requirements
Operating system: Microsoft Windows 10 (64 bit).

Recommendation: High-performance NVIDIA graphics card such as GeForce GTX 1080ti.

## Installation
We provide standalone versions (pyinstaller version) and Python source codes.

### Pyinstaller version 

1.	Download one of the following two versions, and unzip it:
	- CPU version (Ver0.54: 262 MB): 
   	- <https://www.dropbox.com/s/zy92gi1cfohwn9z/Dojo_Standalone0.54_pyinstaller.zip?dl=0>
   	- GPU version (Ver0.50: 700 MB):
   	- <https://www.dropbox.com/s/9mpdvzpystrb6y1/Dojo_Standalone0.50_gpu_pyinstaller.zip?dl=0>

2.	Download sample EM/segmentation data from the following website, and unzip it:
   	- <https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0>

3.	Please click the link "main.exe" in Dojo_StandaloneX.XX to launch a control panel.


### Python version 
1.	Install Python 3.5 or 3.6 in a Microsoft Windows PC.
2.	Install cuda 9.0 and cuDNN v7 for Tensorflow 1.12 (latest combination on 2018/12/20) if GPU is used.
3.	Download the source code from the github site:
   	- git clone https://github.com/urakubo/Dojo-standalone
4. Install the following modules of Python: Tensorflow-gpu, PyQt5, openCV3, pypng, tornado, pillow, 
libtiff, mahotas, h5py, lxml, numpy, scipy, scikit-image, pypiwin32, numpy-stl. Check also "requirements.txt". 
5. Copy Dojo_StandaloneX.XX/Marching_cube/marching_cubes.cp3X-win_amd64.pyd and paste it to {$INSTALL_PYTHON}\Lib\site-packages.

	- This is the compiled marching cubes from ilastik. https://github.com/ilastik/marching_cubes

6. Execute "python main.py" in the Dojo_StandaloneX.XX/ folder to see a control panel.

7. Download sample EM/segmentation data from the following website, and unzip it:
   	- https://www.dropbox.com/s/pxds28wdckmnpe8/ac3x75.zip?dl=0


## How to use
### Dojo proofreading software
This is a proofreading software as a part of Rhoana pipeline developed by Lichtman/Pfister lab (Harvard, USA).

	- https://www.rhoana.org/dojo/
	
1. Select Dojo -> Open Dojo Folder from a pulldown menu, and specify the folder of the sample EM/segmentation data.
2. Dojo will launch as a web application. Please push the "Reload" button first if Dojo is in trouble. You will also see Dojo if you copy the URL [ http://X.X.X.X:8888/dojo/ ] and past it to the address bar of the other web browser. You can also use Dojo through in the  web browsers in other PCs within the same LAN.
3.	The usage of Dojo is described in the original web page [ https://www.rhoana.org/dojo/ ] . Briefly, you can move between the layers by w/s keys, and change the opacity of segmentation by c/d keys.
4.	You can import new EM images and export their segmentation through the Dojo pulldown menu. 


### 3D viewer
This is a prototype. In the pulldown menu, select Plugins -> 3D Viewer (Big Objects) and specify the number of objects (<10). You will see the 3D objects in a web application.


### 2D DNN
We implemented 2D CNN (Resnet/U-net/Highwaynet/Densenet)-based segmentation programs on Tensorflow V1.12. Programmed by Dr Torsten Bullmann.

	- https://github.com/tbullmann/imagetranslation-tensorflow

1.	In the pulldown menu, select Segmentation -> 2D DNN. You will see a dialog that has the two tabs: training and inference.
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
3. Execute training. The default parameters target a sample EM image "data/segment_ 2DNN_img/49.png" and segmentation image "data/segment_ 2DNN_seg/49.png."
4. Select Segmentation -> Tensorboard to inspect the progression of training. It took 5 min for the training of sample data by use of NVIDIA GeForce GTX 1070.
5. We know the end of training if "saving model" appears.
6. Confirm the connectivity file "model-XXXXX.data-XXXXX-of-XXXXX" (800 MB) in the checkpoint folder. 
9. Select Segmentation -> 2D DNN, and set the parameters of the inference tab.
	- Image Folder:	Folder containing EM images (tiff/png images).
   	- Output Segmentation Folder 
	- Checkpoint 
10. Execute inference.
11. You will soon see the inference results in the Output Segmentation Folder.

Hidetoshi Urakubo
2018/12/20
