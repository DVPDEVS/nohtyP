# Just holds the TT class of lex objects and its support

from global_utilities.decorators import vibe_check

class TokenMeta(type):
	def __getattr__(cls, name):
		try:
			return cls._values[name]
		except KeyError:
			raise AttributeError(
				f"{cls.__name__} has no token {name}"
			)
	def _exists_key(cls, keyname) -> bool:
		try:
			cls.__getattr__(keyname)
			return True
		except KeyError:
			return False
	def __get_outer_attr__(cls:object, name):
		try:
			return cls.

class helpers:
	@classmethod
	@staticmethod
	def get_all_token_names(*classes:object) -> set[str]:
		"""Gets all inherent uppercase `str` attributes of the given `classes` not starting with '_'"""
		all_names:set[str] = set()
		for cls in classes:
			names = {
				n for n in vars(cls)
				if isinstance(getattr(cls, n), str) and n.isupper() and not n.startswith("_")
			}
			all_names.update(names)
		return all_names
	@classmethod
	@staticmethod
	def make_tt_diff(*classes:object) -> dict[object, dict[str, str | None]]:
		"""Packs the relevant attributes of `classes` together nicely"""
		all_names = helpers.get_all_token_names(*classes)
		result:dict[object, dict[str, str | None]] = {}
		for cls in classes:
			per_cls = {}
			for name in all_names:
				if hasattr(cls, name):
					per_cls[name] = getattr(cls, name)
				else:
					per_cls[name] = None
			result[cls] = per_cls
		return result

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
	COMMA                          = "COMMA"     # only when it acts as a separator -> ,
	SET_OPERATOR                   = "SET_OPERATOR"
	GROUP_OR_CALL                  = "GROUP_OR_CALL"
	BLOCK                          = "BLOCK"
	COMPUND_ERROR_VALUE_ASSINGMENT = "COMPUND_ERROR_VALUE_ASSINGMENT"
	COMPOUND_ERROR_PIPE            = "COMPOUND_ERROR_PIPE"
	COMPOUND_COMPLEX_ASSIGNMENT    = "COMPOUND_COMPLEX_ASSIGNMENT"
	UNARY_FLOW                     = "UNARY_FLOW"
	UNARY_CONTINUOUS_FLOW          = "UNARY_CONTINUOUS_FLOW"
	CONDITIONAL                    = "CONDITIONAL"
	CONDITIONAL_FAIL               = "CONDITIONAL_FAIL"
	BOUNDARY                       = "BOUNDARY"
	UNKNOWN                        = "UNKNOWN"	# Copied wholesale for compatibility with libraries. should be registered for parsing with native python install

class TT_CTX:
	PY:object = TT_PYTHON
	YP:object = TT_NOHTYP

