Face Recognition System
This project is a real-time face recognition system using OpenCV, DeepFace, and face_recognition libraries in Python. The system captures video from the webcam, detects faces, and verifies them against a set of reference images or a single reference image. The program dynamically displays whether the captured face matches the reference image(s).

Note: The reference image provided in this repository is for demonstration purposes only. You can update the reference images by adding your own pictures to the specified directory or using a dataset of images.

Features
Real-time Face Detection: Captures live video feed from your webcam and detects faces in real-time.
Face Recognition: Verifies detected faces against a reference image or dataset.
Dynamic GUI: Displays a real-time video feed with face bounding boxes and match status.
Full-Screen Mode: The video feed occupies the entire screen for a better viewing experience.
Graceful Exit: Properly handles exit signals and ensures the camera is released and windows are closed when the program is interrupted.
Installation
Prerequisites
Make sure you have Python 3.x installed on your system. You will also need to install the following Python libraries:

pip install opencv-python-headless deepface face_recognition screeninfo

Clone the Repository

git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
Usage
Running the Script
Place Reference Image(s):

Replace the reference image with your own image or use a directory containing multiple reference images. The reference image provided (your_image.jpeg) is just a placeholder and should be replaced for actual use.
Run the Script:

python3 main.py

Exit the Program:

To exit, press the q key while the video feed window is active.
You can also stop the program by pressing Ctrl + C in the terminal, which will gracefully release the camera and close the OpenCV window.
Key Features to Note:
Full-Screen Mode: The video feed window will automatically be set to full-screen mode.
Face Matching: The program will display a green "Match! Welcome back!" message if the detected face matches the reference image(s). If not, it will display a red "No Match!" message.
Code Structure
main.py: The main script that handles face detection and recognition.
your_image.jpeg: A placeholder reference image. Replace this with your own image or use a dataset of images.
Modifications
Using a Dataset of Reference Images:
To use multiple images as references, place your images in a directory and modify the script to load and compare faces against all images in that directory.
python
Copy code
reference_dir = "/path/to/your/reference/images"
reference_images = []
for filename in os.listdir(reference_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(reference_dir, filename)
        reference_images.append(cv2.imread(img_path))
Adjust Frame Processing Interval:
You can adjust the frequency of face recognition by modifying the counter variable in the script.
Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
OpenCV for providing powerful tools for computer vision.
DeepFace for the face recognition capabilities.
face_recognition for the easy-to-use face detection library.
