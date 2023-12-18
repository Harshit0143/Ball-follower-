# cd myenv\Scripts
# .\Activate
# python ./main.py
import cv2
import numpy as np
import base64

from imutils.video import VideoStream
import imutils
import pyfirmata
import time
import sys


def add_text_detected(frame , center , direction):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    height , width , _ = frame.shape
    

    font_color = (255, 0 , 0)  # BGR color (white in this case)
    font_thickness = 3
    text_size = cv2.getTextSize(direction , font, font_scale, font_thickness)[0]
    text_x = center[0] - text_size[0] // 2
    text_y = center[1] + text_size[1] // 2
    cv2.putText(frame, direction, (text_x, text_y), font, font_scale, font_color, font_thickness)
    
    text_size = cv2.getTextSize("Ball detected" , font, font_scale, font_thickness)[0]
    cv2.putText(frame, "Ball detected", (0, 3 +  text_size[1]), font, font_scale, font_color, font_thickness)
    cv2.imshow('Ball Position', frame)

def add_text_lost(frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    height , width , _ = frame.shape
    

    font_color = (255, 0 , 0)  # BGR color (white in this case)
    font_thickness = 3
    text_size = cv2.getTextSize("Ball lost" , font, font_scale, font_thickness)[0]
    cv2.putText(frame, "Ball lost", (0, 3 +  text_size[1]), font, font_scale, font_color, font_thickness)
    cv2.imshow('Ball Position', frame)




def detect_objects(frame):
    frame = imutils.resize(frame , width = 600)
    blurred = cv2.GaussianBlur(frame , (11 , 11) , 0)
    hsv = cv2.cvtColor(blurred , cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv , GREEN_LOWER, GREEN_UPPER)
    mask = cv2.erode(mask , None , iterations = 2)
    mask = cv2.dilate(mask , None , iterations = 2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
   
    center = None
    height , width , _ = frame.shape
    mid_x  = width // 2 
    
    line_color = (0, 0, 255)  # BGR color (green in this case)
    line_thickness = 2
    direction = None
    cv2.line(frame, (mid_x, 0), (mid_x, height), line_color, line_thickness)

    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        ((x , y) , radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > MIN_RADIUS:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            if  center[0] < mid_x - LATERAL_THRESHOLD:
                direction = 'Left' 
            elif center[0] > mid_x + LATERAL_THRESHOLD:
                direction = 'Right'
            else:
                direction = 'Straight'
            add_text_detected(frame , center , direction)
            
    if direction == None:
        direction = 'Stop'
        add_text_lost(frame)
 

    return direction

class machine:
    def __init__(self , com_port , left0 , left1 , right0 , right1 , stop_led , running_led):
        print("Establishing Bluetooth Connection with Arduino")
        self.board = pyfirmata.Arduino(com_port)
        print("Bluetooth Communication Successfully started")
        self._left0_ , self._left1_ = left0 , left1
        self._right0_ , self._right1_ = right0 , right1
        self._stop_led_ , self._running_led_ = stop_led , running_led

    def _left_wheel_(self , direction):
        # direction: True if front , False if back 
        self.board.digital[self._left0_].write(direction)
        self.board.digital[self._left1_].write(not direction)

    def _right_wheel_(self , direction):
        # direction: True if front , False if back 
        self.board.digital[self._right0_].write(not direction)
        self.board.digital[self._right1_].write(direction)

    def _right_stop_(self):
        self.board.digital[self._right0_].write(False)
        self.board.digital[self._right1_].write(False)
        
    def _left_stop_(self):
        self.board.digital[self._left0_].write(False)
        self.board.digital[self._left1_].write(False)

    def left(self):
        self._left_wheel_(False)
        self._right_wheel_(True)

    def right(self):
        self._left_wheel_(True)
        self._right_wheel_(False)

    def front(self):
        self._left_wheel_(True)
        self._right_wheel_(True)

    def back(self):
        self._left_wheel_(False)
        self._right_wheel_(False)

    def stop(self):
        self._right_stop_()
        self._left_stop_()


    def led_stop_state(self , state):
        self.board.digital[self._stop_led_].write(state)

    def led_running_state(self , state):
        self.board.digital[self._running_led_].write(state)

# now turn till LOWER THreshold and get disturbed only if crosses higher threshold

if __name__ == '__main__':

    ip_address = '192.168.1.6'
    port = 8080
    username = 'harshit'
    password = 'home123'
    url = f'http://{username}:{password}@{ip_address}:{port}/video'
    print("Video feed from: ", url)
    credentials = f'{username}:{password}'
    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    auth_header = f'Basic {base64_credentials}'
    headers = {'Authorization': auth_header}
    cap = cv2.VideoCapture(url)

    ##### Let's ssee later the coloir ranges
    GREEN_LOWER = (29, 86, 6)
    GREEN_UPPER = (64, 255, 255)
    MIN_RADIUS = 10
    LATERAL_THRESHOLD = 100
    TURNING = False
    WAIT_TIME = 2
    car = machine('COM3' , 10 , 11 , 9 , 8 , 13 , 7)
    car.stop()
    car.front()
    time.sleep(5)
    car.stop()
    sys.exit()

    car.led_stop_state(False)
    time.sleep(WAIT_TIME)
    car.led_stop_state(False)
    while(True):
        car.led_running_state(True)
        ret , frame = cap.read()
        if not ret:
            print("No video feed!")
            break
    
        direction = detect_objects(frame)

        if direction == 'Left':
            car.front()
        elif direction == 'Right':
            car.front()
        elif direction == 'Stop':
            car.front()
        else:
            car.front()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    car.stop()
    car.led_running_state(False)
    car.led_stop_state(True)
    time.sleep(WAIT_TIME)
    car.led_stop_state(False)
    cap.release()
    cv2.destroyAllWindows()


