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
				# then error value assignment
				elif next_char == "$":
					if re.match(r"[a-zA-Z_]", next_char):
						# validate bareword
						n = 3
						while True:
							token += next_char
							next_char = text[i+n]
							if re.match(r"", next_char):
								...
				# add a check here for type decl
				else:
					if next_char == "*":
						token += next_char
						next_char = text[i+2]
					if next_char == "=":
						token += next_char
				result.append(token)
				continue
			if re.match(r"[a-zA-Z_]", char): #* barewords strings
				token = text[i:i+4] # text[i] through i+4 (5 chars)
				quote = '"""' if '"""' in token else "'''" if "'''" in token else "'" if "'" in token else '"' if '"' in token else '´' if '´' in token else '`' if '`' in token else ""
				if quote != "":
					# string token
					stringtype = token[0:token.index(quote)]
					## validate string type
					if re.match(r"(rf|fr|r|f|u|b|br|rb)", stringtype):
						# eternal loop of lookahead appends until the quote appears without a \ before it
						## single quotes
						if len(quote) == 1:
							counter = 0
							while True:
								next_char = text[i+5+counter]
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
								next_char = text[i+5+counter]
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
									elif text[i+5+counter:i+7+counter] == quote: # valid end quote
										token += quote
										skips += counter+len(stringtype)+6 # string length + string decl
										result.append(token)
										break
									else: # invalid length
										token += next_char
										counter += 1
										continue
					else: # invalid string type, assume it to be a bareword instead
						result.append(stringtype)
						skips += len(stringtype-1)
						continue
				else:
					# remove anything past a whitespace if there is ws
					for i in range(0,4,1):
						if not re.match(r"^(?![\.])(?![0-9])[\w\.]+(?<![\.])$", token[0:i]):
							# the best bareword check is just the same regex as the identifier uses
							continue
						else:
							token = token[0:i]
							result.append(token)
							break
					if len(token) != 5: continue
					# continue appends for bareword string
					...
				continue
				# for j in range(0,4,1):
				# 	next_char = text[i+j]
				# 	if next_char in [ "'", '"', '´', '`', ]: # 
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
