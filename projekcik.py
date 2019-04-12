import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("!!! Error during opening camera !!!")
else:
    print("!!! Camera has been opened !!!")

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow("camera", frame)

    if cv2.waitKey(1000):
        break

    cap.release()
    cv2.destroyAllWindows()
