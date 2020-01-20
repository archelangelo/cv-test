import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R

# Read images
img_b = cv2.imread('airplane.jpg')
wid_b = img_b.shape[1]
hei_b = img_b.shape[0]
img_f = cv2.imread('cat.jpg')
wid_f = img_f.shape[1]
hei_f = img_f.shape[0]

# x0 y0 move image center to (0,0)
x0 = -wid_f/2.
y0 = -hei_f/2.
x1 = wid_b/2.
y1 = hei_b/2.

# Prepare the transformation matrix
# Get Euler angles
ang_z = 0 # (np.random.random_sample() - 0.5) * 10.
ang_y = 30 # (np.random.random_sample() - 0.5) * 1.
ang_x = 0 # (np.random.random_sample() - 0.5) * 30.
rot_m = R.from_euler('y', ang_y, degrees=True).as_matrix()
# Move the display in the room (Translation)
del_x = (np.random.random_sample() - 0.5) * 500.
del_y = (np.random.random_sample() - 0.5) * 500.
del_z = -3000 # (np.random.random_sample() - 1.5) * 10.
# Set the viewbox constants (http://www.songho.ca/opengl/gl_projectionmatrix.html)
t = 10.
r = 10.
n = 8000.
f = 1500000.
# Perspective transformation matrix
tran_m = np.array([
    [n/r*rot_m[0,0] - x1*rot_m[2,0], n/r*rot_m[0,1] - x1*rot_m[2,1], n/r*(rot_m[0,0]*x0 + rot_m[0,1]*y0 + del_x) - x1*(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
    [n/t*rot_m[1,0] - y1*rot_m[2,0], n/t*rot_m[1,1] - y1*rot_m[2,1], n/t*(rot_m[1,0]*x0 + rot_m[1,1]*y0 + del_y) - y1*(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
    [-rot_m[2,0], -rot_m[2,1], -(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
])
# proj_m = np.array([
#     [n/r, 0, 0, 0],
#     [0, n/t, 0, 0],
#     [0, 0, -(f+n)/(f-n), -2*f*n/(f-n)],
#     [0, 0, -1, 0],
# ])
# # proj_m = np.eye(4)
# rect_v0 = np.array([
#     [0, 0, wid_f, wid_f],
#     [0, hei_f, hei_f, 0],
#     [0, 0, 0, 0],
# ])
# print(rect_v0)
# rect_v1 = rect_v0 + np.array([[x0],[y0],[0.]])
# print(rect_v1)
# rect_v2 = np.matmul(rot_m, rect_v1) + np.array([[del_x],[del_y],[del_z]])
# print(rect_v2)
# rect_v3 = np.matmul(proj_m, np.concatenate((rect_v2, np.ones((1, 4)))))
# print(rect_v3)
# rect_v3[0:3, :] = rect_v3[0:3, :] / rect_v3[3, :]
# rect_v3 = rect_v3[0:3, :] + np.array([[x1],[y1],[0.]])
# print(rect_v3)
# tran_m = cv2.getPerspectiveTransform(np.float32(rect_v0[:2, :].T), np.float32(rect_v3[:2, :].T))

# print(tran_m)

# Warp the forground image
img_w = cv2.warpPerspective(img_f, tran_m, img_b.shape[1::-1])

print(img_w.shape)

cv2.imshow('Warpped image', img_w)
cv2.waitKey(0)
cv2.destroyAllWindows()