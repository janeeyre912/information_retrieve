import os

file_list = os.listdir("mod3_data")
file_list = [file for file in file_list if file.endswith(".txt")]
term_docIDs = []
for file in file_list:
    filename = os.path.splitext(file)[0]
    with open("mod3_data/" + file, "r") as f:
        tokens_list = f.read().splitlines()
        term_docID = [(term, int(filename)) for term in tokens_list]
        term_docIDs = term_docIDs + term_docID
# print(term_docs)
sorted_pairs = sorted(term_docIDs, key=lambda x: (x[1], x[0]))
remove_dup_pairs = list(dict.fromkeys(sorted_pairs))
print(remove_dup_pairs)
term_postings_list = [(term, []) for term in remove_dup_pairs]

for x in term_postings_list:
    for y in x:
        print(y)
