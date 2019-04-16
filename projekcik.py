import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("!!! Error during opening camera !!!")
else:
    print("!!! Camera has been opened !!!")
    
# HSV color range describtion:
# H stands for color
# S stands for strenth of color
# V stands for lighting of the color

low_boundary_orange=np.array([10,150,255])
high_boundary_orange=np.array([47,255,255])


while (cap.isOpened()):
    #our original frame image
    ret, frame = cap.read()
    
    if ret == True:
         #creating black-white binary image of captured video
        hsv_view = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #checking if there is an object that is located between boundaries of color that we have chosen
        filter = cv2.inRange(hsv_view, low_boundary_orange, high_boundary_orange)
        
         contours, _ = cv2.findContours(filter.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #If the contours where detected then...
        if len(contours) > 0:
            cv2.putText("Contours detected!",[47, 255, 255])
            main_contour = max(contours, key=cv2.contourArea)
            main_contour_area = cv2.contourArea(main_contour)

            # Here You need to prase the FLOAT into INT because funtion takes integers as an argument but gets float instead what will cause an error
            if main_contour_area >= min_valid_area:
                (contour_x, contour_y), contour_radius = cv2.minEnclosingCircle(main_contour)
                cv2.circle(frame, (int(contour_x), int(contour_y)), int(contour_radius / 20), (0, 255, 0), -1)

        #making bitwise AND operation on our rt frame with filter in image variable (mask is some bit operation 8bits array or something)
        res = cv2.bitwise_and(frame,frame,mask=filter)
        #frame = cv2.flip(frame, 1)

        #our frame with rt video
        cv2.imshow("NAI PROJECT:)", frame)
        cv2.imshow("COLOR FILTER", res)
        cv2.imshow("filter", filter)

        
        if cv2.waitKey(25) & 0xFF == ord('x'):
            break
    else:
        break

cap.release()

cv2.destroyAllWindows()
