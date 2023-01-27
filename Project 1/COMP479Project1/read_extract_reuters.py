import os


def read_split_article(path):
    reuters = []
    article = ''
    extract = False
    f = open(path, 'r', encoding="utf8", errors='ignore')
    for line in f.readlines():
        if line.startswith("<REUTERS"):
            extract = True
        if extract:
            article = article + line
        if line.startswith("</REUTERS>"):
            reuters.append(article)
            extract = False
            article = ''
    print(f'read {path} successfully.')
    f.close()
    return reuters


def extract_article_text(article):
    index_newID_start = article.find('NEWID="') + len('NEWID="')
    index_newID_end = article.find('">')
    article_ID = article[index_newID_start:index_newID_end]
    if article.find('<TITLE>') == -1:
        article_title = ""
    else:
        index_title_start = article.find('<TITLE>') + len('<TITLE>')
        index_title_end = article.find('</TITLE>')
        article_title = article[index_title_start:index_title_end]
    if article.find('<BODY>') == -1:
        article_body = article_title
    else:
        index_body_start = article.find('<BODY>') + len('<BODY>')
        # print(index_body_start)
        index_body_end = article.find('\n&#3;</BODY>')
        # print(index_body_end)
        article_body = article[index_body_start:index_body_end]
        article_body = article_body[:article_body.rfind('\n')]
    # article_text = article_ID + "\n" +  article_title + "\n" + article_body + "\n"
    return article_ID, article_body


def output_file(input_path, file_num, file_ends, output_path):
    count = 0
    # count_article = 50
    while count < file_num:
        file_list = os.listdir(input_path)
        file_list = [file for file in file_list if file.endswith(file_ends)]
        for file in file_list[:file_num]:
            articles_text = ""
            reuters_list = read_split_article(input_path + "/" + file)
            for reuter in reuters_list:
                article_ID, article_body = extract_article_text(reuter)
                # articles_text = articles_text + extract_article_text(reuter)
                with open(output_path + '/' + str(article_ID) + '.txt', "a") as f:
                    f.write(article_body)
                    print(f'write to {output_path} successfully.')
                count = count + 1

