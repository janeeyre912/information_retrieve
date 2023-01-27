import util
import pickle


# Subproject II: Convert your indexer into a probabilistic search engine
term_posList = util.process_doc("data")
inverted_index = util.remove_dup_did(term_posList)
# term_posList, length_docs, total_docs = util.process_doc_tf("data")
# print(len(term_posList))

# # save the information of the dictionary to file
# with open('term_posList.txt', 'wb') as handle:
#     pickle.dump((term_posList, length_docs, total_docs), handle)

# load the data from the saved file
with open('term_posList.txt', 'rb') as handle:
    term_posList_tf, length_docs, total_docs = pickle.loads(handle.read())

# single query (a)
print("----Query processing for single term: four one-word challenge queries -----")
print(util.query_term("outlook", inverted_index))
print(util.query_term("zone", inverted_index))
print(util.query_term("week", inverted_index))

print(util.query_term("copper", inverted_index))
print(util.query_term("Samjens", inverted_index))
print(util.query_term("Carmark", inverted_index))
print(util.query_term("Bundesbank", inverted_index))

# Query processing for several keywords
queries = []
query_a = "Democrats' welfare and healthcare reform policies"
query_b = "Drug company bankruptcies"
query_c = "George Bush"

queries.append(query_a)
queries.append(query_b)
queries.append(query_c)

for query in queries:
    print("\nQUERY: ", query)
    # BM25 (b)
    RSVd_ranked_list = util.RSVd_ranked(query, term_posList_tf, total_docs, length_docs)
    print("\n----Query processing for several keywords for BM25 ranked-----")
    print("length of the ranked list", len(RSVd_ranked_list))
    print("Top 10 of the ranked list", RSVd_ranked_list[:10])
    print("All of the ranked list", RSVd_ranked_list)

    # (c) a multiple keyword query returning documents containing all the keywords (AND)
    # for unranked Boolean retrieval
    print("\n----Query processing for several keywords for AND retrieval-----")
    print(util.and_retrieve(query, inverted_index))

    # (d) a multiple keywords query returning documents containing at least one keyword (OR), where documents
    # are ordered by how many keywords they contain), for unranked Boolean retrieval
    print("\n----Query processing for several keywords for OR retrieval-----")
    or_retrieve_ordered_list = util.or_retrieve(query, inverted_index)
    print("length of the or retrieve ordered list", len(or_retrieve_ordered_list))
    print("Top 10 of the or retrieve ordered list", or_retrieve_ordered_list[:10])
    print("All of the or retrieve ordered list", or_retrieve_ordered_list)
