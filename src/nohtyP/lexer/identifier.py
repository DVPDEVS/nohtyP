from __future__ import annotations
from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.types import *
import re
# Identify objects

@api_level(0)
class __TT_PYTHON:
	"""Holds lexical element definitions for Python"""
	def __class_getitem__(cls, key :str):
		return cls.__getattribute__(key)

	# Standard python lex types and objects
	INT       = "INT"		# Native int                    -> 123, 0, -42, 0b1010, 0o77, 0xFF
	FLOAT     = "FLOAT"		# Native float                  -> 1.23, .5, 10., 1e10, -3.4e-2
	BOOL      = "BOOL"		# Native bool                   -> True, False
	NONE      = "NONE"		# NoneType                      -> None
	BYTES     = "BYTES"		# Native bytes                  -> b"bytes", br"raw"
	BYTEARRAY = "BYTEARRAY"	# Native bytearray              -> bytearray(b"bytes")
	STR       = "STR"		# Native str                    -> "text", 'text', """text""", r"raw", f"format"

	ID        = "ID"		# Known identifiers             -> variable_name, _private, ClassName
	KEYWORD   = "KEYWORD"	# Python keywords               -> if, else, while, def, class, return, import
	OP        = "OP"		# Operators                     -> +, -, *, /, //, %, **, =, ==, !=, <, >, <=, >=, and, or, not, is, in
	PUNCT     = "PUNCT"		# General punctuation           -> :, ;, ., @, = (contextual), ->
	EOF       = "EOF"		# End of file/input             -> <EOF>

	LIST      = "LIST"		# Native list literal           -> [1, 2, 3]
	TUPLE     = "TUPLE"		# Native tuple literal          -> (1, 2), ()
	SET       = "SET"		# Native set literal            -> {1, 2, 3}
	DICT      = "DICT"		# Native dict literal           -> {"a": 1, "b": 2}
	ELLIPSIS  = "ELLIPSIS"	# Ellipsis object               -> ...
	SLICE     = "SLICE"		# Slice syntax                  -> a:b, a:b:c

	LPAREN    = "LPAREN"	# Left parenthesis              -> (
	RPAREN    = "RPAREN"	# Right parenthesis             -> )
	LBRACE    = "LBRACE"	# Left brace                    -> {
	RBRACE    = "RBRACE"	# Right brace                   -> }
	LBRACKET  = "LBRACKET"	# Left bracket                  -> [
	RBRACKET  = "RBRACKET"	# Right bracket                 -> ]

	DOT       = "DOT"		# Attribute access              -> .
	COLON     = "COLON"		# Colon                         -> :
	SEMICOLON = "SEMICOLON"	# Statement separator           -> ;
	ARROW     = "ARROW"		# Function return annotation    -> ->
	AT        = "AT"		# Decorator/operator            -> @

	ASSIGN    = "ASSIGN"	# Assignment                    -> =
	AUGASSIGN = "AUGASSIGN"	# Augmented assignment          -> +=, -=, *=, /=, //=, %=, **=, &=, |=, ^=, <<=, >>=

	BITOP     = "BITOP"		# Bitwise operators             -> &, |, ^, ~, <<, >>
	COMPARE   = "COMPARE"	# Comparison operators          -> ==, !=, <, >, <=, >=, is, is not, in, not in
	LOGIC     = "LOGIC"		# Logical operators             -> and, or, not

	NEWLINE   = "NEWLINE"	# Line break                    -> \n
	INDENT    = "INDENT"	# Indentation increase          -> (whitespace block start)
	DEDENT    = "DEDENT"	# Indentation decrease          -> (whitespace block end)

	COMMENT   = "COMMENT"	# Comment                       -> # comment text
	FSTRING   = "FSTRING"	# Formatted string              -> f"{x}", f"text {expr}"
	FORMAT    = "FORMAT"	# Format specifier (inside fstr)-> {value:.2f}

	GENEXP    = "GENEXP"	# Generator expression          -> (x for x in y)
	LISTCOMP  = "LISTCOMP"	# List comprehension            -> [x for x in y]
	SETCOMP   = "SETCOMP"	# Set comprehension             -> {x for x in y}
	DICTCOMP  = "DICTCOMP"	# Dict comprehension            -> {k: v for k, v in y}

	LAMBDA    = "LAMBDA"	# Lambda expression             -> lambda x: x + 1
	YIELD     = "YIELD"		# Yield expression              -> yield x, yield from x
	AWAIT     = "AWAIT"		# Await expression              -> await coro()
	ASYNC     = "ASYNC"		# Async keyword                 -> async def, async for

	DECORATOR = "DECORATOR"	# Decorator usage               -> @decorator
	TYPEHINT  = "TYPEHINT"	# Type annotations              -> x: int, -> str

