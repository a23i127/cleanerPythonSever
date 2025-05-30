from model_setup import load_model
from transforms_setup import get_transforms
from dataset_loader import get_dataloader

if __name__ == '__main__':
    data_dir = 'dataset'  # dataset/clean/, dataset/messy/ という構造
    transform = get_transforms()
    dataloader = get_dataloader(data_dir, transform)
    model = load_model()

    print("✅ モデルとデータローダーの準備が完了しました")
