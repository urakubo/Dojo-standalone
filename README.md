# Dojo standalone

Varieties of software have been launched to manage electron microscopic (EM) images, some of which have provided functions to handle automated EM segmentation in connectomics. However, only few aim for the proofreading of automated EM segmentation that involves agglomeration/futher segmentation, most of which work only on a specific platform on databases, and some is not open-source.


   Here I present a open-source, multi-platform, and standalone version of such proofreading software - Dojo standalone from a part of Rhoana pipeline (Pfister lab/Harvard, 2014; http://www.rhoana.org/dojo/). Dojo has provided functions for proof reading and 3D visualization, and I modified this software for desktop use. Dojo standalone has been built on Python2.7 (Python3.5 in near future), Javascript, and webGL on Windows10. It should also work on Linux and Mac (although I have not tested it). Thus, users can easily modify it for their own use.


## In addition to the original Dojo:


1) A small gui was appended to control dojo at a desktop pc.
2) Many input/output image file formats are supported. 
3) Some codes were refactored for stability.
4) Plugin section was created. Users can easily insert new Python functions.


## Requirements
A software package for Windows10/64bit is provided (pyinstaller version). If you do not use this, please build a Python2.7/(Python3.5 in near future) environment on your pc with the following modules:


1) open CV3: conda install -c conda-forge opencv=3.2.0
2) pypng: pip install pypng
3) Pillow: conda install -c anaconda pillow
4) libtiff: conda install libtiff
5) wxpython: conda install -c newville wxpython-phoenix
6) wxpython: pip install -U wxPython
7) marching cubes from ilastik. This is necesssary only for a Plugin function, and compilation is required: https://github.com/ilastik/marching_cubes
8) mahotas: conda install mahotas


## How to use:

Please download

Launch the .

Load a stack of 2D EM images (tiff/png sequential files) and by use of .


## A part of many unresolved problems:

1) Manual operation board (the bottom half of the small GUI panel) is under development.

2) It nearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop that is required by Python3 (tornado is provided in: DojoStandalone.py, stop signals are sent by TerminateDojo/wxFileIO.py/wxMain and SaveChanges.py/Filesystem). 

3) Dojo accepts any size of 2D stack images, but unnecessary fringe appears if you do not import images with 512*n xy size.  

4) 3D viewer is buggy.

Hidetoshi Urakubo
2018/8/7