@api_level(0)
class __TT_NOHTYP():
	"""Holds lexical element definitions for nohtyP"""
	def __class_getitem__(cls, key :str):
		return cls.__getattribute__(key)
	# nohtyP lex types and objects
	# TODO: Redefine based on syntax spec
	SEPARATOR           = "SEPARATOR"           #? ;
	BAREWORD            = "BAREWORD"            #? <anything>
	CBRACKET_LEFT       = "CBRACKET_LEFT"       #? {
	CBRACKET_RIGHT      = "CBRACKET_RIGHT"      #? }
	ASS_EQ              = "ASS_EQ"              #? =
	FLOW_Q              = "FLOW_Q"              #? ?
	FLOW_HASH_Q         = "FLOW_HASH_Q"         #? #?
	GEN_AST             = "GEN_AST"             #? *
	WHILE               = "WHILE"               #? ?=
	ITERATOR            = "ITERATOR"            #? @
	CONDITION_TILDE     = "CONDITION_TILDE"     #? ~
	CONDITION_AST_TILDE = "CONDITION_AST_TILDE"	#? *~
	ARROW_LEFT          = "ARROW_LEFT"          #? ->
	ARROW_RIGHT         = "ARROW_RIGHT"         #? <-
	EXCEPT_STORE        = "EXCEPT_STORE"        #? *$<insert var>
	EXCEPT_GET          = "EXCEPT_GET"          #? $<insert var>
	EXCEPT_HANDLE       = "EXCEPT_HANDLE"       #? *?
	EXCEPT_SET          = "EXCEPT_SET"          #? *set
	EXCEPT_SET_NEG      = "EXCEPT_SET_NEG"      #? -e
	EXCEPT_SET_POS      = "EXCEPT_SET_POS"      #? +e
	KW_GO               = "KW_GO"               #? go
	KW_FETCH            = "KW_FETCH"            #? fetch
	KW_MATCH            = "KW_MATCH"            #? match
	UNKNOWN             = "UNKNOWN"	# Copied wholesale for compatibility with libraries. should be registered for parsing with native python install

@regex
@api_level(0)
class YP:
	# Elements
	ELEM: type[__TT_NOHTYP] = __TT_NOHTYP
	# Regex dict
	REGEX: dict[str, str] = {
		# TODO: Redefine based on syntax spec
	}

