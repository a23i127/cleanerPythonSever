import torch
from torchvision import models

def load_model():
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)  # 2クラス分類
    return model