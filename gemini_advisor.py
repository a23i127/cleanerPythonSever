import google.generativeai as genai
from PIL import Image
import base64
import json
from model import RoomCleanliness  # ← model.py から import する想定
genai.configure(api_key="AIzaSyAT-tD3-8hh5zHs0SrBV8lZW7vKPIYb9XE")
def analyze_image_for_cleanliness(image_path: str) -> RoomCleanliness | None:
    print("[INFO] Gemini APIモック応答を返します（Renderデプロイ用）")
    return RoomCleanliness(
        score = 80,
        state = "やや整理されている",
        advice = "床の上の物を片付けるとより良くなります。"
    )

 