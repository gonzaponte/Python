import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

rval  = True
frame = None

while rval:
    if frame is not None:
        cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
