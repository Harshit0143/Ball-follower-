

import pyfirmata
import time


## 5 6 9 10 

def right_front():
    board.digital[5].write(0)
    board.digital[6].write(1)


def right_back():
    board.digital[5].write(1)
    board.digital[6].write(0)

def left_front():
    board.digital[9].write(1)
    board.digital[10].write(0)

def left_back():
    board.digital[9].write(0)
    board.digital[10].write(1)

def right_stop():
    board.digital[5].write(0)
    board.digital[6].write(0)
def left_stop():
    board.digital[9].write(0)
    board.digital[10].write(0)

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
    right_stop()
    left_stop()
    while True:
        board.digital[13].write(1)
        car_front()
    board.digital[13].write(0)
    left_stop()
    right_stop()
    
  


       
