import os


def lowercase(path):
    text = open(path, "r").read()
    text = text.lower()
    print(f'read {path} successfully.')
    return text


def output_file(input_path, file_ends, output_path):
    file_list = os.listdir(input_path)
    file_list = [file for file in file_list if file.endswith(file_ends)]
    for file in file_list:
        lowercase_list = lowercase(input_path + "/" + file)
        filename = os.path.splitext(file)[0]
        with open(output_path + '/' + str(filename) + '.txt', "a") as f:
            f.writelines(lowercase_list)
            print(f'write to {output_path} successfully.')
