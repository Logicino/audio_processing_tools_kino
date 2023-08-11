import numpy as np
import h5py
import soundfile  # Optional. Use any library you like to write audio files.
import librosa  # Optional. Use any library you like to read audio files.
import os
from slicer2 import Slicer

ROOT_DIR = '/Users/logickino/Downloads/Medley_DB/Medley'
TARGET_DIR = '/Users/logickino/Downloads/Medley_DB/Medley_h5'

SAMPLE_RATE = 16000
INSTR_NAME = 'Str'
FRAMES_PER_SEC = 100

#test_dir = '/Users/logickino/Downloads/Medley_DB/Medley/AlexanderRoss_GoodbyeBolero/AlexanderRoss_GoodbyeBolero_STEMS/AlexanderRoss_GoodbyeBolero_STEM_02.wav'

def remove_empty_segment(audio, sr):
	slicer = Slicer(
		sr=sr,
		threshold=-40,
		min_length=5000,
		min_interval=300,
		hop_size=10,
		max_sil_kept=500
	)
	chunks = slicer.slice(audio)
	return chunks


def float32_to_int16(x):
	x = np.clip(x, -1, 1)
	assert np.max(np.abs(x)) <= 1.
	return (x * 32767.).astype(np.int16)

def pack_to_hdf5():
	# 按照train.lst里的文件写成h5文件
	train_list_dir = f'/Users/logickino/Documents/dataset_processing/{INSTR_NAME}/train.lst'
	# cnt = 0
	with open(train_list_dir, 'r') as file:
		for line in file:
			# cnt += 1
			address = line.strip()  # 去除行末尾的换行符和空格
			print(address)  # 或者执行你希望的其他操作

			dst_file = f'/Users/logickino/Downloads/Medley_DB/Medley_h5/{INSTR_NAME}/' + address.split('/')[-1].replace('.wav', '.h5')
			print(dst_file)
			# 读取 wav 文件的音频数据
			(audio, _) = librosa.load(address, sr=SAMPLE_RATE, mono=True)
			(hq_audio, _) = librosa.load(address, sr=SAMPLE_RATE * 2, mono=True)

			# 将音频数据转换为 int16 类型的 Numpy 数组
			audio_array = float32_to_int16(audio)

			# dense_audio需要做vad
			scale = 3  # PITCH_SHIFT = 1
			chunks_audio = remove_empty_segment(audio, SAMPLE_RATE)
			chunks_hq_audio = remove_empty_segment(hq_audio, SAMPLE_RATE * 2)
			if len(chunks_audio)==0:
				print("{} is jumped".format(address))
				continue
			else:
				dense_audio = np.concatenate(chunks_audio)
				dense_hq_audio = np.concatenate(chunks_hq_audio)


			for i in range(scale):
				shift_pitch = i - (scale // 2)
				packed_hdf5_path = os.path.join(TARGET_DIR, '{}/{}._TRAIN_shift_pitch_{}.h5'.format(INSTR_NAME, os.path.splitext(os.path.split(address)[-1])[0], shift_pitch))
				if os.path.exists(packed_hdf5_path):
					print("{} already exitst, skipped".format(TARGET_DIR))
					continue

				if shift_pitch == 0:
					shift_audio = audio
					shift_dense_audio = dense_audio

				else:
					shift_audio = librosa.effects.pitch_shift(hq_audio, SAMPLE_RATE * 2, n_steps = shift_pitch)
					shift_audio = librosa.core.resample(shift_audio, SAMPLE_RATE * 2, SAMPLE_RATE)
					shift_dense_audio = librosa.effects.pitch_shift(dense_hq_audio, SAMPLE_RATE * 2, n_steps = shift_pitch)
					shift_dense_audio = librosa.core.resample(shift_dense_audio, SAMPLE_RATE * 2, SAMPLE_RATE)

				with h5py.File(packed_hdf5_path, 'w') as hf:
					hf.create_dataset(name='shift_waveform', data=float32_to_int16(shift_audio), dtype=np.int16)
					hf.create_dataset(name='shift_dense_waveform', data=float32_to_int16(shift_dense_audio),dtype=np.int16)
					# hf.create_dataset(name='frame_roll', data=shift_frame_roll, dtype=np.int16)

			# 使用 h5py 库创建 HDF5 数据文件，并将音频数据存储在其中
			with h5py.File(dst_file, 'w') as hf:
				hf.create_dataset(name='waveform', data=audio_array, dtype=np.int16)

			# if cnt > 1:
			# 	break




# for i, chunk in enumerate(chunks):
#     if len(chunk.shape) > 1:
#         chunk = chunk.T  # Swap axes if the audio is stereo.
#     soundfile.write(f'clips/example_{i}.wav', chunk, SAMPLE_RATE)  # Save sliced audio files with soundfile.

# soundfile.write(f'clips/res.wav', res, SAMPLE_RATE)

pack_to_hdf5()