from tkinter import *

ourWindow = Tk()
ourWindow.geometry('275x75+200+150')
ourWindow.title('Textbox to Label')

ourVariable = StringVar()
ourVariable.set('Hi Everyone')

ourLabel1 = Label(ourWindow,textvariable = ourVariable)
ourLabel1.pack()

ourTextArea = Entry(ourWindow,textvariable = ourVariable)
ourTextArea.pack()
ourWindow.mainloop()