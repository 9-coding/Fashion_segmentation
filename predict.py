from ultralytics import YOLO
import torch

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
model.predict(source='img.png', conf=0.4, save=True, save_crop= True, line_thickness=2)

# terminal에 저장된 경로가 나오는데 거기로 이동해서 확인해보면 됩니다.


