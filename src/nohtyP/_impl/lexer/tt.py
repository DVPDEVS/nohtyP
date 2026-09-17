from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import regex, api_level
from nohtyP._impl.lexer.types import *

@regex
@api_level(0)
class TT:
	ELEM: dict[LexTypeList, str] = {
		#! nohtyP elements
		LexTypeList.SEMICOLON           : r";", # shouldnt require boundaries but they wont hurt either #? ;
		LexTypeList.BAREWORD            : r"^(?![0-9])\w+$",                #? <anything>                                #* sauce: https://regex101.com/r/L0MnX3/3 
		LexTypeList.TYPE_DECLARATION    : r"^\*?(?![0-9])\w+\:$",           #? optional * followed by a bareword and a : #* sauce: https://regex101.com/r/lhwcEL/2 
		LexTypeList.CBRACKET_LEFT       : r"\{",                            #? {
		LexTypeList.CBRACKET_RIGHT      : r"\}",                            #? }
		LexTypeList.BRACKET_LEFT        : r"\[",                            #? [
		LexTypeList.BRACKET_RIGHT       : r"\]",                            #? ]
		LexTypeList.CALL                : r"\(\)",                          #? ()
		LexTypeList.PAREN_LEFT          : r"\(",                            #? (
		LexTypeList.PAREN_RIGHT         : r"\)",                            #? )
		LexTypeList.ASS_EQ              : r"=",                             #? =
		LexTypeList.FLOW_Q              : r"\?",                            #? ?
		LexTypeList.FLOW_HASH_Q         : r"#\?",                           #? #?
		LexTypeList.FLOW_WHILE          : r"\?=",                           #? ?=
		LexTypeList.SYMBOL_AT           : r"@",                             #? @
		LexTypeList.TILDE               : r"~",                             #? ~
		LexTypeList.CONDITION_AST_TILDE : r"\*~",                           #? *~
		LexTypeList.ARROW_LEFT          : r"<-",                            #? <-
		LexTypeList.ARROW_RIGHT         : r"->",                            #? ->
		LexTypeList.EXCEPT_STORE        : r"\b(?<!\.)\*\$[\w\.]*(?!\.+)\b", #? *$<insert var>
		LexTypeList.EXCEPT_GET          : r"\b(?<!\.)\$[\w\.]*(?!\.+)\b",   #? $<insert var>
		LexTypeList.EXCEPT_HANDLE       : r"\*\?",                          #? *?
		LexTypeList.EXCEPT_SET          : r"(?<!\.)\*set\ [-+]e(?!\.)",     #? *set -e/+e # case sensitive               #* sauce: https://regex101.com/r/3QG7Y0/1 
		LexTypeList.KW_FETCH            : r"(?<!\.)fetch(?!\.)",            #? fetch      # case sensitive
		LexTypeList.KW_MATCH            : r"(?<!\.)match(?!\.)",            #? match      # case sensitive
		#! Python elements
		# --- literals ---
		LexTypeList.INT   : r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])",             # Native int   -> 123, 0, -42, 0b1010, 0o77, 0xFF
		LexTypeList.FLOAT : r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?",       # Native float -> 1.23, .5, 10., 1e10, -3.4e-2
		LexTypeList.BOOL  : r"\b(?:True|False)\b",                                                       # Native bool  -> True, False
		LexTypeList.NONE  : r"\bNone\b",                                                                 # NoneType     -> None
		LexTypeList.STR   : '^(rf|fr|r|f|u|b|br|rb)?(\\"\\"\\"|\'\'\'|\\"|\'|´|`)((?!\\2)(.*)\\2|\\2)$', #* sauce : https://regex101.com/r/Hhihv5/5 
		# --- identifiers / keywords ---
		LexTypeList.KEYWORD : r"\b(?:def|class|pass|break|continue|raise|with|yield|lambda|async|await|global|nonlocal|assert|del)\b", # Python keywords -> if, else, while, def, class, return, import
		# --- operators ---
		LexTypeList.OP        : r"(?:\*\*|//|==|!=|<=|>=|<|>|\+|-|\*|/|%|=)",         # Operators            -> +, -, *, /, //, %, **, =, ==, !=, <, >, <=, >=, and, or, not, is, in
		LexTypeList.AUGASSIGN : r"(?:\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)", # Augmented assignment -> +=, -=, *=, /=, //=, %=, **=, &=, |=, ^=, <<=, >>=
		LexTypeList.BITOP     : r"(?:&|\||\^|~|<<|>>)",                               # Bitwise operators    -> &, |, ^, ~, <<, >> #! ~ will be consumed by earlier nohtyp lex
		LexTypeList.COMPARE   : r"(?:==|!=|<=|>=|<|>|is(?:\s+not)?|in|not\s+in)",     # Comparison operators -> ==, !=, <, >, <=, >=, is, is not, in, not in
		LexTypeList.LOGIC     : r"\b(?:and|or|not)\b",                                # Logical operators    -> and, or, not
		# --- punctuation ---
		LexTypeList.COMMA    : r",",      # General punctuation -> :, ;, ., @, = (contextual), -> #! ->, ;, :, ., = and @ will be consumed by other lex
		LexTypeList.DOT      : r"\.",     # Attribute access    -> . 
		LexTypeList.COLON    : r":",      # Colon               -> : 
		LexTypeList.ELLIPSIS : r"\.\.\.", # Ellipsis object     -> ... 
		# --- misc ---
		LexTypeList.COMMENT : r"#.*", # Comment -> # comment text #! only really relevant in parser/lexical validation
		#! Generic elements
		LexTypeList.TOKENIZER_FAIL : "¤__NOHTYP_NOT_TOKENIZABLE__¤", #? ¤__NOHTYP_NOT_TOKENIZABLE__¤()
		LexTypeList.STAR           : r"\*",                          #? *
		LexTypeList.UNKNOWN        : r".*", 
	}
