# MulticameraHandRecognition
This Python script reads the output from multiple cameras, uses OpenCV to detect a hand, and prints corresponding information to the terminal based on the input received by OpenCV.


Before running the program make sure you have the following packages installed:

python3 (version = 3.11) and then you can run

pip3 install numpy

pip3 install mediapipe

pip3 install tensorflow

Now you can download all the files to your computer including MulticamREcognition.py file. This is where all the work is done.

Hardware note: For this project I used three usb connected cameras (esp32). If you plan to use the same esp32 cameras, please refer to https://github.com/derekja/espcam for proper instructions. If you would like to use something else, you would need to modify the code a little bit, but as long as you know how to access desired cameras, it shouldn't be a problem. You can refer to this repository https://github.com/sofiiak13/OpenCV , if you would like to see an example of how to use OpenCV with a webcam. Also, you should manually change the number of cameras in the code if you are using more or less than three.

In order to run a program you can either use your code editor or terminal/command prompt.

For Code Editor: Double click on MulticamREcognition.py to open it in the code editor of your choice (i.e. VS Studio). Then, run the file without debugging.

For command prompt: Open command prompt and navigate to hand-gesture-recognition-code and from this folder run the folllowing command: python3 MulticamREcognition.py

For this particular program I would recommend the command prompt because we want to see the print statements that appear as the program is running. 

If the script is successfully complied, you should see following messages in the terminal:

Starting Camera 1
Starting Camera 2
Starting Camera 3

This indicates that all the cameras have started working and analyzing the input visible to each of them. One crucial feature of this program is its continuous monitoring of cameras to detect any instances of a hand, followed by displaying the corresponding camera's video feed featuring the detected hand. So, you will not see any video output unless you show a hand to the camera. 

Moreover, this program uses OpenCV library to check which hand (left or right) is currently visible and then prints out this information to the command line. For example, if camera 1 detects a left hand, you will see the video feed from camera 1, as well as message "Left hand on the camera 1" appear in the Terminal. The algorithm checks and prints correct hand information every 2 seconds. If all cameras are able to detect the same hand at the same time, it will print "Same left/right hand on all cameras!".

Note: There is a small inconvenience since OpenCV and TensorFlow librarys also use terminal for the output, messages from our script will be mixed with some other messages printed out by default. So, please ignore tensorflow warnings or information about how fast OpenCV detects cerain gestures!

Lastly, if you would like to exit the prgram you need to stop showing hands to all your cameras, type "exit" in the terminal and hit enter. You should see the cameras are closing one by one and eventually a message "Program is closed". This indicates that the script has stopped running. 

There is still some future work to be done. For instance, I aim to display all my messages in a window separate from the terminal used by TensorFlow. Additionally, implementing a single-key exit instead of typing and hitting enter would enhance user experience. There's always room for improvement, but for now, you can still enjoy this small script I've created!
