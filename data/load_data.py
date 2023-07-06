import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os

import sys
sys.path.append('/data/xyth/query_based_source_separation/')

from src.conf.feature import *
from src.models.models import MSSBaseline

# 先写一个用于训练QueryNet的Dataset/DataLoader



class QueryNetDataset(Dataset):
    '''
    用于训练QueryNet的Dataset格式
    只用读出来非mixed的乐器
    '''
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.instrument_lst = [elem for elem in os.listdir(root_dir) if 'mixed' not in elem]
        self.
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index):
        file_path = os.path.join(self.root_dir, self.file_list[index])
        # 加载原始数据，这里假设数据是npy格式
        spect = np.load(file_path)
        # 将数据转换为torch张量
        spect = torch.Tensor(spect)
        # 添加通道维度，如果不加则需要在模型中处理
        spect = spect.unsqueeze(0)

        return spect

dataset = QueryNetDataset(ROOT_DIR)
print(dataset.instrument_lst)
# 再写一个用于训练U-Net的DataLoader


print("hello")
# # 数据集目录
# data_dir = '/path/to/data/'

# # 实例化数据集类
# dataset = AudioDataset(data_dir)

# # 实例化数据加载器
# dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# # 迭代读取数据进行训练或测试
# for data in dataloader:
#     # do something with the data


# 模型测试
'''
model = MSSBaseline()
# 查看模型结构
print(model)
# 设计一个contrastive loss

data = np.load('/data/xyth/dealed_dataset/bn/AuSep_4_bn_28_Fugue.npy', 'r')

model(data, mode="query")
'''