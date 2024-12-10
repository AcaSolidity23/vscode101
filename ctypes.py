import ctypes
from tkinter import *
import time
import winsound
import os
import webbrowser
import urllib.request

#cafile = 'cacert.pem' # http://curl.haxx.se/ca/cacert.pem
#r = requests.get(url, verify=cafile)

temp = 'https://www.google.com/'
theurl = urllib.request.urlopen(temp)
print(theurl.read)
input('Press Enter to Close App')
