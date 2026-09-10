import unittest
from sys import argv
from itertools import accumulate
# from nohtyP.lexer.identifier import TT
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
from nohtyP._impl.lexer.tokenizer import *
from nohtyP._impl.lexer.types import *
from nohtyP._impl.lexer.identifier import Identify

__all__ = [
	"unittest",
	"Tokenizer",
	"Display_Types",
	"Lexer",
	"modes",
]

class modes:
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
			# more quote bullshit
			'""""""',
			"''''''",
			'"""""""',
			"'''''''",
			'r"""',
			"r'''",
			'fr"""',
			'rf"""',
			'""""a',
			"''''",
			'r""""a',
			"f''''",
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
			[ '-', '-', '-', '___', '+', '+', '+', '**', '*' ],
			[ '123', 'abc', 'abc123' ],
			[ '_leading', 'trailing_' ],
			[ 'f"1"', 'f"2"', 'f"3"' ],
			[ '1', '"2"', '3', '"4"', '5' ],
			[ 'abc', """'def"ghi'""", 'jkl' ],
			# quote bses
			[ '""""""', ],
			[ "''''''", ],
			[ '""""""', '"', ],
			[ "''''''", "'", ],
			[ 'r"""', ],
			[ "r'''", ],
			[ 'fr"""', ],
			[ 'rf"""', ],
			[ '""""a', ],
			[ "''''", ],
			[ 'r""""a', ],
			[ "f''''", ],
		]
	class realistic:
		string = """__future__:annotations?fetch;asyncio?fetch;dataclasses:dataclass?fetch;typing:Callable,Optional,TypeAlias?fetch;TypeAlias:Number=int|float;{{{f"calling {fn.__name__}"?print();*args,**kwargs?fn()?return}<-*args,**kwargs<-wrapped<-def;wrapped?return}<-Callable[...,Number]?fn<-tracer->Callable[...,Number]<-def{int:x;None?str|None:name{self.name|anonymous?return}<-self<-method->str<-def{tuple:a,b?match{(a,b)~0=result*~(x,y)~x>y~x-y=result*~(x,y)~x+y=result}{@*2}<-v<-lambda?fn;result?fn()?direct;self.method()?bound;-direct++result?value;value*3//2%5?value;value**2?value;value&7|2^1?value;value<<=1;value~1?value;{bound~value*~0?}?return}*$e*?$e==ZeroDivisionError~-1?return;$e==Exception~-2?return}<-self,int:a,int:b<-calc->Number<-def<-@tracer;{0?asyncio.sleep()?await;self.x,5?self.calc()?return}<-self<-async_calc->int<-def<-async}<-Demo<-class<-@dataclass"""
		result = []
		expected = [
			'__future__', ':', 'annotations', '?', 'fetch', ';', 'asyncio', '?', 'fetch', ';', 'dataclasses', ':', 'dataclass', 
			'?', 'fetch', ';', 'typing', ':', 'Callable', ',', 'Optional', ',', 'TypeAlias', '?', 'fetch', ';', 'TypeAlias', ':', 
			'Number', '=', 'int', '|', 'float', ';', '{', '{', '{', 'f"calling {fn.__name__}"', '?', 'print', '()', ';', '*args', 
			',', '**', 'kwargs', '?', 'fn', '()', '?', 'return', '}', '<-', '*args', ',', '**', 'kwargs', '<-', 'wrapped', '<-', 
			'def', ';', 'wrapped', '?', 'return', '}', '<-', 'Callable', '[', '.', '.', '.', ',', 'Number', ']', '?', 'fn', '<-', 
			'tracer', '->', 'Callable', '[', '.', '.', '.', ',', 'Number', ']', '<-', 'def', '{', 'int', ':', 'x', ';', 'None', 
			'?', 'str', '|', 'None', ':', 'name', '{', 'self', '.', 'name', '|', 'anonymous', '?', 'return', '}', '<-', 'self', 
			'<-', 'method', '->', 'str', '<-', 'def', '{', 'tuple', ':', 'a', ',', 'b', '?', 'match', '{', '(', 'a', ',', 'b', 
			')', '~', '0', '=', 'result', '*~', '(', 'x', ',', 'y', ')', '~', 'x', '>', 'y', '~', 'x', '-', 'y', '=', 'result', 
			'*~', '(', 'x', ',', 'y', ')', '~', 'x', '+', 'y', '=', 'result', '}', '{', '@', '*', '2', '}', '<-', 'v', '<-', 
			'lambda', '?', 'fn', ';', 'result', '?', 'fn', '()', '?', 'direct', ';', 'self', '.', 'method', '()', '?', 'bound', 
			';', '-', 'direct', '+', '+', 'result', '?', 'value', ';', 'value', '*', '3', '//', '2', '%', '5', '?', 'value', ';', 
			'value', '**', '2', '?', 'value', ';', 'value', '&', '7', '|', '2', '^', '1', '?', 'value', ';', 'value', '<<=', '1', 
			';', 'value', '~', '1', '?', 'value', ';', '{', 'bound', '~', 'value', '*~', '0', '?', '}', '?', 'return', '}', 
			'*$e', '*?', '$e', '==', 'ZeroDivisionError', '~', '-', '1', '?', 'return', ';', '$e', '==', 'Exception', '~', '-', 
			'2', '?', 'return', '}', '<-', 'self', ',', 'int', ':', 'a', ',', 'int', ':', 'b', '<-', 'calc', '->', 'Number', 
			'<-', 'def', '<-', '@', 'tracer', ';', '{', '0', '?', 'asyncio', '.', 'sleep', '()', '?', 'await', ';', 'self', '.', 
			'x', ',', '5', '?', 'self', '.', 'calc', '()', '?', 'return', '}', '<-', 'self', '<-', 'async_calc', '->', 'int', 
			'<-', 'def', '<-', 'async', '}', '<-', 'Demo', '<-', 'class', '<-', '@', 'dataclass',
		]
	def basic(self):
		for i in range(len(self.base.strings)):
			self.base.results[i] = tokenize_str(self.base.strings[i])._tokens_only()
			self.assertListEqual(self.base.expected[i], self.base.results[i])
		if modes.showmode:
			if modes.verbmode: print("\n")
			for i in self.base.results: print(i)
	def vnums(self):
		def ints():
			for i in range(len(self.valid_nums.ints)):
				self.valid_nums.results_ints[i] = tokenize_str(self.valid_nums.ints[i])._tokens_only()
				self.assertListEqual(self.valid_nums.expected_ints[i], self.valid_nums.results_ints[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.valid_nums.results_ints: print(i)
		def floats():
			for i in range(len(self.valid_nums.floats)):
				self.valid_nums.results_floats[i] = tokenize_str(self.valid_nums.floats[i])._tokens_only()
				self.assertListEqual(self.valid_nums.expected_floats[i], self.valid_nums.results_floats[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.valid_nums.results_floats: print(i)
		def scientifics():
			for i in range(len(self.valid_nums.scientifics)):
				self.valid_nums.results_scis[i] = tokenize_str(self.valid_nums.scientifics[i])._tokens_only()
				self.assertListEqual(self.valid_nums.expected_scientifics[i], self.valid_nums.results_scis[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.valid_nums.results_scis: print(i)
		ints(); floats(); scientifics() 
	def inums(self):
		def ints():
			for i in range(len(self.invalid_nums.ints)):
				self.invalid_nums.results_ints[i] = tokenize_str(self.invalid_nums.ints[i])._tokens_only()
				self.assertListEqual(self.invalid_nums.expected_ints[i], self.invalid_nums.results_ints[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.invalid_nums.results_ints: print(i)
		def floats():
			for i in range(len(self.invalid_nums.floats)):
				self.invalid_nums.results_floats[i] = tokenize_str(self.invalid_nums.floats[i])._tokens_only()
				self.assertListEqual(self.invalid_nums.expected_floats[i], self.invalid_nums.results_floats[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.invalid_nums.results_floats: print(i)
		def scientifics():
			for i in range(len(self.invalid_nums.scientifics)):
				self.invalid_nums.results_scis[i] = tokenize_str(self.invalid_nums.scientifics[i])._tokens_only()
				self.assertListEqual(self.invalid_nums.expected_scientifics[i], self.invalid_nums.results_scis[i])
			if modes.showmode:
				if modes.verbmode: print("\n")
				for i in self.invalid_nums.results_scis: print(i)
		ints(); floats(); scientifics() 
	def stress(self):
		for i in range(len(self.stress_test.strings)):
			self.stress_test.results[i] = tokenize_str(self.stress_test.strings[i])._tokens_only()
			self.assertListEqual(self.stress_test.expected[i], self.stress_test.results[i])
		if modes.showmode:
			if modes.verbmode: print("\n")
			for i in self.stress_test.results: print(i)
	def realistic_input(self):
		self.maxDiff = 4000
		self.realistic.result = tokenize_str(self.realistic.string)._tokens_only()
		self.assertListEqual(self.realistic.expected, self.realistic.result)
		if modes.showmode:
			if modes.verbmode: print("\n")
			print(self.realistic.result)

@test
class Display_Types(unittest.TestCase):
	class lex:
		lt_name = "test_type"
		lo_value = ("TESTING_TESTING", 0) # would be pulled from a tokenseries, so we emulate that
		lt = LexType(lt_name, lexer_langs.NOHTYP)
		lo = LexObject(lo_value, lt)
		ls = LexObjectSeries()
		ls.append(lo)
	def display_lex(self):
		if modes.showmode or not modes.quietmode:
			print(self.lex.lt)
			print(self.lex.lo)
			print(self.lex.ls)
			print(self.lex.lt.__repr__())
			print(self.lex.lo.__repr__())
			print(self.lex.ls.__repr__())
		self.assertTrue(self.lex.ls != None)

@test
class Lexer(unittest.TestCase):
	class input_data:
		token_data: list[TokenSeries] = [tokenize_str(s) for s in Tokenizer.stress_test.strings]
		token_data_los: list[LexObjectSeries] = [] # given data below bc it depends on token_data
		expected_los_data: list[list[list[str]]] = [
			[
				["NOHTYP", "BAREWORD", 'a'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'b'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'c'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'd'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'e'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'f'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'g'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'h'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'i'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'j'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'k'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'l'],
			],[
				["NOHTYP", "BAREWORD", 'a'],
				["PYTHON", "STR", '"b"'],
				["NOHTYP", "BAREWORD", 'c'],
				["PYTHON", "STR", "'d'"],
				["NOHTYP", "BAREWORD", 'e'],
			],[
				["PYTHON", "INT", '1'],
				["PYTHON", "STR", '"2"'],
				["PYTHON", "INT", '3'],
			],[
				["PYTHON", "STR", 'f"1"'],
				["PYTHON", "STR", 'f"2"'],
			],[
				["NOHTYP", "SYMBOL_AT", '@'],
				["NOHTYP", "SYMBOL_AT", '@'],
				["NOHTYP", "SYMBOL_AT", '@'],
				["GENERIC", "UNKNOWN", '$'],
				["GENERIC", "UNKNOWN", '$'],
				["GENERIC", "UNKNOWN", '$'],
				["PYTHON", "OP", '%'],
				["PYTHON", "OP", '%'],
				["PYTHON", "OP", '%'],
				["PYTHON", "BITOP", '^'],
				["PYTHON", "BITOP", '^'],
				["PYTHON", "BITOP", '^'],
				["PYTHON", "BITOP", '&'],
				["PYTHON", "BITOP", '&'],
				["PYTHON", "BITOP", '&'],
			],[
				["NOHTYP", "BAREWORD", 'foo'],
				["PYTHON", "DOT", '.'],
				["PYTHON", "DOT", '.'],
				["PYTHON", "DOT", '.'],
				["NOHTYP", "BAREWORD", 'bar'],
			],[
				["PYTHON", "DOT", '.'],
				["NOHTYP", "BAREWORD", 'leading'],
				["PYTHON", "DOT", '.'],
				["PYTHON", "DOT", '.'],
				["NOHTYP", "BAREWORD", 'trailing'],
				["PYTHON", "DOT", '.'],
			],[
				["PYTHON", "COMMA", ','],
				["PYTHON", "COMMA", ','],
				["PYTHON", "COMMA", ','],
				["NOHTYP", "SEMICOLON", ';'],
				["NOHTYP", "SEMICOLON", ';'],
				["NOHTYP", "SEMICOLON", ';'],
				["PYTHON", "COLON", ':'],
				["PYTHON", "COLON", ':'],
				["PYTHON", "COLON", ':'],
			],[
				["PYTHON", "CALL", '()'],
				["NOHTYP", "BRACKET_LEFT", '['],
				["NOHTYP", "BRACKET_RIGHT", ']'],
				["NOHTYP", "CBRACKET_LEFT", '{'],
				["NOHTYP", "CBRACKET_RIGHT", '}'],
				["PYTHON", "OP", '<'],
				["PYTHON", "OP", '>'],
			],[
				["PYTHON", "STR", '"quoted"'],
			],[
				["PYTHON", "STR", "'single-quoted'"],
			],[
				["PYTHON", "STR", '''"mix'ed"'''],
			],[
				["NOHTYP", "BAREWORD", 'a'],
				["PYTHON", "STR", '""'],
				["PYTHON", "STR", "b''"],
				["NOHTYP", "BAREWORD", 'c'],
			],[
				["NOHTYP", "BAREWORD", 'x'],
				["NOHTYP", "ASS_EQ", '='],
				["NOHTYP", "BAREWORD", 'y'],
				["PYTHON", "OP", '+'],
				["NOHTYP", "BAREWORD", 'z'],
				["PYTHON", "OP", '-'],
				["PYTHON", "INT", '1'],
				["PYTHON", "OP", '*'],
				["PYTHON", "INT", '2'],
				["PYTHON", "OP", '/'],
				["PYTHON", "INT", '3'],
			],[
				["PYTHON", "INT", '1'],
				["PYTHON", "COMMA", ','],
				["PYTHON", "INT", '234'],
				["PYTHON", "COMMA", ','],
				["PYTHON", "FLOAT", '567.89'],
			],[
				["PYTHON", "INT", '0xFF'],
				["PYTHON", "INT", '0b1010'],
				["PYTHON", "INT", '0o755'],
			],[
				["PYTHON", "FLOAT", '3.14159e-10'],
			],[
				["NOHTYP", "BAREWORD", 'NaN'],
				["NOHTYP", "BAREWORD", 'INF'],
				["PYTHON", "OP", '-'],
				["NOHTYP", "BAREWORD", 'INF'],
			],[
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🙂)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(😂)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🔥)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(💯)'],
			],[
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🏳)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(️)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(‍)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(⚧)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(️)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🏳)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(️)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(‍)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🌈)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🇳)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(🇴)'],
			],[
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(汉)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(字)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(か)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(な)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(カ)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(ナ)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(한)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(글)'],
			],[
				["NOHTYP", "BAREWORD", 'e'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(́)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(é)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(ê)'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(ë)'],
			],[
				["NOHTYP", "BAREWORD", 'a'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(​)'],
				["NOHTYP", "BAREWORD", 'b'],
			],[
				["NOHTYP", "BAREWORD", 'a'],
				["NOHTYP", "BAREWORD", 'b'],
			],[
				["NOHTYP", "BAREWORD", 'word'],
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(⁠)'],
				["NOHTYP", "BAREWORD", 'word'],
			],[
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(‮)'],
				["NOHTYP", "BAREWORD", 'abc'],
			],[
				["GENERIC", "TOKENIZER_FAIL", '¤__NOHTYP_NOT_TOKENIZABLE__¤(\ufeff)'],
				["NOHTYP", "BAREWORD", 'bom'],
			],[
				["PYTHON", "OP", '<<'],
				["PYTHON", "OP", '>>'],
				["NOHTYP", "ASS_EQ", '=='],
				["PYTHON", "OP", '!='],
				["PYTHON", "OP", '<='],
				["PYTHON", "OP", '>='],
				["PYTHON", "BITOP", '&'],
				["PYTHON", "BITOP", '&'],
				["PYTHON", "BITOP", '|'],
				["PYTHON", "BITOP", '|'],
				["PYTHON", "COLON", ':'],
				["PYTHON", "COLON", ':'],
				["NOHTYP", "ARROW_RIGHT", '->'],
				["NOHTYP", "ASS_EQ", '='],
				["PYTHON", "OP", '>'],
			],[
				["PYTHON", "OP", '-'],
				["PYTHON", "OP", '-'],
				["PYTHON", "OP", '-'],
				["NOHTYP", "BAREWORD", '___'],
				["PYTHON", "OP", '+'],
				["PYTHON", "OP", '+'],
				["PYTHON", "OP", '+'],
				["PYTHON", "OP", '**'],
				["PYTHON", "OP", '*'],
			],[
				["PYTHON", "INT", '123'],
				["NOHTYP", "BAREWORD", 'abc'],
				["NOHTYP", "BAREWORD", 'abc123'],
			],[
				["NOHTYP", "BAREWORD", '_leading'],
				["NOHTYP", "BAREWORD", 'trailing_'],
			],[
				["PYTHON", "STR", 'f"1"'],
				["PYTHON", "STR", 'f"2"'],
				["PYTHON", "STR", 'f"3"'],
			],[
				["PYTHON", "INT", '1'],
				["PYTHON", "STR", '"2"'],
				["PYTHON", "INT", '3'],
				["PYTHON", "STR", '"4"'],
				["PYTHON", "INT", '5'],
			],[
				["NOHTYP", "BAREWORD", 'abc'],
				["PYTHON", "STR", """'def"ghi'"""],
				["NOHTYP", "BAREWORD", 'jkl'],
			],[
				["PYTHON", "STR", '""""""'],
			],[
				["PYTHON", "STR", "''''''"],
			],[
				["PYTHON", "STR", '""""""'],
				["GENERIC", "UNKNOWN", '"'],
			],[
				["PYTHON", "STR", "''''''"],
				["GENERIC", "UNKNOWN", "'"],
			],[
				["GENERIC", "UNKNOWN", 'r"""'],
			],[
				["GENERIC", "UNKNOWN", "r'''"],
			],[
				["GENERIC", "UNKNOWN", 'fr"""'],
			],[
				["GENERIC", "UNKNOWN", 'rf"""'],
			],[
				["GENERIC", "UNKNOWN", '""""a'],
			],[
				["GENERIC", "UNKNOWN", "''''"],
			],[
				["GENERIC", "UNKNOWN", 'r""""a'],
			],[
				["GENERIC", "UNKNOWN", "f''''"],
				]
			]
	#  define token_data_los
	input_data.token_data_los = [ Identify.identify_series(series) for series in input_data.token_data ]
	def identify(self):
		# correct identification of strings
		for index in range(len(self.input_data.token_data_los)):
			res: LexObjectSeries = self.input_data.token_data_los[index]
			res_ls: list[list[str, str, str]] = res.format_list(False)
			if modes.showmode:
				if modes.verbmode: print("\n")
				print(res)
				(fails, failed, fcount) = Identify.has_error_los(res)
				if failed:
					print(f"Failure observed:\n\tCount: {fcount}\n\t{fails}")
			self.assertListEqual(self.input_data.expected_los_data[index], res_ls)
	def position_preservation(self):
		# test if positions are preserved when converting from tokenseries to lexobjectseries
		for index in range(len(self.input_data.token_data)):
			token_positions: list[int] = self.input_data.token_data[index]._positions_only()
			los_positions: list[int] = [ lexobj.position() for lexobj in self.input_data.token_data_los[index] ]
			self.assertListEqual(token_positions, los_positions)

if __name__ == "__main__":
	args = argv
	if len(args) >= 2:
		if args[1] == "v":
			modes.verbmode = True
			args.pop(1)
		elif args[1] == "q":
			modes.quietmode = True
			args.pop(1)
	if len(args) >= 2:
		if args[1] == "s":
			modes.showmode = True
			args.pop(1)
	unittest.main(
		argv=args,
		verbosity = 0 if modes.quietmode else 2 if modes.verbmode else 1,
		defaultTest=[
			"Tokenizer.basic",
			"Tokenizer.vnums",
			"Tokenizer.inums",
			"Tokenizer.stress",
			"Tokenizer.realistic_input",
			# "Display_Types.display_lex",
			"Lexer.identify",
			"Lexer.position_preservation",
		]
	)
