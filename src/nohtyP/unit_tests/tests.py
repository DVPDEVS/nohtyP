import unittest
# from nohtyP.lexer.identifier import TT
# from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.tokenizer import funcs

# @test
# class TestLexerVars(unittest.TestCase):
#     # lexobj = TT().REGEX
#     def test_regex_attrs(self):
#         self.assertEqual(super.lexobj.NOHTYP.UNKNOWN, ".+")
#     def test_decorator(self):
#         @api_level(1)
#         def tested(): ...
#         self.assertEqual(tested.__getattribute__("__NOHTYP_API_LEVEL"), "PUBLIC")

class TestTokenizer(unittest.TestCase):
    test_string = "sejejfoise () + *? f\"ghjkl\" r'''test2''' #? |= ]"
    def test_tokenize(self):
        result = funcs.tokenize(self.test_string)
        print(result)
        self.assertListEqual(result, ['sjejfoise', '()', '+', '*?', 'f"ghjkl"', "r'''test2'''", '|=', ']'])

if __name__ == "__main__": unittest.main()
