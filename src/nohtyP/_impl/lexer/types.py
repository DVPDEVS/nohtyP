from __future__ import annotations
from collections.abc import Iterable
from typing import Never
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
# Lexer output types

__all__ = [
	"TokenSeries",
	"lexer_langs",
	"LexType",
	"LexObject",
	"LexObjectSeries",
]

@api_level(0)
class TokenSeries(list[str]):
	"""Series of tokens  \n
	Subclasses `list`  \n
	Requires a `list[str]`"""
	def __init__(self, iterable=()) -> None:
		if not all(isinstance(x, str) for x in iterable):
			raise TypeError("TokenSeries only accepts strings")
		super().__init__(iterable)
	def append(self, item: str) -> None:
		if not isinstance(item, str):
			raise TypeError("TokenSeries only accepts strings")
		super().append(item)
	# Block all other ways to add to the list (besides setattr)
	def extend     (self, iterable: Iterable[str]                  ) -> Never: raise NotImplementedError
	def insert     (self, index: int, item: str                    ) -> Never: raise NotImplementedError
	def __setitem__(self, key: int|slice, value: str|Iterable[str] ) -> Never: raise NotImplementedError
	def __iadd__   (self, other: Iterable[str]                     ) -> Never: raise NotImplementedError

@api_level(0)
class lexer_langs:
	NOHTYP = "NOHTYP"
	PYTHON = "PYTHON"
	GENERIC = "GENERIC"

@api_level(0)
class LexType:
	def __init__(self, name :str, lang :lexer_langs = None) -> None:
		self.__name__ :str = name
		self.__lang__ :lexer_langs = lang
	def __repr__(self) -> str:
		return f"LexType({self.__name__}), lang={self.__lang__}"
	def __str__(self) -> str:
		return f"{self.__lang__}[{self.__name__}]"

@api_level(0)
class LexObject:
	"""
	NohtyP class for Lexical Objects
	"""
	def __init__(self, value :str, ltype :LexType) -> None:
		self.ltype :LexType = ltype
		self.__value__ :str = value
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	def __repr__(self) -> str:
		return f"LexObject('{self.__value__}'), type=({self.ltype.__repr__()})"
	def __str__(self) -> str:
		return f"{self.ltype}['{self.__value__}']"
	def __and__(self, issue:str|AnyNohtyPSyntaxError) -> None:
		self.__issue_list__ += tuple([issue])
	def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None:
		# forward to iand dunder
		self &= issue
	def issues(self) -> tuple[str|AnyNohtyPSyntaxError]:
		return self.__issue_list__

@api_level(0)
class LexObjectSeries:
	"""
	NohtyP class for holding a series of `Lexobject`
	"""
	def __init__(self):
		self.objectlist :tuple[LexObject] = []
		pass
	def append(self, obj :LexObject) -> None:
		self.objectlist.append(obj)
	def __str__(self) -> None:
		string = ""
		for i in range(len(self.objectlist)):
			string += f" {i}:\t{self.objectlist[i]}\n"
		return string[0:-1]
	def __repr__(self) -> None:
		string = "LexObjectSeries:\n"
		for i in range(len(self.objectlist)):
			string += f" {i}:\t{self.objectlist[i].__repr__()}\n"
		return string[0:-1]
	def __getitem__(self, key:int):
		return self.objectlist[key] # pass on to a tuple
	def __iter__(self):
		yield from self.objectlist # pass on to a tuple

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
	def __init__(self, value: str, object_type: SyntaxObjectList) -> None:
		self.__type__ :SyntaxObjectList = object_type
		self.__value__ :str = value
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	def __repr__(self) -> str:
		return f"ParseToken('{self.__value__}'), type=({self.__type__.__repr__()})"
	def __str__(self) -> str:
		return f"{self.__type__}['{self.__value__}']"
	def __and__(self, issue:str|AnyNohtyPSyntaxError) -> None:
		self.__issue_list__ += tuple([issue])
	def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None:
		# forward to iand dunder
		self &= issue
	def issues(self) -> tuple[str|AnyNohtyPSyntaxError]:
		return self.__issue_list__

@api_level(0)
class ParseTokenSeries:
	# fully custom implementation i think
	def __init__(self) -> None:
		self.__tokens__ :dict[ParseToken, str|dict] = {}
	
	# def __init__(self, value :str, ltype :LexType) -> None:
	# 	self.ltype :LexType = ltype
	# 	self.__value__ :str = value
	# 	self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	# def __repr__(self) -> str:
	# 	return f"LexObject('{self.__value__}'), type=({self.ltype.__repr__()})"
	# def __str__(self) -> str:
	# 	return f"{self.ltype}['{self.__value__}']"
	# def __and__(self, issue:str|AnyNohtyPSyntaxError) -> None:
	# 	self.__issue_list__ += tuple([issue])
	# def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None:
	# 	# forward to iand dunder
	# 	self &= issue
	# def issues(self) -> tuple[str|AnyNohtyPSyntaxError]:
	# 	return self.__issue_list__

#* Cool but not needed anymore
#// class _example(LexerType):
#// 	name = "example"
#// 	lang = lexer_langs.NOHTYP
#// 
#// # generate the rest of the types
#// from lex_tt import TT_NOHTYP, TT_PYTHON
#// for k in vars(TT_NOHTYP):
#// 	if k.startswith("_"): continue # internal attribute
#// 	if k.upper() != k:    continue # not uppercase
#// 	globals()[k] = LexerType._subclass(k, lang=lexer_langs.NOHTYP, name=k) # Assign new subclass name to global space
#// for k in vars(TT_PYTHON):
#// 	if k.startswith("_"): continue # internal attribute
#// 	if k.upper() != k:    continue # not uppercase
#// 	globals()[k] = LexerType._subclass(k, lang=lexer_langs.PYTHON, name=k) # Assign new subclass name to global space
