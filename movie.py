import moviepy
from moviepy.editor import *
import pygame

ourVid = VideoFileClip('testMovie.mp4').resize(0.3)
ourVid.preview()
pygame.quit()
