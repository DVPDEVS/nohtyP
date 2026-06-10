# note: has to handle sep by whitespace AND semicolon

from nohtyP.lexer.types import TokenSeries
from nohtyP.global_utilities.decorators import api_level
from pathlib import Path
import re

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
		skips = 0
		for i in range(len(text)):
			#* reset token each loop
			token = ""
			if skips > 0:
				skips -= 1
				continue
			char = text[i]
			if char in whitespace:
				continue
			# begin with simpler tokens starts
			if char == ";": #* ;
				result.append(";")
				continue
			## brackets
			if char == "(": #* ( ()
				token = char
				next_char = text[i+1]
				if next_char == ")":
					token += next_char
					skips += 1
				result.append(token)
				continue
			if char == ")": #* )
				result.append(char)
				continue
			if char == "{": #* {
				result.append(char)
				continue
			if char == "}": #* }
				result.append(char)
				continue
			if char == "[": #* [
				result.append(char)
				continue
			if char == "]": #* ]
				result.append(char)
				continue
			## ops
			if char == "+": #* + +=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "/": #* / // /= //=
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
			if char == "^": #* ^ ^=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "%": #* % %=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "&": #* & &=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "!": #* ! !=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			if char == "|": #* | |=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			# various
			if char == "*": #* * *? *: *~ *type: *$variable *= ** **=
				# first check for simpler ops
				token = char
				next_char = text[i+1]
				if next_char in "?:~":
					token += next_char
				elif next_char == "$":
					if re.match(r"[a-zA-Z_]", next_char):
						n = 3
						while True:
							token += next_char
							next_char = text[i+n]
							if re.match(r"", next_char):
								...
				else:
					if next_char == "*":
						token += next_char
						next_char = text[i+2]
					if next_char == "=":
						token += next_char
				result.append(token)
				continue
			if re.match(r"[a-zA-Z_\.]", char): #* barewords strings
				token = text[i:i+4] # text[i] through i+4 (5 chars)
				quote = '"""' if '"""' in token else "'''" if "'''" in token else "'" if "'" in token else '"' if '"' in token else '´' if '´' in token else '`' if '`' in token else ""
				if quote != "":
					... # string token
				else:
					# remove anything past a whitespace if there is ws
					for i in range(0,4,1):
						if token[i] not in whitespace:
							continue
						else:
							token = token[0:i]
							result.append(token)
							break
					if len(token) != 5: continue
				# for j in range(0,4,1):
				# 	next_char = text[i+j]
				# 	if next_char in [ "'", '"', '´', '`', ]: # 
				# 		# verify that token is currently a valid string type
				# 		if re.match(r"(rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b", token):
				# 			quote = next_char
				# 			if text[i+j+1] == next_char: 
				# 				quote += text[i+j+1]
				# 				if text[i+j+2] == next_char: quote += text[i+j+2]
				# 			# reminder to check for if the last char before ending quotation is an escape
				# 			if len(quote) == 2:
				# 				result.append(token+quote)
				# 				continue
				# 		... # idk how to continue here
				# 	elif re.match(r"[\w\.]", next_char):
				# 		token += next_char
			# fallback (improve later)
			result.append(f"¤__NOHTYP_NOT_TOKENIZABLE__¤({char})")
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
