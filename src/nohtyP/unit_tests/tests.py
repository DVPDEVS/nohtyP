import unittest
# from nohtyP.lexer.identifier import TT
from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.tokenizer import *
from sys import argv

verbmode:bool = False
quietmode: bool = False
showmode: bool = False

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
		results = [[] for _ in strings]
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
		ints = [
			# Integers (decimal)
			"+0", "+1", "+123", "0", "1", "123", "-0", "-1", "-123",
			# Integers with underscores
			"+1_000", "1_000", "-1_000", "123_456_789",
			# Binary
			"+0b0", "+0b1010", "0b0", "0b1010", "-0b0", "-0b1010", "0b1010_1100",
			# Octal
			"+0o0", "+0o755", "0o0", "0o755", "-0o0", "-0o755", "0o7_5_5",
			# Hex
			"+0x0", "+0xFF", "0x0", "0xFF", "-0x0", "-0xFF", "0xDEAD_BEEF",
		]
		floats = [
			# Floats with leading integer part
			"+0.0", "+1.0", "+123.456", "0.0", "1.0", "123.456", "-0.0", "-1.0", "-123.456",
			# Floats without leading integer part
			"+.0", "+.5", ".0", ".5", "-.0", "-.5",
			# Floats with trailing decimal point
			"+1.", "+123.", "1.", "123.", "-1.", "-123.",
			# Floats with underscores
			"1_000.000_001", ".123_456", "123_456.",
		]
		scientifics = [
			# Scientific notation (integer mantissa)
			"+1e0", "+1e1", "+1e-1", "+1E+1", "1e0", "1e1", "1e-1", "1E+1", "-1e0", "-1e1", "-1e-1", "-1E+1",
			# Scientific notation (float mantissa)
			"+1.5e2", "+.5e2", "+1.e2", "1.5e2", ".5e2", "1.e2", "-1.5e2", "-.5e2", "-1.e2",
			# Scientific notation with underscores
			"1_000e3", "1.234_567e8", "1_2_3.4_5_6E-7",
		]
		results_ints = [ [] for _ in ints ] 
		results_floats = [ [] for _ in floats ] 
		results_scis = [ [] for _ in scientifics ] 
		expected_ints = [
			[ "+", "0", ],
			[ "+", "1", ],
			[ "+", "123", ],
			[ "0", ],
			[ "1", ],
			[ "123", ],
			[ "-", "0", ],
			[ "-", "1", ],
			[ "-", "123", ],
			[ "+", "1_000", ],
			[ "1_000", ],
			[ "-", "1_000", ],
			[ "123_456_789", ],
			[ "+", "0b0", ],
			[ "+", "0b1010", ],
			[ "0b0", ],
			[ "0b1010", ],
			[ "-", "0b0", ],
			[ "-", "0b1010", ],
			[ "0b1010_1100", ],
			[ "+", "0o0", ],
			[ "+", "0o755", ],
			[ "0o0", ],
			[ "0o755", ],
			[ "-", "0o0", ],
			[ "-", "0o755", ],
			[ "0o7_5_5", ],
			[ "+", "0x0", ],
			[ "+", "0xFF", ],
			[ "0x0", ],
			[ "0xFF", ],
			[ "-", "0x0", ],
			[ "-", "0xFF", ],
			[ "0xDEAD_BEEF", ],
		]
		expected_floats = [
			[ "+", "0.0", ],
			[ "+", "1.0", ],
			[ "+", "123.456", ],
			[ "0.0", ],
			[ "1.0", ],
			[ "123.456", ],
			[ "-", "0.0", ],
			[ "-", "1.0", ],
			[ "-", "123.456", ],
			[ "+", ".", "0", ],
			[ "+", ".", "5", ],
			[ ".", "0", ],
			[ ".", "5", ],
			[ "-", ".", "0", ],
			[ "-", ".", "5", ],
			[ "+", "1.", ],
			[ "+", "123.", ],
			[ "1.", ],
			[ "123.", ],
			[ "-", "1.", ],
			[ "-", "123.", ],
			[ "1_000.000_001", ],
			[ ".", "123_456", ],
			[ "123_456.", ],
		]
		expected_scientifics = [
			[ "+", "1e0", ],
			[ "+", "1e1", ],
			[ "+", "1e-1", ],
			[ "+", "1E+1", ],
			[ "1e0", ],
			[ "1e1", ],
			[ "1e-1", ],
			[ "1E+1", ],
			[ "-", "1e0", ],
			[ "-", "1e1", ],
			[ "-", "1e-1", ],
			[ "-", "1E+1", ],
			[ "+", "1.5e2", ],
			[ "+", ".", "5e2", ],
			[ "+", "1.e2", ],
			[ "1.5e2", ],
			[ ".", "5e2", ],
			[ "1.e2", ],
			[ "-", "1.5e2", ],
			[ "-", ".", "5e2", ],
			[ "-", "1.e2", ],
			[ "1_000e3", ],
			[ "1.234_567e8", ],
			[ "1_2_3.4_5_6E-7", ],
		]
	class invalid_nums:
		ints = [
			# Binary
			"0b", "+0b", "-0b", "0b2", "0b102",
			# Octal
			"0o", "+0o", "-0o", "0o8", "0o9", "0o789",
			# Hex
			"0x", "+0x", "-0x", "0xG", "0xFG",
			# Mixed bases
			"0b0x1", "0o0x1", "0x0o1", "0x0g1",
		]
		floats = [
			# Decimal point only
			".", "+.", "-.",
			# Multiple decimal points
			"1.2.3", "..5", "1..", "..",
			# Bad underscore placement
			"_1.0", "1.0_", "1_.0", "1._0", "1._", "._5", "._0", "1__000.0", "1.0__0",
			# Invalid signs
			"++1.0", "--1.0", "+-1.0", "-+1.0",
			# Non-decimal floats
			"0x1.5", "0b1.0", "0o7.5",
			# Garbage suffixes
			"1.0f", "1.0d", "1.0abc",
		]
		scientifics = [
			# Missing exponent
			"1e", "1E", "+1e", "-1e",
			# Missing exponent digits
			"1e+", "1e-", "1E+", "1E-",
			# Missing mantissa
			"e10", "E10", "+e10", "-e10",
			# Broken decimal/exponent combinations
			".e10", "1.e", "1.5e+", "1.5e-",
			# Multiple exponents
			"1e1e2", "1E1E2", "1e+1e2",
			# Bad underscores
			"_1e10", "1_e10", "1e_10", "1e10_", "1__0e10", "1e1__0", "1.2_e3", "1._2e3",
			# Invalid exponent sign usage
			"1e++2", "1e--2", "1e+-2", "1e-+2",
			# Invalid exponent digits
			"1eA", "1e1A", "1e2.3",
			# Hex/bin/oct with exponent
			"0x1e2", "0b1e2", "0o7e2",
		]
		results_ints = [ [] for _ in ints ] 
		results_floats = [ [] for _ in floats ] 
		results_scis = [ [] for _ in scientifics ] 
		expected_ints = [
			[ "0b", ], 
			[ "+", "0b", ], 
			[ "-", "0b", ], 
			[ "0b", "2", ], 
			[ "0b10", "2", ], 
			[ "0o", ], 
			[ "+", "0o", ], 
			[ "-", "0o", ], 
			[ "0o", "8", ], 
			[ "0o", "9", ], 
			[ "0o7", "89", ], 
			[ "0x", ], 
			[ "+", "0x", ], 
			[ "-", "0x", ], 
			[ "0x", "G" ], 
			[ "0xF", "G" ], 
			[ "0b0", "x1" ], 
			[ "0o0", "x1" ],
			[ "0x0", "o1", ], 
			[ "0x0", "g1", ],
		]
		expected_floats = [
			[ '.', ], 
			[ '+', '.', ], 
			[ '-', '.', ], 
			[ '1.2', '.', '3', ], 
			[ '.', '.', '5', ], 
			[ '1.', '.', ], 
			[ '.', '.',  ], 
			[ "_1", ".", "0", ], 
			[ "1.0_", ], 
			[ "1_.0", ], 
			[ "1._0", ], 
			[ "1._", ], 
			[ ".", "_5", ], 
			[ ".", "_0", ], 
			[ "1__000.0", ], 
			[ "1.0__0", ], 
			[ "+", "+", "1.0", ], 
			[ "-", "-", "1.0", ], 
			[ "+", "-", "1.0", ], 
			[ "-", "+", "1.0", ], 
			[ "0x1", ".", "5", ], 
			[ "0b1", ".", "0", ], 
			[ "0o7", ".", "5", ], 
			[ "1.0", "f", ], 
			[ "1.0", "d", ], 
			[ "1.0", "abc", ], 
		]
		expected_scientifics = [
			[ "1e", ],
            [ "1E", ],
            [ "+", "1e", ],
            [ "-", "1e", ],
			[ "1e+", ],
            [ "1e-", ],
            [ "1E+", ],
            [ "1E-", ],
			[ "e10", ],
            [ "E10", ],
            [ "+", "e10", ],
            [ "-", "e10", ],
			[ ".", "e10", ],
            [ "1.e", ],
            [ "1.5e+", ],
            [ "1.5e-", ],
			[ "1e1", "e2", ],
            [ "1E1", "E2", ],
            [ "1e+1", "e2", ],
			[ "_1e10", ],
            [ "1_e10", ],
            [ "1e_10", ],
            [ "1e10_", ],
            [ "1__0e10", ],
            [ "1e1__0", ],
            [ "1.2_e3", ],
            [ "1._2e3", ],
			[ "1e+", "+", "2", ],
            [ "1e-", "-", "2", ],
            [ "1e+", "-", "2", ],
            [ "1e-", "+", "2", ],
			[ "1e", "A", ],
            [ "1e1", "A", ],
            [ "1e2", ".", "3", ],
			[ "0x1e2", ],
            [ "0b1", "e2", ],
            [ "0o7", "e2", ],
		]
	class stress_test:
		strings = [
			"a + b + c + d + e + f + g + h + i + j + k + l",
			"""a"b"c'd'e""",
			'1"2"3',
			'f"1"f"2"',
			"@@@$$$%%%^^^&&&",
			"foo...bar",
			".leading . .trailing.",
			",,,;;;:::",
			"()[]{}<>",
			"\"quoted\"",
			"'single-quoted'",
			'''"mix'ed"''',
			"""a""b''c""",
			"x=y+z-1*2/3",
			"1,234,567.89",
			"0xFF 0b1010 0o755",
			"3.14159e-10",
			"NaN INF -INF",
			"🙂😂🔥💯",
			"🏳️‍⚧️🏳️‍🌈🇳🇴",
			"汉字かなカナ한글",
			"é é ê ë",
			"a\u200bb",
			"a\u00a0b",
			"word\u2060word",
			"\u202eabc",
			"\ufeffbom",
			"<< >> == != <= >= && || :: -> =>",
			"---___+++***",
			"123abc abc123",
			"_leading trailing_",
			'f"1"f"2"f"3"',
			'1"2"3"4"5',
			'''abc'def"ghi'jkl''',
		]
		results = [[] for _ in strings]
		expected = [
			[ 'a', '+', 'b', '+', 'c', '+', 'd', '+', 'e', '+', 'f', '+', 'g', '+', 'h', '+', 'i', '+', 'j', '+', 'k', '+', 'l' ],
			[ 'a', '"b"', 'c', "'d'", 'e' ],
			[ '1', '"2"', '3' ],
			[ 'f"1"', 'f"2"' ],
			[ '@', '@', '@', '$', '$', '$', '%', '%', '%', '^', '^', '^', '&', '&', '&' ],
			[ 'foo', '.', '.', '.', 'bar' ],
			[ '.', 'leading', '.', '.', 'trailing', '.' ],
			[ ',', ',', ',', ';', ';', ';', ':', ':', ':' ],
			[ '()', '[', ']', '{', '}', '<', '>' ],
			[ '"quoted"' ],
			[ "'single-quoted'" ],
			[ '"mix\'ed"' ],
			[ 'a', '""', "b''", 'c' ],
			[ 'x', '=', 'y', '+', 'z', '-', '1', '*', '2', '/', '3' ],
			[ '1', ',', '234', ',', '567.89' ],
			[ '0xFF', '0b1010', '0o755' ],
			[ '3.14159e-10' ],
			[ 'NaN', 'INF', '-', 'INF' ],
			[ '¤__NOHTYP_NOT_TOKENIZABLE__¤(🙂)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(😂)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(🔥)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(💯)' ],
			[ '¤__NOHTYP_NOT_TOKENIZABLE__¤(🏳)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\ufe0f)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\u200d)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(⚧)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\ufe0f)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(🏳)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\ufe0f)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\u200d)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(🌈)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(🇳)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(🇴)' ],
			#? actually correct for the unicode grapheme cluster. see below:
			#* | Code point | Unicode name                               |
			#* | ---------- | ------------------------------------------ |
			#* | 🏳         | U+1F3F3 WAVING FLAG                        |
			#* | ️          | U+FE0F VARIATION SELECTOR-16               |
			#* | \\u200d    | U+200D ZERO WIDTH JOINER                   |
			#* | ⚧          | U+26A7 TRANSGENDER SYMBOL                  |
			#* | ️          | U+FE0F VARIATION SELECTOR-16               |
			#* | 🏳         | U+1F3F3 WAVING FLAG                        |
			#* | ️          | U+FE0F VARIATION SELECTOR-16               |
			#* | \\u200d    | U+200D ZERO WIDTH JOINER                   |
			#* | 🌈         | U+1F308 RAINBOW                            |
			#* | 🇳         | U+1F1F3 REGIONAL INDICATOR SYMBOL LETTER N |
			#* | 🇴         | U+1F1F4 REGIONAL INDICATOR SYMBOL LETTER O |
			[ '¤__NOHTYP_NOT_TOKENIZABLE__¤(汉)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(字)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(か)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(な)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(カ)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(ナ)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(한)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(글)' ],
			[ 'e', '¤__NOHTYP_NOT_TOKENIZABLE__¤(́)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(é)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(ê)', '¤__NOHTYP_NOT_TOKENIZABLE__¤(ë)' ],
			[ 'a', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\u200b)', 'b' ],
			[ 'a', 'b' ], #? \u00a0 is known whitespace.
			[ 'word', '¤__NOHTYP_NOT_TOKENIZABLE__¤(\u2060)', 'word' ],
			[ '¤__NOHTYP_NOT_TOKENIZABLE__¤(\u202e)', 'abc' ],
			[ '¤__NOHTYP_NOT_TOKENIZABLE__¤(\ufeff)', 'bom' ],
			[ '<<', '>>', '==', '!=', '<=', '>=', '&', '&', '|', '|', ':', ':', '->', '=', '>' ],
			[ '-', '-', '-', '___', '+', '+', '+', '**', '**', '*' ],
			[ '123', 'abc', 'abc123' ],
			[ '_leading', 'trailing_' ],
			[ 'f"1"', 'f"2"', 'f"3"' ],
			[ '1', '"2"', '3', '"4"', '5' ],
			[ 'abc', """'def"ghi'""", 'jkl' ],
		]
	def basic(self):
		for i in range(len(self.base.strings)):
			self.base.results[i] = tokenize_str(self.base.strings[i])
			self.assertListEqual(self.base.expected[i], self.base.results[i])
		if showmode:
			if verbmode: print("\n")
			for i in self.base.results: print(i)
	def vnums(self):
		def ints():
			for i in range(len(self.valid_nums.ints)):
				self.valid_nums.results_ints[i] = tokenize_str(self.valid_nums.ints[i])
				self.assertListEqual(self.valid_nums.expected_ints[i], self.valid_nums.results_ints[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.valid_nums.results_ints: print(i)
		def floats():
			for i in range(len(self.valid_nums.floats)):
				self.valid_nums.results_floats[i] = tokenize_str(self.valid_nums.floats[i])
				self.assertListEqual(self.valid_nums.expected_floats[i], self.valid_nums.results_floats[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.valid_nums.results_floats: print(i)
		def scientifics():
			for i in range(len(self.valid_nums.scientifics)):
				self.valid_nums.results_scis[i] = tokenize_str(self.valid_nums.scientifics[i])
				self.assertListEqual(self.valid_nums.expected_scientifics[i], self.valid_nums.results_scis[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.valid_nums.results_scis: print(i)
		ints(); floats(); scientifics() 
	def inums(self):
		def ints():
			for i in range(len(self.invalid_nums.ints)):
				self.invalid_nums.results_ints[i] = tokenize_str(self.invalid_nums.ints[i])
				self.assertListEqual(self.invalid_nums.expected_ints[i], self.invalid_nums.results_ints[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.invalid_nums.results_ints: print(i)
		def floats():
			for i in range(len(self.invalid_nums.floats)):
				self.invalid_nums.results_floats[i] = tokenize_str(self.invalid_nums.floats[i])
				self.assertListEqual(self.invalid_nums.expected_floats[i], self.invalid_nums.results_floats[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.invalid_nums.results_floats: print(i)
		def scientifics():
			for i in range(len(self.invalid_nums.scientifics)):
				self.invalid_nums.results_scis[i] = tokenize_str(self.invalid_nums.scientifics[i])
				self.assertListEqual(self.invalid_nums.expected_scientifics[i], self.invalid_nums.results_scis[i])
			if showmode:
				if verbmode: print("\n")
				for i in self.invalid_nums.results_scis: print(i)
		ints(); floats(); scientifics() 
	def stress(self):
		for i in range(len(self.stress_test.strings)):
			self.stress_test.results[i] = tokenize_str(self.stress_test.strings[i])
			self.assertListEqual(self.stress_test.expected[i], self.stress_test.results[i])
		if showmode:
			if verbmode: print("\n")
			for i in self.stress_test.results: print(i)

if __name__ == "__main__":
	args = argv
	if len(args) >= 2:
		if args[1] == "v":
			verbmode = True
			showmode = True
			args.pop(1)
		if args[1] == "q":
			quietmode = True
			args.pop(1)
		if args[1] == "s":
			showmode = True
			args.pop(1)
		# This does in fact mean you can do `python -m nohtyP.unit_tests.tests v q s Tokenizer.stress` and itll become quiet + show
	v_flag = 0 if quietmode else 2 if verbmode else 1
	unittest.main(argv=args, verbosity=v_flag, ) # defaultTest=[]

# might make this a bit easier with a higher-level script to call tests with defaults.
