import cv2
import numpy as np

frameWidthh = 640
frameHeight = 480

cap = cv2.VideoCapture(1)
cap.set(3,frameWidthh)
cap.set(4,frameHeight)
cap.set(10,100)

# red, blue , yellow
myColors = [[41,53,62,179,255,255],
            [17,198,50,179,237,255],
            [15,106,60,142,255,255]]

# BGR
myColorValues = [[0,0,255],
                 [153,0,0],
                 [0,255,255]]

points = []  # x, y, color_ID

def find_colors(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    new_point = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(color[0]),mask)
        x,y = getContour(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x != 0 and y!=0:
            new_point.append([x,y,count])
        count += 1
    return new_point



def getContour(img):
    contours, heirarchy = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area >200:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def draw(points,myColorValues):
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success , img = cap.read()
    imgResult = img.copy()
    new_points = find_colors(img,myColors,myColorValues)
    if len(new_points) != 0:
        for newP in new_points:
            points.append(newP)
    if len(points) != 0:
        draw(points, myColorValues)
    cv2.imshow("result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
