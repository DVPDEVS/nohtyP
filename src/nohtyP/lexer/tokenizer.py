# note: has to handle sep by whitespace AND semicolon

from nohtyP.lexer.types import TokenSeries
from nohtyP.global_utilities.decorators import api_level
from pathlib import Path

__all__ = [
	"whitespace",
	"tokenize",
	"tokenize_file",
]

whitespace :str = " \t\n\v\f\r\u001C\u001D\u001E\u001F\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"

@api_level(0)
class funcs:
	def tokenize(text :str) -> TokenSeries:
		result = TokenSeries()
		#* loop over text, check for whitespace / semicolon, append to result
		#* separate on all valid operators, too
		token = ""
		skips = 0
		for i in range(len(text)):
			if skips > 0:
				skips -= 1
				continue
			char = text[i]
			if char in whitespace:
				result.append(token)
				token = ""
				continue
			# begin with simpler tokens starts
			if char == ";":
				result.append(";")
				continue
			## brackets
			if char == "(":
				token = char
				next_char = text[i+1]
				if next_char == ")":
					token += next_char
					skips += 1
				result.append(token)
				continue
			if char == ")":
				result.append(char)
				continue
			if char == "{":
				result.append(char)
				continue
			if char == "}":
				result.append(char)
				continue
			if char == "[":
				result.append(char)
				continue
			if char == "]":
				result.append(char)
				continue
			## ops
			if char == "+":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "/":
				token = char
				next_char = text[i+1]
				if next_char == "/":
					token += next_char
					next_char = text[i+2]
					skips += 1
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "^":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "%":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "&":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "!":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "|":
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			...
			#* reset token each loop
			token = ""
		return result
	def tokenize_file(file_path :str|Path) -> TokenSeries:
		path = Path(file_path)
		try:
			if not path.is_file():
				raise ValueError("Provided path is not an accessible file")
			with open() as f:
				return funcs.tokenize(f.read())
		except Exception as e: # broad but idc the only thing that realistically fails here is Path
			raise ValueError(f"Unable to open the provided file path. Error;\n{e}")
