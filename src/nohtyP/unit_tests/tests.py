import unittest
# from nohtyP.lexer.identifier import TT
from nohtyP.global_utilities.decorators import *

@test
class TestLexerVars(unittest.TestCase):
    # lexobj = TT().REGEX
    def test_regex_attrs(self):
        self.assertEqual(super.lexobj.NOHTYP.UNKNOWN, ".+")
    def test_decorator(self):
        @api_level(1)
        def tested(): ...
        self.assertEqual(tested.__getattribute__("__NOHTYP_API_LEVEL"), "PUBLIC")

if __name__ == "__main__": unittest.main()
