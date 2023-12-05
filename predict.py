import random
import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from ultralytics import YOLO
import matplotlib.pyplot as plt

images_path = 'dataset/JPEGImages/'
annotations_path = 'dataset/Annotations_txt/'
path = 'dataset/'



app = FastAPI()

model = YOLO("yolov8m.pt")
i = 13

def add():
    return i + 1

async def predict_and_return(file_path, i):
    img = cv2.imread(file_path)
    model.predict(source=img, conf=0.4, save=True, line_thickness=2)
    i += 1
    return f"runs/detect/predict{i}/image0.jpg"
@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    global i
    file_path = f"images/{image.filename}"
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    img = cv2.imread(file_path)

    result_image_path = await predict_and_return(file_path, i)
    print(result_image_path)
    return FileResponse(result_image_path)
