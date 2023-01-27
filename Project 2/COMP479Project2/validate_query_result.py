import unittest
import util
from util import query_term


class TestModuleOne(unittest.TestCase):
    def test_query_term(self):
        """
        Tests that query term method returns, the list of documentID is correct
        traverses all the associated files to check the existence of the term
        """
        sorted_term_IDs = util.read_file2pairs("F.txt")
        unique_term_IDs = util.remove_dup_pairs(sorted_term_IDs)
        dict_tokens = util.create_posting_list(unique_term_IDs)
        term_list = ["outlook", "zone", "week"]

        validate = []
        for term in term_list:
            result = query_term(term, dict_tokens)
            for i in range(result[0]):
                filename = str(result[1][i]) + ".txt"
                with open("data/" + filename, "r") as f:
                    contents = f.read()
                    if term in contents:
                        _validate = True
                    else:
                        _validate = False
                        validate.append(_validate)
                        break
            validate.append(_validate)
        self.assertEqual(validate, [True, True, True])