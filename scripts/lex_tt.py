# Just holds the TT class of lex objects and its support

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
	COMMA     = "COMMA"     # only when it acts as a separator -> ,
	UNKNOWN   = "UNKNOWN"	# Copied wholesale for compatibility with libraries. should be registered for parsing with native python install

class TT_CTX:
	PY:object = TT_PYTHON
	YP:object = TT_NOHTYP

class TT(TT_PYTHON, TT_NOHTYP):
	"""Holds lex objects for Python and nohtyP in `TT.PY` and `TT.YP`  \n
	Includes a context object and methods for diffing between objects by context."""

	PY:object = TT_PYTHON
	YP:object = TT_NOHTYP
	__CTX:set[object] = { PY, YP }	# Validation
	CTX:object = TT_CTX				# Calls
	global __CURRENT_CTX			# Global context var
	__CURRENT_CTX: object = None	# (default value is not any context)
	__DIFF: dict[object, dict[str, str | None]] = helpers.make_tt_diff(TT_PYTHON, TT_NOHTYP)

	@classmethod
	def diff(name:str|type, context:object = None) -> str|None:
		"""Returns the object of the context which matches `name`  \n
		`name` should be a string referred to from `TT.PY` or `TT.YP`  \n
		`context` should be either option from `TT.CTX`"""
		if context not in TT.__CTX: raise ValueError(f"Invalid context: {context}")
		if context==None:
			if __CURRENT_CTX not in TT.__CTX or __CURRENT_CTX == None:
				# check both contexts
				_ctx_py = TT.__DIFF.get(TT.PY, {}).get(name, None) # Safe gets due to double defaults to {} and None
				_ctx_yp = TT.__DIFF.get(TT.YP, {}).get(name, None)
				if _ctx_py != None and _ctx_yp == None: return _ctx_py  # Context inferred by exclusion
				if _ctx_py == None and _ctx_yp != None: return _ctx_yp  # Context inferred by exclusion
				if _ctx_py != None and _ctx_yp != None:
					raise NameError(f"Both contexts support a value for `name` {name}. Please supply a context.")
				raise NameError(f"`name` {name} was not found in any context.")
			return TT.__DIFF.get(__CURRENT_CTX, {}).get(name, None)		# Global context
		return TT.__DIFF.get(context, {}).get(name, None)				# Supplied context

	@classmethod
	def set_global_mode(mode:object):
		if mode not in TT.__CTX:
			raise ValueError(f"Invalid mode: {mode}")
		__CURRENT_CTX = mode

