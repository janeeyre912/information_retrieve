import os
from nltk.stem import PorterStemmer
from prettytable import PrettyTable

ps = PorterStemmer()


def process_doc(path):
    """
    reads the document as a list of tokens and outputs term_positions-list
    :param path: the directory of the data
    :return: dictionary {term : positions list} (hash table)
    """
    file_list = os.listdir(path)
    file_list = [file for file in file_list if file.endswith(".txt")]
    term_posList = {}
    for file in file_list:
        filename = os.path.splitext(file)[0]
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            for term in tokens_list:
                docID = int(filename)
                if term not in term_posList:
                    term_posList[term] = [docID]
                elif term in term_posList:
                    term_posList[term].append(int(filename))

    return term_posList


def remove_dup_sort_did(term_plist):
    """
    removes the duplication of documents Ids in the dictionary
    :param dict: dictionary contains the term and related documents ID with duplication
    :return: dictionary contains the term and related documents ID without duplication
    """
    for k, v in term_plist.items():
        term_plist[k] = sorted(set(v))
    return term_plist


def process_doc_pairs(path):
    """
    reads the document as a list of tokens and outputs term_documentsID pairs to a list
    :param path: the directory of the data
    :return: term_documentsID pairs
    """
    file_list = os.listdir(path)
    file_list = [file for file in file_list if file.endswith(".txt")]
    term_docIDs = []
    for file in file_list:
        filename = os.path.splitext(file)[0]
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            term_docID = [(term, int(filename)) for term in tokens_list]
            term_docIDs = term_docIDs + term_docID
    return term_docIDs


def read_from_path(path):
    """
    reads the document as a list of tokens and outputs term_documentsID pairs to a list
    :param path: the directory of the data
    :return: term_documentsID pairs
    """
    file_list = os.listdir(path)
    file_list = [file for file in file_list if file.endswith(".txt")]
    term_docIDs = []
    term_docID_positions = []
    for file in file_list:
        filename = os.path.splitext(file)[0]
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            term_docID = [(term, int(filename)) for term in tokens_list]
            term_docID_position = [(tokens_list[i], int(filename), i) for i in range(len(tokens_list))]
            term_docIDs = term_docIDs + term_docID
            term_docID_positions = term_docID_positions + term_docID_position
    return term_docIDs, term_docID_positions


def sorted_pairs(pairs_list):
    """
    sorts the list of term_documentsID pairs
    :param pairs_list: unsorted term_documentsID pairs
    :return:sorted term_documentsID pairs
    """
    sorted_terms = sorted(pairs_list, key=lambda x: (x[1], x[0]))
    sorted_IDs = sorted(sorted_terms, key=lambda x: (x[0], x[1]))
    return sorted_IDs


def sorted_triple(triple_list):
    """
    sorts the list of term_documentsID pairs
    :param triple_list: unsorted term_documentsID pairs
    :return:sorted term_documentsID pairs
    """
    sorted_terms = sorted(triple_list, key=lambda x: (x[1], x[2], x[0]))
    sorted_IDs = sorted(sorted_terms, key=lambda x: (x[0], x[2], x[1]))
    sorted_positions = sorted(sorted_IDs, key=lambda x: (x[0], x[1], x[2]))
    return sorted_positions


