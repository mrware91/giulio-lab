# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FPS, 60.)
vc.set(cv2.CAP_PROP_EXPOSURE, -3)
vc.set(cv2.CAP_PROP_GAIN,2710)
vc.set(cv2.CAP_PROP_SETTINGS,1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

n = 0
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    if frame is None:
        continue
    if n==0:
        print(frame.shape)
        sumy = np.sum(frame , (0,2))
    else:
        sumy += np.sum(frame , (0,2))
    print(sumy.shape)
    n+=1

    # print(sumy)

    ax1.clear()
    ax1.plot( sumy/float(n) )
    plt.draw()
    plt.pause(0.1)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
plt.close()
print("Exposure: ",vc.get(cv2.CAP_PROP_EXPOSURE))
print("Gain: ",vc.get(cv2.CAP_PROP_GAIN))
