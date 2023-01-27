import os


def remove_stop_words(path, words):
    with open(path, "r") as f:
        lines = f.read().splitlines()
        start_len = len(lines)
    lines = [line for line in lines if not line in words]
    end_len = len(lines)
    print(f'read {path} successfully.')
    print(f'remove {start_len - end_len} words')
    return lines


def output_file(input_path, file_ends, output_path, words):
    file_list = os.listdir(input_path)
    file_list = [file for file in file_list if file.endswith(file_ends)]
    for file in file_list:
        stem_list = remove_stop_words(input_path + "/" + file, words)
        filename = os.path.splitext(file)[0]
        with open(output_path + '/' + str(filename) + '.txt', "a") as f:
            f.writelines("%s\n" % stem for stem in stem_list)
            print(f'write to {output_path} successfully.')
