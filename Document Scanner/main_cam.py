import cv2 as cv
import numpy as np
import mapper

def mouse_click(event, x, y, 
                flags, param):
    global frame, cont_x, cont_y, cont_h, cont_w, approx
    if event == cv.EVENT_LBUTTONDOWN:
        print('left mouse button was clicked')
        cropped = frame[cont_y:cont_y+cont_h, cont_x:cont_x+cont_w]
        # cv.imshow('Video2',cropped)
        pts = np.float32([[0,0], [cont_w,0], [cont_w,cont_h], [0,cont_h]])
        op = cv.getPerspectiveTransform(approx, pts)
        dst = cv.warpPerspective(frame, op, (cont_w,cont_h))
        imgWarpGray = cv.cvtColor(dst,cv.COLOR_BGR2GRAY)
        imgAdaptiveThre= cv.adaptiveThreshold(imgWarpGray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, 10 ) 
        cv.imshow('video3', imgAdaptiveThre)
        cv.imwrite('saved.jpg', imgAdaptiveThre)


img = cv.VideoCapture(0)


while True:
    isTrue, frame = img.read() #Reading each frame
    dupframe = frame.copy() #Making a copy of original frame to use later
    grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #Applying Grayscale
    blurImg = cv.GaussianBlur(grayImg, (5,5), 0) #Applying GaussianBlur
    cannyImg = cv.Canny(blurImg, 0, 50) #Applying Canny

    cnts = cv.findContours(cannyImg, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0] #Finding contours
    cnts = sorted(cnts, key = cv.contourArea, reverse = True) #Sorting contours by area DESC
    for c in cnts:
        # approximate the contour
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
    
        # if our approximated contour has four points, it's a rectangle
        if len(approx) == 4:
            screenCnt = approx
            break
        
    try:
        cont_x,cont_y,cont_w,cont_h = cv.boundingRect(screenCnt) #getting the points
        cv.drawContours(dupframe, [screenCnt], -1, (0, 255, 0), 2) #drawing contour
        approx = mapper.mapp(screenCnt) #Mapp function from mapper.py
    except: pass


    cv.imshow('Video',dupframe)
    cv.setMouseCallback('Video', mouse_click) #Firing the func when mouse-left is clicked
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

img.release()
cv.destroyAllWindows()
