import os

def dealURMP():
    urmp_path = '/Users/logickino/Downloads'
    list_dir = os.listdir(urmp_path)
    instrument_list = []
    for dir in list_dir:
        instruments = dir.split('_')[2:]
        for instrument in instruments:
            instrument_list.append(instrument)
    instrument_list = list(set(instrument_list))

    testdata_path = '/Users/logickino/Downloads'
    # for instrument in instrument_list:
    #     instrument_path = os.path.join(testdata_path, instrument)
    #     if not os.path.exists(instrument_path):
    #         os.makedirs(instrument_path)

    urmp_folder_list = [os.path.join(urmp_path, dir) for dir in list_dir]
    for urmp_folder in urmp_folder_list:
        file_list = os.listdir(urmp_folder)
        for file in file_list:
            if file.startswith('AuSep') or file.startswith('F0s'):
                file_instrument = file.split('_')[2]
                os.system("xcopy " + os.path.join(urmp_folder, file) + " " + os.path.join(testdata_path, file_instrument))



if __name__ == '__main__':
    dealURMP()