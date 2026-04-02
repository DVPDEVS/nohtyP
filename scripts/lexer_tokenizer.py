import re
from dataclasses import dataclass
import utils
from utils import spec, regex_patterns

KEYWORDS = {"if", "else", "while"}  # temporary core; you will extend with nohtyP keywords


@dataclass
class Token:
	type: str
	value: str
	line: int
	col: int

	def __repr__(self):
		return f"Token({self.type}, {self.value!r}, {self.line}:{self.col})"


class NohtyPLex:
	def __init__(self, text: str):
		self.text = text
		self.pos = 0
		self.line = 1
		self.col = 1
		self.current_char = self.text[self.pos] if self.text else None
		self.tokens: list[Token] = []

	# ------------- basic cursor ops -------------

	def advance(self, n: int = 1):
		for _ in range(n):
			if self.current_char == "\n":
				self.line += 1
				self.col = 1
			else:
				self.col += 1

			self.pos += 1
			if self.pos >= len(self.text):
				self.current_char = None
				return
			else:
				self.current_char = self.text[self.pos]

	def peek(self, offset: int = 1):
		idx = self.pos + offset
		if idx >= len(self.text):
			return None
		return self.text[idx]

	# ------------- skipping -------------

	def skip_whitespace(self):
		while self.current_char is not None and utils.lex_helpers.is_whitespace(self.current_char):
			self.advance()

	def skip_comment(self):
		# '#' to end of line
		while self.current_char is not None and self.current_char != "\n":
			self.advance()

	# ------------- token builders -------------

	def number(self):
		start_line, start_col = self.line, self.col
		result = ""
		while self.current_char is not None and utils.lex_helpers.is_digit(self.current_char):
			result += self.current_char
			self.advance()
		self.tokens.append(Token(TT.INT, result, start_line, start_col))

	def identifier_or_keyword(self):
		start_line, start_col = self.line, self.col
		result = ""
		while self.current_char is not None and utils.lex_helpers.is_alnum(self.current_char):
			result += self.current_char
			self.advance()
		tok_type = TT.KEYWORD if result in KEYWORDS else TT.ID
		self.tokens.append(Token(tok_type, result, start_line, start_col))

	def string(self):
		# supports all quotes in utils.spec.string_quotes_ls
		start_quote = self.current_char
		start_line, start_col = self.line, self.col
		self.advance()  # skip opening quote

		value_chars = []
		while self.current_char is not None and self.current_char != start_quote:
			# TODO: handle escapes later
			value_chars.append(self.current_char)
			self.advance()

		if self.current_char == start_quote:
			self.advance()  # skip closing quote
		# else: unterminated string; you might want to raise later

		value = "".join(value_chars)
		self.tokens.append(Token(TT.STR, value, start_line, start_col))

	# ------------- comma rule -------------

	def handle_comma_or_char(self):
		"""
		Comma separates ONLY if surrounded by whitespace on at least one side.

		h h          -> ["h", "h"]
		h, h         -> ["h", "h"]     (comma+whitespace = separator)
		h,h          -> ["h,h"]        (no whitespace = single token)
		"h,",h       -> ["h,", "h"]
		"h","h"      -> ["h", "h"]
		"""
		ch = self.current_char
		start_line, start_col = self.line, self.col

		if ch == ",":
			prev_ch = self.peek(-1) if self.pos > 0 else None
			next_ch = self.peek(1)

			prev_ws = prev_ch is not None and utils.lex_helpers.is_whitespace(prev_ch)
			next_ws = next_ch is not None and utils.lex_helpers.is_whitespace(next_ch)

			if prev_ws or next_ws:
				# acts as separator: emit COMMA then advance
				self.tokens.append(Token(TT.COMMA, ",", start_line, start_col))
				self.advance()
				return

			# otherwise treat as a normal char to be glued into identifier-like token
			# easiest: just emit as UNKNOWN single-char token for now
			self.tokens.append(Token(TT.UNKNOWN, ",", start_line, start_col))
			self.advance()
			return

		# fallback: single char operators / punctuation (will extend this)
		self.tokens.append(Token(TT.UNKNOWN, ch, start_line, start_col))
		self.advance()

	# ------------- public API -------------

	def next_token(self):
		while self.current_char is not None:
			# skip whitespace
			if utils.lex_helpers.is_whitespace(self.current_char):
				self.skip_whitespace()
				continue

			# comments: '#' to end of line
			if self.current_char == "#":
				self.skip_comment()
				continue

			# strings
			if self.current_char in spec.string_quotes_ls:
				self.string()
				return self.tokens[-1]

			# numbers
			if utils.lex_helpers.is_digit(self.current_char):
				self.number()
				return self.tokens[-1]

			# identifiers / keywords
			if utils.lex_helpers.is_alpha(self.current_char):
				self.identifier_or_keyword()
				return self.tokens[-1]

			# comma / misc chars
			if self.current_char == ",":
				self.handle_comma_or_char()
				return self.tokens[-1]

			# TODO: operators and nohtyP tokens (*set, #?, ?=, ~, *~, etc.)
			self.handle

if __name__ == "__main__":
	# Create the lexer and start scanning
	lexer = NohtyPLex()
	# lexer.scan("hello \"world\" ? print() # comment")

# TODO: Implement the following
# I did not yet implement bareword-as-string resolution; that’s a later phase where the translator rewrites IDs to STR based on scope. The lexer just gives you IDs and STRs separately, which matches your “translator performs bareword resolution and whitespace normalization before AST translation” statement.

# The nohtyP operators (*set, #?, ?, ?=, ~, *~, *$, *?, {}, (), ;) should be recognized in next_token() by looking for multi-character sequences using spec.tokens. You can add a small “longest match from spec.tokens.values()`” function there.

# The utils.regex_patterns are currently unused in this version; if you want, next step is to replace skip_whitespace and skip_comment with a single regex-based scanner chunk using regex_patterns.whitespace and regex_patterns.comment.

