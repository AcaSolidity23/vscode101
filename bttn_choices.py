import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ourTitle = "Greeting App"

def ourFunction():
    ourText = "Ready?"
    return ourText

choice = ctypes.windll.user32.MessageBoxW(0,ourFunction(), ourTitle, 3)

if (choice == 6):
    print("pressed Yes")
if (choice == 7):
    print("pressed No")
if (choice == 2):
    print("pressed Cancel")
    
input('Press Enter to Exit')