import cv2

video = cv2.VideoCapture(0) # Open the webcam

while True:
    check, frame = video.read() # Ask the webcam for the next frame
    cv2.imshow("Webcam", frame) # Display the frame in a window

    key = cv2.waitKey(1) # Wait 1 millisecond for a key press

    if key == ord("q"): # If the user presses "q", exit the loop
        break

video.release()