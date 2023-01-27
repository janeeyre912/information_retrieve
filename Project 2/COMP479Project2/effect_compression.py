import util
from nltk.stem import PorterStemmer

# reads file to a list of triples
sorted_term_IDs_pos = util.read_file2triples("F_triples.txt")

# finds the stopwords
stopwords = list(util.get_stop_words(sorted_term_IDs_pos))
print(stopwords)

# Subproject III: implement lossy dictionary compression, `recreate' Table 5.1
print("\n--------------------Effect of preprocessing for Reuters-21578 Dictionary--------------------")
word_types = [pair[0] for pair in sorted_term_IDs_pos]
util.calculate_effect_compression(word_types, stopwords)

print("\n--------------------Effect of preprocessing for Reuters-21578 non-positional index--------------------")
unique_term_IDs = [(term[0], term[1]) for term in sorted_term_IDs_pos]
dict_tokens = util.calculate_effect_compression_2(unique_term_IDs, stopwords)

print("\n--------------------Effect of preprocessing for Reuters-21578 positional index--------------------")
unique_term_IDs = [(term[0], term[1], term[2]) for term in sorted_term_IDs_pos]
util.calculate_effect_compression_3(unique_term_IDs, stopwords)

print("----------------------Query processing for single term After Compression---------------------------")

ps = PorterStemmer()
dict_tokens_after = util.create_posting_list(dict_tokens)
print(util.query_term(ps.stem("outlook"), dict_tokens_after))
print(util.query_term(ps.stem("zone"), dict_tokens_after))
print(util.query_term(ps.stem("week"), dict_tokens_after))

print("----Query processing for single term After Compression: four one-word challenge queries for Project 2-----")
util.print_posting_list("copper", dict_tokens_after)
util.print_posting_list("Samjens", dict_tokens_after)
util.print_posting_list("Carmark", dict_tokens_after)
util.print_posting_list("Bundesbank", dict_tokens_after)


