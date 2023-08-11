import h5py
file_path = '/Users/logickino/Documents/dataset_processing/instruments_final'

import random

# file_path = "your_file.txt"  # 文件路径
train_file_path = "EGt/train.lst"  # train.lst文件路径
test_file_path = "EGt/test.lst"  # test.lst文件路径

addresses = []

with open(file_path, "r") as file:
    for line in file:
        if line.startswith("EGt:"):
            addresses.extend(line.strip().split(", ")[1:])  # 提取地址并添加到地址列表中

random.shuffle(addresses)  # 随机打乱地址列表

train_addresses = addresses[:int(len(addresses) * 0.8)]  # 获取80%的地址
test_addresses = addresses[int(len(addresses) * 0.8):]  # 获取剩下的20%地址

# 将训练地址写入train.lst文件
with open(train_file_path, "w") as train_file:
    for address in train_addresses:
        train_file.write(address + "\n")

# 将测试地址写入test.lst文件
with open(test_file_path, "w") as test_file:
    for address in test_addresses:
        test_file.write(address + "\n")




# 转h5py