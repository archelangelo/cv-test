import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R

# Read images
img_b = cv2.imread('room.jpg')
wid_b = img_b.shape[1]
hei_b = img_b.shape[0]
img_f = cv2.imread('cat.jpg')
wid_f = img_f.shape[1]
hei_f = img_f.shape[0]
img_mask = np.ones(img_f.shape[:2]) * 255

# x0 y0 move image center to (0,0)
x0 = -wid_f/2.
y0 = -hei_f/2.
x1 = wid_b/2.
y1 = hei_b/2.

def draw_circle(img, tran_m):
    c0 = np.array([[
        [0, 0],
        [wid_f, 0],
        [wid_f, hei_f],
        [0, hei_f],
    ]], dtype=np.float32)
    ct = cv2.perspectiveTransform(c0, tran_m).reshape(-1, 2).astype(np.int)
    radius = 8
    color = (255, 0, 0)
    img = cv2.circle(img, (ct[0, 0], ct[0, 1]), radius, color, -1)
    img = cv2.circle(img, (ct[1, 0], ct[1, 1]), radius, color, -1)
    img = cv2.circle(img, (ct[2, 0], ct[2, 1]), radius, color, -1)
    img = cv2.circle(img, (ct[3, 0], ct[3, 1]), radius, color, -1)
    return img

def image_gen(idx:int):
    # Prepare the transformation matrix
    # Get Euler angles
    ang_z = (np.random.random_sample() - 0.5) * 10.
    ang_y = (np.random.random_sample() - 0.5) * 60.
    ang_x = (np.random.random_sample() - 0.5) * 30.
    rot_m = R.from_euler('zyx', [ang_z, ang_y, ang_x], degrees=True).as_matrix()
    # Move the display in the room (Translation)
    del_x = (np.random.random_sample() - 0.5) * 500.
    del_y = (np.random.random_sample() - 0.5) * 500.
    del_z = np.random.random_sample() * (-1500.) - 3000.
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
    interpo_flag = cv2.INTER_LINEAR
    img_w = cv2.warpPerspective(img_f, tran_m, img_b.shape[1::-1], flags=interpo_flag)
    img_mask_w = cv2.warpPerspective(img_mask, tran_m, img_b.shape[1::-1], flags=interpo_flag)[:, :, np.newaxis]
    print("mask max = {}".format(np.amax(img_mask_w)))
    print("mask min = {}".format(np.amin(img_mask_w)))
    print("img_w datatype is {}".format(img_w.dtype))
    # foreground = cv2.bitwise_and(img_w, img_w, mask=img_mask_w)
    # background = cv2.bitwise_and(img_b, img_b, mask=cv2.bitwise_not(img_mask_w))
    foreground = np.uint8(img_w * (img_mask_w / 255.))
    background = np.uint8(img_b * (1. - img_mask_w / 255.))
    dst = cv2.add(foreground, background)
    # dst = cv2.GaussianBlur(dst, (0, 0), 2)
    dst = draw_circle(dst, tran_m)
    cv2.imshow('Warpped image {}'.format(idx), dst)
    # cv2.imwrite('image_{}.png'.format(idx), dst)
    # cv2.imwrite('foreground_{}.png'.format(idx), foreground)

# Set number of generated images
n_images = 4
for i in range(n_images):
    image_gen(i)

cv2.waitKey(0)
cv2.destroyAllWindows()