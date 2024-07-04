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


class CustomRippleDataset(Dataset):
    def __init__(self, ripple_dir, clean_dir, transform=None):
        self.ripple_dir = ripple_dir
        self.clean_dir = clean_dir
        self.transform = transform
        self.ripple_images = sorted(os.listdir(ripple_dir))
        self.clean_images = sorted(os.listdir(clean_dir))

    def __len__(self):
        return len(self.ripple_images)

    def __getitem__(self, idx):
        ripple_image_path = os.path.join(self.ripple_dir, self.ripple_images[idx])
        clean_image_path = os.path.join(self.clean_dir, self.clean_images[idx])
        
        ripple_image = Image.open(ripple_image_path).convert('RGB')
        clean_image = Image.open(clean_image_path).convert('RGB')
        
        if self.transform:
            ripple_image = self.transform(ripple_image)
            clean_image = self.transform(clean_image)
        
        return ripple_image, clean_image

transform = transforms.Compose([
    transforms.ToTensor()
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

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False, pin_memory=True)
