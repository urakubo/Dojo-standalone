##
##
## http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_segmentations.html
##
##

import matplotlib.pyplot as plt
import numpy as np
import PIL
import PIL.Image

from skimage.data import astronaut
from skimage.color import gray2rgb
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
import skimage.util

# img = img_as_float(astronaut()[::2, ::2])
img = PIL.Image.open('y=00000000,x=00000000.tif')
img = skimage.util.img_as_float( img )

print 'Grayscale Dim: ', img.shape
print 'Color Dim: ', gray2rgb(img).shape

segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
segments_slic = slic(gray2rgb(img), n_segments=250, compactness=10, sigma=1)
segments_quick = quickshift(gray2rgb(img), kernel_size=3, max_dist=6, ratio=0.5)
gradient = sobel(img)
segments_watershed = watershed(gradient, markers=250, compactness=0.001)

print("Felzenszwalb number of segments: {}".format(len(np.unique(segments_fz))))
print('SLIC number of segments: {}'.format(len(np.unique(segments_slic))))
print('Quickshift number of segments: {}'.format(len(np.unique(segments_quick))))

fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

ax[0, 0].imshow(mark_boundaries(img, segments_fz))
ax[0, 0].set_title("Felzenszwalbs's method")
ax[0, 1].imshow(mark_boundaries(img, segments_slic))
ax[0, 1].set_title('SLIC')
ax[1, 0].imshow(mark_boundaries(img, segments_quick))
ax[1, 0].set_title('Quickshift')
ax[1, 1].imshow(mark_boundaries(img, segments_watershed))
ax[1, 1].set_title('Compact watershed')

for a in ax.ravel():
    a.set_axis_off()

plt.tight_layout()
plt.show()
