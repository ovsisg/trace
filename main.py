import cv2
from motion_alert import send_email

# Open the webcam
video = cv2.VideoCapture(0) 
first_frame = None
status_list = []

while True:
    # Assume there is no movement in the current frame
    status = False

    # Ask the webcam for the next frame
    _, frame = video.read() 

    # Convert the frame from colour to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # Blur the frame to reduce small changes and noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0) 

    # Use the first frame as the reference for detecting movement
    if first_frame is None:
        first_frame = blurred_frame

    # Calculate the difference between the first frame and current frame 
    delta_frame = cv2.absdiff(first_frame, blurred_frame)

    # Convert the differences into a black-and-white image
    threshold_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]  

    # Expand the white areas to make detected movement easier to identify
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=2) 
    cv2.imshow("Webcam", dilated_frame)

    # Find the outlines of areas where movement was detected 
    contours, _ = cv2.findContours(
        dilated_frame, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Ignore small areas that are unlikely to be meaningful movement
        if cv2.contourArea(contour) < 5000:
            continue

        # Get the position and size of the detected area
        x, y, w, h = cv2.boundingRect(contour) 

        # Draw a rectangle around the detected movement
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Movement was detected
        status = True

    # Store the current motion status
    status_list.append(status)

    # Keep only the two most recent statuses
    status_list = status_list[-2:]

    # Send an email when movement changes from detected to not detected
    if status_list[0] and not status_list[1]:
        send_email()

    print(status_list)

    cv2.imshow("Video", frame)

    # Wait 1 millisecond for a key press
    key = cv2.waitKey(1) 

    # If the user presses "q", exit the loop
    if key == ord("q"): 
        break

video.release()