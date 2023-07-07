import numpy as np
import librosa

ROOT_DIR = '/data/xyth/musdb/test'
TARGET_DIR = '/data/xyth/A-unified-model-for-zero-shot-musical-source-separation-transcription-and-synthesis/dataset/hdf5s/musdb'

import os
import shutil
import h5py
import sys

def float32_to_int16(x):
	x = np.clip(x, -1, 1)
	assert np.max(np.abs(x)) <= 1.
	return (x * 32767.).astype(np.int16)


def pack_musdb_to_hdf5():
    # 获取 ROOT_DIR 中所有子目录的名称
    subdirs = next(os.walk(ROOT_DIR))[1]
    cnt = 0

    # 遍历每个子目录，并在 TARGET_DIR 下创建相应的目录，并将 wav 文件移动并打包为 h5 文件
    for subdir in subdirs:
        if cnt > 10:
            break
        # 构造源目录和目标目录的完整路径
        src_path = os.path.join(ROOT_DIR, subdir)
        dst_path = os.path.join(TARGET_DIR, subdir)

        # 创建目标目录
        os.makedirs(dst_path, exist_ok=True)

        # 遍历源目录中的文件，并找到后缀为 .wav 的文件
        for filename in os.listdir(src_path):
            if filename.endswith('.wav'):
                # 构造源文件和目标文件的完整路径
                src_file = os.path.join(src_path, filename)
                dst_file = os.path.join(dst_path, f'{filename[:-4]}.h5')

                # 读取 wav 文件的音频数据
                audio_data, sr = librosa.load(src_file)

                # 将音频数据转换为 int16 类型的 Numpy 数组
                audio_array = float32_to_int16(audio_data)

                # 使用 h5py 库创建 HDF5 数据文件，并将音频数据存储在其中
                with h5py.File(dst_file, 'w') as hf:
                    hf.create_dataset(name='waveform', data=audio_array, dtype=np.int16)
                    
        cnt += 1

# pack_musdb_to_hdf5()

def rename_folder():
    # 遍历指定目录下的所有子目录
    for foldername in os.listdir(TARGET_DIR):
        # 如果子目录名包含空格
        if ' ' in foldername:
            # 去掉空格
            newfoldername = foldername.replace(' ', '')
            # 生成新路径
            oldpath = os.path.join(TARGET_DIR, foldername)
            newpath = os.path.join(TARGET_DIR, newfoldername)
            # 重命名文件夹
            os.rename(oldpath, newpath)

rename_folder()