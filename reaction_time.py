import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import WindowCapture
import win32api, win32con
import time


import pickle
try:
    with open('reaction:buttonpos','rb') as f:
        butList = pickle.load(f)
except:
    butList = []
h,w = 5,5


def mouseclick(events,x,y,flags,params):
    if events == cv.EVENT_RBUTTONDOWN:
        butList.append((x,y))

    if events == cv.EVENT_MBUTTONDOWN:
        for i, but in enumerate(butList):
            x1, y1 = but
            if x1 < x <x1 + w and y1 < y <y1 + h:
                butList.pop(i)

    with open('reaction:buttonpos','wb') as f:
        pickle.dump(butList,f)

def frame_color(but,img):
    frame = img[(but[1]+(h//2)),(but[0]+(w//2))]
    return frame

def click_screen(but):
    win32api.SetCursorPos((but[0],but[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)



#Wont work for browsers


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    try:
        for but in butList:
            cv.rectangle(screenshot,but,(but[0]+w,but[1]+h), (255,0,0),2)
            screenshot = wincap.get_screenshot()
        click = frame_color(butList[0],screenshot)
        if click[0] == 106 and click[1] == 219 and click[2]== 75:
            click_screen(butList[0])
    except:
        print('No point')
    cv.imshow('Vision', screenshot)
    cv.setMouseCallback('Vision', mouseclick)


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')