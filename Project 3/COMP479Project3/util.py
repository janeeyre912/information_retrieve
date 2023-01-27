import os
import numpy as np
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')


def process_doc_pairs(path):
    """
    reads the document as a list of tokens and outputs term_documentsID pairs to a list
    :param count:  test for 10000 term-docID pairings
    :param path: the directory of the data
    :return: term_documentsID pairs
    """
    file_list = os.listdir(path)
    file_list = [file for file in file_list if file.endswith(".txt")]
    file_list.sort(key=lambda x: int(x[:-4]))
    term_docIDs = []
    for file in file_list:
        filename = os.path.splitext(file)[0]
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            term_docID = []
            docID = int(filename)
            for term in tokens_list:
                term_docID.append((term, docID))
            term_docIDs = term_docIDs + term_docID
    return term_docIDs


def process_doc(path):
    """
    reads the document as a list of tokens and outputs term_positions-list
    :param path: the directory of the data
    :return: dictionary {term : positions list} (hash table)
    """
    file_list = os.listdir(path)
    total_docs = len(file_list)
    file_list = [file for file in file_list if file.endswith(".txt")]
    file_list.sort(key=lambda x: int(x[:-4]))
    term_posList = {}
    for file in file_list:
        filename = os.path.splitext(file)[0]
        docID = int(filename)
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            for term in tokens_list:
                if term not in term_posList:
                    term_posList[term] = [docID]
                elif term in term_posList:
                    term_posList[term].append(int(filename))
    return term_posList


def process_doc_tf(path):
    """
    reads the document as a list of tokens and outputs term_positions-list
    :param path: the directory of the data
    :return: dictionary {term : positions list} (hash table), dictionary {docID : length}, int total number of documents
    """
    file_list = os.listdir(path)
    total_docs = len(file_list)
    file_list = [file for file in file_list if file.endswith(".txt")]
    term_posList = {}
    length_docs = {}
    for file in file_list:
        filename = os.path.splitext(file)[0]
        docID = int(filename)
        with open(path + "/" + file, "r") as f:
            tokens_list = f.read().splitlines()
            length_docs[docID] = len(tokens_list)
            for term in tokens_list:
                if term not in term_posList:
                    term_frequency_doc = 1
                    term_posList[term] = [[term_frequency_doc, docID]]
                elif term in term_posList:
                    if term_posList[term][-1][1] == docID:
                        term_frequency_doc = term_posList[term][-1][0]
                        term_posList[term][-1][0] = term_frequency_doc + 1
                    else:
                        term_frequency_doc = 1
                        term_posList[term].append([term_frequency_doc, docID])
    return term_posList, length_docs, total_docs


def remove_dup_did(term_plist):
    """
    removes the duplication of documents Ids in the dictionary
    :param term_plist: dictionary contains the term and related documents ID with duplication
    :return: dictionary contains the term and related documents ID without duplication
    """
    for k, v in term_plist.items():
        term_plist[k] = list(dict.fromkeys(v).keys())
    return term_plist


def sorted_pairs(pairs_list):
    """
    sorts the list of term_documentsID pairs
    :param pairs_list: unsorted term_documentsID pairs
    :return:sorted term_documentsID pairs
    """
    sorted_terms = sorted(pairs_list, key=lambda x: (x[1], x[0]))
    sorted_IDs = sorted(sorted_terms, key=lambda x: (x[0], x[1]))
    return sorted_IDs


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


def RSV(dft, N, Ld, Lave, tftd, tftq, k1=1.2, k3=0, b=0.75):
    """
    Calculates the RSVd of one term
    :param tftq: term frequency in query
    :param tftd: term frequency in document
    :param N: the total number of documents in the whole collection
    :param k1: parameter associated with term frequency in document
    :param k3: parameter associated with term frequency in query
    :param b: parameter associated with Ld and Lave
    :param Ld: number of tokens in document
    :param Lave: average document length in the whole collection
    :return: RSVd, score for ranked retrieve
    """
    return np.log(N / dft) * (((k1 + 1) * tftd) / (k1 * ((1 - b) + b * (Ld / Lave)) + tftd)) * (
            ((k3 + 1) * tftq) / (k3 + tftq))


def RSVd_ranked(query, dict_tokens, total_docs, length_docs):
    """
    calculates the related document's (contain at least one term in the query) scores by using RSV method
    :param query: a sentence or several terms are separated by space
    :param dict_tokens: the dictionary contains the information of  tokens' frequency and posting list
    :param total_docs: the numbers of documents in the collection
    :param length_docs: dictionary {docID : length}
    :return: ranked_list (docID, scores) sorted by scores (decreasing)
    """
    global ranked_list
    terms_list = tokenizer.tokenize(query)
    queries_dict = {term: terms_list.count(term) for term in terms_list}
    N = total_docs
    Lave = sum(length_docs.values())/total_docs
    ranked_dict = {}
    for term in queries_dict.keys():
        tftq = queries_dict[term]
        dft, posting_list_tf = query_term(term, dict_tokens)
        for tftd, docID in posting_list_tf:
            Ld = length_docs[docID]
            score_RSV = RSV(dft, N, Ld, Lave, tftd, tftq)
            if docID not in ranked_dict:
                ranked_dict[docID] = score_RSV
            else:
                ranked_dict[docID] = ranked_dict[docID] + score_RSV
        ranked_list = sorted(ranked_dict.items(), key=lambda x: x[1], reverse=True)
    return ranked_list


def and_retrieve(query, dict_tokens):
    """
    intersects all the posting lists of the terms in the query
    :param query:  a sentence or several terms are separated by space
    :param dict_tokens: the dictionary contains the information of  tokens' frequency and posting list
    :return: the intersection result of all the posting lists
    """
    temp_intersect_set = set()
    queries_list = tokenizer.tokenize(query)
    for i, term in enumerate(queries_list):
        _, temp = query_term(term, dict_tokens)
        temp_set = set(temp)
        if i == 0:
            temp_intersect_set = temp_set
        else:
            temp_intersect_set = temp_intersect_set & temp_set
    return list(temp_intersect_set)


def or_retrieve(query, dict_tokens):
    """
    unions all the posting lists of the terms in the query and ordered by how many keywords they contain
    :param query:a sentence or several terms are separated by space
    :param dict_tokens: the dictionary contains the information of tokens' frequency and posting list
    :return: the union and ordered result of all the posting lists
    """
    temp_union_list = []
    queries_list = tokenizer.tokenize(query)
    for term in queries_list:
        _, temp = query_term(term, dict_tokens)
        temp_union_list = temp_union_list + temp
    result = sorted(temp_union_list, key=temp_union_list.count, reverse=True)
    return list(dict.fromkeys(result))
