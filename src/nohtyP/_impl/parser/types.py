from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError

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
