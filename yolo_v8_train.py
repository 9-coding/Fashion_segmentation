import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt

print(torch.__version__)
device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')

print (f"PyTorch version:{torch.__version__}") # 1.12.1 이상
print(f"MPS 장치를 지원하도록 build 되었는지: {torch.backends.mps.is_built()}") # True 여야 합니다.
print(f"MPS 장치가 사용 가능한지: {torch.backends.mps.is_available()}") # True 여야 합니다.
model = YOLO("yolov8m.pt")

model.train(data='data.yaml', epochs=5, device='mps')

model_path = 'runs/detect/train/'

def plot(ls, size):
    c = 1
    plt.figure(figsize=(15,10))
    for im in ls:
        plt.subplot(size[0],size[1],c)
        im = plt.imread(model_path+im)
        plt.imshow(im)
        c += 1
    plt.show()

plot(['P_curve.png', 'R_curve.png'], (1,2))
plot(['F1_curve.png', 'PR_curve.png'], (1,2))
plot(['confusion_matrix.png', 'labels.jpg'], (1,2))
plot(['results.png'],(1,1))