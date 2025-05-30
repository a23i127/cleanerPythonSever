from torchvision import datasets
from torch.utils.data import DataLoader

def get_dataloader(data_dir, transform, batch_size=32):
    dataset = datasets.ImageFolder(data_dir, transform=transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)

