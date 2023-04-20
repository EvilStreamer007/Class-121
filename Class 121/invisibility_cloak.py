import cv2 
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*"XVID") #fourcc - compresses data
outputfile = cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))
cap = cv2.VideoCapture(0) #opening the camera

time.sleep(2)
bg = 0

for i in range(60):
    ret, bg = cap.read() #reads the background for 60 seconds

bg = np.flip(bg, axis = 1) #flips the background

#reading the captured frame, until the camera is open
while(cap.isOpened()):
    ret, img = cap.read() #ret = returns TRUE if value is true
    if not ret:
        break
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #HSV - Hue Saturation Value

    #generating mask to detect redcolor
    lowerRed = np.array([0, 120, 50]) #the values are the hue saturation value
    upperRed = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lowerRed, upperRed) #the cloth

    lowerRed = np.array([170, 120, 70])
    upperRed = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lowerRed, upperRed) #the background

    mask1 = mask1 + mask2
    cv2.imshow("Mask1", mask1)
    
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) #used to make the image more prominent
    #uint8 contains all binary numbers / unsigned integer
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    #selecting only the path, that does not have mask1, and saving in mask2
    mask2 = cv2.bitwise_not(mask1) #flips the pixel values
    res1 = cv2.bitwise_and(img, img, mask = mask2) #residue 1, source1 and source2 is image
    res2 = cv2.bitwise_and(bg, bg, mask = mask1) #residue 2, source 1 and source2 is background

    #generating the final output by merging res1 and res2
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)

    outputfile.write(finalOutput)
    cv2.imshow("Magic", finalOutput) #output is displayed

    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows() #closes all windows open by CV2
