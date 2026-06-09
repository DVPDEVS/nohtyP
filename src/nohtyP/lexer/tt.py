from __future__ import annotations
from nohtyP.global_utilities.decorators import regex, api_level
from nohtyP.lexer.types import *

# Native int                    -> 123, 0, -42, 0b1010, 0o77, 0xFF
# Native float                  -> 1.23, .5, 10., 1e10, -3.4e-2
# Native bool                   -> True, False
# NoneType                      -> None
# Native bytes                  -> b"bytes", br"raw"
# Native bytearray              -> bytearray(b"bytes")
# Native str                    -> "text", 'text', """text""", r"raw", f"format"

# Known identifiers             -> variable_name, _private, ClassName
# Python keywords               -> if, else, while, def, class, return, import
# Operators                     -> +, -, *, /, //, %, **, =, ==, !=, <, >, <=, >=, and, or, not, is, in
# General punctuation           -> :, ;, ., @, = (contextual), ->
# End of file/input             -> <EOF>

# Native list literal           -> [1, 2, 3]
# Native tuple literal          -> (1, 2), ()
# Native set literal            -> {1, 2, 3}
# Native dict literal           -> {"a": 1, "b": 2}
# Ellipsis object               -> ...
# Slice syntax                  -> a:b, a:b:c

# Left parenthesis              -> (
# Right parenthesis             -> )
# Left brace                    -> {
# Right brace                   -> }
# Left bracket                  -> (
# Right bracket                 -> ]

# Attribute access              -> .
# Colon                         -> :
# Statement separator           -> ;
# Function return annotation    -> ->
# Decorator/operator            -> @

# Assignment                    -> =
# Augmented assignment          -> +=, -=, *=, /=, //=, %=, **=, &=, |=, ^=, <<=, >>=

# Bitwise operators             -> &, |, ^, ~, <<, >>
# Comparison operators          -> ==, !=, <, >, <=, >=, is, is not, in, not in
# Logical operators             -> and, or, not

# Line break                    -> \n
# Indentation increase          -> (whitespace block start)
# Indentation decrease          -> (whitespace block end)

# Comment                       -> # comment text
# Formatted string              -> f"{x}", f"text {expr}"
# Format specifier (inside fstr)-> {value:.2f}

# Generator expression          -> (x for x in y)
# List comprehension            -> [x for x in y]
# Set comprehension             -> {x for x in y}
# Dict comprehension            -> {k: v for k, v in y}

# Lambda expression             -> lambda x: x + 1
# Yield expression              -> yield x, yield from x
# Await expression              -> await coro()
# Async keyword                 -> async def, async for

# Decorator usage               -> @decorator
# Type annotations              -> x: int, -> str

