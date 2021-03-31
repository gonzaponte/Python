import cv2
import time
import numpy as np

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

interval  = 100 # milliseconds
threshold = 7e3

rval     = True
previous = None
current  = None

while rval:
    rval, current = vc.read()
    cv2.imshow("preview", current)

    if previous is None: previous = current

    diff = current - previous
    diff = np.sum(diff**2)
    diff = np.sqrt(diff)
    print(diff)
    if diff > threshold:
        raise RuntimeError

    previous = current

    key = cv2.waitKey(interval)
    if key == 27: # exit on ESC
        break


cv2.destroyWindow("preview")
