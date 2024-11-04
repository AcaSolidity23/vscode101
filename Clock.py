from tkinter import *
from time import*

ourWindow = Tk()
ourWindow.geometry('400x50+200+150')
ourWindow.title('Keep Updating Clock')

def ourFunction():
    theTime = localtime()
    formattedTime = asctime(theTime)
    ourText.set(formattedTime)
    ourLabel1.after(1000, ourFunction)
    
ourText = StringVar()
ourText.set('Click for Time')

ourLabel1 = Label(ourWindow,textvariable = ourText, font=("Arial", 25))
ourLabel1.pack()

ourFunction()
ourWindow.mainloop()