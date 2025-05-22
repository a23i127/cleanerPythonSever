from flask import Flask, request, jsonify
from PIL import Image
import os
import io
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    image_file = request.files['image']
    
    try:
        # 画像を読み込み（PIL形式で）
        image = Image.open(image_file.stream).convert("RGB")

        # ファイル名をユニークにして保存
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(path)

        # 🧠 ここに画像処理（YOLOやAIモデル）の処理を書く！
        result = {
            'message': '画像を受け取りました',
            'savedAs': filename,
            'status': 'analyzed (仮)'  # 実際の処理結果に差し替える
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)