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
			elif char == ";": #* ;
				result.append(";")
				continue
			## brackets
			elif char == "(": #* ( ()
				token = char
				next_char = text[i+1]
				if next_char == ")":
					token += next_char
					skips += 1
				result.append(token)
				continue
			elif char == ")": #* )
				result.append(char)
				continue
			elif char == "{": #* {
				result.append(char)
				continue
			elif char == "}": #* }
				result.append(char)
				continue
			elif char == "[": #* [
				result.append(char)
				continue
			elif char == "]": #* ]
				result.append(char)
				continue
			## ops
			elif char == "+": #* + +=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			elif char == "/": #* / // /= //=
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
			elif char == "^": #* ^ ^=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			elif char == "%": #* % %=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			elif char == "&": #* & &=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			elif char == "!": #* ! !=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			elif char == "|": #* | |=
				token = char
				next_char = text[i+1]
				if next_char == "=":
					token += next_char
					skips += 1
				result.append(char)
				continue
			# various
			elif char == "*": #* * *? *: *~ *type: *$variable *= ** **=
				token = char
				char = text[i+1]
				# first check for simpler ops
				if char in "?:~":
					token += char
					skips += 1
					result.append(token)
					continue
				# then error value assignment
				elif char == "$":
					if re.match(r"[a-zA-Z_]", char):
						# validate bareword
						counter = 3
						while True:
							counter += 1
							char = text[i+counter]
							if re.match(r"\w", char):
								token += char
								continue
							result.append(token)
							break
						skip += counter - 1
						continue
				# check for type decl
				elif re.match(r"[a-zA-Z_]", char):
					counter = 3
					while True:
						counter += 1
						char = text[i+counter]
						if char == ":":
							token += char
						elif re.match(r"\w", char):
							token += char
							continue
						result.append(token)
						break
					continue
				# lastly the easiest checks
				else:
					if char == "*":
						token += char
						char = text[i+2]
					if char == "=":
						token += char
					result.append(token)
					continue
			elif re.match(r"[a-zA-Z_]", char): #* barewords strings
				token = text[i:i+5] # text[i] to i+5 (5 chars)
				quote = '"""' if '"""' in token else "'''" if "'''" in token else "'" if "'" in token else '"' if '"' in token else '´' if '´' in token else '`' if '`' in token else ""
				if not len(quote) == 0:
					# string token
					stringtype = token[0:token.index(quote)]
					## validate string type
					if re.match(r"(rf|fr|r|f|u|b|br|rb)", stringtype):
						token = stringtype + quote
						# eternal loop of lookahead appends until the quote appears without a \ before it
						## single quotes
						if len(quote) == 1:
							counter = 0
							while True:
								next_char = text[i+len(stringtype)+counter+1]
								if next_char == "\n": # explicit break on newline (singles dont accept)
									result.append(token)
									break
								elif not next_char == quote: # non-quote
									token += next_char
									counter += 1
									continue # stay inside the while loop but skip quotation check
								else:
									# quote end?
									if token[-1] == "\\": # escaped
										token += next_char
										counter += 1
										continue
									else: # valid end quote - break out
										token += quote
										skips += counter+len(stringtype)+2 # string length + string decl
										result.append(token)
										break
						## multiline quotes
						else:
							counter = 0
							while True:
								next_char = text[i+len(stringtype)+counter+3]
								#? debug
								# print(next_char)
								if not next_char == quote[0]: # non-quote
									token += next_char
									counter += 1
									continue # stay inside the while loop but skip quotation check
								else:
									# quote end?
									if token[-1] == "\\": # escaped
										token += next_char
										counter += 1
										continue
									elif text[i+len(stringtype)+counter+1:i+len(stringtype)+counter+4] == quote: # valid end quote
										token += next_char
										skips += counter+len(stringtype)+6 # string length + string decl
										result.append(token)
										break
									else: # invalid length
										token += next_char
										counter += 1
										continue
					else: # invalid string type, assume it to be a bareword instead
						result.append(stringtype)
						skips += len(stringtype)-1
						continue
				else:
					# parse through it again from the beginning (simplest way)
					token = char
					counter = 1
					while True:
						counter += 1
						char = text[i+counter]
						if re.match(r"\w", char):
							token += char
							continue
						result.append(token)
						break
					skips += counter-1
				continue
			elif char == "#": #* comment #?
				is_comment = text[i+1] != "?"
				# if comment, loop lookahead appends until \n
				# else just next char
				if not is_comment:
					result.append("#?")
					skips += 1
					continue
				else:
					counter = 0
					while True:
						counter += 1
						char = text[i+counter]
						if char != "\n":
							token += char
							continue
						result.append(token)
						break
					# tweak skips here too, check after testing i think
					continue
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
