import h5py
import numpy as np

train_hdf5_path = "/Users/logickino/Downloads/Medley_DB/Medley_h5/SynFX/AimeeNorwich_Flying_STEM_02._TRAIN_shift_pitch_-1.h5"

def int16_to_float32(x):
	return (x / 32767.).astype(np.float32)

hf = h5py.File(train_hdf5_path, 'r')
data = {'shift_waveform': int16_to_float32(hf['shift_waveform'][:])[None, :],
        'shift_dense_waveform': int16_to_float32(hf['shift_dense_waveform'][:])[None, :]}
# 'frame_roll': hf['frame_roll'][:].astype(np.int)}

shift_pitch = sample_rng.randint(0, POS_SHIFT_SEMITONE) - SHIFT_SEMITONE
hf = load_file(pos, other_nid, shift_pitch)
shift_dense_waveform = hf['shift_dense_waveform']
st = sample_rng.randint(0, shift_dense_waveform.shape[1] - SAMPLE_DURATION)
query_waveform = shift_dense_waveform[:, st: st + SAMPLE_DURATION].copy()
