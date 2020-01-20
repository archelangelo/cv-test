import numpy as np
import cv2

img = cv2.imread('lenna.png', 0)
cv2.imshow('Lenna', img)
cv2.waitKey(0)
cv2.imshow('black', np.zeros(1, dtype=np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()