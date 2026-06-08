from __future__ import annotations
from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.types import *
import re
# Identify objects

@api_level(0)
class __TT_PYTHON:
	"""Holds lexical elements for Python"""
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
	"""Holds lexical elements for nohtyP"""
	def __class_getitem__(cls, key :str):
		return cls.__getattribute__(key)
	# nohtyP lexical objects
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
	EXCEPT_SET          = "EXCEPT_SET"          #? *set -e/+e
	KW_GO               = "KW_GO"               #? go
	KW_FETCH            = "KW_FETCH"            #? fetch
	KW_MATCH            = "KW_MATCH"            #? match

@regex
@api_level(0)
class YP:
	# Elements
	ELEM: type[__TT_NOHTYP] = __TT_NOHTYP
	# Regex dict
	REGEX: dict[str, str] = {
		# TODO: Redefine based on syntax spec
		ELEM.SEPARATOR           : r";", # shouldnt require boundaries but they wont hurt either
		ELEM.BAREWORD            : r"\b(?<!\.)(?![0-9])[\w\.]*(?!\.+)\b", #* sauce: https://regex101.com/r/fPlKx6/1 --- but fucking christ lookbehind/lookahead is painful to use with boundaries
		ELEM.CBRACKET_LEFT       : r"\{",
		ELEM.CBRACKET_RIGHT      : r"\}",
		ELEM.ASS_EQ              : r"=",
		ELEM.FLOW_Q              : r"\?",
		ELEM.FLOW_HASH_Q         : r"#\?",
		ELEM.GEN_AST             : r"\*",
		ELEM.WHILE               : r"\?=",
		ELEM.ITERATOR            : r"@",
		ELEM.CONDITION_TILDE     : r"~",
		ELEM.CONDITION_AST_TILDE : r"\*~",
		ELEM.ARROW_LEFT          : r"<-",
		ELEM.ARROW_RIGHT         : r"->",
		ELEM.EXCEPT_STORE        : r"\b(?<!\.)\*\$[\w\.]*(?!\.+)\b",
		ELEM.EXCEPT_GET          : r"\b(?<!\.)\$[\w\.]*(?!\.+)\b",
		ELEM.EXCEPT_HANDLE       : r"\*\?",
		ELEM.EXCEPT_SET          : r"(?<!\.)\*set\ [-+]e(?!\.)", #* sauce: https://regex101.com/r/3QG7Y0/1	# case sensitive
		ELEM.KW_GO               : r"(?<!\.)go(?!\.)",														# case sensitive
		ELEM.KW_FETCH            : r"(?<!\.)fetch(?!\.)",													# case sensitive
		ELEM.KW_MATCH            : r"(?<!\.)match(?!\.)",													# case sensitive
	}

#! add a generic unknown lexical obj here

@regex
@api_level(0)
class PY:
	# Elements
	ELEM: type[__TT_PYTHON] = __TT_PYTHON
	# Regex dict
	REGEX: dict[str, str] = {
		# --- literals ---
		ELEM.INT: r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])",
		ELEM.FLOAT: r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?",
		ELEM.BOOL: r"\b(?:True|False)\b",
		ELEM.NONE: r"\bNone\b",
		ELEM.BYTES: r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'",
		ELEM.BYTEARRAY: r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)",
		# TT_PYTHON.STR: rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?({'|'.join(REGEX_TT.string_quotes_ls)})([.\n]*)\5(\..+\(\)*',
		# --- identifiers / keywords ---
		ELEM.ID: r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
		ELEM.KEYWORD: r"\b(?:if|else|elif|while|for|def|class|return|import|from|as|pass|break|continue|try|except|finally|raise|with|yield|lambda|async|await|global|nonlocal|assert|del|match|case)\b",
		# --- operators ---
		ELEM.OP: r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)",
		ELEM.ASSIGN: r"=",
		ELEM.AUGASSIGN: r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)",
		ELEM.BITOP: r"(?:&|\||\^|~|<<|>>)",
		ELEM.COMPARE: r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)",
		ELEM.LOGIC: r"\b(?:and|or|not)\b",
		# --- punctuation ---
		ELEM.PUNCT: r"(?:->|:|;|@|\.|,)",
		ELEM.DOT: r"\.",
		ELEM.COLON: r":",
		ELEM.SEMICOLON: r";",
		ELEM.ARROW: r"->",
		ELEM.AT: r"@",
		# --- grouping ---
		ELEM.LPAREN: r"\(",
		ELEM.RPAREN: r"\)",
		ELEM.LBRACE: r"\{",
		ELEM.RBRACE: r"\}",
		ELEM.LBRACKET: r"\[",
		ELEM.RBRACKET: r"\]",
		# --- structures (heuristic, not syntax-perfect) ---
		ELEM.LIST: r"\[[^\[\]]*\]",
		ELEM.TUPLE: r"\([^()]*\)",
		ELEM.SET: r"\{(?![^:]*:)[^{}]*\}",
		ELEM.DICT: r"\{[^{}]*:[^{}]*\}",
		ELEM.SLICE: r"[a-zA-Z_][\w]*\s*:\s*[a-zA-Z_0-9]*\s*(?::\s*[a-zA-Z_0-9]*)?",
		ELEM.ELLIPSIS: r"\.\.\.",
		# --- functions / async / decorators ---
		ELEM.LAMBDA: r"\blambda\b",
		ELEM.YIELD: r"\byield(?:\s+from)?\b",
		ELEM.AWAIT: r"\bawait\b",
		ELEM.ASYNC: r"\basync\b",
		ELEM.DECORATOR: r"@[a-zA-Z_][a-zA-Z0-9_\.]*",
		# --- type hints ---
		ELEM.TYPEHINT: r"(?:->\s*[a-zA-Z_][\w\.\[\], ]*|:\s*[a-zA-Z_][\w\.\[\], ]*)",
		# --- strings / f-strings ---
		ELEM.FSTRING: r"""(?x)
			f(?:\"\"\".*?\"\"\"|''' .*? '''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')
		""",
		ELEM.FORMAT: r"\{[^{}]+\}",
		# --- comprehensions / generators (heuristic) ---
		ELEM.LISTCOMP: r"\[[^\]]+for[^\]]+\]",
		ELEM.SETCOMP: r"\{[^}]+for[^}]+\}",
		ELEM.DICTCOMP: r"\{[^}]+:[^}]+for[^}]+\}",
		ELEM.GENEXP: r"\([^)]+for[^)]+\)",
		# --- misc ---
		ELEM.COMMENT: r"#.*",
		ELEM.NEWLINE: r"\n",
		ELEM.INDENT:   "(\t|\\ +|\n)",
		ELEM.DEDENT:  r"",
	}

@regex
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
