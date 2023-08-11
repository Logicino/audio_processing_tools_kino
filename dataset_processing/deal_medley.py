import os
import yaml
import matplotlib.pyplot as plt

root_dir = '/Users/logickino/Downloads/Medley_DB'
metadata_dir = os.path.join(root_dir, 'Metadata')
medley_dir = os.path.join(root_dir, 'Medley')

print(metadata_dir)

def get_folder_names(folder_path):  # 获取所有文件夹的名字 196首歌曲
    folder_names = []
    for item in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, item)):
            folder_names.append(item)
    return folder_names

def find_matching_files(file_list, search_folder):  # 找到名字列表，目标文件夹里同样名字的文件
    matching_files = []
    for file_name in file_list:
        for root, dirs, files in os.walk(search_folder):
            for file in files:
                if file.startswith(file_name + '_'):
                    matching_files.append(os.path.join(root, file))
    return matching_files

# 把乐器下面存下来一个list

def main():
    file_list = get_folder_names(medley_dir)  # 这个是对的

    matching_files = find_matching_files(file_list, metadata_dir)  # 这里多了一个？？
    print('matching_files', matching_files)

    INSTRUMENTS = {}

    for index, song_name in enumerate(matching_files):
        with open(matching_files[index], 'r') as file:
            data = yaml.safe_load(file)

        # print(matching_files[index])  # xx.yaml
        # 提取instrument值
        if data['has_bleed'] == 'yes':
            continue

        instruments = []
        for stem_idx, stem in enumerate(data['stems'].values()):
            instrument = stem['instrument']

            if stem_idx < 9:
                stem_idx = stem_idx + 1
                idx_str = "0{}".format(stem_idx)
            else:
                stem_idx = stem_idx + 1
                idx_str = str(stem_idx)
            address = "/Users/logickino/Downloads/Medley_DB/Medley/{}/{}_STEMS/{}_STEM_{}.wav".format(file_list[index], file_list[index], file_list[index], file_list[index], idx_str)

            if instrument:
                instruments.append(instrument)
            if instrument in INSTRUMENTS:
                INSTRUMENTS[instrument].append(address)
            else:
                INSTRUMENTS[instrument] = [address]

    # 查看instruments里的
    # for instrument, song_list in INSTRUMENTS.items():
    #  print(instrument + ":", song_list)

    # 将乐器和对应的列表写入txt文件
    with open('instruments.txt', 'w') as file:
        for instrument, song_list in INSTRUMENTS.items():
            file.write(instrument + ": " + ", ".join(song_list) + "\n")

    # 计算每个乐器对应列表的长度
    instrument_lengths = {instrument: len(lst) for instrument, lst in INSTRUMENTS.items()}

    # 按照数量从大到小进行排序
    sorted_instruments = sorted(instrument_lengths, key=instrument_lengths.get, reverse=True)
    sorted_lengths = [instrument_lengths[instrument] for instrument in sorted_instruments]

    # 将乐器和对应的长度写入txt文件
    with open('instrument_lengths.txt', 'w') as file:
        for instrument, length in zip(sorted_instruments, sorted_lengths):
            file.write(f"{instrument}: {length}\n")

    # 绘制柱状图
    plt.bar(sorted_instruments, sorted_lengths)
    plt.xlabel('Instrument')
    plt.ylabel('Length')
    plt.title('Length of Lists for Each Instrument (Sorted)')
    plt.show()

main()