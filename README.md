"# Dojo-standalone"

Varieties of software have been launched to manage electron microscopic (EM) images, some of which have provided functions for connectomics researchers to handle automated EM segmentation. However, only few aim for the proofreading of automated EM segmentation that involves agglomeration/futher segmentation, and most of them work only on a specific platform on databases, and some are not open-source.


   Here I present a open-source, multi-platform, and standalone version of such proofreading software - Dojo standalone from a part of Rhoana pipeline (Pfister lab/Harvard, 2014; http://www.rhoana.org/dojo/). Dojo has provided functions for proof reading and 3D visualization, and this software was modified for desktop users. It has been develped on Python2.7 (Python3.5 in near future), Windows10. It should also work on Linux and Mac (although I have not tested it).


In addition to the original Dojo:

A small gui was appended to control dojo at a desktop pc.

Many input/output file formats have been supported. 

Some codes were refactored for stability.

Requirements:
Python modules
open

Currenly unresolved problem:
  It neearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop that is required by Python3 (file: DojoStandalone.py).
Manual 


Hidetoshi Urakubo
2018/8/7

