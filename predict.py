import os
from fastapi import FastAPI, HTTPException
from ultralytics import YOLO
from firebase import uploadFirestore
import torch

images_path = 'dataset/JPEGImages/'
annotations_path = 'dataset/Annotations_txt/'
path = 'dataset/'

app = FastAPI()

# 모델을 yaml 파일 구성에 맞게 초기화
model = YOLO("yolov8m.yaml")

# 사전 훈련된 가중치를 로드 (클래스 수가 일치하는지 확인 필요)
model.load_state_dict(torch.load('yolov8m_trained-15Epoch.pt'))

class_mapping = {
    0: 'sunglass',
    1: 'hat',
    2: 'jacket',
    3: 'shirt',
    4: 'pants',
    5: 'shorts',
    6: 'skirt',
    7: 'dress',
    8: 'bag',
    9: 'shoe',
}

# source = ''에 내가 원하는 이미지의 경로를 작성하면된다.
results = model(source='img.png')
for result in results:
    for cls_id, custom_label in class_mapping.items():
        if cls_id in result.names:  # check if the class id is in the results
            result.names[cls_id] = custom_label  # replace the class name with the custom label



# 현재까지는 모델을 예측하면 runs/detect/train#number의 경로로 이미지가 저장된다
# 저장은 Detection된 이미지, 옷이 crop된 이미지 이렇게 각각의 클래스 폴더가 생성되고 저장된다.
results = model.predict(source='img.png', conf=0.4, save=True, save_crop= True, line_thickness=2)
print("path: " + results[0].save_dir)
# terminal에 저장된 경로가 나오는데 거기로 이동해서 확인해보면 됩니다.


import requests


@app.post("/detect")
async def detect(image_link: str):
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

            results = model.predict(source=img_path, conf=0.4, save=True, line_thickness=2, project="result", name="result1")
            print(results[0])
            print(f"이미지 다운로드 완료: {img_name}")
        else:
            print("이미지를 다운로드할 수 없습니다.")

        response = requests.get(image_link, stream=True)
        response.raise_for_status()
        # 임시 경로
        predict_path = f"runs/detect/predict/{img_name}"
        uploadFirestore(predict_path, img_name)
        return {"detail": "Image fetched successfully"}
    except requests.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        return HTTPException(status_code=400, detail="Failed to fetch image from URL")