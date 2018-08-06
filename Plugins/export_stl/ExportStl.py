##
## Simple merger
##

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import sqlite3
import itertools
import math
import numpy as np
import h5py
import lxml
import lxml.etree
from itertools import chain, product
from skimage import measure
##
from marching_cubes import march
from stl import mesh
import stl
from os import path, pardir
current_dir = path.abspath(path.dirname(__file__))  # Dir of script
parent_dir  = path.abspath(path.join(current_dir, pardir))  # Parent dir of script
pparent_dir = path.abspath(path.join(parent_dir, pardir))  # Parent dir of script
sys.path.append(path.join(pparent_dir, "Filesystem"))
from DB import DB
from Params import Params
import Miscellaneous as m
#import matplotlib.pyplot as plt
##
import time
#from pyqtgraph.opengl import GLViewWidget, MeshData
#from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem
#from PyQt4.QtGui import QApplication

###
###
class ExportStl:

    ###
    def __init__(self, u_info):

        ## User info
        self.u_info = u_info
        ## Load DB
        db = DB(self.u_info)

        ## Create 3D geometry
        iw = 2
        self.zmax = 128

        cube_size = max([db.canvas_size_y/(2 ** iw), db.canvas_size_x/(2 ** iw), self.zmax])
        self.small_ids = np.zeros([cube_size, cube_size, cube_size], dtype=self.u_info.ids_dtype)
        for iz in range(min(np.array([db.num_tiles_z,self.zmax]))):
            full_map = m.ObtainFullSizeIdsPanel(self.u_info, db, iz)
            small_map  = full_map[::(2 ** iw), ::(2 ** iw)]
            self.small_ids[0:small_map.shape[0], 0:small_map.shape[1], iz] = small_map
        return
    ###
    def GenerateStl(self, id):
        mask = (self.small_ids == id)
        vertices, normals, faces = march(mask, 2)
        print('Generated faces size: ', faces.shape)

        our_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
               our_mesh.vectors[i][j] = vertices[f[j], :]

        return our_mesh
    ###
    ###
    def Run(self):
    ###
    ###
        print('Export Stl Files.')


        ## Obtain biggest ID
        con = sqlite3.connect(self.u_info.segment_info_db_file)
        cur = con.cursor()
        # cur.execute('select id, max(size) from segmentInfo;')
        # maxid = cur.fetchone()[0]
        # con.commit()
        # con.close()
        # print('Id that give maximum: ', maxid)

        cur.execute('select * from segmentInfo order by size desc;')

        ids = []
        for i in range(200):
            id = cur.fetchone()[0]
            print('Stl id{0} was to be saved.'.format(id))
            our_mesh = self.GenerateStl(id)
            our_mesh.save(path.join(pparent_dir, 'i{0}.stl'.format(i)))

        con.commit()
        con.close()
        print('Ids: ', ids)

        #our_mesh = self.GenerateStl(maxid)
        #our_mesh.save( path.join(pparent_dir,'id{0}.stl'.format(maxid) ) )
        #print('Stl id{0} was saved.'.format(maxid) )

        # for id in range(1,800):
        #    our_mesh = self.GenerateStl(id)
        #    our_mesh.save(path.join(pparent_dir, 'id{0}.stl'.format(id)))
        #    print('Stl id{0} was saved.'.format(id))


    ## m.save_hdf5(path.join(pparent_dir, 'vertices.h5'), 'data', vertices)
    ## m.save_hdf5(path.join(pparent_dir, 'faces.h5'), 'data', normals)
    ## m.save_hdf5(path.join(pparent_dir, 'normals.h5'), 'data', faces)

    # our_mesh.vectors[i][2] = vertices[f[0], :]
    # our_mesh.vectors[i][1] = vertices[f[1], :]
    # our_mesh.vectors[i][0] = vertices[f[2], :]

    # Barycenter
    # volume, cog, inertia = our_mesh.get_mass_properties()
    # our_mesh.x -= cog[0]
    # our_mesh.y -= cog[1]
    # our_mesh.z -= cog[2]

    ###
###


