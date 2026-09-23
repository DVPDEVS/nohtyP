from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
from nohtyP._impl.lexer.types import *
from typing import Union
from types import UnionType


@api_level(0)
class SyntaxObject:
	__slots__ = ['_kind',]
	def __init__(self, kind :str) -> None:
		self._kind :str = kind
	def __repr__(self) -> str:
		return f"SyntaxObject(kind:'{self._kind}')"
	def __str__(self) -> str:
		return self._kind

@api_level(0)
class SyntaxObjectList:
	# Names
	IDENTIFIER = SyntaxObject("IDENTIFIER")
	# Literals
	NUMBER  = SyntaxObject("NUMBER")
	STRING  = SyntaxObject("STRING")
	BOOLEAN = SyntaxObject("BOOLEAN")
	NONE    = SyntaxObject("NONE")
	LITERAL = SyntaxObject("LITERAL")
	# Collections
	CONTAINER = SyntaxObject("CONTAINER")
	# Expressions
	FUNCTION_CALL = SyntaxObject("FUNCTION_CALL")
	ATTRIBUTE     = SyntaxObject("ATTRIBUTE")
	INDEX         = SyntaxObject("INDEX")
	SLICE         = SyntaxObject("SLICE")
	UNARY_OP      = SyntaxObject("UNARY_OP")
	BINARY_OP     = SyntaxObject("BINARY_OP")
	COMPARISON    = SyntaxObject("COMPARISON")
	LOGICAL_OP    = SyntaxObject("LOGICAL_OP")
	TERNARY       = SyntaxObject("TERNARY")
	# Comprehensions
	LIST_COMPREHENSION   = SyntaxObject("LIST_COMPREHENSION")
	DICT_COMPREHENSION   = SyntaxObject("DICT_COMPREHENSION")
	SET_COMPREHENSION    = SyntaxObject("SET_COMPREHENSION")
	GENERATOR_EXPRESSION = SyntaxObject("GENERATOR_EXPRESSION")
	# Assignment
	BINARY_OP           = SyntaxObject("BINARY_OP")
	ASSIGNMENT          = SyntaxObject("ASSIGNMENT")
	COMPOUND_ASSIGNMENT = SyntaxObject("COMPOUND_ASSIGNMENT")
	# Keywords
	MATCH    = SyntaxObject("MATCH")
	RETURN   = SyntaxObject("RETURN")
	YIELD    = SyntaxObject("YIELD")
	RAISE    = SyntaxObject("RAISE")
	BREAK    = SyntaxObject("BREAK")
	CONTINUE = SyntaxObject("CONTINUE")
	PASS     = SyntaxObject("PASS")
	# Definitions
	FUNCTION = SyntaxObject("FUNCTION")
	LAMBDA   = SyntaxObject("LAMBDA")
	CLASS    = SyntaxObject("CLASS")
	# Imports
	IMPORT      = SyntaxObject("IMPORT")
	FROM_IMPORT = SyntaxObject("FROM_IMPORT")
	# Context Management
	WITH = SyntaxObject("WITH") # undecided syntax
	# Async
	ASYNC_FUNCTION = SyntaxObject("ASYNC_FUNCTION")
	AWAIT          = SyntaxObject("AWAIT")
	ASYNC_FOR      = SyntaxObject("ASYNC_FOR")   # undecided syntax
	ASYNC_WITH     = SyntaxObject("ASYNC_WITH") # undecided syntax
	# Decorators
	DECORATOR = SyntaxObject("DECORATOR")
	# Typing
	TYPE_DECLARATION = SyntaxObject("TYPE_DECLARATION")
	...
	# add whatever structures here, like comprehensions, dicts, typedecls, classes

@api_level(0)
class ParseObject:
	"""
	NohtyP class for Parsed groups of `LexObjects` matching a given `SyntaxObject` structure
	"""
	__slots__ = ["_sotype", "objectlist", "__issue_list__", ]
	def __init__(self) -> None:
		self._sotype :SyntaxObjectList|None = None # NOP string
		self.objectlist :tuple[LexObject] = () # any non-zero amount
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	# modify
	## objects
	def __iadd__(self, obj:LexObject) -> None: self.objectlist += obj
	def add_object(self, obj:LexObject) -> None: self += obj       # pass to the above dunder
	## type
	def __ilshift__(self, obj: SyntaxObjectList) -> None: self._sotype = obj
	def add_type(self, obj:SyntaxObjectList) -> None: self <<= obj # pass to the above dunder
	# strings
	def __str__(self) -> str: return f"{self._sotype}[{self.objectlist}]"
	def __repr__(self) -> str:
		string = f"ParseObject: (type={self._sotype.__repr__()})\n"
		for i in range(len(self.objectlist)): string += f" {i}:\t{self.objectlist[i].__repr__()}\n"
		return string[0:-1]
	# iteration support
	def __getitem__(self, key:int): return self.objectlist[key] # pass on to a tuple
	def __iter__(self): yield from self.objectlist # pass on to a tuple
	# issues
	## add
	def __and__(self, issue:str|AnyNohtyPSyntaxError) ->   None: self.__issue_list__ += tuple([issue])
	def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None: self & issue # forward to and dunder above
	## get
	def __or__(self, *args, **kwargs) -> dict[str|int,tuple[str|AnyNohtyPSyntaxError]]:
		return {"main":self.__issue_list__}.update({index:self.objectlist[index]|0 for index in range(len(self.objectlist))})
	def get_issues(self) -> dict[str|int,tuple[str|AnyNohtyPSyntaxError]]: return self |0 # call the above or dunder
	# attribs
	...

@api_level(0)
class ParseObjectSeries:
	"""
	NohtyP class for holding a series of `ParseObject`
	"""
	# TODO: update dunders below to reflect actual new data
	__slots__ = ["po_list",]
	def __init__(self):
		self.po_list :tuple[ParseObject] = []
		pass
	# object handling
	def append(self, obj :ParseObject) -> None: self.po_list.append(obj)
	# strings
	def __str__(self) -> None:
		string = ""
		for i in range(len(self.po_list)):
			string += f"  {i}:\t{self.po_list[i]}\n"
		return string[:-1]
	def __repr__(self) -> None:
		string = "LexObjectSeries:\n"
		for i in range(len(self.po_list)):
			string += f" {i}:\t{self.po_list[i].__repr__()}\n"
		return string[0:-1]
	# iteration support
	def __getitem__(self, key:int): return self.po_list[key] # pass on to a tuple
	def __iter__(self): yield from self.po_list # pass on to a tuple
	# added for testing, might be used more
	def format_list(self, include_position: bool = False) -> list[list[str, str, str]] | list[tuple[str, str, str, int]]:
		return [
			[ str(object._sotype._lang), object._sotype._name, object.value() ]
			for object in self.po_list
		] if not include_position else [
			( str(object._sotype._lang), object._sotype._name, object.value(), object.position() )
			for object in self.po_list
		]
