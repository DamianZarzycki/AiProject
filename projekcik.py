import cv2
import numpy as np
import os

# using 0 because its a webcamp
cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("!!! Error during opening camera !!!")
else:
    print("!!! Camera has been opened !!!")

# HSV color range describtion:
# H stands for color
# S stands for strenth of color
# V stands for lighting of the color
low_boundary_green = np.array([30, 80, 80])
high_boundary_green = np.array([80, 255, 255])

# storing location of object
array = []
# max lenght of our line thats chasing the object
maxLineLenght = 25

command = "C:\Program Files\Mozilla Firefox\firefox.exe"

while (cap.isOpened()):

    ret, frame = cap.read()

    if ret==True:
        #W SKROCIE JAK DZIAŁA CALA FILTRACJA:
        # zamieniamy rbg na hsv, zabieg który ulatwia nam okreslanie zakresu koloru ktorego poszukujemy (tak ja to zrozumialem)
        # nastepnie, korzystajac z funkcji inRange() 'wrzucamy' naz obraz do 'pudelka' z granicami koloru pomaranczowego
        # kolejnym krokiem jest operacja AND dzieki ktorej wszystko co jest TRUE bedzie miec mozliwosc wyswietlenie w naszym kolorze w naspenych krokach
        #jedynki nachodza na naszej masce (filter) i pokazuja kolor na ekranie
        hsv_view = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # checking if there is an object that is located between boundaries of color that we have chosen so for this project its everything thats orange
        # if its in the range its 1 (white) if not its 0
        filter = cv2.inRange(hsv_view, low_boundary_green, high_boundary_green)
        # making bitwise AND operation on our rt frame with filter in image variable (mask is some bit operation 8bits array or something)
        # when its one
        res = cv2.bitwise_and(frame, frame, mask=filter)
        # it will clean noises on screen
        blurred = cv2.GaussianBlur(hsv_view, (3, 3), 0)
        # getting the contours of our object
        contours, _ = cv2.findContours(filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # its a var thats describe the biggest object of color that we have chosen
            largest = max(contours, key=cv2.contourArea)
            # getting info about min circle that we can draw around our object
            (x, y), radius = cv2.minEnclosingCircle(largest)

            if radius>5:
                # on what, what draw, from where we start -1 means everything, color, thickness
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                # drawing small circle on object
                cv2.circle(frame, (int(x), int(y)), int(radius / 12),(0, 255, 0), -1)

                # storing coords of object
                array.append((int(x), int(y)))
                for i in range(1, len(array)):
                    cv2.line(frame, array[i - 1], array[i], (0, 255, 0), 3)
                    if len(array)>10:
                        # checking difference of Yaxis
                        if (array[i][1]-array[0][1]) > 50:
                            # checking difference of Xaxis
                         if (array[i][0]-array[0][0]) > 30:
                             # writing letter L on screen if detected
                            cv2.putText(frame,'Litera L',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 3, cv2.LINE_AA)
                            os.popen(command)
                           #print(len(array))

        # when our line will get too long remove 1 element so it will be changing dynamically
        if len(array) > maxLineLenght:
            array.pop(0)

       # frame = cv2.flip(frame, 1)
        cv2.imshow("NAI PROJECT:)", frame)
        #cv2.imshow("COLOR FILTER", res)
        # cv2.imshow("filter", filter)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
