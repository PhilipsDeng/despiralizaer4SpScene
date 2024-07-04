import torch
import numpy as np
import matplotlib.pyplot as plt
from network import model  # 假设network.py中定义了模型
from dataset import test_loader  # 假设dataset.py中定义了test_loader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 加载保存的模型检查点
checkpoint = torch.load('model_checkpoint.pth', map_location=device)

# 加载模型的状态字典
model.load_state_dict(checkpoint['model_state_dict'])

# 将模型设置为评估模式
model.eval()

# 使用模型进行预测并收集所有预测结果
all_ripple_images = []
all_clean_images = []
all_denoised_images = []

with torch.no_grad():
    for batch in test_loader:
        # 提取ripple和clean图像
        ripple_images = batch[0].to(device)
        clean_images = batch[1].to(device)
        
        # 进行预测
        denoised_images = model(ripple_images)

        # 将结果转换为numpy数组
        ripple_images = ripple_images.permute(0, 2, 3, 1).cpu().numpy()
        clean_images = clean_images.permute(0, 2, 3, 1).cpu().numpy()
        denoised_images = denoised_images.permute(0, 2, 3, 1).cpu().numpy()

        all_ripple_images.append(ripple_images)
        all_clean_images.append(clean_images)
        all_denoised_images.append(denoised_images)

# 将所有批次的结果拼接在一起
all_ripple_images = np.concatenate(all_ripple_images, axis=0)
all_clean_images = np.concatenate(all_clean_images, axis=0)
all_denoised_images = np.concatenate(all_denoised_images, axis=0)

all_clean_images = np.clip(all_clean_images, 0, 1)
all_denoised_images = np.clip(all_denoised_images, 0, 1)
all_ripple_images = np.clip(all_ripple_images, 0, 1)

# 显示原始波纹图像和去波纹后的图像
def show_images(ripple, denoised, clean, num_images=10):
    n = min(len(ripple), num_images)
    plt.figure(figsize=(30, 6))
    for i in range(n):
        ax = plt.subplot(3, n, i + 1)
        plt.imshow(ripple[i])
        plt.title("Ripple")
        plt.axis("off")

        ax = plt.subplot(3, n, i + 1 + 2 * n)
        plt.imshow(denoised[i])
        plt.title("Denoised")
        plt.axis("off")

        ax = plt.subplot(3, n, i + 1 + n)
        plt.imshow(clean[i])
        plt.title("Clean")
        plt.axis("off")

    plt.show()

# 显示一些测试结果
show_images(all_ripple_images, all_denoised_images, all_clean_images)

# if __name__ == "__main__":
#     show_images(all_ripple_images, all_clean_images, all_denoised_images)
