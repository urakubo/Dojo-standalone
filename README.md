"# Dojo-standalone"

Varieties of software have been launched to manage electron microscopic (EM) images, some of which have provided functions to handle automated EM segmentation in connectomics. However, only few aim for the proofreading of automated EM segmentation that involves agglomeration/futher segmentation. Most of them work only on a specific platform on databases, and some is not open-source.


   Here I present a open-source, multi-platform, and standalone version of such proofreading software - Dojo standalone from a part of Rhoana pipeline (Pfister lab/Harvard, 2014; http://www.rhoana.org/dojo/). Dojo has provided functions for proof reading and 3D visualization, and I modified this software for desktop users. It has been built on Python2.7 (Python3.5 in near future), Javascript, and webGL on Windows10. It should also work on Linux and Mac (although I have not tested it). Thus, users can easily modify it for their own use.


In addition to the original Dojo:


1) A small gui was appended to control dojo at a desktop pc.
2) Many input/output file formats have been supported. 
3) Some codes were refactored for stability.


#) A standalone package for Windows10 is provided. If you do not use this, please build Python2.7/(Python3.5 in near future) environment on your pc with the following .


1) open CV3: conda install -c conda-forge opencv=3.2.0
2) pypng: pip install pypng
3) Pillow: conda install -c anaconda pillow
4) libtiff: conda install libtiff
5) wxpython: conda install -c newville wxpython-phoenix
6) wxpython: pip install -U wxPython
7) marching cubes from ilastik. This is necesssary only for a Plugin function, and compilation is required: https://github.com/ilastik/marching_cubes
8) mahotas: conda install mahotas



#) Currenly unresolved problem:

1) Manual operation boards at 

It neearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop that is required by Python3 (file: DojoStandalone.py).
Manual 


Hidetoshi Urakubo
2018/8/7

