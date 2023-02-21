import cv2
import numpy as np

# Load the image
img = cv2.imread('car4-thumbnail.jpg')

# Apply mean-shift filtering to the image
shifted = cv2.pyrMeanShiftFiltering(img, 21, 51)

# Convert the shifted image to grayscale
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the grayscale image to create a binary image
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Apply a morphological transformation to the binary image to fill in small holes and gaps
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Find the contours in the binary image
contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a mask from the contours
mask = np.zeros(img.shape[:2], np.uint8)
cv2.drawContours(mask, contours, -1, 255, -1)

# Apply the mask to the original image using bitwise and operation
result = cv2.bitwise_and(img, img, mask=mask)

# Display the resulting image
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
