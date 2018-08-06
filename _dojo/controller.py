from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import h5py
import os, errno
import json
import tifffile as tif
import numpy as np
import mahotas as mh
import math
import shutil
from scipy import ndimage
from skimage import exposure
import tempfile ####  <=================== HU: 180626

import itertools
from itertools import product
import sys
from os import path, pardir
current_dir = path.abspath(path.dirname(__file__))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
sys.path.append(path.join(parent_dir, "Filesystem"))
from DB import DB
from Params import Params
import Miscellaneous as m

class Controller(object):


  def __init__(self, u_info, database):
    '''
    mojo_dir, out_dir, tmp_dir are
    u_info.files_path , u_info.files_path, u_info.tmpdir,
    '''
    self.__websocket = None

    self.__lock_table = {'0':True}

    self.__problem_table = []

    self.__users = []

    # self.__merge_table = u_info.merge_table

    self.u_info = u_info

    self.u_info.merge_table = {}

    self.__mojo_dir = u_info.files_path

    self.__mojo_tmp_dir = u_info.tmpdir

    self.__mojo_out_dir = u_info.files_path
    
    self.__database = database

    ##
    self.__db     = DB(u_info)
    self.__u_info = u_info

    if self.__database:
      self.__largest_id = self.__database.get_largest_id()
    else:
      self.__largest_id = 0

    self.__split_count = 0

    ## HU 180626 ##################
    dir = tempfile.gettempdir()
    self.__tmp_seg2_tif       = dir + os.sep + 'seg2.tif'
    self.__tmp_end_points_tif = dir + os.sep + 'end_points.tif'
    self.__tmp_seeds_mask_tif = dir + os.sep + 'seeds_mask.tif'
    self.__tmp_seeds_tif      = dir + os.sep + 'seeds.tif'
    self.__tmp_ws_tif         = dir + os.sep + 'ws.tif'
    self.__tmp_lines_tif      = dir + os.sep + 'lines.tif'
    self.__tmp_dojobox_tif    = dir + os.sep + 'dojobox.tif'
    ##############################

  def handshake(self, websocket):
    '''
    '''
    self.__websocket = websocket

    self.send_welcome()

    # always send the merge table first thing
    self.send_merge_table('SERVER')
    # then the lock table
    self.send_lock_table('SERVER')
    # then the problem table
    self.send_problem_table('SERVER')

    # then send the redraw command
    self.send_redraw('SERVER')


  def send_welcome(self):
    '''
    '''
    output = {}
    output['name'] = 'WELCOME'
    output['origin'] = 'SERVER'
    output['value'] = ''

    self.__websocket.send(json.dumps(output))


  def send_redraw(self, origin):
    '''
    '''
    output = {}
    output['name'] = 'REDRAW'
    output['origin'] = 'SERVER'
    output['value'] = ''

    self.__websocket.send(json.dumps(output))

  def get_merge_table(self):
    '''
    '''
    return self.u_info.merge_table

  def get_lock_table(self):
    '''
    '''
    return self.__lock_table

  def get_problem_table(self):
    '''
    '''
    return self.__problem_table

  def send_merge_table(self, origin):
    '''
    '''
    output = {}
    output['name'] = 'MERGETABLE'
    output['origin'] = origin
    output['value'] = self.get_merge_table()

    self.__websocket.send(json.dumps(output))

  def send_lock_table(self, origin):
    '''
    '''

    output = {}
    output['name'] = 'LOCKTABLE'
    output['origin'] = origin
    output['value'] = self.get_lock_table()

    self.__websocket.send(json.dumps(output))

  def send_problem_table(self, origin):
    '''
    '''

    output = {}
    output['name'] = 'PROBLEMTABLE'
    output['origin'] = origin
    output['value'] = self.get_problem_table()

    self.__websocket.send(json.dumps(output))


  def on_message(self, message):
    '''
    '''
    
    input = json.loads(message)

    if input['name'] == 'WELCOME':

      self.__users.append(input['origin'])

    elif input['name'] == 'MERGETABLE':
      self.u_info.merge_table = input['value']

      self.send_merge_table(input['origin'])

      self.send_redraw(input['origin'])

    elif input['name'] == 'LOCKTABLE':
      self.__lock_table = input['value']

      self.send_lock_table(input['origin'])

      self.send_redraw(input['origin'])

    elif input['name'] == 'PROBLEMTABLE':
      self.__problem_table = input['value']

      self.send_problem_table(input['origin'])

    elif input['name'] == 'LOG':
      # just echo it
      input['id'] = self.__users.index(input['origin'])
      self.__websocket.send(json.dumps(input))

    elif input['name'] == 'MOUSEMOVE':
      # just echo it
      input['id'] = self.__users.index(input['origin'])
      self.__websocket.send(json.dumps(input))

    elif input['name'] == 'SPLIT':
      self.split(input)
      #print()

    elif input['name'] == 'FINALIZESPLIT':
      self.finalize_split(input)
      #print()

    elif input['name'] == 'ADJUST':
      self.adjust(input)
      #print()

    elif input['name'] == 'SAVE':
      self.save(input)


  def adjust(self, input):

    values = input['value']

    print('adjust')

    #######################
    tile = m.ObtainFullSizeIdsPanel(self.__u_info, self.__db, values["z"])
    #######################

    # 
    label_id = values['id']
    i_js = values['i_js']
    brush_size = values['brush_size']

    for c in i_js:

      x = int(c[0])# - brush_size/2)
      y = int(c[1])# - brush_size/2)

      for i in range(brush_size):
        for j in range(brush_size):

          tile[y+j,x+i] = label_id


    full_coords = np.where(tile == label_id)
    full_bbox = [min(full_coords[1]), min(full_coords[0]), max(full_coords[1]), max(full_coords[0])]


    #######################
    m.SaveFullSizeIdsPanel(self.__u_info, self.__db, values["z"], tile)
    #######################

    output = {}
    output['name'] = 'RELOAD'
    output['origin'] = input['origin']
    output['value'] = {'z':values["z"], 'full_bbox':str(full_bbox)}
    # print output
    self.__websocket.send(json.dumps(output))

    output = {}
    output['name'] = 'ADJUSTDONE'
    output['origin'] = input['origin']
    output['value'] = {'z':values["z"], 'full_bbox':str(full_bbox)}
    self.__websocket.send(json.dumps(output))    



  def finalize_split(self, input):
    '''
    '''
    values = input['value']

    #######################
    tile = m.ObtainFullSizeIdsPanel(self.__u_info, self.__db, values["z"])
    #######################


    # 
    label_id = values['id']
    i_js = values['line']
    bbox = values['bbox']
    click = values['click']

    # run through tile
    # lookup each label
    # for i in range(tile.shape[0]):
    #   for j in range(tile.shape[1]):
    #     tile[i,j] = self.lookup_label(tile[i,j])

    s_tile = np.zeros(tile.shape)

    for l in self.lookup_merge_label(label_id):

      s_tile[tile == int(l)] = 1
      tile[tile == int(l)] = label_id

    #mh.imsave('/tmp/seg.tif', s_tile.astype(np.uint8))


    for c in i_js:
      s_tile[c[1], c[0]] = 0

    label_image,n = mh.label(s_tile)

    if (n!=3):
      print('ERROR',n)

    # check which label was selected
    selected_label = label_image[click[1], click[0]]

    print('selected', selected_label)

    for c in i_js:
      label_image[c[1], c[0]] = selected_label # the line belongs to the selected label

    mh.imsave( self.__tmp_seg2_tif, 10 * label_image.astype(np.uint8))  ################# HU 180626

    # update the segmentation data

    self.__largest_id += 1
    new_id = self.__largest_id

    # unselected_label = selected_label==1 ? unselected_label=2 : unselected_label:1

    if selected_label == 1:
      unselected_label = 2
    else:
      unselected_label = 1

    full_coords = np.where(label_image > 0)
    full_bbox = [min(full_coords[1]), min(full_coords[0]), max(full_coords[1]), max(full_coords[0])]

    label_image[label_image == selected_label] = 0 # should be zero then
    label_image[label_image == unselected_label] = new_id - self.lookup_label(label_id)

    tile = np.add(tile, label_image).astype(np.uint32)

    #######################
    m.SaveFullSizeIdsPanel(self.__u_info, self.__db, values["z"], tile)
    #######################


    output = {}
    output['name'] = 'RELOAD'
    output['origin'] = input['origin']
    output['value'] = {'z':values["z"], 'full_bbox':str(full_bbox)}
    # print output
    self.__websocket.send(json.dumps(output))

    output = {}
    output['name'] = 'SPLITDONE'
    output['origin'] = input['origin']
    output['value'] = {'z':values["z"], 'full_bbox':str(full_bbox)}
    self.__websocket.send(json.dumps(output))    

    self.__split_count += 1




  def split(self, input):
    '''
    TODO: move to separate class
    '''

    ### Image and Segmentation tile
    values = input['value']
    tile = m.ObtainFullSizeImagesPanel(self.__u_info, self.__db, values["z"])
    segtile = m.ObtainFullSizeIdsPanel(self.__u_info, self.__db, values["z"])
    ###############################

    label_id = values['id']


    #
    # crop according to bounding box
    #
    bbox = values['brush_bbox']

    sub_tile = tile[bbox[2]:bbox[3],bbox[0]:bbox[1]]
    seg_sub_tile = segtile[bbox[2]:bbox[3],bbox[0]:bbox[1]]

    mh.imsave(self.__tmp_dojobox_tif, sub_tile);

    sub_tile = mh.gaussian_filter(sub_tile, 1).astype(np.uint8) # gaussian filter
    sub_tile = (255 * exposure.equalize_hist(sub_tile)).astype(np.uint8) # enhance contrast

    brush_mask = np.zeros((1024,1024),dtype=bool)
    brush_size = values['brush_size']

    i_js = values['i_js']

    #
    # Generate dense brush
    #
    dense_brush = []
    for i in range(len(i_js)-1):       
      # two sparse points
      p0 = i_js[i]
      p1 = i_js[i+1]

      # x and y coordinates of sparse points
      xp = [p0[1], p1[1]] if p0[1] < p1[1] else [p1[1], p0[1]]
      yp = [p0[0], p1[0]] if p0[1] < p1[1] else [p1[0], p0[0]]
      
      # linear interpolation between p0 and p1
      xs = [x for x in range(xp[0], xp[1]+1)]
      ys = np.round(np.interp(xs, xp, yp)).astype(np.int32)
          
      # add linear interpolation to brush stroke
      dense_brush += zip(ys,xs)
      
      # make x axis dense
      
      # x and y coordinates of sparse points
      xp = [p0[1], p1[1]] if p0[0] < p1[0] else [p1[1], p0[1]]
      yp = [p0[0], p1[0]] if p0[0] < p1[0] else [p1[0], p0[0]]
      
      # linear interpolation between p0 and p1
      ys = [y for y in range(yp[0], yp[1]+1)]
      xs = np.round(np.interp(ys, yp, xp)).astype(np.int32)
          
      # add linear interpolation to brush stroke
      dense_brush += zip(ys,xs)

      # dense_brush = list(set(dense_brush))

    # add dense brush stroke to mask image
    brush_mask = np.zeros((1024,1024),dtype=bool)

