import unittest
# from nohtyP.lexer.identifier import TT
from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.tokenizer import *
from sys import argv

devmode:bool = False

# @test
# class TestLexerVars(unittest.TestCase):
#     # lexobj = TT().REGEX
#     def test_regex_attrs(self):
#         self.assertEqual(super.lexobj.NOHTYP.UNKNOWN, ".+")
#     def test_decorator(self):
#         @api_level(1)
#         def tested(): ...
#         self.assertEqual(tested.__getattribute__("__NOHTYP_API_LEVEL"), "PUBLIC")

@test
class Tokenizer(unittest.TestCase):
    class base:
        strings = [
            """sejejfoise () + *? f"ghjkl" r'''test2''' #? |= ]""",
            "# comment to newline chars\n\n(should appear separate)",
            '"""multiline bare string\nhere"""',
            "all_symbols + - == %= ! //= @ . , ; ({[]}) <- -> ~ $ehh *$o_ *type:",
            '"unterminated bare single quote string',
            '"""unterminated bare triple quote string',
            "fr'unterminated raw format string",
            "'''string to''''new string''''without space'''",
        ]
        results = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
        expected = [
            ['sejejfoise', '()', '+', '*?', 'f"ghjkl"', "r'''test2'''", '#?', '|=', ']'],
            ['# comment to newline chars', '(', 'should', 'appear', 'separate', ')'],
            ['"""multiline bare string\nhere"""'],
            ['all_symbols', '+', '-', '==', '%=', '!', '//=', '@', '.', ',', ';', '(', '{', '[', ']', '}', ')', '<-', '->', '~', '$ehh', '*$o_', '*type:'],
            ['"unterminated bare single quote string'],
            ['"""unterminated bare triple quote string'],
            ["fr'unterminated raw format string"],
            ["'''string to'''", "'new string'", "'''without space'''"],
        ]
    class valid_nums:
        nums = [
            "0",
            "7",
            "100_0000000",
            "0.0",
            ".5",
            "5.",
            "1_22.0",
            "3.5E-7",
            "1e7",
            "1e+7",
            "1e-7",
            "0b0",
            "0b1010",
            "0B1_0_1",
            "0o7",
            "0o755",
            "0O7_7_7",
            "0x0",
            "0x2e7",
            "0XFF",
            "0x1_e7",
            "0xdeadBEEF",
        ]
        results = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
        expected_tokens = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
    class invalid_nums:
        
        invalid_nums = [
            "",
            "_1",
            "1_",
            "1__0",
            "00",
            "01",
            "1..0",
            ".e1",
            "1e",
            "1e+",
            "1e-",
            "1e1_",
            "1._0",
            "1.00_",
            "1_.0",
            "0b2",
            "0b_1",
            "0b1_",
            "0o8",
            "0o_7",
            "0xG",
            "0x_1",
            "0x1__2",
            "0x1e+7",
            "0b1e7",
            "0o7e2",
            "3,14",
            "5.5.5",
        ]
        results = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
        expected_tokens = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
    class stress_test:
        strings = [
            "a + b + c + d + e + f + g + h + i + j + k + l",
            """a"b"c'd'e""",
            '''1"2"3''',
            '''f"1"f"2"''',
            "@@@###$$$%%%^^^&&&",

        ]
        results = [
            [],
            [],
            [],
            [],
            [],
        ]
        expected = [
            [ 'a', '+', 'b', '+', 'c', '+', 'd', '+', 'e', '+', 'f', '+', 'g', '+', 'h', '+', 'i', '+', 'j', '+', 'k', '+', 'l' ],
            [ 'a', '"b"', 'c', "'d'", 'e' ],
            [ '1', '"2"', '3' ],
            [ 'f', '"1"', 'f', '"2"' ],
            [ '@', '@', '@', '#', '##$$$%%%^^^&&&'],
        ]
    def basic(self):
        for i in range(len(self.base.strings)):
            self.base.results[i] = tokenize_str(self.base.strings[i])
            self.assertListEqual(self.base.expected[i], self.base.results[i])
        if devmode:
            for i in self.base.results: print(i)
    # def vnums(self):
    #     for i in range(len(self.valid_nums.nums)):
    #         self.results[i] = tokenize_str(self.valid_nums.nums[i])
    #         self.assertListEqual(self.valid_nums.expected_tokens[i], self.valid_nums.results[i])
    #     if devmode:
    #         for i in self.results: print(i)
    # def inums(self):
    #     for i in range(len(self.invalid_nums.nums)):
    #         self.results[i] = tokenize_str(self.invalid_nums.nums[i])
    #         self.assertListEqual(self.invalid_nums.expected_tokens[i], self.invalid_nums.results[i])
    #     if devmode:
    #         for i in self.results: print(i)
    def stress(self):
        for i in range(len(self.stress_test.strings)):
            self.stress_test.results[i] = tokenize_str(self.stress_test.strings[i])
            self.assertListEqual(self.stress_test.expected[i], self.stress_test.results[i])
        if devmode:
            for i in self.base.results: print(i)

if __name__ == "__main__":
    args = argv
    if len(argv) >= 2:
        if argv[1] == "dev":
            devmode = True
            args.pop(1)
    unittest.main(argv=args)
