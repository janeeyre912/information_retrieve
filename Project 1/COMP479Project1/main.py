import read_extract_reuters
import tokenize_text
import lowercase_text
import porter_stemmer
import remove_sw
from nltk.corpus import stopwords
# import nltk
# nltk.download('stopwords')

TOP_FILES_NUM = 5
ORIGINAL_FILE_PATH = 'reuters21578'
ORIGINAL_FILE_TYPE = '.sgm'
MODULE_FILE_TYPE = '.txt'
MODULE_ONE_FILE_PATH = 'mod1_data'
MODULE_TWO_FILE_PATH = 'mod2_data'
MODULE_THREE_FILE_PATH = 'mod3_data'
MODULE_FOUR_FILE_PATH = 'mod4_data'
MODULE_FIVE_FILE_PATH = 'mod5_data'


# First Module:  read the Reuter’s collection and extract the raw text of each article from the corpus
print("Starting read the Reuter's collection ...")
read_extract_reuters.output_file(ORIGINAL_FILE_PATH, 22, ORIGINAL_FILE_TYPE, MODULE_ONE_FILE_PATH)
print("Output the handled files in mod1_data directory.")

# Second Module: tokenize
print("Starting read the raw text files ...")
tokenize_text.output_file(MODULE_ONE_FILE_PATH, MODULE_FILE_TYPE, MODULE_TWO_FILE_PATH)
print("Output the handled files in mod2_data directory.")

# # Third Module: make all text lowercase
# print("Starting read the tokens files ...")
# lowercase_text.output_file(MODULE_TWO_FILE_PATH, MODULE_FILE_TYPE, MODULE_THREE_FILE_PATH)
# print("Output the handled files in mod3_data directory.")
#
# # Fourth Module: apply Porter stemmer
# print("Starting read the lowercase files ...")
# porter_stemmer.output_file(MODULE_THREE_FILE_PATH, MODULE_FILE_TYPE, MODULE_FOUR_FILE_PATH)
# print("Output the handled files in mod4_data directory.")
#
# # Fifth Module: remove stop words
# print("Starting read the stem files ...")
# # with open('stop_words.txt', 'r') as f:
# stop_words = set(stopwords.words("english"))
# remove_sw.output_file(MODULE_FOUR_FILE_PATH, MODULE_FILE_TYPE, MODULE_FIVE_FILE_PATH, stop_words)
# print("Output the handled files in mod5_data directory.")


