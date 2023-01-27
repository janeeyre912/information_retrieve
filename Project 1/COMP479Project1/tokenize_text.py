from nltk.tokenize import RegexpTokenizer
import os


def tokenize(path):
    text = open(path, "r").read()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    print(f'read {path} successfully.')
    return tokens


def output_file(input_path, file_ends, output_path):
    file_list = os.listdir(input_path)
    file_list = [file for file in file_list if file.endswith(file_ends)]
    for file in file_list:
        tokens_list = tokenize(input_path + "/" + file)
        filename = os.path.splitext(file)[0]
        with open(output_path + '/' + str(filename) + '.txt', "a") as f:
            f.writelines("%s\n" % token for token in tokens_list)
            print(f'write to {output_path} successfully.')

