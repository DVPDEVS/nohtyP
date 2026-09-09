from __future__ import annotations
from collections.abc import Iterable
from typing import Never, Any
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
class TokenSeries(list[tuple[str,int]]):
	"""Series of tokens.  \n
	Subclasses `list`.  
	Requires `list[tuple[str, int]]`.
	"""
	def __init__(self, iterable:list[tuple[str,int]]=()) -> None:
		if not all(
			isinstance(x, tuple)
			and len(x) == 2
			and isinstance(x[0], str)
			and isinstance(x[1], int)
			for x in iterable
		):
			raise TypeError("TokenSeries only accepts (str, int) tuples")
		super().__init__(iterable)
	def append(self, item: tuple[str, int]) -> None:
		if (
			not isinstance(item, tuple)
			or len(item) != 2
			or not isinstance(item[0], str)
			or not isinstance(item[1], int)
		):
			raise TypeError("TokenSeries only accepts (str, int) tuples")
		super().append(item)
	def _tokens_only(self)->list[str]:
		return [token for token, _ in self]
	def _positions_only(self)->list[int]:
		return [pos for _, pos in self]
	# Block all other ways to add to the list (besides setattr)
	def extend     (self, iterable: Any         ) -> Never: raise NotImplementedError
	def insert     (self, index: Any, item: Any ) -> Never: raise NotImplementedError
	def __setitem__(self, key: Any, value: Any  ) -> Never: raise NotImplementedError
	def __iadd__   (self, other: Any            ) -> Never: raise NotImplementedError

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
	__slots__ = ["ltype", "__value__", "__issue_list__", ]
	def __init__(self, value :tuple[str,int], ltype :LexType) -> None:
		self.ltype :LexType = ltype
		self.__value__ :tuple[str, int] = value
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	# strings
	def __repr__(self) -> str: return f"LexObject('{self.value()}',position={self.position()}), type=({self.ltype.__repr__()})"
	def __str__(self) -> str:  return f"{self.ltype}['{self.value()}']"
	# issues
	## add
	def __and__(self, issue:str|AnyNohtyPSyntaxError) ->   None:   self.__issue_list__ += tuple([issue])
	def add_issue(self, issue:str|AnyNohtyPSyntaxError) -> None: self & issue # forward to and dunder above
	## get
	def __or__(self, *args, **kwargs) -> tuple[str|AnyNohtyPSyntaxError]: return self.__issue_list__
	def get_issues(self) -> tuple[str|AnyNohtyPSyntaxError]:              return self |0 # call or dunder above
	# attribs
	def value(self) -> str: return self.__value__[0]
	def position(self) -> int: return self.__value__[1]

@api_level(0)
class LexObjectSeries:
	"""
	NohtyP class for holding a series of `Lexobject`
	"""
	__slots__ = ["objectlist",]
	def __init__(self):
		self.objectlist :tuple[LexObject] = []
		pass
	# object handling
	def append(self, obj :LexObject) -> None: self.objectlist.append(obj)
	# strings
	def __str__(self) -> None:
		string = ""
		for i in range(len(self.objectlist)):
			string += f"  {i}:\t{self.objectlist[i]}\n"
		return string[:-1]
	def __repr__(self) -> None:
		string = "LexObjectSeries:\n"
		for i in range(len(self.objectlist)):
			string += f" {i}:\t{self.objectlist[i].__repr__()}\n"
		return string[0:-1]
	# iteration support
	def __getitem__(self, key:int): return self.objectlist[key] # pass on to a tuple
	def __iter__(self): yield from self.objectlist # pass on to a tuple
