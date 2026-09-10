from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
from nohtyP._impl.lexer.types import *

@api_level(0)
class SyntaxObject:
	def __init__(self, kind :str) -> None:
		self.__kind__ :str = kind
	def __repr__(self) -> str:
		return f"SyntaxObject({self.__kind__})"
	def __str__(self) -> str:
		return self.__kind__

@api_level(0)
class SyntaxObjectList:
	# Names
	IDENTIFIER = SyntaxObject("IDENTIFIER")
	# Literals
	NUMBER = SyntaxObject("NUMBER")
	STRING = SyntaxObject("STRING")
	BOOLEAN = SyntaxObject("BOOLEAN")
	NONE = SyntaxObject("NONE")
	# Collections
	LIST = SyntaxObject("LIST")
	TUPLE = SyntaxObject("TUPLE")
	DICT = SyntaxObject("DICT")
	SET = SyntaxObject("SET")
	# Expressions
	CALL = SyntaxObject("CALL")
	ATTRIBUTE = SyntaxObject("ATTRIBUTE")
	INDEX = SyntaxObject("INDEX")
	SLICE = SyntaxObject("SLICE")
	UNARY_OP = SyntaxObject("UNARY_OP")
	BINARY_OP = SyntaxObject("BINARY_OP")
	COMPARISON = SyntaxObject("COMPARISON")
	LOGICAL_OP = SyntaxObject("LOGICAL_OP")
	WALRUS = SyntaxObject("WALRUS")
	TERNARY = SyntaxObject("TERNARY")
	# Comprehensions
	LIST_COMPREHENSION = SyntaxObject("LIST_COMPREHENSION")
	DICT_COMPREHENSION = SyntaxObject("DICT_COMPREHENSION")
	SET_COMPREHENSION = SyntaxObject("SET_COMPREHENSION")
	GENERATOR_EXPRESSION = SyntaxObject("GENERATOR_EXPRESSION")
	# Assignment
	ASSIGNMENT = SyntaxObject("ASSIGNMENT")
	COMPOUND_ASSIGNMENT = SyntaxObject("COMPOUND_ASSIGNMENT")
	# Control Flow
	IF = SyntaxObject("IF")
	FOR = SyntaxObject("FOR")
	WHILE = SyntaxObject("WHILE")
	MATCH = SyntaxObject("MATCH")
	TRY = SyntaxObject("TRY")
	# Jump Statements
	RETURN = SyntaxObject("RETURN")
	YIELD = SyntaxObject("YIELD")
	RAISE = SyntaxObject("RAISE")
	BREAK = SyntaxObject("BREAK")
	CONTINUE = SyntaxObject("CONTINUE")
	PASS = SyntaxObject("PASS")
	# Definitions
	FUNCTION = SyntaxObject("FUNCTION")
	LAMBDA = SyntaxObject("LAMBDA")
	CLASS = SyntaxObject("CLASS")
	# Imports
	IMPORT = SyntaxObject("IMPORT")
	FROM_IMPORT = SyntaxObject("FROM_IMPORT")
	# Context Management
	WITH = SyntaxObject("WITH")
	# Async
	ASYNC_FUNCTION = SyntaxObject("ASYNC_FUNCTION")
	AWAIT = SyntaxObject("AWAIT")
	ASYNC_FOR = SyntaxObject("ASYNC_FOR")
	ASYNC_WITH = SyntaxObject("ASYNC_WITH")
	# Decorators
	DECORATOR = SyntaxObject("DECORATOR")
	# Typing
	TYPE_DECLARATION = SyntaxObject("TYPE_DECLARATION")
	...
	# add whatever structures here, like comprehensions, dicts, typedecls, classes

@api_level(0)
class ParseToken:
	"""
	NohtyP class for Parsed Tokens
	"""
	__slots__ = ["_sotype", "__value__", "__issue_list__", ]
	def __init__(self, value :LexObject, ltype :SyntaxObjectList) -> None:
		self._sotype :SyntaxObjectList = ltype
		self.__value__ :LexObject = value
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = value |0
		self.__value__.__issue_list__ = () # reset internal issue list
	# strings
	# TODO: update dunders below to reflect actual new data
	def __repr__(self) -> str: return f"LexObject('{self.value()}',position={self.position()}), type=({self.__value__._ltype.__repr__()})"
	def __str__(self) -> str:  return f"{self.__value__._ltype}['{self.value()}']"
	# issues
	## add
	def __and__(self, issue:str|AnyNohtyPSyntaxError) ->   None: self.__issue_list__ += tuple([issue])
	def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None: self & issue # forward to and dunder above
	## get
	def __or__(self, *args, **kwargs) -> tuple[str|AnyNohtyPSyntaxError]: return self.__issue_list__
	def get_issues(self) -> tuple[str|AnyNohtyPSyntaxError]:              return self |0 # call or dunder above
	# attribs
	def value(self) -> str: return self.__value__.value()
	def position(self) -> int: return self.__value__.position()

@api_level(0)
class ParseTokenSeries:
	"""
	NohtyP class for holding a series of `ParseToken`
	"""
	__slots__ = ["tokenlist",]
	def __init__(self):
		self.tokenlist :tuple[ParseToken] = []
		pass
	# object handling
	def append(self, obj :ParseToken) -> None: self.tokenlist.append(obj)
	# strings
	def __str__(self) -> None:
		string = ""
		for i in range(len(self.tokenlist)):
			string += f"  {i}:\t{self.tokenlist[i]}\n"
		return string[:-1]
	def __repr__(self) -> None:
		string = "LexObjectSeries:\n"
		for i in range(len(self.tokenlist)):
			string += f" {i}:\t{self.tokenlist[i].__repr__()}\n"
		return string[0:-1]
	# iteration support
	def __getitem__(self, key:int): return self.tokenlist[key] # pass on to a tuple
	def __iter__(self): yield from self.tokenlist # pass on to a tuple
	# added for testing, might be used more
	def format_list(self, include_position: bool = False) -> list[list[str, str, str]] | list[tuple[str, str, str, int]]:
		return [
			[ str(object._sotype._lang), object._sotype._name, object.value() ]
			for object in self.tokenlist
		] if not include_position else [
			( str(object._sotype._lang), object._sotype._name, object.value(), object.position() )
			for object in self.tokenlist
		]
