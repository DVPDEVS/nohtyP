from __future__ import annotations
from collections.abc import Iterable
from typing import Never
from nohtyP.global_utilities.decorators import *
# Lexer output types

__all__ = [
	"lexer_langs",
	"LexerObject",
	"LexerSeries",
	"TokenSeries",
]

@api_level(0)
class lexer_langs:
	NOHTYP = "NOHTYP"
	PYTHON = "PYTHON"

@api_level(0)
class LexerObject(type):
	def __init__(self, name :str, lang :lexer_langs = None):
		self.__name__ = name
		self.__lang__ = lang
	def __repr__(self):
		return f"LexerType ({self.__name__}), lang={self.lang}"
	def __str__(self):
		return f"{self.__lang__}[{self.__name__}]"

@api_level(0)
class LexerSeries(type):
	def __init__(self):
		self.objectlist :list[LexerObject] = []
		pass
	def append(self, obj :LexerObject) -> None:
		self.objectlist.append(obj)

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
	# Block all other ways to add to the list
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
