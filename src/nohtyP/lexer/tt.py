from __future__ import annotations
from nohtyP.global_utilities.decorators import regex, api_level
from nohtyP.lexer.types import *

@regex
@api_level(0)
class TT:
	ELEM: dict[str, tuple[str, LexType]] = {
		#! nohtyP elements
		"SEPARATOR" :(
			r";", # shouldnt require boundaries but they wont hurt either
			LexType("SEPARATOR", lexer_langs.NOHTYP) ), #? ;
		"BAREWORD" :(
			r"^(?<![\.])(?![0-9])[\w\.]*(?!\.+)$", #* sauce: https://regex101.com/r/L0MnX3/1 
			LexType("BAREWORD", lexer_langs.NOHTYP) ), #? <anything>
		"TYPE_DECLARATION" :(
			r"^\:\s?(?<![\.])(?![0-9])[\w\.]*(?!\.+)$", #* sauce: https://regex101.com/r/FniyHg/2 
			LexType("TYPE_DECLARATION", lexer_langs.NOHTYP) ), #? bareword preceded by a colon and optional whitespace
		"CBRACKET_LEFT" :(
			r"\{",
			LexType("CBRACKET_LEFT", lexer_langs.NOHTYP) ), #? {
		"CBRACKET_RIGHT" :(
			r"\}",
			LexType("CBRACKET_RIGHT", lexer_langs.NOHTYP) ), #? }
		"ASS_EQ" :(
			r"=",
			LexType("ASS_EQ", lexer_langs.NOHTYP) ), #? =
		"FLOW_Q" :(
			r"\?",
			LexType("FLOW_Q", lexer_langs.NOHTYP) ), #? ?
		"FLOW_HASH_Q" :(
			r"#\?",
			LexType("FLOW_HASH_Q", lexer_langs.NOHTYP) ), #? #?
		"WHILE" :(
			r"\?=",
			LexType("WHILE", lexer_langs.NOHTYP) ), #? ?=
		"ITERATOR" :(
			r"@",
			LexType("ITERATOR", lexer_langs.NOHTYP) ), #? @
		"CONDITION_TILDE" :(
			r"~",
			LexType("CONDITION_TILDE", lexer_langs.NOHTYP) ), #? ~
		"CONDITION_AST_TILDE" :(
			r"\*~",
			LexType("CONDITION_AST_TILDE", lexer_langs.NOHTYP) ), #? *~
		"ARROW_LEFT" :(
			r"<-",
			LexType("ARROW_LEFT", lexer_langs.NOHTYP) ), #? <-
		"ARROW_RIGHT" :(
			r"->",
			LexType("ARROW_RIGHT", lexer_langs.NOHTYP) ), #? ->
		"EXCEPT_STORE" :(
			r"\b(?<!\.)\*\$[\w\.]*(?!\.+)\b",
			LexType("EXCEPT_STORE", lexer_langs.NOHTYP) ), #? *$<insert var>
		"EXCEPT_GET" :(
			r"\b(?<!\.)\$[\w\.]*(?!\.+)\b",
			LexType("EXCEPT_GET", lexer_langs.NOHTYP) ), #? $<insert var>
		"EXCEPT_HANDLE" :(
			r"\*\?",
			LexType("EXCEPT_HANDLE", lexer_langs.NOHTYP) ), #? *?
		"EXCEPT_SET" :(
			r"(?<!\.)\*set\ [-+]e(?!\.)", #* sauce: https://regex101.com/r/3QG7Y0/1 # case sensitive
			LexType("EXCEPT_SET", lexer_langs.NOHTYP) ), #? *set -e/+e
		"KW_FETCH" :(
			r"(?<!\.)fetch(?!\.)", # case sensitive
			LexType("KW_FETCH", lexer_langs.NOHTYP) ), #? fetch
		"KW_MATCH" :(
			r"(?<!\.)match(?!\.)", # case sensitive
			LexType("KW_MATCH", lexer_langs.NOHTYP) ), #? match
		#! Generic elements
		"UNKNOWN" :(
			"",
			LexType("UNKNOWN", lexer_langs.GENERIC)	),
		"STAR" :(
			r"\*",
			LexType("STAR", lexer_langs.GENERIC) ), #? *
		#! Python elements
		# --- literals ---
		# Native int                 -> 123, 0, -42, 0b1010, 0o77, 0xFF
		"INT" :(
			r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])" , 
			LexType("INT", lexer_langs.PYTHON) ),
		# Native float               -> 1.23, .5, 10., 1e10, -3.4e-2
		"FLOAT" :(
			r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?" , 
			LexType("FLOAT", lexer_langs.PYTHON) ),
		# Native bool                -> True, False
		"BOOL" :(
			r"\b(?:True|False)\b" , 
			LexType("BOOL", lexer_langs.PYTHON) ),
		# NoneType                   -> None
		"NONE" :(
			r"\bNone\b" , 
			LexType("NONE", lexer_langs.PYTHON) ),
		# Native bytes               -> b"bytes", br"raw"
		"BYTES" :(
			r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'" , 
			LexType("BYTES", lexer_langs.PYTHON) ),
		# Native bytearray           -> bytearray(b"bytes")
		"BYTEARRAY" :(
			r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)" , 
			LexType("BYTEARRAY", lexer_langs.PYTHON) ),
		# Native str                 -> "text", 'text', """text""", r"raw", f"format"
		"STR" :(
			rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?(\'|\"|´|`|\"\"\"|\'\'\')([.\n]*)\5(\..+\(\)*' , 
			LexType("STR", lexer_langs.PYTHON) ),
		# --- identifiers / keywords ---
		# Known identifiers          -> variable_name, _private, ClassName
		"ID" :(
			r"\b[a-zA-Z_][a-zA-Z0-9_]*\b" , 
			LexType("ID", lexer_langs.PYTHON) ),
		# Python keywords            -> if, else, while, def, class, return, import
		"KEYWORD" :(
			r"\b(?:if|else|elif|while|for|def|class|return|import|from|as|pass|break|continue|try|except|finally|raise|with|yield|lambda|async|await|global|nonlocal|assert|del|match|case)\b" , 
			LexType("KEYWORD", lexer_langs.PYTHON) ),
		# --- operators ---
		# Operators                  -> +, -, *, /, //, %, **, =, ==, !=, <, >, <=, >=, and, or, not, is, in
		"OP" :(
			r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)" , 
			LexType("OP", lexer_langs.PYTHON) ),
		# Assignment                 -> =
		"ASSIGN" :(
			r"=" , 
			LexType("ASSIGN", lexer_langs.PYTHON) ),
		# Augmented assignment       -> +=, -=, *=, /=, //=, %=, **=, &=, |=, ^=, <<=, >>=
		"AUGASSIGN" :(
			r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)" , 
			LexType("AUGASSIGN", lexer_langs.PYTHON) ),
		# Bitwise operators         -> &, |, ^, ~, <<, >>
		"BITOP" :(
			r"(?:&|\||\^|~|<<|>>)" , 
			LexType("BITOP", lexer_langs.PYTHON) ),
		# Comparison operators      -> ==, !=, <, >, <=, >=, is, is not, in, not in
		"COMPARE" :(
			r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)" , 
			LexType("COMPARE", lexer_langs.PYTHON) ),
		# Logical operators         -> and, or, not
		"LOGIC" :(
			r"\b(?:and|or|not)\b" , 
			LexType("LOGIC", lexer_langs.PYTHON) ),
		# --- punctuation ---
		# General punctuation       -> :, ;, ., @, = (contextual), ->
		"PUNCT" :(
			r"(?:->|:|;|@|\.|,)" , 
			LexType("PUNCT", lexer_langs.PYTHON) ),
		# Attribute access          -> .
		"DOT" :(
			r"\." , 
			LexType("DOT", lexer_langs.PYTHON) ),
		# Colon                     -> :
		"COLON" :(
			r":" , 
			LexType("COLON", lexer_langs.PYTHON) ),
		# Statement separator       -> ;
		"SEMICOLON" :(
			r";" , 
			LexType("SEMICOLON", lexer_langs.PYTHON) ),
		# Function return annotation -> ->
		"ARROW" :(
			r"->" , 
			LexType("ARROW", lexer_langs.PYTHON) ),
		# Decorator/operator        -> @
		"AT" :(
			r"@" , 
			LexType("AT", lexer_langs.PYTHON) ),
		# --- grouping ---
		# Left parenthesis          -> (
		"LPAREN" :(
			r"\(" , 
			LexType("LPAREN", lexer_langs.PYTHON) ),
		# Right parenthesis         -> )
		"RPAREN" :(
			r"\)" , 
			LexType("RPAREN", lexer_langs.PYTHON) ),
		# Left brace                -> {
		"LBRACE" :(
			r"\{" , 
			LexType("LBRACE", lexer_langs.PYTHON) ),
		# Right brace               -> }
		"RBRACE" :(
			r"\}" , 
			LexType("RBRACE", lexer_langs.PYTHON) ),
		# Left bracket              -> [
		"LBRACKET" :(
			r"\[" , 
			LexType("LBRACKET", lexer_langs.PYTHON) ),
		# Right bracket             -> ]
		"RBRACKET" :(
			r"\]" , 
			LexType("RBRACKET", lexer_langs.PYTHON) ),
		# --- structures (heuristic, not syntax-perfect) ---
		# Native list literal       -> [1, 2, 3]
		"LIST" :(
			r"\[[^\[\]]*\]" , 
			LexType("LIST", lexer_langs.PYTHON) ),
		# Native tuple literal      -> (1, 2), ()
		"TUPLE" :(
			r"\([^()]*\)" , 
			LexType("TUPLE", lexer_langs.PYTHON) ),
		# Native set literal        -> {1, 2, 3}
		"SET" :(
			r"\{(?![^:]*:)[^{}]*\}" , 
			LexType("SET", lexer_langs.PYTHON) ),
		# Native dict literal       -> {"a": 1, "b": 2}
		"DICT" :(
			r"\{[^{}]*:[^{}]*\}" , 
			LexType("DICT", lexer_langs.PYTHON) ),
		# Slice syntax              -> a:b, a:b:c
		"SLICE" :(
			r"[a-zA-Z_][\w]*\s*:\s*[a-zA-Z_0-9]*\s*(?::\s*[a-zA-Z_0-9]*)?" , 
			LexType("SLICE", lexer_langs.PYTHON) ),
		# Ellipsis object           -> ...
		"ELLIPSIS" :(
			r"\.\.\." , 
			LexType("ELLIPSIS", lexer_langs.PYTHON) ),
		# --- functions / async / decorators ---
		# Lambda expression         -> lambda x: x + 1
		"LAMBDA" :(
			r"\blambda\b" , 
			LexType("LAMBDA", lexer_langs.PYTHON) ),
		# Yield expression          -> yield x, yield from x
		"YIELD" :(
			r"\byield(?:\s+from)?\b" , 
			LexType("YIELD", lexer_langs.PYTHON) ),
		# Await expression          -> await coro()
		"AWAIT" :(
			r"\bawait\b" , 
			LexType("AWAIT", lexer_langs.PYTHON) ),
		# Async keyword             -> async def, async for
		"ASYNC" :(
			r"\basync\b" , 
			LexType("ASYNC", lexer_langs.PYTHON) ),
		# Decorator usage           -> @decorator
		"DECORATOR" :(
			r"@[a-zA-Z_][a-zA-Z0-9_\.]*" , 
			LexType("DECORATOR", lexer_langs.PYTHON) ),
		# --- type hints ---
		# Type annotations          -> x: int, -> str
		"TYPEHINT" :(
			r"(?:->\s*[a-zA-Z_][\w\.\[\), ]*|:\s*[a-zA-Z_][\w\.\[\), ]*)" , 
			LexType("TYPEHINT", lexer_langs.PYTHON) ),
		# --- strings / f-strings ---
		# Formatted string          -> f"{x}", f"text {expr}"
		"FSTRING" :(
			r"(?x )f(?:\"\"\".*?\"\"\"|''' .*? '''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')",
			LexType("FSTRING", lexer_langs.PYTHON) ),
		# Format specifier (inside fstr) -> {value:.2f}
		"FORMAT" :(
			r"\{[^{}]+\}" , 
			LexType("FORMAT", lexer_langs.PYTHON) ),
		# --- comprehensions / generators (heuristic) ---
		# Generator expression      -> (x for x in y)
		"GENEXP" :(
			r"\([^)]+for[^)]+\)" , 
			LexType("GENEXP", lexer_langs.PYTHON) ),
		# List comprehension        -> [x for x in y]
		"LISTCOMP" :(
			r"\[[^\]]+for[^\]]+\]" , 
			LexType("LISTCOMP", lexer_langs.PYTHON) ),
		# Set comprehension         -> {x for x in y}
		"SETCOMP" :(
			r"\{[^}]+for[^}]+\}" , 
			LexType("SETCOMP", lexer_langs.PYTHON) ),
		# Dict comprehension        -> {k: v for k, v in y}
		"DICTCOMP" :(
			r"\{[^}]+:[^}]+for[^}]+\}" , 
			LexType("DICTCOMP", lexer_langs.PYTHON) ),
		# --- misc ---
		# Comment                   -> # comment text
		"COMMENT" :(
			r"#.*" , 
			LexType("COMMENT", lexer_langs.PYTHON) ),
		# Line break                -> \n
		"NEWLINE" :(
			r"\n" , 
			LexType("NEWLINE", lexer_langs.PYTHON) ),
		# Indentation increase      -> (whitespace block start)
		"INDENT" :(
			"(\t|\\ +|\n)" , 
			LexType("INDENT", lexer_langs.PYTHON) ),
		# Indentation decrease      -> (whitespace block end)
		"DEDENT" :(
			r"" , 
			LexType("DEDENT", lexer_langs.PYTHON) ),
	}

