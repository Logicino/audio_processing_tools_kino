import os

input_file = "/Users/logickino/Documents/dataset_processing/Pn/train.lst"
output_file = "/Users/logickino/Documents/dataset_processing/list_on_server/Pn/train.lst"

prefix = "/data/xyth/A-unified-model-for-zero-shot-musical-source-separation-transcription-and-synthesis/dataset/hdf5s/Medley/Pn/"

# 读取输入文件中的路径列表
with open(input_file, 'r') as f:
    paths = f.readlines()

# 处理每个路径并写入输出文件
with open(output_file, 'w') as f:
    for path in paths:
        path = path.strip()  # 去除换行符和空格

        # 获取最后一个名字和后缀
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)

        # 构建新的路径
        new_path = prefix + name + ".h5\n"

        # 写入输出文件
        f.write(new_path)
