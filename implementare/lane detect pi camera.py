import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from comm import trimite_serial, detectat_crosswalk, detectat_fuel, detectat_stop, detectat_park
import math
from picamera.array import PiRGBArray
from picamera import PiCamera   
CASCADE_ITEM = "semn" 
inainte=b'f'
stanga=b'l'
dreapta=b'r'
sstanga=b'L'
ddreapta=b'R'
stop=b's'
#constante folosite la prelucrare
mask_scale_factor = 0.01
mask_width_factor = 0.5

                                            #SEMNE#
#############################################################################################################
cascade_fuel = cv2.CascadeClassifier("fuel.xml")
cascade_stop = cv2.CascadeClassifier("stop.xml")
cascade_crosswalk = cv2.CascadeClassifier("crosswalk.xml")
cascade_park = cv2.CascadeClassifier("park.xml")



#select the region of interest for the detected edges
def roi(image, polygons):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked

#display the lines on the screen
def display_line(image, line):
    line_image = np.zeros_like(image)
    if lines is not None:
            for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(line_image,(x1,y1),(x2,y2),(10,100,255),12)
                    #cv2.line(line_image,(x_1,y),(x_2,y),(0,255,0),3)
                    #cv2.line(line_image,(int(l_x+line_center),y+25),(int(l_x+line_center),y-25),(100,25,50),5)
                    cv2.circle(line_image, (477,360),5,[150,10,25],10)
    return line_image

#processing image for detecting edge using canny edge detection and blur the image using gaussian blur
def proceesed_img(original_image):
            imshape = original_image.shape
            img_width = original_image.shape[1]
            img_height = original_image.shape[0]
            mask_y = int(img_height*mask_scale_factor)
            mask_x = int(img_width*mask_width_factor)       
            proceesed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            proceesed_img = cv2.GaussianBlur(proceesed_img,(5,5), 0)
            proceesed_img = cv2.Canny(proceesed_img, threshold1 =200, threshold2 = 120 )
            #these polygon repressent the data point within with the pixel data are selected for lane detection
            polygons = np.array([[(0,img_height),(mask_x, mask_y-800), (mask_x, mask_y-800), (img_width,img_height)]])
            proceesed_img = roi(proceesed_img, [polygons])
            return proceesed_img


def detectie_semn_fuel():
    if rectangles_fuel is not None:
        time.sleep(0.01)
        print('Detected fuel')
        trimite_serial(detectat_fuel)
    
def detectie_semn_crosswalk():
    if rectangles_crosswalk is not None:
        time.sleep(0.01)
        print('detected crosswalk')
        trimite_serial('detectat_crosswalk')
        CASCADE_ITEM
def detectie_semn_stop():
    if rectangles_stop is not None:
        time.sleep(0.01)
        print('detected stop')
        trimite_serial('detectat_stop')
        
def detectie_semn_park():
    if rectangles_park is not None:
        time.sleep(0.01)
        print('detectat park')
        trimite_serial('detectat_park')     

camera = PiCamera()
camera.resolution = (800, 608)
camera.rotation = 180
rawCapture = PiRGBArray(camera)
time.sleep(0.01)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    screen =  frame.array
    #detectie_semn_crosswalk()
    #detectie_semn_stop()
    #detectie_semn_crosswalk()
    #detectie_semn_fuel()
    #xxxxxxxxxxxxxxxxxxxxx fuel xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    rectangles_fuel = cascade_fuel.detectMultiScale(screen, scaleFactor=1.3, minNeighbors=20,
                minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_fuel):
        # Surround cascade with rectangle
        cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if rectangles_fuel is not None:
            print('Fuel Detected')
        #cv2.putText(screen, CASCADE_ITEM[0] + " #{}".format(i + 1), (x, y - 10),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            
            
    #xxxxxxxxxxxxxxxxxx stop xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    rectangles_stop = cascade_stop.detectMultiScale(screen, scaleFactor=1.3, minNeighbors=20,
                minSize=(75, 75))       
    for (i, (x, y, w, h)) in enumerate(rectangles_stop):
        # Surround cascade with rectangle
        cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if rectangles_stop is not None:
            print('Stop Detected')
        #cv2.putText(screen, CASCADE_ITEM[1] + " #{}".format(i + 1), (x, y - 10),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            
    #xxxxxxxxxxxxxxxxxx crosswalk xxxxxxxxxxxxxxxxxxxxxxxx
    
    rectangles_crosswalk = cascade_crosswalk.detectMultiScale(screen, scaleFactor=1.3, minNeighbors=20,
                minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_crosswalk):
        # Surround cascade with rectangle
        cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if rectangles_crosswalk is not None:
            print('Crosswalk Detected')
        #cv2.putText(screen, CASCADE_ITEM[2] + " #{}".format(i + 1), (x, y - 10),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            
    #################### park ###########################
    rectangles_park = cascade_park.detectMultiScale(screen, scaleFactor=1.3, minNeighbors=20,
                minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_park):
        # Surround cascade with rectangle
        cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if rectangles_park is not None:
            print('Park Detected')
        #cv2.putText(screen, CASCADE_ITEM[3] + " #{}".format(i + 1), (x, y - 10),
        #   cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
############################################################################################################################################3
    cv2.imshow('auto',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    rawCapture.truncate(0)
      
    if cv2.waitKey(25) & 0xff == ord('q'):
       cv2.destroyAllWindows()
       break
    
#plt.imshow(screen)
#plt.show()
