import ctypes
from tkinter import *
import time
import winsound
import os
import webbrowser
import urllib.request

temp = 'https://www.google.com/'
theurl = urllib.request.urlopen(temp)
print(theurl.read)
input('Press Enter to Close App')
