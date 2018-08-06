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

        self.small_ids = np.zeros((db.canvas_size_y/(2 ** iw), db.canvas_size_x/(2 ** iw), self.zmax), dtype=self.u_info.ids_dtype)
        for iz in range(db.num_tiles_z):
            full_map = m.ObtainFullSizeIdsPanel(self.u_info, db, iz)
            self.small_ids[:, :, iz] = full_map[::(2 ** iw), ::(2 ** iw)]
        return
    ###

    ###
    ###
    def Run(self):
    ###
    ###
        print('Export Stl Files.')


        ## Obtain biggest ID
        con = sqlite3.connect(self.u_info.segment_info_db_file)
        cur = con.cursor()
        cur.execute('select id, max(size) from segmentInfo;')
        maxid = cur.fetchone()[0]
        con.commit()
        con.close()

        #maxid = 15
        print('Obtain id: ', maxid)

        mask = (self.small_ids == maxid)

        # print('Mask was made.')
        # print('Mask Size: ', mask.shape)
        # print('Mask Type: ', mask.dtype)
        # print('Mask volume: ', np.sum(mask) )

        # plt.imshow(mask[:, :, 50])
        # plt.show()

        ## Generate mesh

        # volume = np.load( path.join(current_dir, "sample.npy")  )
        # iw = 1
        # volume = volume[::(2 ** iw), ::(2 ** iw), :]
        # print('Volume was loaded.')
        # print('Max Volme: ', np.max(volume))
        # print('Volme Size: ', volume.shape)
        # print('Volme Type: ', volume.dtype)
        # print('Volume volume: ', np.sum(volume))

        # plt.imshow(volume[:, :, 50])
        # plt.show()

        vertices, normals, faces = march(mask, 2)
        faces = np.array(faces)
        vertices = np.array(vertices)

        # app = QApplication([])
        # view = GLViewWidget()
        # mesh = MeshData(vertices / 100, faces)
        # mesh._vertexNormals = normals

        # item = GLMeshItem(meshdata=mesh, color=[1, 0, 0, 1], shader="normalColor")
        # view.addItem(item)
        # view.show()
        # app.exec_()

    ##
    ##
    ##

        print('Mesh was made.')

        # save_hdf5(file, dataset_name, array)

        #print('Faces: ', faces)
        #print('Faces shape: ', faces.shape)
        #print('Vertices: ', vertices)
        #print('Vertices shape: ', vertices.shape)

        our_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                our_mesh.vectors[i][j] = vertices[f[j], :]
        #print('F shape: ', f.shape)
        #print('F shape: ',vertices[0, :])
        ## Export mesh
        our_mesh.save( path.join(pparent_dir,'maxsize_obj.stl') )

        print('Stl was saved.')

    ###
###


