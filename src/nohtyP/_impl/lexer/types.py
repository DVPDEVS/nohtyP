from __future__ import annotations
from collections.abc import Iterable
from typing import Never
from nohtyP._impl.global_utilities.decorators import *
# Lexer output types

__all__ = [
	"lexer_langs",
	"LexType",
	"LexObject",
	"LexObjectSeries",
	"TokenSeries",
]

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
	def __init__(self, value :str, ltype :LexType) -> None:
		self.ltype :LexType = ltype
		self.__value__ :str = value
		self.__issue_list__ :tuple[str|Exception] = ()
	def __repr__(self) -> str:
		return f"LexObject('{self.__value__}'), type=({self.ltype.__repr__()})"
	def __str__(self) -> str:
		return f"{self.ltype}['{self.__value__}']"
	def __iand__(self, issue:str|Exception) -> None:
		self.__issue_list__ += issue
	def add_issue(self, issue:str|Exception) -> None:
		# forward to iand dunder
		self &= issue
	def issues(self) -> tuple[str|Exception]:
		return self.__issue_list__

@api_level(0)
class LexObjectSeries:
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
class ParseToken:
	def __init__(self, name:str) -> None:
		...

@api_level(0)
class ParseObject:
	# fully custom implementation i think
	def __init__(self) -> None:
		self.__objects__ :dict[ParseToken, str|dict] = {}

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
