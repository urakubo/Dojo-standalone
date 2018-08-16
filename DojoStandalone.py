#!/usr/bin/env python

#
# DOJO Image Server
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import socket
import sys
import tornado
import tornado.websocket
import tornado.httpserver

import signal
import subprocess
import pickle

if sys.version_info.major == 3:
  import asyncio

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir    = path.join(main_dir, "icons")

sys.path.append(os.path.join(main_dir, "Filesystem"))
from Params import Params
# import SaveChanges

sys.path.append(main_dir)
import _dojo

if os.name == 'nt':
  try:
    import win32api
  except Exception:
    print('No win32api module.')

#def doSaneThing(sig, func=None):
#    print "Here I am"
#    raise KeyboardInterrupt
#win32api.SetConsoleCtrlHandler(doSaneThing, 1)


#
# default handler
#
class DojoHandler(tornado.web.RequestHandler):

  def initialize(self, logic):
    self.__logic = logic

  def get(self, uri):
    self.__logic.handle(self)

  def post(self, uri):
    self.__logic.handle(self)

class ServerLogic:

  def __init__( self ):
    return

 # def __init__( self ):
 #   if os.name == 'posix':
 #     signal.signal(signal.SIGINT, self.close)            ########## Linux
 #   elif os.name == 'nt':
 #     win32api.SetConsoleCtrlHandler(self.close_win, 1)   ########## Windows
 #   else:
 #     print("Unsupported OS")
 #     sys.exit(1)

  def run( self, u_info ):

    # register two data sources
    self.__segmentation = _dojo.Segmentation( u_info.files_path , u_info.tmpdir)
    self.__image = _dojo.Image( u_info.files_path , u_info.tmpdir)

    # and the controller
    self.__controller = _dojo.Controller( u_info, self.__segmentation.get_database() ) ####

    # and the viewer
    self.__viewer = _dojo.Viewer()


    # and the setup
    self.__setup = _dojo.Setup(self, u_info.files_path, u_info.tmpdir)

    path_gfx = os.path.join(main_dir, "./_web/gfx")
    path_stl = os.path.join(main_dir, "./_web/stl")

    ####
    if sys.version_info.major == 3:
      asyncio.set_event_loop(asyncio.new_event_loop())

    dojo = tornado.web.Application([
      (r'/dojo/gfx/(.*)', tornado.web.StaticFileHandler, {'path': path_gfx}),
      (r'/dojo/stl/(.*)', tornado.web.StaticFileHandler, {'path': path_stl}),
      (r'/ws', _dojo.Websockets, dict(controller=self.__controller)),
      (r'/(.*)', DojoHandler, dict(logic=self))
    ],debug = True) #            (r'/dojo/gfx/(.*)', tornado.web.StaticFileHandler, {'path': '/dojo/gfx'})

    

    # dojo.listen(u_info.port, max_buffer_size=1024*1024*150000)
    server = tornado.httpserver.HTTPServer(dojo)
    server.listen(u_info.port)

    print('*'*80)
    print('*', 'DOJO RUNNING')
    print('*')
    print('*', 'open', '[ http://' + u_info.ip + ':' + str(u_info.port) + '/dojo/ ] ')
    print('*'*80)

    tornado.ioloop.IOLoop.instance().start()
    server.stop()

    # def sig_handler(signum, frame):
    #  IOLoop.current().add_callback_from_signal(receiver.shutdown)


    print("Tornado web server stops.")

    return

    ##
    ## IOLoop.instance().stop()
    ## return
    ##

  def stop():
    asyncio.asyncio_loop.stop()
    server.stop()

  def handle( self, r ):

    content = None

    # viewer is ready
    content, content_type = self.__viewer.handle(r.request) ## call viewer

    # let the data sources handle the request
    if not content:
      content, content_type = self.__segmentation.handle(r.request)

    if not content:
      content, content_type = self.__image.handle(r.request)


    # invalid request
    if not content:
      content = 'Error 404'
      content_type = 'text/html'

    print('IP',r.request.remote_ip)

    r.set_header('Access-Control-Allow-Origin', '*')
    r.set_header('Content-Type', content_type)
    r.write(content)


#  def close(self, signal, frame):
#
#    print('Dojo terminating..')
#    output = {}
#    output['origin'] = 'SERVER'
#    # t = SaveChanges(u_info)
#    # t.run()
#    # self.__controller.save(output)
#    sys.exit(0)


#  def close_win(self, empty):

#    print('Dojo terminating..')
#    output = {}
#    output['origin'] = 'SERVER'
#    # self.__controller.save(output)
#    sys.exit(0)

#
# entry point
#

if __name__ == "__main__":


  user_dir = sys.argv[1]
  with open('u_info.pickle', 'rb') as f:
    u_info = pickle.load(f)

  logic = ServerLogic()
  logic.run( u_info )


