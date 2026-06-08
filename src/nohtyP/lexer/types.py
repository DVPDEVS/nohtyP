from __future__ import annotations
from collections.abc import Iterable
from typing import Never
from nohtyP.global_utilities.decorators import *
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

@api_level(0)
class LexType:
	def __init__(self, name :str, lang :lexer_langs = None):
		self.__name__ :str = name
		self.__lang__ :lexer_langs = lang
	def __repr__(self) -> str:
		return f"LexerType ({self.__name__}), lang={self.lang}"
	def __str__(self) -> str:
		return f"{self.__lang__}[{self.__name__}]"

@api_level(0)
class LexObject:
	def __init__(self, value :str, ltype :LexType):
		self.ltype :LexType = ltype
		self.__value__ :str = value
	def __repr__(self) -> str:
		return f"LexObject ({self.__value__}), type={self.ltype}"
	def __str__(self) -> str:
		return f"{self.ltype}[{self.__value__}]"

@api_level(0)
class LexObjectSeries:
	def __init__(self):
		self.objectlist :tuple[LexObject] = []
		pass
	def append(self, obj :LexObject) -> None:
		self.objectlist.append(obj)

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
