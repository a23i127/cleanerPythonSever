import os
import requests
from face_filter import contains_face 

# --- 🔐 Pexels APIキーを貼り付けてください ---
PEXELS_API_KEY = "3QhQurdrlKiOkl1BqNxsjvIyz8KWHZusb4qJNgyis82VTtYJwhisMWd0"

SEARCH_QUERY = "interior"
SAVE_DIR = "dataset/clean"
PER_PAGE = 15
NUM_PAGES = 10

os.makedirs(SAVE_DIR, exist_ok=True)

headers = {
    "Authorization": PEXELS_API_KEY
}

def download_images():
    # すでに保存されているファイル数を確認して count をスタート
    existing_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")]
    count = len(existing_files)

    for page in range(1, NUM_PAGES + 1):
        params = {
            "query": SEARCH_QUERY,
            "per_page": PER_PAGE,
            "page": page
        }

        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        if response.status_code != 200:
            print(f"⚠️ リクエスト失敗（status: {response.status_code}）")
            continue

        data = response.json()
        for photo in data.get("photos", []):
            url = photo["src"]["large"]
            image_data = requests.get(url).content

            if contains_face(image_data):
                print("🚫 顔が検出されたためスキップします")
                continue

            filename = os.path.join(SAVE_DIR, f"clean_{count}.jpg")
            with open(filename, "wb") as f:
                f.write(image_data)
            print(f"✅ Saved: {filename}")
            count += 1

    print(f"\n🎉 合計 {count - len(existing_files)} 枚の新しい画像を保存しました！")

if __name__ == "__main__":
    download_images()