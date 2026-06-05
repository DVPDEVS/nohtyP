from __future__ import annotations
from nohtyP.global_utilities import decorators
from nohtyP.lexer.types import *
import re
# Identify objects

class TT_PYTHON:
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

class TT_NOHTYP:
	# nohtyP lex types and objects
	# TODO: Redefine based on syntax spec
	UNKNOWN                        = "UNKNOWN"	# Copied wholesale for compatibility with libraries. should be registered for parsing with native python install

#? yp regex
NOHTYP: dict[str, str] = {
	# TODO: Redefine based on syntax spec
}
#? py regex
class PYTHON:
	_values: dict[str, str] = {
		# --- literals ---
		TT_PYTHON.INT: r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])",
		TT_PYTHON.FLOAT: r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?",
		TT_PYTHON.BOOL: r"\b(?:True|False)\b",
		TT_PYTHON.NONE: r"\bNone\b",
		TT_PYTHON.BYTES: r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'",
		TT_PYTHON.BYTEARRAY: r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)",
		# TT_PYTHON.STR: rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?({'|'.join(REGEX_TT.string_quotes_ls)})([.\n]*)\5(\..+\(\)*',
		# --- identifiers / keywords ---
		TT_PYTHON.ID: r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
		TT_PYTHON.KEYWORD: r"\b(?:if|else|elif|while|for|def|class|return|import|from|as|pass|break|continue|try|except|finally|raise|with|yield|lambda|async|await|global|nonlocal|assert|del|match|case)\b",
		# --- operators ---
		TT_PYTHON.OP: r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)",
		TT_PYTHON.ASSIGN: r"=",
		TT_PYTHON.AUGASSIGN: r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)",
		TT_PYTHON.BITOP: r"(?:&|\||\^|~|<<|>>)",
		TT_PYTHON.COMPARE: r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)",
		TT_PYTHON.LOGIC: r"\b(?:and|or|not)\b",
		# --- punctuation ---
		TT_PYTHON.PUNCT: r"(?:->|:|;|@|\.|,)",
		TT_PYTHON.DOT: r"\.",
		TT_PYTHON.COLON: r":",
		TT_PYTHON.SEMICOLON: r";",
		TT_PYTHON.ARROW: r"->",
		TT_PYTHON.AT: r"@",
		# --- grouping ---
		TT_PYTHON.LPAREN: r"\(",
		TT_PYTHON.RPAREN: r"\)",
		TT_PYTHON.LBRACE: r"\{",
		TT_PYTHON.RBRACE: r"\}",
		TT_PYTHON.LBRACKET: r"\[",
		TT_PYTHON.RBRACKET: r"\]",
		# --- structures (heuristic, not syntax-perfect) ---
		TT_PYTHON.LIST: r"\[[^\[\]]*\]",
		TT_PYTHON.TUPLE: r"\([^()]*\)",
		TT_PYTHON.SET: r"\{(?![^:]*:)[^{}]*\}",
		TT_PYTHON.DICT: r"\{[^{}]*:[^{}]*\}",
		TT_PYTHON.SLICE: r"[a-zA-Z_][\w]*\s*:\s*[a-zA-Z_0-9]*\s*(?::\s*[a-zA-Z_0-9]*)?",
		TT_PYTHON.ELLIPSIS: r"\.\.\.",
		# --- functions / async / decorators ---
		TT_PYTHON.LAMBDA: r"\blambda\b",
		TT_PYTHON.YIELD: r"\byield(?:\s+from)?\b",
		TT_PYTHON.AWAIT: r"\bawait\b",
		TT_PYTHON.ASYNC: r"\basync\b",
		TT_PYTHON.DECORATOR: r"@[a-zA-Z_][a-zA-Z0-9_\.]*",
		# --- type hints ---
		TT_PYTHON.TYPEHINT: r"(?:->\s*[a-zA-Z_][\w\.\[\], ]*|:\s*[a-zA-Z_][\w\.\[\], ]*)",
		# --- strings / f-strings ---
		TT_PYTHON.FSTRING: r"""(?x)
			f(?:\"\"\".*?\"\"\"|''' .*? '''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')
		""",
		TT_PYTHON.FORMAT: r"\{[^{}]+\}",
		# --- comprehensions / generators (heuristic) ---
		TT_PYTHON.LISTCOMP: r"\[[^\]]+for[^\]]+\]",
		TT_PYTHON.SETCOMP: r"\{[^}]+for[^}]+\}",
		TT_PYTHON.DICTCOMP: r"\{[^}]+:[^}]+for[^}]+\}",
		TT_PYTHON.GENEXP: r"\([^)]+for[^)]+\)",
		# --- misc ---
		TT_PYTHON.COMMENT: r"#.*",
		TT_PYTHON.NEWLINE: r"\n",
		TT_PYTHON.INDENT:   "(\t|\\ +|\n)",
		TT_PYTHON.DEDENT:  r"",
	}

class Identify:
	def single_element(element :str) -> LexObject:
		for k, v in NOHTYP:
			if re.match(v, element):
				return LexObject(element, TT_NOHTYP[k])
	def series(elements :TokenSeries) -> LexObjectSeries:
		result = LexObjectSeries()
		for i in elements:
			result.append(Identify.single_element(i))
		return result
