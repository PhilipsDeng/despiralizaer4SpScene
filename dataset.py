import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import base_path as bp
'''
data/
  train/
    ripple/
      img1.png
      img2.png
      ...
    clean/
      img1.png
      img2.png
      ...
  test/
    ripple/
      img1.png
      img2.png
      ...
    clean/
      img1.png
      img2.png
      ...
'''

batch_size = bp.batch_size

class CustomRippleDataset(Dataset):
    def __init__(self, ripple_dir, clean_dir, transform=None):
        self.ripple_dir = ripple_dir
        self.clean_dir = clean_dir
        self.transform = transform
        self.ripple_images = sorted(os.listdir(ripple_dir))
        self.clean_images = sorted(os.listdir(clean_dir))
        
        # 预加载所有图片到内存
        self.ripple_images_data = [self.load_image(os.path.join(ripple_dir, img)) for img in self.ripple_images]
        self.clean_images_data = [self.load_image(os.path.join(clean_dir, img)) for img in self.clean_images]

    def __len__(self):
        return len(self.ripple_images)

    def __getitem__(self, idx):
        ripple_image = self.ripple_images_data[idx]
        clean_image = self.clean_images_data[idx]
        
        if self.transform:
            ripple_image = self.transform(ripple_image)
            clean_image = self.transform(clean_image)
        
        return ripple_image, clean_image

    def load_image(self, path):
        return Image.open(path).convert('RGB')

transform = transforms.Compose([
    transforms.ToTensor(),
])

train_dataset = CustomRippleDataset(
    ripple_dir=bp.dataset_path + '/train/ripple',
    clean_dir=bp.dataset_path + '/train/clean',
    transform=transform
)

test_dataset = CustomRippleDataset(
    ripple_dir=bp.dataset_path + '/test/ripple',
    clean_dir=bp.dataset_path + '/test/clean',
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, pin_memory=True)
