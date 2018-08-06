"# Dojo-standalone"

Varieties of software have been launched for managing EM segmentation, but few of them aim for the proofreading of automated segmentation that involves over-segmentation/agglomeration process. Many of them work only on a specific platform on specific database, and others are not open-source.
I here present a open-source, standalone version of such proofreading software - Dojo in part of Rhoana pipeline (Pfister lab/Harvard, 2014). This software provides a 
It has been developed on Python2.7 (Python3.5 in near future) on Windows10. It should also work on Mac and Linux, but I have not tested it.


Requirements: a nunmber of Python modules


What I did:
I made a small gui to control dojo for desktop use.




Currenly unresolved problem:
It neearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop (file: DojoStandalone.py).

Hidetoshi Urakubo
2018/8/6

