from tkinter import *

ourWindow = Tk()
ourTextField1 = Entry(ourWindow)
ourTextField1.pack()

def ourFunc():
    textEntered = ourTextField1.get()    
    ourLab = Label(ourWindow, text = textEntered,fg='aqua',bg='black').pack()
    
ourBttn = Button(ourWindow, text= 'Enter', command= ourFunc).pack()

ourWindow.mainloop()
    