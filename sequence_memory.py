import cv2 as cv
import os
from time import time
from window_capture import WindowCapture
import win32api, win32con
import time



import pickle
try:
    with open('memorybuttonpos','rb') as f:
        butList = pickle.load(f)
except:
    butList = []
h,w = 20,20

sequence = []
Level = 1


# if button change color add it in list
#pushing button will start pushing buttons


def mouseclick(events ,x ,y ,flags,params):
    if events == cv.EVENT_RBUTTONDOWN:
        butList.append((x,y))

    if events == cv.EVENT_MBUTTONDOWN:
        for i, but in enumerate(butList):
            x1, y1 = but
            if x1 < x <x1 + w and y1 < y <y1 + h:
                butList.pop(i)

    with open('memorybuttonpos','wb') as f:
        pickle.dump(butList,f)


def frame_color(but,img):
    x1, y1 = but
    frame = img[(y1+10),(x1+10)]
    if int(frame[0]) == 255:
        if len(sequence) == 0:
            sequence.append(but)
        elif sequence[-1] == but or len(sequence) == Level:
            print('double')
        else:
            sequence.append(but)


def click_screen(but):
    win32api.SetCursorPos((but[0],but[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def click_sequence(sequence,ox,oy):
    for but in sequence:
        x1, y1 = but
        win32api.SetCursorPos((x1+ox,y1+oy))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.1)



os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    try:
        for but in butList:
            cv.rectangle(screenshot,but,(but[0]+w,but[1]+h), (255,0,0),2)
            frame_color(but,screenshot)
            screenshot = wincap.get_screenshot()
            cv.imshow('Vision', screenshot)

    except:
        print('No locations of buttons')
    print(sequence)
    print(Level)

    cv.imshow('Vision', screenshot)
    cv.setMouseCallback('Vision', mouseclick)
    if Level == len(sequence):
        time.sleep(0.1)
        click_sequence(sequence, wincap.offset_x, wincap.offset_y)
        for i in range(len(sequence)):
            sequence.pop()
        Level += 1
        time.sleep(0.5)


    if cv.waitKey(1) == ord('r'):
        sequence = []
        Level = 1

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')