@regex
@api_level(0)
class TT:
	YP: dict[str, tuple[str, LexType]] = {
		#! nohtyP elements
		"SEPARATOR" :(
			r";", # shouldnt require boundaries but they wont hurt either
			LexType("SEPARATOR", lexer_langs.NOHTYP) ), #? ;
		"BAREWORD" :(
			r"\b(?<!\.)(?![0-9])[\w\.]*(?!\.+)\b", #* sauce: https://regex101.com/r/fPlKx6/1 --- but fucking christ lookbehind/lookahead is painful to use with boundaries
			LexType("BAREWORD", lexer_langs.NOHTYP) ), #? <anything>
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
		"GEN_AST" :(
			r"\*",
			LexType("GEN_AST", lexer_langs.NOHTYP) ), #? *
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
		"KW_GO" :(
			r"(?<!\.)go(?!\.)", # case sensitive
			LexType("KW_GO", lexer_langs.NOHTYP) ), #? go
		"KW_FETCH" :(
			r"(?<!\.)fetch(?!\.)", # case sensitive
			LexType("KW_FETCH", lexer_langs.NOHTYP) ), #? fetch
		"KW_MATCH" :(
			r"(?<!\.)match(?!\.)", # case sensitive
			LexType("KW_MATCH", lexer_langs.NOHTYP) ), #? match
	}
	G: dict[str, tuple[str, LexType]] = {
		#! Generic elements
		"UNKNOWN" :(
			"",
			LexType("UNKNOWN", lexer_langs.GENERIC)	),
	}
	PY: dict[str, tuple[str, LexType]] = {
		#! Python elements
		# --- literals ---
		"INT" :(
			r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])" , 
			LexType("INT", lexer_langs.PYTHON) ),
		"FLOAT" :(
			r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?" , 
			LexType("FLOAT", lexer_langs.PYTHON) ),
		"BOOL" :(
			r"\b(?:True|False)\b" , 
			LexType("BOOL", lexer_langs.PYTHON) ),
		"NONE" :(
			r"\bNone\b" , 
			LexType("NONE", lexer_langs.PYTHON) ),
		"BYTES" :(
			r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'" , 
			LexType("BYTES", lexer_langs.PYTHON) ),
		"BYTEARRAY" :(
			r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)" , 
			LexType("BYTEARRAY", lexer_langs.PYTHON) ),
		"STR" :(
			rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?(\'|\"|´|`|\"\"\"|\'\'\')([.\n]*)\5(\..+\(\)*' , 
			LexType("STR", lexer_langs.PYTHON) ),
		# --- identifiers / keywords ---
		"ID" :(
			r"\b[a-zA-Z_][a-zA-Z0-9_]*\b" , 
			LexType("ID", lexer_langs.PYTHON) ),
		"KEYWORD" :(
			r"\b(?:if|else|elif|while|for|def|class|return|import|from|as|pass|break|continue|try|except|finally|raise|with|yield|lambda|async|await|global|nonlocal|assert|del|match|case)\b" , 
			LexType("KEYWORD", lexer_langs.PYTHON) ),
		# --- operators ---
		"OP" :(
			r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)" , 
			LexType("OP", lexer_langs.PYTHON) ),
		"ASSIGN" :(
			r"=" , 
			LexType("ASSIGN", lexer_langs.PYTHON) ),
		"AUGASSIGN" :(
			r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)" , 
			LexType("AUGASSIGN", lexer_langs.PYTHON) ),
		"BITOP" :(
			r"(?:&|\||\^|~|<<|>>)" , 
			LexType("BITOP", lexer_langs.PYTHON) ),
		"COMPARE" :(
			r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)" , 
			LexType("COMPARE", lexer_langs.PYTHON) ),
		"LOGIC" :(
			r"\b(?:and|or|not)\b" , 
			LexType("LOGIC", lexer_langs.PYTHON) ),
		# --- punctuation ---
		"PUNCT" :(
			r"(?:->|:|;|@|\.|,)" , 
			LexType("PUNCT", lexer_langs.PYTHON) ),
		"DOT" :(
			r"\." , 
			LexType("DOT", lexer_langs.PYTHON) ),
		"COLON" :(
			r":" , 
			LexType("COLON", lexer_langs.PYTHON) ),
		"SEMICOLON" :(
			r";" , 
			LexType("SEMICOLON", lexer_langs.PYTHON) ),
		"ARROW" :(
			r"->" , 
			LexType("ARROW", lexer_langs.PYTHON) ),
		"AT" :(
			r"@" , 
			LexType("AT", lexer_langs.PYTHON) ),
		# --- grouping ---
		"LPAREN" :(
			r"\(" , 
			LexType("LPAREN", lexer_langs.PYTHON) ),
		"RPAREN" :(
			r"\)" , 
			LexType("RPAREN", lexer_langs.PYTHON) ),
		"LBRACE" :(
			r"\{" , 
			LexType("LBRACE", lexer_langs.PYTHON) ),
		"RBRACE" :(
			r"\}" , 
			LexType("RBRACE", lexer_langs.PYTHON) ),
		"LBRACKET" :(
			r"\[" , 
			LexType("LBRACKET", lexer_langs.PYTHON) ),
		"RBRACKET" :(
			r"\]" , 
			LexType("RBRACKET", lexer_langs.PYTHON) ),
		# --- structures (heuristic, not syntax-perfect) ---
		"LIST" :(
			r"\[[^\[\]]*\]" , 
			LexType("LIST", lexer_langs.PYTHON) ),
		"TUPLE" :(
			r"\([^()]*\)" , 
			LexType("TUPLE", lexer_langs.PYTHON) ),
		"SET" :(
			r"\{(?![^:]*:)[^{}]*\}" , 
			LexType("SET", lexer_langs.PYTHON) ),
		"DICT" :(
			r"\{[^{}]*:[^{}]*\}" , 
			LexType("DICT", lexer_langs.PYTHON) ),
		"SLICE" :(
			r"[a-zA-Z_][\w]*\s*:\s*[a-zA-Z_0-9]*\s*(?::\s*[a-zA-Z_0-9]*)?" , 
			LexType("SLICE", lexer_langs.PYTHON) ),
		"ELLIPSIS" :(
			r"\.\.\." , 
			LexType("ELLIPSIS", lexer_langs.PYTHON) ),
		# --- functions / async / decorators ---
		"LAMBDA" :(
			r"\blambda\b" , 
			LexType("LAMBDA", lexer_langs.PYTHON) ),
		"YIELD" :(
			r"\byield(?:\s+from)?\b" , 
			LexType("YIELD", lexer_langs.PYTHON) ),
		"AWAIT" :(
			r"\bawait\b" , 
			LexType("AWAIT", lexer_langs.PYTHON) ),
		"ASYNC" :(
			r"\basync\b" , 
			LexType("ASYNC", lexer_langs.PYTHON) ),
		"DECORATOR" :(
			r"@[a-zA-Z_][a-zA-Z0-9_\.]*" , 
			LexType("DECORATOR", lexer_langs.PYTHON) ),
		# --- type hints ---
		"TYPEHINT" :(
			r"(?:->\s*[a-zA-Z_][\w\.\[\), ]*|:\s*[a-zA-Z_][\w\.\[\), ]*)" , 
			LexType("TYPEHINT", lexer_langs.PYTHON) ),
		# --- strings / f-strings ---
		"FSTRING" :(
			r"(?x )f(?:\"\"\".*?\"\"\"|''' .*? '''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')",
			LexType("FSTRING", lexer_langs.PYTHON) ),
		"FORMAT" :(
			r"\{[^{}]+\}" , 
			LexType("FORMAT", lexer_langs.PYTHON) ),
		# --- comprehensions / generators (heuristic) ---
		"LISTCOMP" :(
			r"\[[^\]]+for[^\]]+\]" , 
			LexType("LISTCOMP", lexer_langs.PYTHON) ),
		"SETCOMP" :(
			r"\{[^}]+for[^}]+\}" , 
			LexType("SETCOMP", lexer_langs.PYTHON) ),
		"DICTCOMP" :(
			r"\{[^}]+:[^}]+for[^}]+\}" , 
			LexType("DICTCOMP", lexer_langs.PYTHON) ),
		"GENEXP" :(
			r"\([^)]+for[^)]+\)" , 
			LexType("GENEXP", lexer_langs.PYTHON) ),
		# --- misc ---
		"COMMENT" :(
			r"#.*" , 
			LexType("COMMENT", lexer_langs.PYTHON) ),
		"NEWLINE" :(
			r"\n" , 
			LexType("NEWLINE", lexer_langs.PYTHON) ),
		"INDENT" :(
			"(\t|\\ +|\n)" , 
			LexType("INDENT", lexer_langs.PYTHON) ),
		"DEDENT" :(
			r"" , 
			LexType("DEDENT", lexer_langs.PYTHON) ),
	}

