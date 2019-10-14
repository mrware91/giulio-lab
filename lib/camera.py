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

px0 = 430                   # ROI
px1 = 480
py0 = 200
py1 = 350

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

n = 0
y = [i-i for i in range(0,30)]
avg = [float(i) for i in y]
std = [float(i) for i in y]
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,3,1)
ax2 = fig1.add_subplot(1,3,2)
ax3 = fig1.add_subplot(1,3,3)

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    if frame is None:
        continue
    roi = frame[py0:py1,px0:px1,0]
    # Warn if camera is saturated in the ROI
    if roi.max()==255:
        print(n,": SATURATED PIXEL!")
    roi = roi - roi.min()
    A = np.sum(roi)             # ROI integrated signal

    y = np.roll(y,-1)
    avg = np.roll(avg,-1)
    std = np.roll(std,-1)

    y[-1] = A
    avg[-1] = np.mean(y)            # moving average mean
    std[-1] = np.std(y)/avg[-1] # moving average std

    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax1.imshow(roi,clim = (0,256))
    ax2.plot(y)
    ax3.plot(std)
    plt.draw()
    plt.pause(0.1)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    n = n+1

cv2.destroyWindow("preview")
plt.close()
print("Exposure: ",vc.get(cv2.CAP_PROP_EXPOSURE))
print("Gain: ",vc.get(cv2.CAP_PROP_GAIN))
