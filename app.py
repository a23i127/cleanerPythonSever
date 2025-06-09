from flask import Flask, request, jsonify
from PIL import Image
import torch
from torchvision import transforms
from model_setup import load_model
from gemini_advisor import analyze_image_for_cleanliness
import os
from datetime import datetime

app = Flask(__name__)

# --- アップロード保存先フォルダ ---
UPLOAD_FOLDER = "uploadfolder"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- モデルの読み込み ---
model = load_model()
model.load_state_dict(torch.load("room_cleanliness_model.pth", map_location="cpu"))
model.eval()

# --- 前処理 ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# --- 推論APIエンドポイント ---
@app.route('/analyze', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': '画像が含まれていません'}), 400

    file = request.files['image']

    # 画像ファイル保存
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
   
    # 画像読み込みと前処理
    image = Image.open(save_path)  # ← まずはそのまま開く
    image = image.convert("RGB")  # ← format取得後に変換
    input_tensor = transform(image).unsqueeze(0)

    # モデルによる推論
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1).item()

    label_map = {0: 'clean', 1: 'messy'}
    result_label = label_map[prediction]

    # Gemini API によるアドバイス
    gemini_advice = analyze_image_for_cleanliness(save_path)

    return jsonify({
        "filename": filename,
        "result": gemini_advice.state,
        "advice": gemini_advice.advice,
        "score": gemini_advice.score
    })

# --- サーバー起動 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)