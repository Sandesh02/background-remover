
# importing libraries
import cv2
import numpy as np


img = cv2.imread('bird.jpg')

# Createing a mask using numpy
mask = np.zeros(img.shape[:2], np.uint8)

# Define  (ROI)
rect = (50, 50, img.shape[1]-100, img.shape[0]-100)

# fit data into GrabCut algorithm
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

# Createing a binary mask from the results taken from GrabCut algorithm
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

# Applying the mask to the image
result = img*mask2[:,:,np.newaxis]

# Display the resulting image
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
