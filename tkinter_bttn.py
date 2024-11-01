from tkinter import *
def ourFunc():
    print('Blue')
    ourWindow.configure(bg='blue')
ourWindow = Tk()
ourWindow.geometry('300x200+300+200')
ourWindow.title('Here is Our Window')
ourButton = Button(ourWindow,text = 'Change Color',command = ourFunc, fg = 'white', bg = 'black').place(x = 100, y = 50)
ourWindow.mainloop()