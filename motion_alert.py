import cv2

video = cv2.VideoCapture(0) # Open the webcam

while True:
    check, frame = video.read() # Ask the webcam for the next frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame from colour to grayscale
    blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0) 
    cv2.imshow("Webcam", blurred_frame) # Display the frame in a window

    key = cv2.waitKey(1) # Wait 1 millisecond for a key press

    if key == ord("q"): # If the user presses "q", exit the loop
        break

video.release()