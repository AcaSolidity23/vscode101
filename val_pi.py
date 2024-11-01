import math
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

ourTitle = "Value of Pi"

def ourFunction():
    ourText = math.pi
    answer = str(ourText)
    return answer

ctypes.windll.user32.MessageBoxW(0,ourFunction(), ourTitle, 0)