

import pyfirmata
import time


## RIGHT0 RIGHT1 LEFT0 LEFT1 

def right_front():
    board.digital[RIGHT0].write(0)
    board.digital[RIGHT1].write(1)


def right_back():
    global RIGHT0 , RIGHT1
    board.digital[RIGHT0].write(1)
    board.digital[RIGHT1].write(0)

def left_front():
    global LEFT0 , LEFT1
    board.digital[LEFT0].write(1)
    board.digital[LEFT1].write(0)

def left_back():
    global LEFT0 , LEFT1
    board.digital[LEFT0].write(0)
    board.digital[LEFT1].write(1)

def right_stop():
    global RIGHT0 , RIGHT1
    board.digital[RIGHT0].write(0)
    board.digital[RIGHT1].write(0)
def left_stop():
    global LEFT0 , LEFT1
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


if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")
    LEFT0 = 10
    LEFT1 =  11
    RIGHT0 = 9
    RIGHT1 = 8       
    left_stop()
    right_stop()
    board.digital[13].write(0)
    time.sleep(2)
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)
    board.digital[13].write(1)


car_front()
import time
time.sleep(5)
car_stop()
    
  


       
