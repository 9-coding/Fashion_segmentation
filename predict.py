import os
from fastapi import FastAPI, HTTPException
from ultralytics import YOLO
from firebase import uploadFirestore, firestore
import requests
import torch

images_path = 'dataset/JPEGImages/'
annotations_path = 'dataset/Annotations_txt/'
path = 'dataset/'

app = FastAPI()


@app.post("/detect")
async def detect(feedbackID: str):
    print(feedbackID)
    feedbackID = feedbackID[1:]
    print(feedbackID)
    db = firestore.client()
    users_ref = db.collection(u'feedback')
    docs = users_ref.stream()

    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        if doc.id == feedbackID:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
            print(doc.get('downloadURL'))
            imgSrc = doc.get('downloadURL')
            time = doc.get('timestamp')

    model = YOLO("yolov8m.yaml")

    # 사전 훈련된 가중치를 로드 (클래스 수가 일치하는지 확인 필요)
    model.load_state_dict(torch.load('yolov8m_Epoch-100.pt'))

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

    results = model()
    for result in results:
        for cls_id, custom_label in class_mapping.items():
            if cls_id in result.names:  # check if the class id is in the results
                result.names[cls_id] = custom_label  # replace the class name with the custom label

    try:
        print("link", imgSrc)
        response = requests.get(imgSrc)
        # 요청이 성공했는지 확인
        if response.status_code == 200:
            img_name = imgSrc.split('2F')[-1].split('?')[0]
            # 파일 이름 추출
            img_path = os.path.join("images/" + img_name)

            # 이미지 파일 저장
            with open(img_path, 'wb') as file:
                file.write(response.content)

            results = model.predict(source=img_path, conf=0.4, save=True, save_crop=True, line_thickness=2, project="result", name=f"{img_name}")
            print("path: " + results[0].save_dir)
            print(results[0])
            print(f"이미지 다운로드 완료: {img_name}")
        else:
            print("이미지를 다운로드할 수 없습니다.")

        uploadFirestore(imgSrc, time, img_path, img_name)
        return {"detail": "Image fetched successfully"}
    except requests.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        return HTTPException(status_code=400, detail="Failed to fetch image from URL")