#    for c in i_js:
    for c in dense_brush:
        brush_mask[c[1],c[0]] = True
        
    # crop
    brush_mask = brush_mask[bbox[2]:bbox[3],bbox[0]:bbox[1]]
    brush_mask = mh.morph.dilate(brush_mask, np.ones((2*brush_size, 2*brush_size)))

    brush_image = np.copy(sub_tile)
    brush_image[~brush_mask] = 0


    # compute frame
    frame = np.zeros(brush_mask.shape,dtype=bool)
    frame[0,:] = True
    frame[:,0] = True
    frame[-1,:] = True
    frame[:,-1] = True

    # dilate non-brush segments
    outside_brush_mask = np.copy(~brush_mask)
    outside_brush_mask = mh.morph.dilate(outside_brush_mask, np.ones((brush_size, brush_size)))

    # compute end points of line
    end_points = np.zeros(brush_mask.shape,dtype=bool)

    first_point = i_js[0]
    last_point = i_js[-1]

    first_point_x = min(first_point[0] - bbox[0],brush_mask.shape[1]-1)
    first_point_y = min(first_point[1] - bbox[2], brush_mask.shape[0]-1)
    last_point_x = min(last_point[0] - bbox[0], brush_mask.shape[1]-1)
    last_point_y = min(last_point[1] - bbox[2], brush_mask.shape[0]-1)

    end_points[first_point_y, first_point_x] = True
    end_points[last_point_y, last_point_x] = True
    end_points = mh.morph.dilate(end_points, np.ones((2*brush_size, 2*brush_size)))


    # compute seeds
    seed_mask = np.zeros(brush_mask.shape,dtype=bool)
    # seed_mask[outside_brush_mask & brush_mask] = True 
    seed_mask[outside_brush_mask] = True 
    seed_mask[frame] = True
    # seed_mask[corners] = False
    seed_mask[end_points] = False



    # seeds,n = mh.label(brush_boundary_mask)
    seeds,n = mh.label(seed_mask)

    print(n)

    # remove small regions
    sizes = mh.labeled.labeled_size(seeds)
    min_seed_size = 5
    too_small = np.where(sizes < min_seed_size)
    seeds = mh.labeled.remove_regions(seeds, too_small).astype(np.uint8)


    #
    # run watershed
    #
    ws = mh.cwatershed(brush_image.max() - brush_image, seeds)

    mh.imsave(self.__tmp_end_points_tif, 50*end_points.astype(np.uint8))   ###########################################
    mh.imsave(self.__tmp_seeds_mask_tif, 50*seed_mask.astype(np.uint8))
    mh.imsave(self.__tmp_seeds_tif, 50*seeds.astype(np.uint8))
    mh.imsave(self.__tmp_ws_tif, 50*ws.astype(np.uint8))

    lines_array = np.zeros(ws.shape,dtype=np.uint8)
    lines = []

    print(label_id)

    # valid_labels = [label_id]

    # while label_id in self.__merge_table.values():
    #   label_id = self.__merge_table.values()[]
    #   valid_labels.append(label_id)

    for y in range(ws.shape[0]-1):
      for x in range(ws.shape[1]-1):

        if ws[y,x] != ws[y,x+1] and self.lookup_label(seg_sub_tile[y,x]) == label_id:  
          lines_array[y,x] = 1
          lines.append([bbox[0]+x,bbox[2]+y])
        if ws[y,x] != ws[y+1,x] and self.lookup_label(seg_sub_tile[y,x]) == label_id:
          lines_array[y,x] = 1
          lines.append([bbox[0]+x,bbox[2]+y])

    for y in range(1,ws.shape[0]):
      for x in range(1,ws.shape[1]):
        if ws[y,x] != ws[y,x-1] and self.lookup_label(seg_sub_tile[y,x]) == label_id:  
          lines_array[y,x] = 1
          lines.append([bbox[0]+x,bbox[2]+y])
        if ws[y,x] != ws[y-1,x] and self.lookup_label(seg_sub_tile[y,x]) == label_id:
          lines_array[y,x] = 1
          #lines_array[y-1,x] = 1
          lines.append([bbox[0]+x,bbox[2]+y])          
                
    mh.imsave(self.__tmp_lines_tif, 50*lines_array.astype(np.uint8))  ###############################

    output = {}
    output['name'] = 'SPLITRESULT'
    output['origin'] = input['origin']
    output['value'] = lines
    # print output
    self.__websocket.send(json.dumps(output))

  def lookup_label(self, label_id):
    '''
    '''
    # print self.__merge_table, label_id
    # print self.__merge_table.keys()
    while str(label_id) in self.u_info.merge_table.keys():
      # print 'label id', label_id
      # print 'merge[label id]', self.u_info.merge_table[str(label_id)]
      label_id = self.u_info.merge_table[str(label_id)]

    # print 'new label', label_id

    return label_id

  def lookup_merge_label(self,label_id):
    '''
    '''

    labels = [str(label_id)]

    for (k,v) in self.u_info.merge_table.items():

      if v == int(label_id):
        labels = labels + self.lookup_merge_label(k)

    return labels



