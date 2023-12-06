import random
import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from ultralytics import YOLO
from pydantic import BaseModel
from typing import Optional
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



import requests


@app.post("/detect")
async def detect(image_link: str):
    global i
    try:
        print("link", image_link)
        model.predict()
        response = requests.get(image_link, stream=True)
        response.raise_for_status()
        return {"detail": "Image fetched successfully"}


    except requests.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        return HTTPException(status_code=400, detail="Failed to fetch image from URL")