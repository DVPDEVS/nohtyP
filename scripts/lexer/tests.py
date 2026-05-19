import unittest
from lex_tt import TT

class TestLexerVars(unittest.TestCase):
    lexobj = TT().REGEX
    def test_regex_attrs(self):
        self.assertEqual(super.lexobj.NOHTYP.UNKNOWN, ".+")

if __name__ == "__main__": unittest.main()