def write_pairs2file(pairs_list):
    """
    writes the list of term_documentsID pairs into a file
    :param pairs_list: the list of term_documentsID pairs
    """
    with open('F.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join('{} {}'.format(*tup) for tup in pairs_list))


def write_triples2file(triples_list):
    """
    writes the list of term_documentsID_position triples into a file
    :param triples_list: the list of term_documentsID_position triples
    """
    with open('F_triples.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join('{} {} {}'.format(*tup) for tup in triples_list))


def read_file2pairs(path):
    """
    reads the file including the information of term_documentsID to a pairs list
    :param path: the directory of the data
    :return: the list of term_documentsID pairs
    """
    result = []
    with open(path) as f:
        for i in f.readlines():
            temp = i.split(' ')
            result.append((str(temp[0]), int(temp[1])))
    return result


def read_file2triples(path):
    """
     reads the file including the information of term_documentsID_position to a triples list
    :param path: the directory of the data
    :return: the list of term_documentsID_position triples
    """
    result = []
    with open(path) as f:
        for i in f.readlines():
            temp = i.split(' ')
            result.append((str(temp[0]), int(temp[1]), int(temp[2])))
    return result


def remove_dup_pairs(pairs_list):
    """
    removes duplicates in pairs list
    :param pairs_list: term_documentsID pairs with duplicate
    :return:term_documentsID pairs without duplicate
    """
    return list(dict.fromkeys(pairs_list))


def create_posting_list(pairs_list):
    """
    creates inverted index, structure of return dictionary {term. (frequency, posting_list)}
    :param pairs_list: term_documentsID pairs without duplicate
    :return: dictionary of term associated with posting list
    """
    dict_tokens = {}
    for tuple_value in pairs_list:
        term = tuple_value[0]
        doc_ID = tuple_value[1]
        if term in dict_tokens.keys():
            frequency, posting_list = dict_tokens[term]
            count = frequency + 1
            posting_list.append(doc_ID)
            dict_tokens[term] = (count, posting_list)

        else:
            posting_list = [doc_ID]
            dict_tokens[term] = (1, posting_list)
    return dict_tokens


def query_term(term, dict_tokens):
    """
    implement a query processor for single term queries
    :param term: single term for query
    :param dict_tokens: the dictionary contains the information of  tokens' frequency and posting list
    :return: the posting list of the term
    """
    try:
        return len(dict_tokens[term]), dict_tokens[term]
    except KeyError:
        return None


def changed_rate(after, before):
    """
    calculates the changed rate after executing one step of lossy compression
    :param after: the size after executing one step of lossy compression
    :param before: the size before executing one step of lossy compression
    :return: the changed rate
    """
    return int((after - before) / before * 100)


def remove_stop_words_d(term_list, stopwords, num):
    """
    removes a certain num of stop words from the term_list
    :param term_list: terms of dictionary after case folding
    :param num: the number of stop words wants to remove
    :return: list after remove the certain amount of stopwords
    """
    stop_words = stopwords[:num]
    stop_words_rm = []
    for w in term_list:
        if w not in stop_words:
            stop_words_rm.append(w)
    return stop_words_rm


def remove_stop_words_npi(term_IDs_list, stopwords, num):
    """
     removes a certain num of stop words from the term_IDs_list
    :param term_IDs_list: terms of non-positional index after case folding
    :param num: the number of stop words wants to remove
    :return: list after remove the certain amount of stopwords
    """
    stop_words = stopwords[:num]
    stop_words_rm = []
    for w in term_IDs_list:
        if w[0] not in stop_words:
            stop_words_rm.append(w)
    return stop_words_rm


def stemming(term_list):
    """
    stems the term in the list
    :param term_list: the list of terms
    :return: the list of terms after porter stemming
    """
    ps = PorterStemmer()
    stem_list = []
    for w in term_list:
        stem_list.append(ps.stem(w))
    stem_terms = list(dict.fromkeys(stem_list))
    return stem_terms


def stemming_npi(term_list):
    """
    stems the term in the list
    :param term_list: the list of terms_documentID
    :return: the list of terms_documentID pairs after porter stemming for the terms
    """
    ps = PorterStemmer()
    stem_list = []
    for w in term_list:
        stem_list.append((ps.stem(w[0]), w[1]))
    stem_terms = list(dict.fromkeys(stem_list))
    return stem_terms


def stemming_pi(term_list):
    """
    stems the term in the list
    :param term_list: the list of terms_documentID_position
    :return: the list of terms_documentID_position triples after porter stemming for the terms
    """
    ps = PorterStemmer()
    stem_list = []
    for w in term_list:
        stem_list.append((ps.stem(w[0]), w[1], w[2]))
    stem_terms = list(dict.fromkeys(stem_list))
    return stem_terms


def get_stop_words(term_list):
    """
    gives certain term_list and finds the 150 common words of it and return
    :param term_list: the list of terms_documentID_position
    :return: the list of the 150 common words in it
    """
    unfiltered = list(dict.fromkeys(term_list))
    no_numbers = [item for item in unfiltered if not (item[0].isdigit() or item[0][0].isdigit())]
    lower_case = [(item[0].lower(), item[1]) for item in no_numbers]
    case_folding = list(dict.fromkeys(lower_case))
    dict_tok = create_posting_list(case_folding)
    dict_tok_top_150 = dict(sorted(dict_tok.items(), key=lambda x: x[1], reverse=True)[:150]).keys()
    return dict_tok_top_150


def calculate_effect_compression(term_list, stopwords):
    """
    prints out the effect of compression preprocessing for Reuters-21578 dictionary
    :param stopwords: top 150 common words
    :param term_list: the list of terms_documentID_position
    :return: print the table of the effect
    """
    # unfiltered information
    table = PrettyTable([" ", "size", "▲", "cml"])
    unfiltered = list(dict.fromkeys(term_list))  # remove the duplicate
    unfiltered_size = len(unfiltered)
    table.add_row(["unfiltered", unfiltered_size, " ", " "])

    # no_numbers information
    no_numbers = [item for item in unfiltered if not (item.isdigit() or item[0].isdigit())]
    no_numbers_size = len(no_numbers)
    changed_rate_list = []
    change_rate = changed_rate(no_numbers_size, unfiltered_size)
    changed_rate_list.append(change_rate)
    table.add_row(["no_numbers", no_numbers_size, change_rate, sum(changed_rate_list)])

    # case folding information
    lower_case = [item.lower() for item in no_numbers]
    case_folding = list(dict.fromkeys(lower_case))
    case_folding_size = len(case_folding)
    changed_rate_cf = changed_rate(case_folding_size, no_numbers_size)
    changed_rate_list.append(changed_rate_cf)
    table.add_row(["case folding", case_folding_size, changed_rate_cf, sum(changed_rate_list)])

    # 30 stopw's information
    remove_sw_30 = remove_stop_words_d(case_folding, stopwords, 30)
    remove_sw_30_size = len(remove_sw_30)
    changed_rate_sw_30 = changed_rate(remove_sw_30_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_30)
    table.add_row(["30 stopw's", remove_sw_30_size, changed_rate_sw_30, sum(changed_rate_list)])

    # 150 stopw's information
    changed_rate_list.pop()
    remove_sw_150 = remove_stop_words_d(case_folding, stopwords, 150)
    remove_sw_150_size = len(remove_sw_150)
    changed_rate_sw_150 = changed_rate(remove_sw_150_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_150)
    table.add_row(["150 stopw's", remove_sw_150_size, changed_rate_sw_150, sum(changed_rate_list)])

    # stemming information
    _stemming = stemming(remove_sw_150)
    stemming_size = len(_stemming)
    changed_rate_stemming = changed_rate(stemming_size, remove_sw_150_size)
    changed_rate_list.append(changed_rate_stemming)
    table.add_row(["stemming", stemming_size, changed_rate_stemming, sum(changed_rate_list)])
    print(table)


def calculate_effect_compression_2(term_list, stopwords):
    """
    prints out the effect of compression preprocessing for Reuters-21578 non-positional index
    :param stopwords: top 150 common words
    :param term_list: the list of terms_documentID_position
    :return: print the table of the effect
    """
    # unfiltered information
    table = PrettyTable([" ", "size", "▲", "cml"])
    unfiltered = list(dict.fromkeys(term_list))  # remove the duplicate
    unfiltered_size = len(unfiltered)
    table.add_row(["unfiltered", unfiltered_size, " ", " "])

    # no_numbers information
    no_numbers = [item for item in unfiltered if not (item[0].isdigit() or item[0][0].isdigit())]
    no_numbers_size = len(no_numbers)
    changed_rate_list = []
    change_rate = changed_rate(no_numbers_size, unfiltered_size)
    changed_rate_list.append(change_rate)
    table.add_row(["no_numbers", no_numbers_size, change_rate, sum(changed_rate_list)])

    # case folding information
    lower_case = [(item[0].lower(), item[1]) for item in no_numbers]
    case_folding = list(dict.fromkeys(lower_case))
    case_folding_size = len(case_folding)
    changed_rate_cf = changed_rate(case_folding_size, no_numbers_size)
    changed_rate_list.append(changed_rate_cf)
    table.add_row(["case folding", case_folding_size, changed_rate_cf, sum(changed_rate_list)])

    # 30 stopw's information
    remove_sw_30 = remove_stop_words_npi(case_folding, stopwords, 30)
    remove_sw_30_size = len(remove_sw_30)
    changed_rate_sw_30 = changed_rate(remove_sw_30_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_30)
    table.add_row(["30 stopw's", remove_sw_30_size, changed_rate_sw_30, sum(changed_rate_list)])

    # 150 stopw's information
    changed_rate_list.pop()
    remove_sw_150 = remove_stop_words_npi(case_folding, stopwords, 150)
    remove_sw_150_size = len(remove_sw_150)
    changed_rate_sw_150 = changed_rate(remove_sw_150_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_150)
    table.add_row(["150 stopw's", remove_sw_150_size, changed_rate_sw_150, sum(changed_rate_list)])

    # stemming information
    _stemming = stemming_npi(remove_sw_150)
    stemming_size = len(_stemming)
    changed_rate_stemming = changed_rate(stemming_size, remove_sw_150_size)
    changed_rate_list.append(changed_rate_stemming)
    table.add_row(["stemming", stemming_size, changed_rate_stemming, sum(changed_rate_list)])
    print(table)
    return _stemming


def calculate_effect_compression_3(term_list, stopwords):
    """
    prints out the effect of compression preprocessing for Reuters-21578 positional index
    :param stopwords: top 150 common words
    :param term_list: the list of terms_documentID_position
    :return: print the table of the effect
    """
    # unfiltered information
    table = PrettyTable([" ", "size", "▲", "cml"])
    unfiltered = list(dict.fromkeys(term_list))  # remove the duplicate
    unfiltered_size = len(unfiltered)
    table.add_row(["unfiltered", unfiltered_size, " ", " "])

    # no_numbers information
    no_numbers = [item for item in unfiltered if not (item[0].isdigit() or item[0][0].isdigit())]
    no_numbers_size = len(no_numbers)
    changed_rate_list = []
    change_rate = changed_rate(no_numbers_size, unfiltered_size)
    changed_rate_list.append(change_rate)
    table.add_row(["no_numbers", no_numbers_size, change_rate, sum(changed_rate_list)])

    # case folding information
    lower_case = [(item[0].lower(), item[1], item[2]) for item in no_numbers]
    case_folding = list(dict.fromkeys(lower_case))
    case_folding_size = len(case_folding)
    changed_rate_cf = changed_rate(case_folding_size, no_numbers_size)
    changed_rate_list.append(changed_rate_cf)
    table.add_row(["case folding", case_folding_size, changed_rate_cf, sum(changed_rate_list)])

    # 30 stopw's information
    remove_sw_30 = remove_stop_words_npi(case_folding, stopwords, 30)
    remove_sw_30_size = len(remove_sw_30)
    changed_rate_sw_30 = changed_rate(remove_sw_30_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_30)
    table.add_row(["30 stopw's", remove_sw_30_size, changed_rate_sw_30, sum(changed_rate_list)])

    # 150 stopw's information
    changed_rate_list.pop()
    remove_sw_150 = remove_stop_words_npi(case_folding, stopwords, 150)
    remove_sw_150_size = len(remove_sw_150)
    changed_rate_sw_150 = changed_rate(remove_sw_150_size, case_folding_size)
    changed_rate_list.append(changed_rate_sw_150)
    table.add_row(["150 stopw's", remove_sw_150_size, changed_rate_sw_150, sum(changed_rate_list)])

    # stemming information
    _stemming = stemming_pi(remove_sw_150)
    stemming_size = len(_stemming)
    changed_rate_stemming = changed_rate(stemming_size, remove_sw_150_size)
    changed_rate_list.append(changed_rate_stemming)
    table.add_row(["stemming", stemming_size, changed_rate_stemming, sum(changed_rate_list)])
    print(table)


def print_posting_list(term, term_list):
    print((query_term(ps.stem(term), term_list)[0],
           (sorted(query_term(ps.stem(term), term_list)[1]))))
