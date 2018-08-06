import wx
import os
import os.path

import numpy as np
import PIL
import PIL.Image

from skimage.data import astronaut
from skimage.color import gray2rgb
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
import skimage.util

import matplotlib.pyplot as plt
# sys.path.append('./../../ControlPanel/')
# import DefaultParams

xsize = 256
ysize = 256
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def MakeBitmapRGB(self, width, height):
    # Make a bitmap using an array of RGB bytes
    bpp = 3  # bytes per pixel
    bytes = array.array('B', [0] * width * height * bpp)

    for y in xrange(height):
        for x in xrange(width):
            offset = y * width * bpp + x * bpp
            r, g, b = self.GetRGB(x, y, bpp)
            bytes[offset + 0] = r
            bytes[offset + 1] = g
            bytes[offset + 2] = b

    self.rgbBmp = wx.BitmapFromBuffer(width, height, bytes)

def _Execute_Segmentation(self, img):

    scale_factor = img.shape[0] * img.shape[1] / (xsize * ysize)

    ID_Algorithm = self.SelectAlgorithm.GetSelection()
    if ID_Algorithm == 0: # Felzenszwalbs's method
        f_scale   = self.f_scale.GetValue()
        f_sigma   = self.f_sigma.GetValue()
        f_minsize = self.f_minsize.GetValue()
        segments = felzenszwalb(img, scale=f_scale, sigma=f_sigma, min_size=f_minsize)
        print("Felzenszwalb number of segments: {}".format(len(np.unique(segments))))
    elif ID_Algorithm == 1: # SLIC
        s_nseg = self.s_nseg.GetValue() * scale_factor
        s_comp = self.s_comp.GetValue()
        s_sigma = self.s_sigma.GetValue()
        segments = slic(gray2rgb(img), n_segments=s_nseg, compactness=s_comp, sigma=s_sigma)
        print('SLIC number of segments: {}'.format(len(np.unique(segments))))
    elif ID_Algorithm == 2: # Quickshift
        q_ksize   = self.q_ksize.GetValue()
        q_maxdist = self.q_maxdist.GetValue()
        q_ratio   = self.q_ratio.GetValue()
        segments = quickshift(gray2rgb(img), kernel_size=q_ksize, max_dist=q_maxdist, ratio=q_ratio)
        print('Quickshift number of segments: {}'.format(len(np.unique(segments))))
    elif ID_Algorithm == 3: # Compact watershed
        w_nmark   = self.w_nmark.GetValue() * scale_factor
        w_comp    = self.w_comp.GetValue()
        gradient = sobel(img)
        segments = watershed(gradient, markers=w_nmark, compactness=w_comp)

    return segments

def SP_PrepareInitalPreview(self):

    img = PIL.Image.open('y=00000000,x=00000000.tif')
    img = img.crop((0, 0, xsize, ysize))
    img = img.convert("RGB")
    w, h = img.size
    bimg = wx.Bitmap.FromBuffer(w, h, img.tobytes())

    return bimg

def SP_UpdatePreview(self, event):

    img = PIL.Image.open('y=00000000,x=00000000.tif')
    box = (0, 0, xsize, ysize)
    img = img.crop(box)
    img = skimage.util.img_as_float(img)
    segments = _Execute_Segmentation(self, img)
    img = mark_boundaries(img, segments, color=(1, 1, 0.5))
    img = (img * 255).astype('uint8')

    #print 'Max: ', np.max(img)
    #print 'Min: ', np.min(img)
    #print 'Segmant.shape: ', img.shape
    #print 'Segmant.shape: ', img.dtype



    #img = wx.ImageFromBuffer(img.shape[0], img.shape[1], img)
    #img = img.Scale(xsize, ysize, wx.IMAGE_QUALITY_HIGH)
    #bimg = img.ConvertToBitmap()
    # bimg = MakeBitmap2(img[:,:,0], img[:,:,1], img[:,:,2], 128)
    # bimg = wx.BitmapFromBuffer(img.shape[0], img.shape[1], img)
    # bimg = wx.BitmapFromBufferRGBA(img.shape[0], img.shape[1], img)

    image = PIL.Image.fromarray(img)
    bimg = wx.Bitmap.FromBuffer(img.shape[0], img.shape[1], image.tobytes())
    self.bitmap_1.SetBitmap(bimg)
    self.Refresh()
    self.Update()
