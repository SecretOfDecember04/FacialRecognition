import threading
import cv2
from deepface import DeepFace
import face_recognition
import time

# Initialize the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize variables
counter = 0
face_match = False
reference_img = cv2.imread("temp.jpeg")
color = (0, 0, 255)  # Default color is red


def check_face(frame):
    global face_match, color
    face_locations = face_recognition.face_locations(frame)
    for (top, right, bottom, left) in face_locations:
        # Decide the color based on recognition result
        if face_match:
            color = (0, 255, 0)  # Green for match
        else:
            color = (0, 0, 255)  # Red for no match

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Add recognition message
        if face_match:
            cv2.putText(frame, "Stay in position for verification...", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        color, 2)

    try:
        result = DeepFace.verify(frame, reference_img.copy(), model_name="VGG-Face", enforce_detection=True)
        if result['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

    return face_locations


# Allow the camera to warm up
time.sleep(2)

# Make the window full screen
cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Start the video loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Resize frame to half the size

    if counter % 10 == 0:  # Skip more frames for better performance
        face_locations = check_face(small_frame)

    counter += 1

    # Display the text based on face match result
    if face_match:
        cv2.putText(frame, "Match! Welcome back!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
    else:
        cv2.putText(frame, "No Match!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

    # Show the video frame
    cv2.imshow("video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close the window
cv2.destroyAllWindows()
cap.release()
