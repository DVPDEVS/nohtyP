from __future__ import annotations
from typing import Never, Any
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import AnyNohtyPSyntaxError
# Lexer output types

__all__ = [
	"TokenSeries",
	"lexer_langs",
	"LexType",
	"LexTypeList",
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
		self._name :str = name
		self._lang :lexer_langs = lang
	def __repr__(self) -> str:
		return f"LexType({self._name}), lang={self._lang}"
	def __str__(self) -> str:
		return f"{self._lang}[{self._name}]"

@api_level(0)
class LexTypeList:
	#! nohtyP specific
	SEMICOLON           :LexType = LexType("SEMICOLON",           lexer_langs.NOHTYP) #? ;
	BAREWORD            :LexType = LexType("BAREWORD",            lexer_langs.NOHTYP) #? <anything>
	TYPE_DECLARATION    :LexType = LexType("TYPE_DECLARATION",    lexer_langs.NOHTYP) #? optional * followed by a bareword and a :
	CBRACKET_LEFT       :LexType = LexType("CBRACKET_LEFT",       lexer_langs.NOHTYP) #? {
	CBRACKET_RIGHT      :LexType = LexType("CBRACKET_RIGHT",      lexer_langs.NOHTYP) #? }
	BRACKET_LEFT        :LexType = LexType("BRACKET_LEFT",        lexer_langs.NOHTYP) #? [
	BRACKET_RIGHT       :LexType = LexType("BRACKET_RIGHT",       lexer_langs.NOHTYP) #? ]
	CALL                :LexType = LexType("CALL",                lexer_langs.PYTHON) #? ()
	PAREN_LEFT          :LexType = LexType("PAREN_LEFT",          lexer_langs.NOHTYP) #? (
	PAREN_RIGHT         :LexType = LexType("PAREN_RIGHT",         lexer_langs.NOHTYP) #? )
	ASS_EQ              :LexType = LexType("ASS_EQ",              lexer_langs.NOHTYP) #? =
	FLOW_Q              :LexType = LexType("FLOW_Q",              lexer_langs.NOHTYP) #? ?
	FLOW_HASH_Q         :LexType = LexType("FLOW_HASH_Q",         lexer_langs.NOHTYP) #? #?
	FLOW_WHILE          :LexType = LexType("FLOW_WHILE",          lexer_langs.NOHTYP) #? ?=
	SYMBOL_AT           :LexType = LexType("SYMBOL_AT",           lexer_langs.NOHTYP) #? @
	TILDE               :LexType = LexType("TILDE",               lexer_langs.NOHTYP) #? ~
	CONDITION_AST_TILDE :LexType = LexType("CONDITION_AST_TILDE", lexer_langs.NOHTYP) #? *~
	ARROW_LEFT          :LexType = LexType("ARROW_LEFT",          lexer_langs.NOHTYP) #? <-
	ARROW_RIGHT         :LexType = LexType("ARROW_RIGHT",         lexer_langs.NOHTYP) #? ->
	EXCEPT_STORE        :LexType = LexType("EXCEPT_STORE",        lexer_langs.NOHTYP) #? *$<insert var>
	EXCEPT_GET          :LexType = LexType("EXCEPT_GET",          lexer_langs.NOHTYP) #? $<insert var>
	EXCEPT_HANDLE       :LexType = LexType("EXCEPT_HANDLE",       lexer_langs.NOHTYP) #? *?
	EXCEPT_SET          :LexType = LexType("EXCEPT_SET",          lexer_langs.NOHTYP) #? *set -e/+e
	KW_FETCH            :LexType = LexType("KW_FETCH",            lexer_langs.NOHTYP) #? fetch
	KW_MATCH            :LexType = LexType("KW_MATCH",            lexer_langs.NOHTYP) #? match
	#! Python native
	INT                 :LexType = LexType("INT",                 lexer_langs.PYTHON)
	FLOAT               :LexType = LexType("FLOAT",               lexer_langs.PYTHON)
	BOOL                :LexType = LexType("BOOL",                lexer_langs.PYTHON)
	NONE                :LexType = LexType("NONE",                lexer_langs.PYTHON)
	STR                 :LexType = LexType("STR",                 lexer_langs.PYTHON)
	KEYWORD             :LexType = LexType("KEYWORD",             lexer_langs.PYTHON)
	OP                  :LexType = LexType("OP",                  lexer_langs.PYTHON)
	AUGASSIGN           :LexType = LexType("AUGASSIGN",           lexer_langs.PYTHON)
	BITOP               :LexType = LexType("BITOP",               lexer_langs.PYTHON)
	COMPARE             :LexType = LexType("COMPARE",             lexer_langs.PYTHON)
	LOGIC               :LexType = LexType("LOGIC",               lexer_langs.PYTHON)
	COMMA               :LexType = LexType("COMMA",               lexer_langs.PYTHON)
	DOT                 :LexType = LexType("DOT",                 lexer_langs.PYTHON)
	COLON               :LexType = LexType("COLON",               lexer_langs.PYTHON)
	ELLIPSIS            :LexType = LexType("ELLIPSIS",            lexer_langs.PYTHON)
	LAMBDA              :LexType = LexType("LAMBDA",              lexer_langs.PYTHON)
	YIELD               :LexType = LexType("YIELD",               lexer_langs.PYTHON)
	AWAIT               :LexType = LexType("AWAIT",               lexer_langs.PYTHON)
	ASYNC               :LexType = LexType("ASYNC",               lexer_langs.PYTHON)
	COMMENT             :LexType = LexType("COMMENT",             lexer_langs.PYTHON)
	#! Generics
	TOKENIZER_FAIL      :LexType = LexType("TOKENIZER_FAIL",      lexer_langs.GENERIC) #? ¤__NOHTYP_NOT_TOKENIZABLE__¤()
	STAR                :LexType = LexType("STAR",                lexer_langs.GENERIC) #? *
	UNKNOWN             :LexType = LexType("UNKNOWN",             lexer_langs.GENERIC)

@api_level(0)
class LexObject:
	"""
	NohtyP class for Lexical Objects
	"""
	__slots__ = ["_ltype", "__value__", "__issue_list__", ]
	def __init__(self, value :tuple[str,int], ltype :LexType) -> None:
		self._ltype :LexType = ltype
		self.__value__ :tuple[str, int] = value
		self.__issue_list__ :tuple[str|AnyNohtyPSyntaxError] = ()
	# strings
	def __repr__(self) -> str: return f"LexObject('{self.value()}',position={self.position()}), type=({self._ltype.__repr__()})"
	def __str__(self) -> str:  return f"{self._ltype}['{self.value()}']"
	# issues
	## add
	def __and__(self, issue:str|AnyNohtyPSyntaxError) ->   None: self.__issue_list__ += tuple([issue])
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
	def __str__(self) -> str:
		string = ""
		for i in range(len(self.objectlist)):
			string += f"  {i}:\t{self.objectlist[i]}\n"
		return string[:-1]
	def __repr__(self) -> str:
		string = "LexObjectSeries:\n"
		for i in range(len(self.objectlist)):
			string += f" {i}:\t{self.objectlist[i].__repr__()}\n"
		return string[0:-1]
	# iteration support
	def __getitem__(self, key:int): return self.objectlist[key] # pass on to a tuple
	def __iter__(self): yield from self.objectlist # pass on to a tuple
	# added for testing, might be used more
	def format_list(self, include_position: bool = False) -> list[list[str, str, str]] | list[tuple[str, str, str, int]]:
		return [
			[ str(object._ltype._lang), object._ltype._name, object.value() ]
			for object in self.objectlist
		] if not include_position else [
			( str(object._ltype._lang), object._ltype._name, object.value(), object.position() )
			for object in self.objectlist
		]
