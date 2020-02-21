import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from comm import trimite_serial, detectat_crosswalk, detectat_fuel, detectat_stop, detectat_park
import math
from picamera.array import PiRGBArray
from picamera import PiCamera	

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
cascade_fuel = cv2.CascadeClassifier(fuel)
cascade_stop = cv2.CascadeClassifier(stop)
cascade_crosswalk = cv2.CascadeClassifier(crosswalk)
cascade_park = cv2.CascadeClassifier(park)




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

##this funtions sends the input to pic
def straight():
    trimite_serial(inainte)
def little_left():
	trimite_serial(stanga)
def full_left():
	trimite_serial(sstanga)

def little_right():
	trimite_serial(dreapta)
def full_right():
	trimite_serial(ddreapta)
       
def slow():
	trimite_serial(stop)
##last_time  = time.time()

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
rawCapture = PiRGBArray(camera)
time.sleep(0.01)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    screen =  frame.array
    detectie_semn_crosswalk()
    detectie_semn_stop()
    detectie_semn_crosswalk()
    detectie_semn_fuel()
    new_image = proceesed_img(screen)
    lines = cv2.HoughLinesP(new_image, 1 ,np.pi/180, 100,np.array([]), minLineLength = 50, maxLineGap = 15)
    left_coordinate = []
    right_coordinate = []
      
    if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                slope = (x2-x1)/(y2-y1)
                if slope<0:
                        left_coordinate.append([x1,y1,x2,y2])
                elif slope>0:
                        right_coordinate.append([x1,y1,x2,y2])
            l_avg = np.average(left_coordinate, axis =0)
            r_avg = np.average(right_coordinate, axis =0)
            l =l_avg.tolist()
            r = r_avg.tolist()
            try:
                  #with the finded slope and intercept, this is used to find the value of point x on both left and right line
                  #the center point is denoted by finding center distance between two lines
                  
                c1,d1,c2,d2 = r
                a1,b1, a2,b2 = l
                l_slope = (b2-b1)/(a2-a1)
                r_slope = (d2-d1)/(c2-c1)
                l_intercept = b1 - (l_slope*a1)
                r_intercept = d1 - (r_slope*c1)
                y=360
                l_x = (y - l_intercept)/l_slope
                r_x = (y - r_intercept)/r_slope
                distance = math.sqrt((r_x - l_x)**2+(y-y)**2)
                #line_center repressent the center point on the line
                line_center = distance/2
                  
                center_pt =[(l_x+line_center)]
                f_r = [(l_x+(line_center*0.25))]
                f_l = [(l_x+(line_center*1.75))]
                  #create a center point which is fixed
                center_fixed =[477]
                x_1 = int(l_x)
                x_2 = int(r_x)
                '''The logic behind this code is simple,
                the center_fixed should be in the center_line.
                means the cars is in center of the lane, if its get away from center,
                then the left and right functions are used accordingly,then if
                the center fixed is too far from the center_pt the car takes complete left or right accordingly!'''
                if center_pt==center_fixed:
                    straight()
                    print('forward')
                elif center_pt > center_fixed and center_fixed > f_r:
                    little_right()
                    print('right')
                elif center_pt < center_fixed and center_fixed < f_l:
                    little_left()
                    print('left')
                elif center_fixed < f_r:
                    full_right()
                    print('full_ right')
                elif center_fixed > f_l:
                    full_left()
                    print('full_left')
                else:
                    slow()
                    print('slow')

            except:
                pass
                straight()
                print('FORWARD')


    
    line_image = display_line(screen,lines)
    combo_image = cv2.addWeighted(screen,0.8, line_image,1.2,2)
	#xxxxxxxxxxxxxxxxxxxxx fuel xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    rectangles_fuel = cascade_fuel.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=20,
    			minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_fuel):
    	# Surround cascade with rectangle
    	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.putText(image, CASCADE_ITEM[0] + " #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    		
    		
    #xxxxxxxxxxxxxxxxxx stop xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    rectangles_stop = cascade_stop.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=20,
    			minSize=(75, 75))		
    for (i, (x, y, w, h)) in enumerate(rectangles_stop):
    	# Surround cascade with rectangle
    	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.putText(image, CASCADE_ITEM[1] + " #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    		
    #xxxxxxxxxxxxxxxxxx crosswalk xxxxxxxxxxxxxxxxxxxxxxxx
    
    rectangles_crosswalk = cascade_crosswalk.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=20,
    			minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_crosswalk):
    	# Surround cascade with rectangle
    	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.putText(image, CASCADE_ITEM[2] + " #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    		
    #################### park ###########################
    rectangles_park = cascade_park.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=20,
    			minSize=(75, 75))
    for (i, (x, y, w, h)) in enumerate(rectangles_park):
    	# Surround cascade with rectangle
    	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.putText(image, CASCADE_ITEM[3] + " #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
############################################################################################################################################3
    cv2.imshow('auto',cv2.cvtColor(combo_image, cv2.COLOR_BGR2RGB))
    rawCapture.truncate(0)
      
    if cv2.waitKey(25) & 0xff == ord('q'):
       cv2.destroyAllWindows()
       break
    
#plt.imshow(screen)
#plt.show()
