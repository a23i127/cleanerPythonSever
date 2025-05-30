# 📁 train.py
import torch
import torch.nn as nn
import torch.optim as optim

from model_setup import load_model
from transforms_setup import get_transforms
from dataset_loader import get_dataloader

# --- ハイパーパラメータ ---
EPOCHS = 5
LEARNING_RATE = 0.001
BATCH_SIZE = 32
DATA_DIR = "dataset"  # dataset/clean, dataset/messy

# --- モデルとデータの準備 ---
transform = get_transforms()
dataloader = get_dataloader(DATA_DIR, transform, batch_size=BATCH_SIZE)
model = load_model()

# GPUが使える場合は使う
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- 損失関数と最適化 ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# --- 学習ループ ---
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        # 勾配を初期化
        optimizer.zero_grad()

        # 推論
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"[{epoch+1}/{EPOCHS}] Loss: {running_loss:.4f}, Accuracy: {accuracy:.2f}%")

# --- モデル保存 ---
torch.save(model.state_dict(), "room_cleanliness_model.pth")
print("✅ 学習完了・モデル保存済み")