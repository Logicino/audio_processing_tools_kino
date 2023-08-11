import os

def modify_path(path):
    # 获取目录和文件名
    dir_name = os.path.dirname(path)
    file_name = os.path.basename(path)

    # 拆分目录名并删除重复的部分
    dirs = dir_name.split('/')
    new_dirs = [dirs[0]]
    for i in range(1, len(dirs)):
        if dirs[i] != dirs[i-1]:
            new_dirs.append(dirs[i])

    # 构建新路径
    new_path = os.path.join('/'.join(new_dirs), file_name)

    return new_path

# 读取train.lst文件
with open("EGt/train.lst", "r") as file:
    lines = file.readlines()

# 修改路径并写入新的train.lst文件
with open("EGt/train.lst", "w") as file:
    for line in lines:
        old_path = line.strip()
        new_path = modify_path(old_path)
        file.write(new_path + "\n")

print("路径修改完成！")
