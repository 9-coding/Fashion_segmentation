import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from ultralytics import YOLO
import firebase_admin
from firebase import uploadFirestore
from PIL import Image
import js2py

images_path = 'dataset/JPEGImages/'
annotations_path = 'dataset/Annotations_txt/'
path = 'dataset/'

app = FastAPI()

model = YOLO("yolov8m.pt")
i = 33

def add():
    return i + 1

async def predict_and_return(file_path, i):
    img = cv2.imread(file_path)
    model.predict(source=img, conf=0.4, save=True, line_thickness=2)
    return f"runs/detect/predict29/image0.jpg"

import requests


@app.post("/detect")
async def detect(image_link: str):
    global i
    try:
        print("link", image_link)
        response = requests.get(image_link)

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            img_name = image_link.split('/')[-1].split('?')[0]
            # 파일 이름 추출
            img_path = os.path.join("images/" + img_name)

            # 이미지 파일 저장
            with open(img_path, 'wb') as file:
                file.write(response.content)

            model.predict(source=img_path, conf=0.4, save=True, line_thickness=2)
            print(f"이미지 다운로드 완료: {img_name}")
        else:
            print("이미지를 다운로드할 수 없습니다.")

        response = requests.get(image_link, stream=True)
        response.raise_for_status()
        # 임시 경로
        predict_path = f"runs/detect/predict{i}/{img_name}"
        uploadFirestore(predict_path, img_name)
        return {"detail": "Image fetched successfully"}
    except requests.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        return HTTPException(status_code=400, detail="Failed to fetch image from URL")