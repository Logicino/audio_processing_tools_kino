import numpy as np
import os
import librosa
import matplotlib.pyplot as plt

import sys
sys.path.append('/data/xyth/query_based_source_separation/')

from src.conf.feature import *

import random
import fnmatch
import soundfile as sf

# Consts
ROOT_DIR = "/data/xyth/dealed_dataset"
TARGET_LENGTH = 174  # 单位：seconds
INSTRUMENT_NUM = 13
MIX_LST = '/data/xyth/query_based_source_separation/data_saved/mix_list.txt'
MIX_DIR = '/data/xyth/dealed_dataset/mixed'
SAMPLE_RATE = 16000


def get_all_instruments(root_dir):
    instrument_lst = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    return instrument_lst

def get_instrument_dirs(root_dir):
    '''
    return sub_dirs: [dir_1, dir_2, ..., dir_n]
    '''
    res = []
    instrument_lst = get_all_instruments(root_dir=root_dir)
    for instrument in instrument_lst:
        instrument_dir = os.path.join(root_dir, instrument)
        res.append(instrument_dir)
        
    return res

def count_the_length():
    '''
    计算每首歌的长度
    返回：每首歌长度的list
    '''
    # 先获得instrument list
    instrument_lst = get_all_instruments(root_dir=ROOT_DIR) 
    song_length = []
    for instrument in instrument_lst:
        instrument_dir = os.path.join(ROOT_DIR, instrument)
        # song_lst = [song for song in os.listdir(instrument_dir)]
        for song in os.listdir(instrument_dir): 
            file_path = os.path.join(instrument_dir, song)
            audio, sr = librosa.load(file_path, sr=None)
            duration_s = librosa.get_duration(y=audio, sr=sr)
            song_length.append(duration_s)
    return song_length      
    
# 保存长度
# song_length = count_the_length()
# np.save('/data/xyth/query_based_source_separation/data_npy/length.npy', song_length)

def plot_dist(data):
    # 统计分布
    plt.hist(data, bins = 10)
    plt.show()

def delete_npy(root_dir=ROOT_DIR):
    '''
    清除根目录下的所有后缀名为.npy文件
    '''
    instrument_lst = get_all_instruments(root_dir=ROOT_DIR)
    for instrument in instrument_lst:
        instrument_dir = os.path.join(ROOT_DIR, instrument)
        # song_lst = [song for song in os.listdir(instrument_dir)]
        for song in os.listdir(instrument_dir): 
            if song.endswith('.npy'):
                os.remove(os.path.join(instrument_dir, song))

# 所有预处理都要走这个：削长度 + 重采样
def trim_or_pad_audio_length(audio_dir):
    '''
    输入：audio_dir
    输出：resampled_audio
    '''
    audio, sr = librosa.load(audio_dir) # 这里不做resample，直接采用原始采样率
    duration_s = librosa.get_duration(y=audio, sr=sr)
    if duration_s > TARGET_LENGTH:  # 长度比目标大，截断
        start_sample = 0
        duration_samples = TARGET_LENGTH * sr   # sr是采样率
        y_target = audio[start_sample:start_sample + duration_samples]
    else:  # 长度小于等于目标，补0
        y_target = librosa.util.pad_center(data=audio, size=TARGET_LENGTH * sr, axis=0)
    ## 重采样
    resampled_audio = librosa.resample(y_target, orig_sr = sr, target_sr = SAMPLE_RATE)
    return resampled_audio
    
def change_into_spec():
    instrument_lst = get_all_instruments(root_dir=ROOT_DIR) 
    song_length = []
    for instrument in instrument_lst:
        instrument_dir = os.path.join(ROOT_DIR, instrument)
        # song_lst = [song for song in os.listdir(instrument_dir)]
        for song in os.listdir(instrument_dir): 
            file_path = os.path.join(instrument_dir, song)
            y_target = trim_or_pad_audio_length(audio_dir=file_path)
            y_spec = librosa.stft(y_target, n_fft = N_FFT, hop_length = HOP_SIZE, window = WINDOW, win_length = WINDOW_SIZE)
            y_save_path = os.path.join(instrument_dir, song)
            y_save_path = y_save_path.replace('.wav', '.npy')
            # print(y_save_path)
            np.save(y_save_path, abs(y_spec))  # 存成幅度谱

# change_into_spec()

# 写一个抽取的list_file，保证结果可复现
list_log = open('/data/xyth/query_based_source_separation/data_saved/mix_list.txt', 'a')

def generate_mix_audio_lst():
    '''
    在mix_list.txt里生成combine的list
    '''
    for stem in range(2, STEM_RANGE + 1):
        for iter in range(SELECT_NUMBER):
            # 获取所有乐器的文件夹的名称
            instrument_dir_lst = get_instrument_dirs(root_dir=ROOT_DIR)
            
            # 随机抽取stem个子文件夹
            selected_subdirs = random.sample(instrument_dir_lst, stem)
            # 在这个dir下面随机选取一个文件
            
            # 遍历列表中的每个目录，获取所有符合条件的文件名，并随机选取一个文件
            random_files = []
            for dir in selected_subdirs:
                wav_files = [f for f in os.listdir(dir) if fnmatch.fnmatch(f, '*.wav')]
                if wav_files:
                    random_file = random.choice(wav_files)
                    random_files.append(os.path.join(dir, random_file))
                
            print(random_files)
            
            list_log.write(str(random_files)+'\n')  # 把随机抽取的这个file写到list_log里面

def get_instrument_name(input_file_name):
    filename = os.path.basename(input_file_name)
    
    # 分割文件名和扩展名
    name, ext = filename.split('.')
    
    # 根据'_'字符拆分文件名，获取第3个元素
    instr_name = name.split('_')[2]
    
    return instr_name

# print(get_instrument_name('/data/xyth/dealed_dataset/ob/AuSep_3_ob_30_Fugue.wav'))
    
mix_list_log = open('/data/xyth/query_based_source_separation/data_saved/mix_wav_list.txt', 'a')

def mix_audio():
    # 逐个加载音频文件并将其添加到mix_audio中
    mixed_audio = None
    with open(MIX_LST, 'r') as f:
        lines = f.readlines()
        for line in lines:
            mix_file_lst = eval(line.strip()) # 获得txt中一行的list ['/data/xyth/dealed_dataset/ob/AuSep_3_ob_30_Fugue.wav', '/data/xyth/dealed_dataset/tbn/AuSep_4_tbn_42_Arioso.wav']
            mix_file_name = get_instrument_name(mix_file_lst[0]) # 获得每个文件的乐器名字，例如ob,tbn
            
            y1 = trim_or_pad_audio_length(mix_file_lst[0])
            
            for mix_file in mix_file_lst[1:]:
                ins_name = get_instrument_name(mix_file)
                mix_file_name += "+" + ins_name
                # y2, sr2 = librosa.load(mix_file)
                y2 = trim_or_pad_audio_length(mix_file)
                
                y1 += y2
                
            mixed_file_path = os.path.join(MIX_DIR, mix_file_name + '.wav')     # 起个名字
            
            # 写入一个mixture list
            # mix_list_log.write(str(mixed_file_path)+'\n')  
            
            print(mix_file_name)
            print(mixed_file_path)
            
            # 写入文件
            sf.write(mixed_file_path, y1, SAMPLE_RATE)
            # librosa.output.write_wav(mixed_file_path, y1, sr = SAMPLE_RATE)
            

print("hello")