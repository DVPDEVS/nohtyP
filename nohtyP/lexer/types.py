from ..global_utilities.decorators import api_level
# This is gonna hold lexer output types

@api_level(0)
class lexer_langs:
	NOHTYP = 1
	PYTHON = 2

@api_level(1)
class LexerType():
	lang:lexer_langs = None
	name: str = None
	def __init__(self, value=None):
		self.value = value
	def __repr__(self):
		return f"{self.name}({self.value!r}), lang={self.lang}"
	@classmethod
	def _subclass(cls, name:str, **attrs):
		return type(name, (cls,), attrs)

class _example(LexerType):
	name = "example"
	lang = lexer_langs.NOHTYP

# generate the rest of the types
from lex_tt import TT_NOHTYP, TT_PYTHON
for k in vars(TT_NOHTYP):
	if k.startswith("_"): continue # internal attribute
	if k.upper() != k:    continue # not uppercase
	globals()[k] = LexerType._subclass(k, lang=lexer_langs.NOHTYP, name=k) # Assign new subclass name to global space
for k in vars(TT_PYTHON):
	if k.startswith("_"): continue # internal attribute
	if k.upper() != k:    continue # not uppercase
	globals()[k] = LexerType._subclass(k, lang=lexer_langs.NOHTYP, name=k) # Assign new subclass name to global space
