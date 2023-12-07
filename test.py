import cv2
import os
import requests
from io import BytesIO
import time
from PIL import Image

url = "https://firebasestorage.googleapis.com/v0/b/cloc-bdf74.appspot.com/o/Cloth%2F1701950259641.jpg?alt=media&token=f58ccddb-04ce-4ee7-aa70-77652658240b"

response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # 파일 이름 추출
    img = response.content
    img_data = Image.open(BytesIO(response.content))
    img_data.show()

    print(f"이미지 다운로드 완료: {file_name}")
else:
    print("이미지를 다운로드할 수 없습니다.")