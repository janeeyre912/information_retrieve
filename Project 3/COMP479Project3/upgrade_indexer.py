import util
import time

# Subproject I: Compare timing of inspired procedure with the naive indexer(for 10000 term_docID pairing)
start_time1 = time.time()
# Reads documents and outputs term_documentID pairs
term_IDs = util.process_doc_pairs("test_time_data")
print("length of term_IDs:", len(term_IDs))
# sorts the list of term_documentsID pairs
sorted_term_IDs = util.sorted_pairs(term_IDs)

# removes duplicates in pairs list
unique_term_IDs = util.remove_dup_pairs(sorted_term_IDs)

# creates inverted index, structure of return dictionary {term. (frequency, posting_list)}
dict_tokens = util.create_posting_list(unique_term_IDs)
print("Length of dictionary: ", len(dict_tokens))
print("naive index ----- %s seconds ----" % (time.time() - start_time1))

start_time2 = time.time()
term_posList = util.process_doc("test_time_data")

inverted_index = util.remove_dup_did(term_posList)
print("Length of dictionary: ", len(inverted_index))
# print(inverted_index)
print("upgrade by SPIMI inspired procedure ----- %s seconds ----" % (time.time() - start_time2))

# # Subproject I : Upgrade naive indexer by SPIMI inspired procedure
term_posList = util.process_doc("data")

inverted_index = util.remove_dup_did(term_posList)
print(len(inverted_index))

# Subproject II: single term query processing
print("----------------------Query processing for single term---------------------------")
print(util.query_term("outlook", inverted_index))
print(util.query_term("zone", inverted_index))
print(util.query_term("week", inverted_index))

print("----Query processing for single term: four one-word challenge queries for Project 2-----")
print(util.query_term("copper", inverted_index))
print(util.query_term("Samjens", inverted_index))
print(util.query_term("Carmark", inverted_index))
print(util.query_term("Bundesbank", inverted_index))
