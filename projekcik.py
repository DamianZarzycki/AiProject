import cv2
import numpy as np

#using 0 because its a webcamp
cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("!!! Error during opening camera !!!")
else:
    print("!!! Camera has been opened !!!")

low_boundary_orange=np.array([10,150,255])
high_boundary_orange=np.array([20,255,255])

#creating empty oints array
array = []

while (cap.isOpened()):
    #our original frame image
    ret, frame = cap.read()

#W SKROCIE JAK DZIAŁA CALA FILTRACJA:
# zamieniamy rbg na hsv, zabieg który ulatwia nam okreslanie zakresu koloru ktorego poszukujemy (tak ja to zrozumialem)
# nastepnie, korzystajac z funkcji inRange() 'wrzucamy' naz obraz do 'pudelka' z granicami koloru pomaranczowego
# kolejnym krokiem jest operacja AND dzieki ktorej wszystko co jest TRUE bedzie miec mozliwosc wyswietlenie w naszym kolorze w naspenych krokach
    #jedynki nachodza na naszej masce (filter) i pokazuja kolor na ekranie


    if ret == True:
        #converting from rbg/bgr to hsv image of captured video
        hsv_view = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(hsv_view, (3, 3), 0)

        #checking if there is an object that is located between boundaries of color that we have chosen so for this project its everything thats orange
        #if its in the range its 1 (white) if not its 0
        filter = cv2.inRange(hsv_view, low_boundary_orange, high_boundary_orange)

        #making bitwise AND operation on our rt frame with filter in image variable (mask is some bit operation 8bits array or something)
        #when its one
        res = cv2.bitwise_and(frame,frame,mask=filter)
        #frame = cv2.flip(frame, 1)

        #getting the contours. Contours function returns 3 values and we only need 1
        contours, _ = cv2.findContours(filter, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 1000:
                #on what, what draw, from where we stsart -1 means everything, color, thickness
                cv2.drawContours(frame, contours, -1 , (0,255,0), 3)




        frame = cv2.flip(frame, 1)
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
