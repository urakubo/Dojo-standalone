"# Dojo-standalone"

Varities of software for EM segmentation have been launched, but few of them aim for proofreading that involves oversegmentation/agglomeration. 
This is a standalone version of Dojo in part of Rhoana pipeline (Pfister lab/Harvard). It works on Python2.7 (Python3.5) on Windows. It should also work on Mac and Linux, but I have not tested it.


Requirements: a nunmber of Python modules


What I did:
I made a small gui to control dojo for desktop use.




Currenly unresolved problem:
It neearly works on Python3.5. But I do not understand how to stop tornado.web.Application under asyncio.set_event_loop (file: DojoStandalone.py).

Hidetoshi Urakubo
2018/8/6