class REGEX_TT:
	"""Holds regex strings to match the equivalent lexer object as ´TT.PY´ and ´TT.YP´  \n
	The subclasses hold attributes matching their respective ´TT´ object."""
	#? class-level local vars
	# whitespace eligible characters
	whitespace_ls:list[str] = [ ' ', '\n', '\t',  ]
	whitespace_str:str = ''.join(whitespace_ls)
	# String quote character sets
	string_quotes_ls:list[str] = [ "'", '"', '´', '`', '"""', "'''", ]
	#? diff class
	class GET:
		"""Get an attribute from either class.  \n
		Instantiate this class with the name of the attribute you want, eg:  \n
		> `re_conditional: str = TT.REGEX.GET(TT.YP.CONDITIONAL)`  \n
		Here, `re_conditional` becomes either the wanted attribute's value or  \n
		`None` if the attribute isnt found"""
		@vibe_check(":3")
		def __new__(cls, attributename:str) -> str|None:
			# Production code = ternaries
			return cls.NOHTYP.__getattr__(attributename) if cls.NOHTYP._exists_key(attributename) else cls.PYTHON.__getattr__(attributename) if cls.PYTHON._exists_key(attributename) else None
			# if cls.NOHTYP._exists_key(attributename):
			# 	return cls.NOHTYP.__getattr__(attributename)
			# if cls.PYTHON._exists_key(attributename):
			# 	return cls.PYTHON.__getattr__(attributename)
			# return None
	#? yp regex
	class NOHTYP(metaclass=TokenMeta):
		_values: dict[str, str] = {
			TT_NOHTYP.COMMA                          : r",",
			TT_NOHTYP.SET_OPERATOR                   : rf"\*set",
			TT_NOHTYP.GROUP_OR_CALL                  : r"\(.*\)",
			TT_NOHTYP.BLOCK                          : r"\{.*\}",
			TT_NOHTYP.COMPUND_ERROR_VALUE_ASSINGMENT : r"\*\$",
			TT_NOHTYP.COMPOUND_ERROR_PIPE            : r"\*\?",
			TT_NOHTYP.COMPOUND_COMPLEX_ASSIGNMENT    : r"#\?",
			TT_NOHTYP.UNARY_FLOW                     : r"\?",
			TT_NOHTYP.UNARY_CONTINUOUS_FLOW          : r"\?=",
			TT_NOHTYP.CONDITIONAL                    : r"~",
			TT_NOHTYP.CONDITIONAL_FAIL               : r"\*~",
			TT_NOHTYP.BOUNDARY                       : r";",
			TT_NOHTYP.UNKNOWN                        : r".+",
		}
	#? py regex
	class PYTHON(metaclass=TokenMeta):
		_values: dict[str, str] = {
			# --- literals ---
			TT_PYTHON.INT: r"[+-]?(?:0b[01_]+|0o[0-7_]+|0x[\da-fA-F_]+|\d[\d_]*)(?![\w.])",
			TT_PYTHON.FLOAT: r"[+-]?(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*\.)(?:[eE][+-]?\d+)?",
			TT_PYTHON.BOOL: r"\b(?:True|False)\b",
			TT_PYTHON.NONE: r"\bNone\b",
			TT_PYTHON.BYTES: r"(?i)\b(?:b|br)\"(?:\\.|[^\"\\])*\"|\b(?:b|br)'(?:\\.|[^'\\])*'",
			TT_PYTHON.BYTEARRAY: r"bytearray\s*\(\s*b?(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\s*\)",
			TT_PYTHON.STR: rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?({'|'.join(REGEX_TT.string_quotes_ls)})([.\n]*)\5(\..+\(\)*',
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

# TODO: Make this instancable with a local context
class TT(TT_PYTHON, TT_NOHTYP):
	"""Holds lex objects for Python and nohtyP in `TT.PY` and `TT.YP`  \n
	Includes a context object and methods for diffing between objects by context.  \n
	Holds regex strings for the equivalent lex objects in ´TT.REGEX´"""

	# Class-level vars
	PY:object = TT_PYTHON
	YP:object = TT_NOHTYP
	REGEX:object = REGEX_TT
	__CTX:set[object] = { PY, YP }	# Validation
	CTX:object = TT_CTX				# Calls
	# Generate the diff object @ runtime # Use the same object for instances as its only read from; Save some memory
	__DIFF: dict[object, dict[str, str | None]] = helpers.make_tt_diff(TT_PYTHON, TT_NOHTYP)

	# Singleton-level vars
	__CURRENT_CTX: object = None	# (default value is not any context)

	# Instance-level vars
	def __init__(self):
		self.__INSTANCE_CURRENT_CTX:object = None

	@classmethod
	def diff(name:str, context:object = None) -> str|None:
		"""Returns the object of the context which matches `name`  \n
		`name` should be a string referred to from `TT.PY` or `TT.YP`  \n
		`context` should be either option from `TT.CTX`  \n
		Defaults to context from `__CURRENT_CTX` (the global context) or  \n
		infers the correct context from presence. (which may fail.)"""
		if context not in TT.__CTX: raise ValueError(f"Invalid context: {context}")
		if context==None:
			if TT.__CURRENT_CTX not in TT.__CTX or TT.__CURRENT_CTX == None:
				# check both contexts
				_ctx_py = TT.__DIFF.get(TT.PY, {}).get(name, None) # Safe gets due to double defaults to {} and None
				_ctx_yp = TT.__DIFF.get(TT.YP, {}).get(name, None)
				if _ctx_py != None and _ctx_yp == None: return _ctx_py  # Context inferred by exclusion
				if _ctx_py == None and _ctx_yp != None: return _ctx_yp  # Context inferred by exclusion
				if _ctx_py != None and _ctx_yp != None:
					raise NameError(f"Both contexts support a value for `name` {name}. Please supply a context.")
				raise NameError(f"`name` {name} was not found in any context.")
			return TT.__DIFF.get(TT.__CURRENT_CTX, {}).get(name, None)		# Global context
		return TT.__DIFF.get(context, {}).get(name, None)				# Supplied context

	@classmethod
	def set_global_mode(mode:object):
		if mode not in TT.__CTX:
			raise ValueError(f"Invalid mode: {mode}")
		TT.__CURRENT_CTX = mode

