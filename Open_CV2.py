import cv2

cap = cv2.VideoCapture(0) # Here 0 says that capture the video from default web cam. Basically it's called id.

while True:
    ret , frame = cap.read() #Here ret is a boolean value
    # gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
    # Try the command above the line to convert video into grayscale
    # Suppose image is not captured it will show an error

    if ret == False:
        continue # You continue in that case
    
    cv2.imshow("Video Capture",frame)
    # cv2.imshow("GrayScale Video",gray_scale) - Add this line of code to show the video captured in Gray Scale.


    # Wait for an user input - If user press q than it should stop capturing video

    key_pressed = cv2.waitKey(1) & 0xFF # Conversion of 32 bit to 8 bit
    # Becomes easy to read Ascii number
    
    if key_pressed == ord('q'): # Here ord means ASCII value for character
        break

cap.release()
cv2.destroyAllWindows()
