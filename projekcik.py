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

        #frame = cv2.flip(frame, 1)

        if cv2.waitKey(25) & 0xFF == ord('x'):
            break
    else:
        break

cap.release()

cv2.destroyAllWindows()
