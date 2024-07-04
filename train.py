import torch
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn as nn
import numpy as np
from dataset import train_loader,test_loader  # 确保导入你的数据加载器
from network import model  # 确保导入你的模型

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
num_epochs = 100
for epoch in range(num_epochs):
    model.train()  
    for ripple_images, clean_images in train_loader:
        ripple_images = ripple_images.to(device, non_blocking=True)
        clean_images = clean_images.to(device, non_blocking=True)
        
        optimizer.zero_grad()
        outputs = model(ripple_images)
        loss = criterion(outputs, clean_images)
        loss.backward()
        optimizer.step()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 保存模型
torch.save({
    'epoch': num_epochs,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss.item(),
}, 'model_checkpoint.pth')

print('Model saved successfully.')

# 加载模型并评估
checkpoint = torch.load('model_checkpoint.pth', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

all_ripple_images = []
all_clean_images = []
all_denoised_images = []

with torch.no_grad():
    for batch in test_loader:
        ripple_images = batch[0].to(device)
        clean_images = batch[1].to(device)
        
        denoised_images = model(ripple_images)

        ripple_images = ripple_images.permute(0, 2, 3, 1).cpu().numpy()
        clean_images = clean_images.permute(0, 2, 3, 1).cpu().numpy()
        denoised_images = denoised_images.permute(0, 2, 3, 1).cpu().numpy()

        all_ripple_images.append(ripple_images)
        all_clean_images.append(clean_images)
        all_denoised_images.append(denoised_images)

all_ripple_images = np.concatenate(all_ripple_images, axis=0)
all_clean_images = np.concatenate(all_clean_images, axis=0)
all_denoised_images = np.concatenate(all_denoised_images, axis=0)

def show_images(ripple, clean, denoised, num_images=10):
    n = min(len(ripple), num_images)
    plt.figure(figsize=(30, 6))
    for i in range(n):
        ax = plt.subplot(3, n, i + 1)
        plt.imshow(ripple[i])
        plt.title("Ripple")
        plt.axis("off")

        ax = plt.subplot(3, n, i + 1 + n)
        plt.imshow(clean[i])
        plt.title("Clean")
        plt.axis("off")

        ax = plt.subplot(3, n, i + 1 + 2 * n)
        plt.imshow(denoised[i])
        plt.title("Denoised")
        plt.axis("off")

    plt.show()

show_images(all_ripple_images, all_clean_images, all_denoised_images)