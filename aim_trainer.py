import cv2 as cv
import os
from time import time
from window_capture import WindowCapture
import win32api, win32con
import time

tries = 50




# if button change color add it in list
#pushing button will start pushing buttons

def click_screen(but):
    win32api.SetCursorPos((but[0],but[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


def find_target(img, target,ox, oy):
    height, width, kakka = target.shape
    result = cv.matchTemplate(img, target, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    cv.rectangle(img,max_loc,((max_loc[0] + width),(max_loc[1] + height)),255, 5)
    mid =[(max_loc[0] + width//2 + ox),(max_loc[1] + height//2 + oy)]
    click_screen(mid)
    return img





os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()
target = cv.imread('target22.JPG',1)

while(tries != 0):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    screenshot = find_target(screenshot,target,wincap.offset_x, wincap.offset_y)
    #cv.imshow('Vision', screenshot)
    tries -= 1




    if cv.waitKey(1) == ord('r'):
        sequence = []
        Level = 1

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')