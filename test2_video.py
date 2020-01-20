import numpy as np
import cv2
import time

# cap = cv2.VideoCapture('vtest.avi')
i = 0
start_time = time.time()

while(True):
    i += 1
    if (i % 2 == 0):
        cv2.imshow('frame', np.ones((200, 200), dtype=np.uint8) * 1.)
    else:
        cv2.imshow('frame', np.ones((200, 200), dtype=np.uint8) * 0.8)
    if cv2.waitKey(16) & 0xFF == ord('q'):
        break

end_time = time.time()
avg_time_per_loop = (end_time - start_time) / i * 1000.
print('On average each loop took {}ms'.format(avg_time_per_loop))
print('{} loops elapsed.'.format(i))

cv2.destroyAllWindows()