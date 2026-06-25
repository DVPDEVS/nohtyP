from nohtyP._impl.global_utilities.decorators import *
from typing import Union

__all__ = [
	"SPDX_License_Identifers",
	"NohtyPBaseSyntaxError",
	"NohtyPInternalFailure",
	"NohtyPTokenizerInternalFailure",
	"NohtyPLexerInternalFailure",
	"NohtyPParserInternalFailure",
	"NohtyPTranspilerInternalFailure",
	"NohtyPTokenizerSyntaxError",
	"NohtyPLexerSyntaxError",
	"NohtyPParserSyntaxError",
	"AnyNohtyPSyntaxError",
]

class SPDX_License_Identifers: # https://spdx.org/licenses/
	"""Enum of license identifiers. Shorthand name, SPDX ID value"""
	AGPL3_o = "AGPL-3.0-only"
	AGPL3_l = "AGPL-3.0-or-later"
	LGPL3_o = "LGPL-3.0-only"
	LGPL3_l = "LGPL-3.0-or-later"
	CCA4I   = "CC-BY-4.0"
	MPL2    = "MPL-2.0"
#* Comment style
#* Single-line comment in any style, eg. `# ` followed by the text `SPDX-License-Identifier`, a colon and whitespace,`: ` then the unquoted ID.
#? Should avoid false positive parsing.

#* NohtyP errors
class NohtyPBaseSyntaxError(RuntimeError):
	"""
	Base SyntaxError class for NohtyP-related errors.
	"""
	def __init__(self, message: str, cause: str = "Unknown") -> None:
		super().__init__(message, cause)

class NohtyPInternalFailure(SystemError):
	"""
	Base SystemError class for NohtyP internal failures.  \n
	Please report any occurrence to the developer along with the traceback.
	"""
	def __init__(self, *args):
		super().__init__(*args)

class NohtyPTokenizerInternalFailure(NohtyPInternalFailure):
	"""
	Internal Tokenizer failure.  \n
	Please report any occurrence to the developer along with the traceback.
	"""
	def __init__(self, *args):
		super().__init__(*args)

class NohtyPLexerInternalFailure(NohtyPInternalFailure):
	"""
	Internal Lexer failure.  \n
	Please report any occurrence to the developer along with the traceback.
	"""
	def __init__(self, *args):
		super().__init__(*args)

class NohtyPParserInternalFailure(NohtyPInternalFailure):
	"""
	Internal Parser failure.  \n
	Please report any occurrence to the developer along with the traceback.
	"""
	def __init__(self, *args):
		super().__init__(*args)

class NohtyPTranspilerInternalFailure(NohtyPInternalFailure):
	"""
	Internal Transpiler failure.  \n
	Please report any occurrence to the developer along with the traceback.
	"""
	def __init__(self, *args):
		super().__init__(*args)

class NohtyPTokenizerSyntaxError(NohtyPBaseSyntaxError):
	"""
	Tokenizer error:  \n
	Failure to tokenize the input.
	"""
	def __init__(self, message: str, cause: str = "Unknown") -> None:
		super().__init__(message, cause)

class NohtyPLexerSyntaxError(NohtyPBaseSyntaxError):
	"""
	Lexer error:  \n
	Failure to lexically validate or parse the input.
	"""
	def __init__(self, message, cause: str = "Unknown") -> None:
		super().__init__(message, cause)

class NohtyPParserSyntaxError(NohtyPBaseSyntaxError):
	"""
	Parser error:  \n
	Failure to syntactically validate or semantically parse the input.
	"""
	def __init__(self, message: str, cause: str = "Unknown") -> None:
		super().__init__(message, cause)

#* syntax error union
AnyNohtyPSyntaxError = Union[NohtyPBaseSyntaxError, NohtyPTokenizerSyntaxError, NohtyPLexerSyntaxError, NohtyPParserSyntaxError]
