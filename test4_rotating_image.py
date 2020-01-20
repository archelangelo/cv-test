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

# Move the display in the room (Translation)
del_x = (np.random.random_sample() - 0.5) * 500.
del_y = (np.random.random_sample() - 0.5) * 500.
del_z = -10 # (np.random.random_sample() - 1.5) * 10.
# Set the viewbox constants (http://www.songho.ca/opengl/gl_projectionmatrix.html)
t = 100.
r = 100.
n = 90.
f = 2.

ang_z = 0 # (np.random.random_sample() - 0.5) * 10.
ang_y = 0
ang_x = 0 # (np.random.random_sample() - 0.5) * 30.
while (True):
    rot_m = R.from_euler('y', ang_y, True).as_matrix()
    # Perspective transformation matrix
    tran_m = np.array([
        [n/r*rot_m[0,0] - x1*rot_m[2,0], n/r*rot_m[0,1] - x1*rot_m[2,1], n/r*(rot_m[0,0]*x0 + rot_m[0,1]*y0 + del_x) - x1*(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
        [n/t*rot_m[1,0] - y1*rot_m[2,0], n/t*rot_m[1,1] - y1*rot_m[2,1], n/t*(rot_m[1,0]*x0 + rot_m[1,1]*y0 + del_y) - y1*(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
        [-rot_m[2,0], -rot_m[2,1], -(rot_m[2,0]*x0 + rot_m[2,1]*y0 + del_z)],
    ])

    # Warp the forground image
    img_w = cv2.warpPerspective(img_f, tran_m, img_b.shape[1::-1])

    cv2.imshow('Warpped image', img_w)
    print("y angle = {}".format(ang_y))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    ang_y += 0.5
cv2.destroyAllWindows()