@regex
@api_level(0)
class PY:
	# Elements
	ELEM: type[__TT_PYTHON] = __TT_PYTHON
	# Regex dict
	REGEX: dict[str, str] = {
		# --- literals ---
		__TT_PYTHON.INT: r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])",
		__TT_PYTHON.FLOAT: r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?",
		__TT_PYTHON.BOOL: r"\b(?:True|False)\b",
		__TT_PYTHON.NONE: r"\bNone\b",
		__TT_PYTHON.BYTES: r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'",
		__TT_PYTHON.BYTEARRAY: r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)",
		# TT_PYTHON.STR: rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?({'|'.join(REGEX_TT.string_quotes_ls)})([.\n]*)\5(\..+\(\)*',
		# --- identifiers / keywords ---
		__TT_PYTHON.ID: r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
		__TT_PYTHON.KEYWORD: r"\b(?:if|else|elif|while|for|def|class|return|import|from|as|pass|break|continue|try|except|finally|raise|with|yield|lambda|async|await|global|nonlocal|assert|del|match|case)\b",
		# --- operators ---
		__TT_PYTHON.OP: r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)",
		__TT_PYTHON.ASSIGN: r"=",
		__TT_PYTHON.AUGASSIGN: r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)",
		__TT_PYTHON.BITOP: r"(?:&|\||\^|~|<<|>>)",
		__TT_PYTHON.COMPARE: r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)",
		__TT_PYTHON.LOGIC: r"\b(?:and|or|not)\b",
		# --- punctuation ---
		__TT_PYTHON.PUNCT: r"(?:->|:|;|@|\.|,)",
		__TT_PYTHON.DOT: r"\.",
		__TT_PYTHON.COLON: r":",
		__TT_PYTHON.SEMICOLON: r";",
		__TT_PYTHON.ARROW: r"->",
		__TT_PYTHON.AT: r"@",
		# --- grouping ---
		__TT_PYTHON.LPAREN: r"\(",
		__TT_PYTHON.RPAREN: r"\)",
		__TT_PYTHON.LBRACE: r"\{",
		__TT_PYTHON.RBRACE: r"\}",
		__TT_PYTHON.LBRACKET: r"\[",
		__TT_PYTHON.RBRACKET: r"\]",
		# --- structures (heuristic, not syntax-perfect) ---
		__TT_PYTHON.LIST: r"\[[^\[\]]*\]",
		__TT_PYTHON.TUPLE: r"\([^()]*\)",
		__TT_PYTHON.SET: r"\{(?![^:]*:)[^{}]*\}",
		__TT_PYTHON.DICT: r"\{[^{}]*:[^{}]*\}",
		__TT_PYTHON.SLICE: r"[a-zA-Z_][\w]*\s*:\s*[a-zA-Z_0-9]*\s*(?::\s*[a-zA-Z_0-9]*)?",
		__TT_PYTHON.ELLIPSIS: r"\.\.\.",
		# --- functions / async / decorators ---
		__TT_PYTHON.LAMBDA: r"\blambda\b",
		__TT_PYTHON.YIELD: r"\byield(?:\s+from)?\b",
		__TT_PYTHON.AWAIT: r"\bawait\b",
		__TT_PYTHON.ASYNC: r"\basync\b",
		__TT_PYTHON.DECORATOR: r"@[a-zA-Z_][a-zA-Z0-9_\.]*",
		# --- type hints ---
		__TT_PYTHON.TYPEHINT: r"(?:->\s*[a-zA-Z_][\w\.\[\], ]*|:\s*[a-zA-Z_][\w\.\[\], ]*)",
		# --- strings / f-strings ---
		__TT_PYTHON.FSTRING: r"""(?x)
			f(?:\"\"\".*?\"\"\"|''' .*? '''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')
		""",
		__TT_PYTHON.FORMAT: r"\{[^{}]+\}",
		# --- comprehensions / generators (heuristic) ---
		__TT_PYTHON.LISTCOMP: r"\[[^\]]+for[^\]]+\]",
		__TT_PYTHON.SETCOMP: r"\{[^}]+for[^}]+\}",
		__TT_PYTHON.DICTCOMP: r"\{[^}]+:[^}]+for[^}]+\}",
		__TT_PYTHON.GENEXP: r"\([^)]+for[^)]+\)",
		# --- misc ---
		__TT_PYTHON.COMMENT: r"#.*",
		__TT_PYTHON.NEWLINE: r"\n",
		__TT_PYTHON.INDENT:   "(\t|\\ +|\n)",
		__TT_PYTHON.DEDENT:  r"",
	}

@api_level(0)
class Identify:
	"""Identify lexical objects"""
	def single_element(element :str) -> LexObject:
		"""Try to identify a single lexical object in a `str` container"""
		for key, regex in YP.REGEX:
			if re.match(regex, element):
				return LexObject(element, YP.ELEM[key])
		for key, regex in PY.REGEX:
			if re.match(regex, element):
				return LexObject(element, PY.ELEM[key])
		return LexObject(element, ...)
	def series(elements :TokenSeries) -> LexObjectSeries:
		result = LexObjectSeries()
		for i in elements:
			result.append(Identify.single_element(i))
		return result
