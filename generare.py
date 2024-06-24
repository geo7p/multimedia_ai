# -*- coding: utf-8 -*-
"""generare.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10A3unams6b9foHe9DyhjOcdAZruhd2pv
"""

!pip install -q --upgrade keras-cv
!pip install -q --upgrade keras
!pip install pyttsx3
!pip install pydub

import time
import keras_cv
import keras
import matplotlib.pyplot as plt
import cv2
import numpy as np
from google.colab import drive
from google.colab.patches import cv2_imshow
from moviepy.editor import *
import pyttsx3
from pydub import AudioSegment

model = keras_cv.models.StableDiffusion(
    img_width=512, img_height=512, jit_compile=False
)

drive.mount('/content/drive')

images = model.text_to_image("a laptop which is pink in a supermarket", batch_size=3)

def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")

plot_images(images)

def save_images(images):
    for i in range(len(images)):
        img = cv2.imwrite(f"/content/drive/My Drive/image_{i+1}.png", images[i])

save_images(images)

drive.mount('/content/drive')

image = cv2.imread("/content/drive/My Drive/image.png")
cv2.rectangle(image, (50, 65), (425, 430), (0, 0, 255), 2)
cv2_imshow(image)

image = cv2.imread("/content/drive/My Drive/image.png")

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_pink = np.array([130, 50, 50])
upper_pink = np.array([170, 255, 255])


mask = cv2.inRange(hsv_image, lower_pink, upper_pink)


result = cv2.bitwise_and(image, image, mask = mask)

cv2_imshow(mask)
cv2_imshow(result)

mask = cv2.imwrite("/content/drive/My Drive/mask.png", mask)
result = cv2.imwrite("/content/drive/My Drive/result.png", result)

imrez = cv2.imread("/content/drive/My Drive/result.png")

imrez = cv2.cvtColor(imrez, cv2.COLOR_BGR2GRAY)

cv2_imshow(imrez)

imrez = cv2.imwrite("/content/drive/My Drive/rezgray.png", imrez)

img1 = cv2.imread("/content/drive/My Drive/image.png")
img2 = cv2.imread("/content/drive/My Drive/result.png")
img3 = cv2.imread("/content/drive/My Drive/rezgray.png")

width, height, layers = img1.shape
size = (width, height)

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter("/content/drive/My Drive/video.mp4", fourcc, 30, size, True)

for i in range(0, 150):
  video.write(img1)

for i in range(0, 150):
  video.write(img2)

for i in range(0, 150):
  video.write(img3)

video.release()

newvideo = cv2.VideoWriter("/content/drive/My Drive/newvideo.mp4", fourcc, 30, size, True)

text1 = "Original image"
text2 = "Mask with the object"
text3 = "Grayscale image"

cv2.putText(img1, text1, (50, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
for i in range(0, 150):
  newvideo.write(img1)

cv2.putText(img2, text2, (50, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
for i in range(0, 150):
  newvideo.write(img2)


cv2.putText(img3, text3, (50, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
for i in range(0, 150):
  newvideo.write(img3)

newvideo.release()

!sudo apt-get update
!sudo apt-get install espeak

engine = pyttsx3.init()

engine.save_to_file(text1, "/content/drive/My Drive/audio1.wav")
engine.runAndWait()

engine.save_to_file(text2, "/content/drive/My Drive/audio2.wav")
engine.runAndWait()

engine.save_to_file(text3, "/content/drive/My Drive/audio3.wav")
engine.runAndWait()

audio1 = AudioSegment.from_wav("/content/drive/My Drive/audio1.wav")

audio2 = AudioSegment.from_wav("/content/drive/My Drive/audio2.wav")

audio3 = AudioSegment.from_wav("/content/drive/My Drive/audio3.wav")

audiofin = audio1 + audio2 + audio3

audiofin.export("/content/drive/My Drive/audiofin.mp3", format = "mp3")

videoclip = VideoFileClip("/content/drive/My Drive/newvideo.mp4")
audioclip = AudioFileClip("/content/drive/My Drive/audiofin.mp3")

videoclip = videoclip.set_audio(audioclip)

videoclip.write_videofile("newvideo2.mp4")