from tkinter import *
ourWindow = Tk()
ourWindow.geometry('700x400+300+150')
ourWindow.title('Our Window')
ourLabel = Label(ourWindow,text = 'This is Fun', width = '200',font=("Courier", 25), fg = 'aqua',
bg = 'black').pack()
ourWindow.mainloop()
