import win32gui as win
import win32con as con
import win32api as api
import win32ui as ui
import ctypes

#1
win.MessageBox()
#2
win.MessageBox(None, "hello", "title", 0x00000004)
#3
win.MessageBox(None, "Arik Einstein", "title", con.MB_YESNO | con.MB_HELP)
#4
ans = win.MessageBox(None, "Arik Einstein", "title", con.MB_YESNO | con.MB_HELP)
if ans == 6:
    print("drive slow")
if ans == 7:
    print("drive fast")
#5 + 6
api.MessageBox(None, "hello", "title", 0x00000004) #yes, it works
#7
ui.MessageBox("hello", "title", 0x00000004)
#8 + 9
my_library = ctypes.WinDLL("User32.dll")
my_library.MessageBoxW(None, "hello", "title", 0x00000004)


