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
    strings = [
        "sejejfoise () + *? f\"ghjkl\" r'''test2''' #? |= ]",
        "# comment to newline chars\n\n(should appear separate)",
        '"""multiline bare string\nhere"""',
        "all_symbols + - == %= ! //= @ . , ; ({[]}) <- -> ~ $ehh *$o_ *type:",
        # '"unterminated bare string',
        # "fr'unterminated raw format string",
    ]
    results = [
        [],
        [],
        [],
        [],
        # [],
        # [],
    ]
    expected = [
        ['sejejfoise', '()', '+', '*?', 'f"ghjkl"', "r'''test2'''", '#?', '|=', ']'],
        ['# comment to newline chars', '(', 'should', 'appear', 'separate', ')'],
        ['"""multiline bare string\nhere"""'],
        ['all_symbols', '+', '-', '==', '%=', '!', '//=', '@', '.', ',', ';', '(', '{', '[', ']', '}', ')', '<-', '->', '~', '$ehh', '*$o_', '*type:'],
        # [],
        # [],
    ]
    def test_tokenize(self):
        for i in range(len(self.strings)):
            self.results[i] = funcs.tokenize(self.strings[i])
            self.assertListEqual(self.expected[i], self.results[i])
        # for i in self.results: print(i)

if __name__ == "__main__": unittest.main()
