import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ourTitle = "Greeting App"

def ourFunction():
    ourText = "Ready?"
    return ourText

choice = ctypes.windll.user32.MessageBoxW(0,ourFunction(), ourTitle, 1)

if (choice == 1):
    print("pressed ok")
if (choice == 2):
    print("pressed cancel")
    
input('Press Enter to Exit')