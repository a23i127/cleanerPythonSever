import sys
import torch
from PIL import Image
from model_setup import load_model
from transforms_setup import get_transforms

LABELS = ['clean', 'messy']

def predict_image(image_path):
    transform = get_transforms()
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # shape: (1, 3, 224, 224)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model()
    model.load_state_dict(torch.load("room_cleanliness_model.pth", map_location=device))
    model.to(device)
    model.eval()

    with torch.no_grad():
        image = image.to(device)
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        label = LABELS[predicted.item()]
        return label

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("使い方: python inference.py <画像ファイルのパス>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = predict_image(image_path)
    print(f"🧠 推論結果: {result}")