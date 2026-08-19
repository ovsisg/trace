import cv2

video = cv2.VideoCapture(0) # Open the webcam
first_frame = None

while True:
    _, frame = video.read() # Ask the webcam for the next frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame from colour to grayscale
    blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0) 

    if first_frame is None:
        first_frame = blurred_frame

    delta_frame = cv2.absdiff(first_frame, blurred_frame)
    threshold_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=2)
    cv2.imshow("Webcam", dilated_frame)

    contours, _ = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1) # Wait 1 millisecond for a key press

    if key == ord("q"): # If the user presses "q", exit the loop
        break

video.release()