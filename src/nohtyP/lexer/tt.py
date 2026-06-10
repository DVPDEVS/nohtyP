from __future__ import annotations
from nohtyP.global_utilities.decorators import regex, api_level
from nohtyP.lexer.types import *

@regex
@api_level(0)
class TT:
	ELEM: dict[str, tuple[str, LexType]] = {
		#! nohtyP elements
		"SEMICOLON" :(
			r";", # shouldnt require boundaries but they wont hurt either
			LexType("SEMICOLON", lexer_langs.NOHTYP) ), #? ;
		"BAREWORD" :(
			r"^(?![\.])(?![0-9])[\w\.]+(?<![\.])$", #* sauce: https://regex101.com/r/L0MnX3/2 
			LexType("BAREWORD", lexer_langs.NOHTYP) ), #? <anything>
		"TYPE_DECLARATION" :(
			r"^\*?(?![\.])(?![0-9])[\w\.]+(?<![\.])\:$", #* sauce: https://regex101.com/r/lhwcEL/1 
			LexType("TYPE_DECLARATION", lexer_langs.NOHTYP) ), #? optional * followed by a bareword and a :
		"CBRACKET_LEFT" :(
			r"\{",
			LexType("CBRACKET_LEFT", lexer_langs.NOHTYP) ), #? {
		"CBRACKET_RIGHT" :(
			r"\}",
			LexType("CBRACKET_RIGHT", lexer_langs.NOHTYP) ), #? }
		"BRACKET_LEFT" :(
			r"\[",
			LexType("BRACKET_LEFT", lexer_langs.NOHTYP) ), #? [
		"BRACKET_RIGHT" :(
			r"\]",
			LexType("BRACKET_RIGHT", lexer_langs.NOHTYP) ), #? ]
		"PAREN_LEFT" :(
			r"\(",
			LexType("PAREN_LEFT", lexer_langs.NOHTYP) ), #? (
		"PAREN_RIGHT" :(
			r"\)",
			LexType("PAREN_RIGHT", lexer_langs.NOHTYP) ), #? )
		"ASS_EQ" :(
			r"=",
			LexType("ASS_EQ", lexer_langs.NOHTYP) ), #? =
		"FLOW_Q" :(
			r"\?",
			LexType("FLOW_Q", lexer_langs.NOHTYP) ), #? ?
		"FLOW_HASH_Q" :(
			r"#\?",
			LexType("FLOW_HASH_Q", lexer_langs.NOHTYP) ), #? #?
		"FLOW_WHILE" :(
			r"\?=",
			LexType("FLOW_WHILE", lexer_langs.NOHTYP) ), #? ?=
		"SYMBOL_AT" :(
			r"@",
			LexType("SYMBOL_AT", lexer_langs.NOHTYP) ), #? @
		"TILDE" :(
			r"~",
			LexType("TILDE", lexer_langs.NOHTYP) ), #? ~
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
		#* Covered by native string
		# Native bytearray           -> bytearray(b"bytes")
		#* Just native bytes flowed into bytearray()
		# Native str                 -> "text", 'text', """text""", r"raw", f"format"
		"STR" :(
			rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?(\'|\"|´|`|\"\"\"|\'\'\')([.\n]*)\5(\..+\(\)*' , #* sauce : https://regex101.com/r/Hhihv5/1 
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
		# Augmented assignment       -> +=, -=, *=, /=, //=, %=, **=, &=, |=, ^=, <<=, >>=
		"AUGASSIGN" :(
			r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)" , 
			LexType("AUGASSIGN", lexer_langs.PYTHON) ),
		# Bitwise operators         -> &, |, ^, ~, <<, >>
		"BITOP" :(
			r"(?:&|\||\^|~|<<|>>)" , #! ~ will be consumed by earlier nohtyp lex
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
			r"(?:->|:|;|@|\.|,)" , #! -> will be consumed by earlier nohtyp lex
			LexType("PUNCT", lexer_langs.PYTHON) ),
		# Attribute access          -> .
		"DOT" :(
			r"\." , 
			LexType("DOT", lexer_langs.PYTHON) ),
		# Colon                     -> :
		"COLON" :(
			r":" , 
			LexType("COLON", lexer_langs.PYTHON) ),
		# Function return annotation -> ->
			#! -> will be consumed by earlier nohtyp lex
		# Decorator/operator        -> @
			#! @ will be consumed by earlier nohtyp lex
		# --- structures (heuristic, not syntax-perfect) ---
		# Native list literal       -> [1, 2, 3]
			#! all new syntax handled in the parser
		# Native tuple literal      -> (1, 2), ()
			#! all new syntax handled in the parser
		# Native set literal        -> {1, 2, 3}
			#! all new syntax handled in the parser
		# Native dict literal       -> {"a": 1, "b": 2}
			#! all new syntax handled in the parser
		# Slice syntax              -> a:b, a:b:cssssss
		"SLICE" :(
			r"^(?![\.])[\w\.]+(?<![\.])*\s*:\s*(?![\.])[\w\.]+(?<![\.])*\s*(?::\s*(?![\.])[\w\.]+(?<![\.])*)?$" , 
			LexType("SLICE", lexer_langs.PYTHON) ), #* additionally needs validation as it should be in an index block []
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
			#! should be considered in lex val or parser.
		# --- strings / f-strings ---
		# Formatted string          -> f"{x}", f"text {expr}"
			#! covered by earlier string def
		# Format specifier (inside fstr) -> {value:.2f}
			#! not considered in nohtyp
		# --- comprehensions / generators (heuristic) ---
			#! not considered in nohtyp
		# --- misc ---
		# Comment                   -> # comment text
		"COMMENT" :(
			r"#" , #! only really relevant in parser/lexical validation
			LexType("COMMENT", lexer_langs.PYTHON) ),
		# Line break                -> \n
		# Indentation increase      -> (whitespace block start)
		# Indentation decrease      -> (whitespace block end)
		#! not used
	}

from typing import reveal_type

reveal_type(TT)
