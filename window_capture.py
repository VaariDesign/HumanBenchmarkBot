import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.GetDesktopWindow()
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 400
        titlebar_pixels = 200
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        # get the window image data
        wdc = win32gui.GetWindowDC(self.hwnd)
        dcobj = win32ui.CreateDCFromHandle(wdc)
        cdc = dcobj.CreateCompatibleDC()
        databitmap = win32ui.CreateBitmap()
        databitmap.CreateCompatibleBitmap(dcobj, self.w, self.h)
        cdc.SelectObject(databitmap)

        cdc.BitBlt((0, 0), (self.w, self.h), dcobj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        databitmap.SaveBitmapFile(cdc, 'debug.bmp')
        signedintsarray = databitmap.GetBitmapBits(True)

        img = np.fromstring(signedintsarray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcobj.DeleteDC()
        cdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wdc)
        win32gui.DeleteObject(databitmap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img

    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)