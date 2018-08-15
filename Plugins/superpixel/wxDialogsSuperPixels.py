from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import os, sys
import os.path
import glob     # Wild card

import numpy as np
import PIL
import PIL.Image
from os import path, pardir
import cv2

from skimage.data import astronaut
from skimage.color import gray2rgb
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
import skimage.util

#import matplotlib.pyplot as plt
# sys.path.append('./../../ControlPanel/')
# import DefaultParams


class SuperPixels():
    def __init__(self, *args, **kwds):

        self.xsize = 256
        self.ysize = 256

        #self.input_images_path  = "D:\Kubota180625\Cropped_CLAHE_Cropped"
        #self.output_images_path = "D:\Kubota180625\Cropped_CLAHE_Cropped_ids"
        main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
        Plugins_dir  = path.abspath(path.join(main_dir, "Plugins"))
        superpixel_dir  = path.abspath(path.join(Plugins_dir, "superpixel"))
        self.input_images_path  = superpixel_dir
        search1 = os.path.join(self.input_images_path, '*.tif')
        stack = sorted(glob.glob(search1))
        if stack == []:
            print('No PNG/TIFF images.')
            return

        self.image_files = stack
        self.preview_file = stack[0]

    # ----------------------------------------------------------------------

    def _save_tif16(self, id_data, filename):
        cv2.imwrite(filename, id_data.astype('uint16'))

        """
        Since Pillow has poor support for 16-bit TIFF,
        we make our own save function to properly save a 16-bit TIFF.
        http://blog.itsayellow.com/index.php/2017/09/21/saving-16-bit-tiff-images-with-pillow-in-python/
        """
        # PIL interprets mode 'I;16' as "uint16, little-endian"
        # img_out = Image.new('I;16', size)

        # make sure u16in little-endian, output bytes
        # outpil = u16in.astype(u16in.dtype.newbyteorder("<")).tobytes()
        # img_out.frombytes(outpil)
        # img_out.save(filename)

    # ----------------------------------------------------------------------

    def _Execute_Segmentation(self, wx_spx, img):

        scale_factor = img.shape[0] * img.shape[1] / (self.xsize * self.ysize)

        ID_Algorithm = wx_spx.SelectAlgorithm.GetSelection()
        if ID_Algorithm == 0: # Felzenszwalbs's method
            f_scale   = wx_spx.f_scale.GetValue()
            f_sigma   = wx_spx.f_sigma.GetValue()
            f_minsize = wx_spx.f_minsize.GetValue()
            segments = felzenszwalb(img, scale=f_scale, sigma=f_sigma, min_size=f_minsize)
            print("Felzenszwalb number of segments: {}".format(len(np.unique(segments))))
        elif ID_Algorithm == 1: # SLIC
            s_nseg = wx_spx.s_nseg.GetValue() * scale_factor
            s_comp = wx_spx.s_comp.GetValue()
            s_sigma = wx_spx.s_sigma.GetValue()
            segments = slic(gray2rgb(img), n_segments=s_nseg, compactness=s_comp, sigma=s_sigma)
            print('SLIC number of segments: {}'.format(len(np.unique(segments))))
        elif ID_Algorithm == 2: # Quickshift
            q_ksize   = wx_spx.q_ksize.GetValue()
            q_maxdist = wx_spx.q_maxdist.GetValue()
            q_ratio   = wx_spx.q_ratio.GetValue()
            segments = quickshift(gray2rgb(img), kernel_size=q_ksize, max_dist=q_maxdist, ratio=q_ratio)
            print('Quickshift number of segments: {}'.format(len(np.unique(segments))))
        elif ID_Algorithm == 3: # Compact watershed
            w_nmark   = wx_spx.w_nmark.GetValue() * scale_factor
            w_comp    = wx_spx.w_comp.GetValue()
            gradient = sobel(img)
            segments = watershed(gradient, markers=w_nmark, compactness=w_comp)

        return segments

    # ----------------------------------------------------------------------

    def SP_PrepareInitalPreview(self, wx_spx):

        img = PIL.Image.open(self.preview_file)
        img = img.crop((0, 0, self.xsize, self.ysize))
        img = img.convert("RGB")
        w, h = img.size
        bimg = wx.Bitmap.FromBuffer(w, h, img.tobytes())

        return bimg


    # ----------------------------------------------------------------------

    def SP_UpdatePreview(self, wx_spx, event):

        img = PIL.Image.open(self.preview_file)
        box = (0, 0, self.xsize, self.ysize)
        img = img.crop(box)
        img = skimage.util.img_as_float(img)
        segments = self._Execute_Segmentation(wx_spx, img)
        # print('Shape of segment: ', segments)
        img = mark_boundaries(img, segments, color=(1, 1, 0.5))
        img = (img * 255).astype('uint8')

        image = PIL.Image.fromarray(img)
        bimg = wx.Bitmap.FromBuffer(img.shape[0], img.shape[1], image.tobytes())
        wx_spx.bitmap_1.SetBitmap(bimg)

        # sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer_3.Add(wx_spx.bitmap_1, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 0)
        # sizer_3.Add(wx_spx.panel_5, 0, wx.EXPAND, 0)
        # sizer_2.Add(sizer_3, 1, wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND, 0)

        wx_spx.sizer_3.Layout()  ### Important!
        wx_spx.Refresh()
        wx_spx.Update()


    # ----------------------------------------------------------------------

    def SP_Execute(self, wx_spx, event):

        image_no = len(self.image_files)
        for zi, file in enumerate(self.image_files):
            print('Image No: ', zi+1,'/', image_no)
            img = PIL.Image.open(file)
            img = skimage.util.img_as_float(img)
            segments = self._Execute_Segmentation(wx_spx, img)
            path, fname = os.path.split(file)
            output_fname = os.path.join(self.output_images_path, fname)
            self._save_tif16(segments, output_fname)


    # ----------------------------------------------------------------------

