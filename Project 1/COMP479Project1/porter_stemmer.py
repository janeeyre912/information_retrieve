from nltk.stem import PorterStemmer
import os


def porter_stemmer(path):
    ps = PorterStemmer()
    with open(path, "r") as f:
        lines = f.read().splitlines()
    lines = [ps.stem(line) for line in lines]
    print(f'read {path} successfully.')
    return lines


def output_file(input_path,file_ends, output_path):
    file_list = os.listdir(input_path)
    file_list = [file for file in file_list if file.endswith(file_ends)]
    for file in file_list:
        stem_list = porter_stemmer(input_path + "/" + file)
        filename = os.path.splitext(file)[0]
        with open(output_path + '/' + str(filename) + '.txt', "a") as f:
            f.writelines("%s\n" % stem for stem in stem_list)
            print(f'write to {output_path} successfully.')

