from __future__ import annotations
import os, re, subprocess
from pathlib import Path
from nohtyP._impl.globals.decorators import *

@api_level(0)
class lex_helpers:
	whitespace :str = " \t\n\v\f\r\u001C\u001D\u001E\u001F\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"

	@staticmethod
	def is_whitespace(ch: str) -> bool:
		return ch in lex_helpers.whitespace

	@staticmethod
	def is_digit(ch: str) -> bool:
		return "0" <= ch <= "9"

	@staticmethod
	def is_alpha(ch: str) -> bool:
		return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"

	@staticmethod
	def is_alnum(ch: str) -> bool:
		return lex_helpers.is_alpha(ch) or lex_helpers.is_digit(ch)

