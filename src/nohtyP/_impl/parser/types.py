from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
from nohtyP._impl.lexer.types import *


@api_level(0)
class SyntaxObject:
	__slots__ = ['_kind', '_struct']
	def __init__(self, kind :str, structure :tuple[LexTypeList|type]) -> None:
		self._kind :str = kind
		self._struct :tuple[LexTypeList|type] = structure
	def __repr__(self) -> str:
		return f"SyntaxObject(kind:'{self._kind}', structure: {self._struct})"
	def __str__(self) -> str:
		return self._kind

@api_level(0)
class SOLStructs:
	...
	#* define structures for instances of SyntaxObject
	# i really would have preferred rust for this part especially. its perfect for traits, impls, structs, enums and the strong typing.
	# Names
	IDENTIFIER: tuple[LexTypeList] = (LexTypeList.BAREWORD)
	# Literals
	NUMBER: tuple[LexTypeList|type] = ()
	STRING: tuple[LexTypeList|type] = ()
	BOOLEAN: tuple[LexTypeList|type] = ()
	NONE: tuple[LexTypeList|type] = ()
	# Collections
	LIST: tuple[LexTypeList|type] = ()
	TUPLE: tuple[LexTypeList|type] = ()
	DICT: tuple[LexTypeList|type] = ()
	SET: tuple[LexTypeList|type] = ()
	# Expressions
	CALL: tuple[LexTypeList] = (LexTypeList.PAREN_LEFT, LexTypeList.PAREN_RIGHT)
	ATTRIBUTE: tuple[LexTypeList|type] = ()
	INDEX: tuple[LexTypeList|type] = ()
	SLICE: tuple[LexTypeList|type] = ()
	UNARY_OP: tuple[LexTypeList|type] = ()
	BINARY_OP: tuple[LexTypeList|type] = ()
	COMPARISON: tuple[LexTypeList|type] = ()
	LOGICAL_OP: tuple[LexTypeList|type] = ()
	WALRUS: tuple[LexTypeList|type] = ()
	TERNARY: tuple[LexTypeList|type] = ()
	# Comprehensions
	LIST_COMPREHENSION: tuple[LexTypeList|type] = ()
	DICT_COMPREHENSION: tuple[LexTypeList|type] = ()
	SET_COMPREHENSION: tuple[LexTypeList|type] = ()
	GENERATOR_EXPRESSION: tuple[LexTypeList|type] = ()
	# Assignment
	ASSIGNMENT: tuple[LexTypeList|type] = ()
	COMPOUND_ASSIGNMENT: tuple[LexTypeList|type] = ()
	# Control Flow
	IF: tuple[LexTypeList|type] = ()
	FOR: tuple[LexTypeList|type] = ()
	WHILE: tuple[LexTypeList|type] = ()
	MATCH: tuple[LexTypeList|type] = ()
	TRY: tuple[LexTypeList|type] = ()
	# Jump Statements
	RETURN: tuple[LexTypeList|type] = ()
	YIELD: tuple[LexTypeList|type] = ()
	RAISE: tuple[LexTypeList|type] = ()
	BREAK: tuple[LexTypeList|type] = ()
	CONTINUE: tuple[LexTypeList|type] = ()
	PASS: tuple[LexTypeList|type] = ()
	# Definitions
	FUNCTION: tuple[LexTypeList|type] = ()
	LAMBDA: tuple[LexTypeList|type] = ()
	CLASS: tuple[LexTypeList|type] = ()
	# Imports
	IMPORT: tuple[LexTypeList|type] = ()
	FROM_IMPORT: tuple[LexTypeList|type] = ()
	# Context Management
	WITH: tuple[LexTypeList|type] = ()
	# Async
	ASYNC_FUNCTION: tuple[LexTypeList|type] = ()
	AWAIT: tuple[LexTypeList|type] = ()
	ASYNC_FOR: tuple[LexTypeList|type] = ()
	ASYNC_WITH: tuple[LexTypeList|type] = ()
	# Decorators
	DECORATOR: tuple[LexTypeList|type] = ()
	# Typing
	TYPE_DECLARATION: tuple[LexTypeList|type] = ()

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
class ParseObject:
	"""
	NohtyP class for Parsed groups of `LexObjects` matching a given `SyntaxObject` structure
	"""
	__slots__ = ["_sotype", "objectlist", "__issue_list__", ]
	def __init__(self) -> None:
		self._sotype :SyntaxObjectList|None = None # NOP string
		self.objectlist :tuple[LexObject] = () # any non-zero amount
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
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
	__slots__ = ["tokenlist",]
	def __init__(self):
		self.tokenlist :tuple[ParseObject] = []
		pass
	# object handling
	def append(self, obj :ParseObject) -> None: self.tokenlist.append(obj)
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
