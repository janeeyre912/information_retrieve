import unittest

from read_extract_reuters import read_split_article, extract_article_text
from tokenize_text import tokenize
from lowercase_text import lowercase
from porter_stemmer import porter_stemmer
from remove_sw import remove_stop_words


class TestModuleOne(unittest.TestCase):
    def test_split_article(self):
        """
        Test that it can separate the whole text into each article
        """
        path_0 = "reuters21578/reut2-000.sgm"
        path_21 = "reuters21578/reut2-021.sgm"
        result = read_split_article(path_0)
        self.assertEqual(len(result), 1000)
        result = read_split_article(path_21)
        self.assertEqual(len(result), 578)

    def test_extract_article(self):
        """
        Test that it can extract the body content for each article
        """
        article_2 = """ <REUTERS TOPICS="YES" LEWISSPLIT="TRAIN" CGISPLIT="TRAINING-SET" OLDID="16319" NEWID="999">
<DATE> 3-MAR-1987 09:16:02.85</DATE>
<TOPICS><D>money-fx</D><D>interest</D></TOPICS>
<PLACES><D>uk</D></PLACES>
<PEOPLE></PEOPLE>
<ORGS></ORGS>
<EXCHANGES></EXCHANGES>
<COMPANIES></COMPANIES>
<UNKNOWN> 
&#5;&#5;&#5;RM
&#22;&#22;&#1;f0277&#31;reute
b f BC-U.K.-MONEY-MARKET-SHO   03-03 0049</UNKNOWN>
<TEXT>&#2;
<TITLE>U.K. MONEY MARKET SHORTAGE FORECAST REVISED DOWN</TITLE>
<DATELINE>    LONDON, March 3 - </DATELINE><BODY>The Bank of England said it had revised
its forecast of the shortage in the money market down to 450
mln stg before taking account of its morning operations. At
noon the bank had estimated the shortfall at 500 mln stg.
 REUTER
&#3;</BODY></TEXT>
</REUTERS>"""
        result = extract_article_text(article_2)
        expected_result = """999
U.K. MONEY MARKET SHORTAGE FORECAST REVISED DOWN
The Bank of England said it had revised
its forecast of the shortage in the money market down to 450
mln stg before taking account of its morning operations. At
noon the bank had estimated the shortfall at 500 mln stg.
"""
        self.assertEqual(result, expected_result)

    if __name__ == '__main__':
        unittest.main()


class TestModuleTwo(unittest.TestCase):
    def test_tokenize(self):
        """
        Test that it can tokenize the text to single word and punctuation
        """
        path_0 = "mod1_data/raw_text-0.txt"
        result = tokenize(path_0)
        self.assertEqual(result[1], 'BAHIA')

    if __name__ == '__main__':
        unittest.main()


class TestModuleThree(unittest.TestCase):
    def test_lowercase(self):
        """
        Test that it can lowercase the word
        """
        path_0 = "mod2_data/tokens-0.txt"
        result = lowercase(path_0)
        self.assertEqual(result[2:2 + len('bahia')], 'bahia')

    if __name__ == '__main__':
        unittest.main()


class TestModuleFour(unittest.TestCase):
    def test_porter_stemmer(self):
        """
        Test that it can porter stemmer the word
        """
        path_0 = "mod3_data/lowercase-0.txt"
        result = porter_stemmer(path_0)
        self.assertEqual(result[1], 'bahia')
        self.assertEqual(result[5], 'continu')

    if __name__ == '__main__':
        unittest.main()


class TestModuleFive(unittest.TestCase):
    def test_remove_stop_words(self):
        """
        Test that it can porter stemmer the word
        """
        path_0 = "mod4_data/stem-0.txt"
        result = remove_stop_words(path_0, 'because')
        without = 'because' in result
        self.assertEqual(without, False)

    if __name__ == '__main__':
        unittest.main()