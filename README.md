Prerequisites
To run the code, you need access to a webcam and Python installed, preferably a version equal to or higher than 3.8. After that, you need to install the required packages with the following commands:

pip install python-vlc
pip install mediapipe
pip install opencv-python
Note that, due to a possible error caused by using more than one video capture device/webcam, it may be necessary to modify the value of X in "cap = cv2.VideoCapture(X)" at line 70 of HandVideoControl.py and line 17 of virtualpainter.py.

Running the program
The code is quite easy to run; however, I've added some arguments that can be used to meet the user's needs and preferences.

If you're running the code for the first time, it is advisable to run only the code in the most straightforward way after navigating to the folder where the project files are located in the command line:

python HandVideoControl.py

However, if the user prefers to only watch a video without the tutorial, the program should be run as follows:

python HandVideoControl.py -t 0

If you want to choose a video from your computer, the video should be in the project folder, and the command to execute should be:

python HandVideoControl.py -t 0 -v YourVideo.mp4

This will be the command in case the video is in .mp4 format and has the name "YourVideo".

It is also possible to run only the drawing mode algorithm; however, there must be an image named "gt" in .png format already included in the project folder. To do this, simply execute:

python virtualpainter.py
