###
###
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os, time, errno

import h5py
import numpy as np
import copy
#import shutil
import sqlite3
import lxml
import lxml.etree
from itertools import chain, product
from skimage import measure
from distutils.dir_util import copy_tree
import pickle

import time
import csv
##

from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QWidget, QSizePolicy, QInputDialog, \
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QMessageBox, \
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator
from PyQt5.QtCore import Qt, pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(main_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))

from marching_cubes import march
from stl import mesh

from DB import DB
from Params import Params
import Miscellaneous as m
##
import time
#from pyqtgraph.opengl import GLViewWidget, MeshData
#from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem
#from PyQt4.QtGui import QApplication

###
###
class StlViewer:

    ###
    def __init__(self, parent):

        self.parent = parent
        ## User info
        self.u_info = self.parent.u_info
        ## Load DB
        db = DB(self.u_info)

        ## Create 3D geometry

        scale_factor_xy =  2

        self.zmax = db.num_tiles_z
        cube_size = max([db.canvas_size_y/(2 ** scale_factor_xy), db.canvas_size_x/(2 ** scale_factor_xy), self.zmax])
        cube_size = np.ceil(cube_size)
        cube_size = cube_size.astype(np.int32)
        self.small_ids = np.zeros([cube_size, cube_size, cube_size], dtype=self.u_info.ids_dtype)

        for iz in range( db.num_tiles_z ):
            full_map = m.ObtainFullSizeIdsPanel(self.u_info, db, iz)
            small_map  = full_map[::(2 ** scale_factor_xy), ::(2 ** scale_factor_xy)]
            self.small_ids[0:small_map.shape[0], 0:small_map.shape[1], iz] = small_map

        return

    def rangeexpand(self, txt):
        lst = []
        for r in txt.split(','):
            if '-' in r[1:]:
                r0, r1 = r[1:].split('-', 1)
                lst += range(int(r[0] + r0), int(r1) + 1)
            else:
                lst.append(int(r))
        return lst

    ## https: // www.rosettacode.org / wiki / Range_expansion  # Python

    def ObtainIDs(self):

        ## Obtain biggest ID
        con = sqlite3.connect(self.u_info.segment_info_db_file)
        cur = con.cursor()
        cur.execute('select id, max(size) from segmentInfo;')
        maxid = cur.fetchone()[0]
        con.commit()
        con.close()
        print('Id that give maximum: ', maxid)

        # ID number
        text = 'Please Input IDs [1,2,3-5] (Max ID: {})'.format(maxid)
        # id_numbers, okPressed = QInputDialog.getText(self, "Stl Viewer", text, QLineEdit.Normal, "")
        id_numbers, okPressed = QInputDialog.getText(self.parent, "3D Viewer", text)
        if okPressed and id_numbers != '':
            id_numbers = self.rangeexpand(id_numbers)
            id_numbers = list(set(id_numbers))
            id_numbers = [i for i in id_numbers if i <= maxid]
            id_numbers = [i for i in id_numbers if i >= 0]
            id_size = []
            for id in id_numbers:
                mask = (self.small_ids == id)
                id_size.append(np.sum(mask))
            print('IDs: ',id_numbers)
            print('Voxel Num: ',id_size)
            print('ID is removed if Voxel Num < 5.')
            id_numbers = [i for i in id_numbers if 5 <= id_size[id_numbers.index(i)]]
            print('IDs: ', id_numbers)
            return id_numbers
        else:
            return False

    ###
    def GenerateOneStl(self, id):
        mask = (self.small_ids == id)
        vertices, normals, faces = march(mask, 2)
        print('ID: ', id)
        print('Generated Face Number: ', faces.shape)
        our_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
               our_mesh.vectors[i][j] = vertices[f[j], :]
        return our_mesh
    ###
    ###
    def GenerateStls(self, IDs):
    ###

        if getattr(sys, 'frozen', False):
            # print('Run on pyinstaller.')
            tmp_dir = os.path.normpath( os.path.join(main_dir, "../..") )
        else:
            # print('Run on live python.')
            tmp_dir = main_dir



        for id in IDs:
            our_mesh = self.GenerateOneStl(id)
            our_mesh.save(os.path.join(tmp_dir, '_web_stl/stls/i{0}.stl'.format(id) ))

        colormap = []
        hdf5_file = h5py.File(self.u_info.color_map_file, 'r')
        colornum  = len( hdf5_file[self.u_info.hdf_color_name][:, 0].tolist() )
        print(colornum)
        for id in IDs:
            if colornum > id :
                colormap.append( hdf5_file[self.u_info.hdf_color_name][id, :].tolist() )
            else :
                colormap.append( [128, 128, 128] )

        print('Colormap: ', colormap)

        with open(os.path.join(tmp_dir,'_web_stl/stls/stl_ids.csv'), 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # Enter code
            for i, id in enumerate(IDs):
                #print('Color: ', colormap[i])
                #print('Id: ', id)
                id_col = colormap[i]
                id_col.insert(0, id)
                #print(id_col)
                writer.writerow(id_col)


    ###
    ###
    def ObtainIDs2(self):

        #
        e = QLineEdit()
        e.setValidator(QIntValidator())
        e.setMaxLength(2)
        ##
        ##
        ##
        text = 'Input Number of Objects (1-99)'
        bigNUM, okPressed = QInputDialog.getInt(self.parent, "3D Viewer (Big)", text, 1,  1, 99, 1)
        # id_numbers, okPressed = QInputDialog.getText(self.parent, "Stl Viewer (Big)", text)
        if okPressed and bigNUM >= 1:
            # bigNUM = int(bigNUM)
            print('id_numbers: ', bigNUM)

            ## Obtain biggest IDs
            con = sqlite3.connect(self.u_info.segment_info_db_file)
            cur = con.cursor()
            cur.execute('select * from segmentInfo order by size desc;')
            ids = []
            for i in range(bigNUM):
                id = cur.fetchone()[0]
                ids.append(id)
            con.commit()
            con.close()
            print('IDs: ', ids)
            return ids
        else:
            return False



    def Run2(self):
        ###
        ###
        print('Export Stl Files.')

        if getattr(sys, 'frozen', False):
            # print('Run on pyinstaller.')
            tmp_dir = os.path.normpath( os.path.join(main_dir, "../..") )
        else:
            # print('Run on live python.')
            tmp_dir = main_dir


        ## Obtain biggest ID
        con = sqlite3.connect(self.u_info.segment_info_db_file)
        cur = con.cursor()
        cur.execute('select * from segmentInfo order by size desc;')

        ids = []
        for i in range(20):
            id = cur.fetchone()[0]
            print('Stl id{0} was to be saved.'.format(id))
            our_mesh = self.GenerateOneStl(id)
            our_mesh.save(os.path.join(tmp_dir, '_web_stl/stls/i{0}.stl'.format(i) ))

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


