import random
import os
import cv2
import numpy as np

from ultralytics import YOLO
import matplotlib.pyplot as plt

images_path = 'dataset/JPEGImages/'
annotations_path = 'dataset/Annotations_txt/'
path = 'dataset/'

model = YOLO("yolov8m.pt")

img = 'img.png'
model.predict(source=img, conf=0.4, save=True, line_thickness=2)