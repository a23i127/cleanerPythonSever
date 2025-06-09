import google.generativeai as genai
from PIL import Image
import base64
import json
from model import RoomCleanliness  # ← model.py から import する想定
genai.configure(api_key="AIzaSyAT-tD3-8hh5zHs0SrBV8lZW7vKPIYb9XE")
def analyze_image_for_cleanliness(image_path: str) -> RoomCleanliness | None:
    try:
        # 画像読み込み
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Gemini モデル呼び出し
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {"text": """
                    この写真が整理されているかどうか判断し、読み手が分かりやすいように観点別にアドバイスして欲しい。以下のJSON形式で出力してください：

                    {
                        "score": 0〜100の整数（点数が高いほど整理されている）,
                        "state": "整理されている / やや整理されている / 散らかっている など",
                        "advice": "普通のアドバイスに加えて、どのように整理すると、(整理スコアが上がるかも含めてアドバイスしてください)"
                    }

                    ※JSONのみで出力してください。他の文章は不要です。
                    """},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_bytes
                        }
                    }
                ]
            }])

        # JSONパースはここで別tryでもよいが簡単なエラーチェックならそのままでもOK
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()
            if response_text.endswith("```"):
                 response_text = response_text[:-3].strip()
        data = json.loads(response_text)
        cleanliness = RoomCleanliness(
            score = data.get("score", 0),
            state = data.get("state", ""),
            advice = data.get("advice", "")
        )
        return cleanliness

    except json.JSONDecodeError:
        print("❌ JSONパースに失敗しました。Geminiの出力:", response.text)
        return None

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return None