import cv2

cascade_fuel = cv2.CascadeClassifier("fuel.xml")
cascade_stop = cv2.CascadeClassifier("stop.xml")
cascade_crosswalk = cv2.CascadeClassifier("crosswalk.xml")
cascade_park = cv2.CascadeClassifier("park.xml")

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



