import cv2
import numpy as np

print(cv2.__version__)
# 3.3.0

#img = np.full((210, 425, 1), 128, dtype=np.uint32) Error!
#img = np.full((300, 500, 1), 128, dtype=np.uint16)
img = np.full((400, 300, 1), 128, dtype=np.uint8)
# img = np.full((210, 425, 1), 128, dtype=np.bool)

# pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = np.array([[1,5],[20,30],[10,20],[20,10]], np.int64) * 10
# pts = pts.reshape((-1,1,2))

for i in range(1,5):
	img = cv2.polylines(img, [np.array([[50,i*50], [250,i*50]])], False, 255, i*5, 4, 1) #


for i in range(1,5):
	img = cv2.polylines(img, [np.array([[50,i*50], [250,i*50]])], False, 128, 1,4) #


cv2.imwrite('opencv_draw_argument.png', img)

