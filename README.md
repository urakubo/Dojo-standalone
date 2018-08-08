# Dojo standalone

Varieties of software have been developed to manage electron microscopic (EM) images, some of which have provided functions to handle automated EM segmentation in connectomics. However, only few aim for the proofreading of automated EM segmentation that involves agglomeration/futher segmentation, most of which work only on a specific platform on databases, and some is not open-source.


   Here I present a open-source, multi-platform, and standalone version of such proofreading software - Dojo standalone from a part of Rhoana pipeline (Pfister lab/Harvard, 2014; http://www.rhoana.org/dojo/). Dojo has provided functions for proof reading and 3D visualization, and I modified this software for desktop use. Dojo standalone has been built on Python2.7 (Python3.5 in near future), Javascript, and webGL on Windows10. It should also work on Linux and Mac (although I have not tested it). Thus, users can easily modify it for their own use.


## In addition to the original Dojo:


1) A small gui was equipped to control dojo at a desktop pc.
2) Many input/output image file formats are supported. 
3) Some codes were refactored for stability.
4) Plugin section was created. Users can easily insert new Python functions.


## Requirements
A software package for Windows10/64bit is provided (pyinstaller version). If you do not use this, please build a Python2.7/(Python3.5 in near future) anaconda environment on your pc with the following modules:


1) open CV3: conda install -c conda-forge opencv=3.2.0
2) pypng: pip install pypng
3) Pillow: conda install -c anaconda pillow
4) libtiff: conda install libtiff
5) wxpython: conda install -c newville wxpython-phoenix
6) wxpython: pip install -U wxPython
7) marching cubes from ilastik. This is necesssary only for a Plugin function, and compilation is required: https://github.com/ilastik/marching_cubes
8) mahotas: conda install mahotas
9) h5py: conda h5py install

## How to use:

1-x. Download Dojo_pyinstaller.zip on Windows10/64bit from https://1drv.ms/u/s!Ar0M8vZTxk-whyWDozBUZ0dQc9D- (300MB large file). Unzip it, and click main.exe to confirm the launch of a small GUI.

1-y. Download all the files on a PC with Python environment. Execute "python main.py" to confirm the launch of a small GUI.

2-a. Download a Dojo/Mojo-style file.

3-a. File -> Open Dojo folder, and specify the Dojo/Mojo-style file.

2-b. Prepare a stack of 2D EM images (tiff/png sequential files) and segmentation images (tiff/png sequential files).

3-b. File -> Import, and specify the stack of 2D EM images, the segmentation images, and a output mojo folder.

4. The message "please click here" appears if those files are successfully opened/imported. Plese click it, then the web-based dojo will launch for further editing. Users can save/export the editied file through the small GUI (control panel). 

## A part of many unresolved problems:

1) Dojo_pyinstaller.zip ( https://1drv.ms/u/s!Ar0M8vZTxk-whyWDozBUZ0dQc9D- ) is big (300MB). This is because mahotas, h5py, and numpy require MKL module.  

2) Manual operation board (the bottom half of the small GUI) is under development.

3) It nearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop that is required by Python3 (tornado is provided in: DojoStandalone.py, stop signals are sent by TerminateDojo/wxFileIO.py/wxMain and SaveChanges.py/Filesystem). 

4) Dojo accepts any size of 2D stack images, but unnecessary fringe appears if you do not import images with 512*n xy size.  

5) 3D viewer is buggy.

Hidetoshi Urakubo
2018/8/7

