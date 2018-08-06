"# Dojo-standalone"

Varieties of software have been launched to manage electron microscopic(EM) images, some of which have provided functions for connectomics researchers to manually edit automated EM segmentation. However, only few aim for the proofreading of automated EM segmentation that involves agglomeration/futher segmentation, and most of them work only on a specific platform on databases, and some are not open-source.
   I here present a open-source, multi-platform, and standalone version of such proofreading software - Dojo standalone from a part of Rhoana pipeline (Pfister lab/Harvard, 2014; http://www.rhoana.org/dojo/). Dojo provides functions for proof reading and 3D visualization, and I modified the Dojo for desktop use. Users can easily examine automated segmentation results. It has been develped on Python2.7 (Python3.5 in near future), Windows10. It should also work on Linux and Mac (although I have not tested it).


What I did on the original Dojo tool:
I made a small gui to control dojo for desktop use.
I append many 
I appended some control 

Requirements:
Python modules


Currenly unresolved problem:
  It neearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop that is required by Python3 (file: DojoStandalone.py).
Manual 


Hidetoshi Urakubo
2018/8/7

