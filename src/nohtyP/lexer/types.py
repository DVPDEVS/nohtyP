from __future__ import *
from nohtyP.global_utilities.decorators import *
# This is gonna hold lexer output types

@api_level(0)
class lexer_langs:
	NOHTYP = "NOHTYP"
	PYTHON = "PYTHON"

@api_level(0)
class LexerType(type):
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
		self.objectlist :list[LexerType] = []
		pass
	def append(self, obj :LexerType):
		self.objectlist.append(obj)

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
