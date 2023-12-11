
# import necessary packages
import cv2
import numpy as np
import mediapipe as mp
import urllib.request
import tensorflow as tf
import threading
import time

HANDS = []
LENGTH = 3              # change the length to the number of cameras you are going to use
PROGRAM_RUNNING = True

class camThread(threading.Thread):
    def __init__(self, previewName, camURL, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camURL = camURL
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camURL, self.camID)



def camPreview(previewName, camURL, camID):

    output = False

    while PROGRAM_RUNNING:
        # initialize mediapipe
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = tf.keras.models.load_model('mp_hand_gesture')

        # Load class names
        f = open('gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()
        #print(classNames)

        img_resp=urllib.request.urlopen(camURL)
        # use numpy to turn the image into an array of values
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        # use openCV to turn the array of values into an openCV image
        frame = cv2.imdecode(imgnp,-1)

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)
        className = ''
        global HANDS
        # post process the result
        # this loop checks if any hand is detected, which hand it is and what gesture it shows
        if result.multi_hand_landmarks:
            landmarks = []
            #update value inside HANDS accordingly to what hand is detected 
            for hand in result.multi_handedness:
                leftOrRight = hand.classification[0].label 
                HANDS[camID-1] = leftOrRight

            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
               
                classID = np.argmax(prediction)
                className = classNames[classID]
        else:                 #if no hand is detected
            HANDS[camID-1] = ''

        #now if there is no hand detected we check if the cam output is true, then we close the window
        if HANDS[camID-1] == '':
            if output:
                cv2.destroyWindow(previewName)
                output = False
        else:                                   #if there is any hand detected we want to show the output
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.imshow(previewName, frame) 
            output = True

        
       
        key = cv2.waitKey(1)
        
    cv2.destroyAllWindows()
    HANDS[camID-1] = 'closed'
    print(previewName, " is closed")



# initialize array with hands that will tell us the number of camera and the hand that it is detecting right now

def hand_on_camera():
    global HANDS
    for camera in range(LENGTH):
        #print(camera)
        HANDS.append('')        #initialize HANDS with empty strings because camera hasn't detected any hands yet

hand_on_camera()

# Create two threads as follows
url1 = 'http://10.0.1.42/cam-hi.jpg'
thread1 = camThread("Camera 1", url1, 1)

url2 = 'http://10.0.1.50/cam-hi.jpg'
thread2 = camThread("Camera 2", url2, 2)

url3 = 'http://10.0.1.51/cam-hi.jpg'
thread3 = camThread("Camera 3", url3, 3)

thread1.start()
thread2.start()
thread3.start()

#create a function that prints out current information about the hand(s) detected
def print_hand_info():
    closed = 0
    while closed < LENGTH:
        time.sleep(2)                           #check hand result every 2 seconds
        same = True

        #iterale through each camera and either print inforamtion for each camera or one statement if hands are the same on all cameras
        for camera_num in range(LENGTH):        
            if HANDS[camera_num] != '' and HANDS[camera_num] != 'closed':
                first = HANDS[0]
                for hand in HANDS:
                    if hand != first:
                        same = False
                        break

                if not same:
                    print(HANDS[camera_num], " hand on the camera ", (camera_num + 1))
                else:
                    print("Same ", first, " hand on all cameras!")
                    break
                
            if HANDS[camera_num] == 'closed':
                closed += 1 
    print("Program is closed")

x = threading.Thread(target = print_hand_info)
x.start() 


def exit():
    global PROGRAM_RUNNING
    while PROGRAM_RUNNING:
        usr_input = input()  
        if usr_input == "exit":
            PROGRAM_RUNNING = False
        else:
            print("TYPE 'exit' AND HIT ENTER IF YOU WOULD LIKE TO EXIT THE PROGRAM") 
    
exit()

