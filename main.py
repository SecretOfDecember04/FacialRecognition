import cv2
from deepface import DeepFace
import face_recognition
import time
import screeninfo
import signal
import sys
import os

# Handle exit signal to release the camera properly
def signal_handler(sig, frame):
    print("Exiting and releasing camera...")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Get screen resolution
screen = screeninfo.get_monitors()[0]
screen_width, screen_height = screen.width, screen.height

# Initialize the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    sys.exit(1)

# Set camera resolution to match screen resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Initialize variables
counter = 0
face_match = False
reference_img = cv2.imread("your_image.jpeg")  # Placeholder for your image

def check_face(frame):
    global face_match
    # Resize the frame to a smaller size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resize frame to 25% of the original size

    face_locations = face_recognition.face_locations(small_frame)
    for (top, right, bottom, left) in face_locations:
        # Scale the face location back to the original frame size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        color = (0, 255, 0) if face_match else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Add recognition message
        if face_match:
            cv2.putText(frame, "Stay in position for verification...", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    try:
        result = DeepFace.verify(frame, reference_img.copy(), model_name="OpenFace", enforce_detection=False)
        face_match = result['verified']
    except ValueError:
        face_match = False

    return face_locations

# Allow the camera to warm up
time.sleep(2)

# Make the window full screen and allow resizing
cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Start the video loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Resize the frame for display to reduce GUI load
    display_frame = cv2.resize(frame, (int(screen_width * 0.75), int(screen_height * 0.75)))

    if counter % 100 == 0:  # Skip even more frames for better performance
        check_face(frame)

    counter += 1

    # Display the text based on face match result
    color = (0, 255, 0) if face_match else (0, 0, 255)
    message = "Match! Welcome back!" if face_match else "No Match!"
    cv2.putText(display_frame, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

    # Show the video frame
    cv2.imshow("video", display_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close the window
cv2.destroyAllWindows()
cap.release()
