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


def right_front():
    board.digital[RIGHT0].write(0)
    board.digital[RIGHT1].write(1)


def right_back():
    global RIGHT0 , RIGHT1
    board.digital[RIGHT0].write(1)
    board.digital[RIGHT1].write(0)

def left_front():
    board.digital[LEFT0].write(1)
    board.digital[LEFT1].write(0)

def left_back():
    board.digital[LEFT0].write(0)
    board.digital[LEFT1].write(1)

def right_stop():
    board.digital[RIGHT0].write(0)
    board.digital[RIGHT1].write(0)
def left_stop():
    board.digital[LEFT0].write(0)
    board.digital[LEFT1].write(0)

def car_left():
    left_back()
    right_front()

def car_right():
    right_back()
    left_front()

def car_front():
    left_front()
    right_front()

def car_back():
    left_back()
    right_back()

def car_stop():
    right_stop()
    left_stop()


def led_stop_state(state):
    board.digital[STOP_LED].write(state)

def led_running_state(state):
    board.digital[RUNNING_LED].write(state)

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
    print("Establishing Bluetooth Connection with Arduino")
    board = pyfirmata.Arduino('COM3')
    print("Bluetooth Communication Successfully started")
    TURNING = False
    LEFT0 = 10
    LEFT1 =  11
    RIGHT0 = 9
    RIGHT1 = 8  
    STOP_LED = 13
    RUNNING_LED = 7
    WAIT_TIME = 2
    left_stop()
    right_stop()
    led_stop_state(True)
    time.sleep(WAIT_TIME)
    led_stop_state(False)
    while(True):
        led_running_state(True)
        ret , frame = cap.read()
        if not ret:
            print("No video feed!")
            break
    
        direction = detect_objects(frame)

        if direction == 'Left':
            car_left()
        elif direction == 'Right':
            car_right()
        elif direction == 'Stop':
            car_stop()
        else:
            car_front()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    left_stop()
    right_stop()
    led_running_state(False)
    led_stop_state(True)
    time.sleep(WAIT_TIME)
    led_stop_state(False)
    cap.release()
    cv2.destroyAllWindows()


