from __future__ import annotations
from nohtyP.lexer.types import TokenSeries
from nohtyP.global_utilities.decorators import api_level
from pathlib import Path
import re

__all__ = [
	"whitespace",
	"tokenize_str",
	"tokenize_file",
]

whitespace :str = " \t\n\v\f\r\u001C\u001D\u001E\u001F\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"

@api_level(0)
class funcs:
	def tokenize_str(text :str) -> TokenSeries:
		result = TokenSeries()
		txtlen = len(text)
		#* loop over text, check for whitespace / semicolon, append to result
		#* separate on all valid operators, too
		skips = 0
		for i in range(txtlen):
			#* reset token each loop
			token = ""
			if skips > 0:
				skips -= 1
				continue
			char = text[i]
			if char in whitespace:
				continue
			# begin with simpler tokens starts
			elif char in ";,~@:": #* ; , ~ @ :
				result.append(char)
				continue
			## brackets
			elif char == "(": #* ( ()
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == ")":
						token += char
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
			elif char == "/": #* / // /= //=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "/":
						token += char
						next_val = i+2
						if next_val < txtlen:
							char = text[next_val]
						skips += 1
					if char == "=": # fails anyways if next char isnt assigned
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "^": #* ^ ^=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "%": #* % %=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "&": #* & &=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "!": #* ! !=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "|": #* | |=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "=": #* = ==
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "?": #* ? ?=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "$": #* $variable
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if re.match(r"[a-zA-Z_]", char):
						counter = 0
						# validate bareword
						while True:
							counter += 1
							next_val = i+counter
							if next_val < txtlen:
								char = text[next_val]
								if re.match(r"[\w_]", char):
									token += char
									continue
							else: counter -= 1
							break
						skips += counter - 1
					result.append(token)
					continue
				else:
					result.append(char)
			# various
			elif char == "*": #* * *? *: *~ *type: *$variable *= ** **=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					# first check for simpler ops
					if char in "?:~":
						token += char
						skips += 1
						result.append(token)
						continue
					# then error value assignment
					elif char == "$":
						token += char
						next_val = i+2
						if next_val < txtlen:
							# validate bareword
							char = text[next_val]
							if re.match(r"[a-zA-Z_]", char):
								token += char
								counter = 2
								while True:
									counter += 1
									next_val = i+counter
									if next_val < txtlen:
										char = text[next_val]
										if re.match(r"[\w_]", char):
											token += char
											continue
									break
						result.append(token)
						skips += counter-1
						continue
					# check for type decl
					elif re.match(r"[a-zA-Z_]", char):
						counter = 0
						while True:
							counter += 1
							next_val = i + counter
							if next_val < txtlen:
								char = text[next_val]
								if char == ":":
									token += char
								elif re.match(r"\w", char):
									token += char
									continue
								else: counter -= 1
							break
						result.append(token)
						skips += counter
						continue
					# lastly the easiest checks
					else:
						if char == "*":
							token += char
							next_val = i+2
							if next_val < txtlen:
								char = text[next_val]
						if char == "=": # fails anyways if next char isnt assigned
							token += char
				result.append(token)
				continue
			#! mostly guarded.
			elif re.match(r"[a-zA-Z_]", char): #* barewords strings
				next_val = min(i+6, txtlen-1)
				if next_val < txtlen:
					token:str = text[i:next_val] # text[i] to i+6 (5 chars)
					# new approach to getting the quote here
					quote = ""
					for j in range(len(token)):
						if token[j] in "'\"":
							if j < len(token)-3:
								if token[j] == token[j+1] == token[j+2]:
									quote = token[j]*3
									break
							quote = token[j]
							break
					if not len(quote) == 0:
						# string token
						stringtype = token.split()[0].split(quote)[0]
						## validate string type
						if re.match(r"(rf|fr|r|f|u|b|br|rb)", stringtype):
							token = stringtype + quote
							# eternal loop of lookahead appends until the quote appears without a \ before it
							## single quotes
							if len(quote) == 1:
								counter = 0
								while True:
									next_val = i+len(stringtype)+1+counter
									if next_val < txtlen:
										char = text[next_val]
										if char == "\n": # explicit break on newline (singles dont accept)
											break
										elif char == quote:
											if token[-1] == "\\": # escaped
												token += char
												counter += 1
											else: # valid end quote - break out
												token += quote
												break
										else: # non-quote
											token += char
											counter += 1
									else: break
								skips += counter+len(stringtype)+1 # string length + string decl
								result.append(token)
								continue
							## multiline quotes
							elif len(quote) == 3:
								counter = 0
								while True:
									next_val = i+len(stringtype)+counter+3
									if next_val < txtlen:
										char = text[next_val]
										if char == quote[0]: # quote end?
											if token[-1] == "\\": # escaped
												token += char
												counter += 1
											else:
												if next_val+2 < txtlen:
													if text[next_val:next_val+3] == quote: # valid end quote
														token += quote
														break
													else: # invalid length
														token += char
														counter += 1
												else: break
										else: # non-quote
											token += char
											counter += 1
									else: break
								#! break out even with an unclosed string. warn in validation instead, prioritize avoiding errors
								skips += counter+len(stringtype)+5 # string length + string decl
								result.append(token)
								continue
							# invalid quote or empty single quoted string
							result.append(stringtype + quote)
							skips += 1
						else: # invalid string type, assume it to be a bareword instead
							result.append(stringtype)
							skips += len(stringtype)-1
							continue
					else:
						# parse through it again from the beginning (simplest way)
						token = char
						counter = 0
						while True:
							counter += 1
							next_val = i+counter
							if next_val < txtlen:
								char = text[next_val]
								if re.match(r"[\w_]", char):
									token += char
									continue
							break
						result.append(token)
						skips += counter - 1
						continue
				result.append(token)
				# TODO: this may need correction in parsing though. later investigate if this causes issues and nmw add guards
			elif char == "#": #* comment #?
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "?":
						token += char
						result.append(token)
						skips += 1
						continue
					else:
						# loop lookahead appends until \n
						counter = 0
						while True:
							counter += 1
							next_val = i + counter
							if next_val < txtlen:
								char = text[next_val]
								if char != "\n":
									token += char
									continue
							break
				result.append(token)
				skips += counter+1
				continue
			#! mostly guarded.
			elif char in "'\"": #* strings
				next_val = min(i+4, txtlen-1)
				if next_val < txtlen:
					token:str = text[i:next_val] # text[i] to i+4 (3 chars)
					# new approach to getting the quote here
					quote = char
					if len(token) >= 3:
						if token[0] == token[1] == token[2] == quote:
							quote *=3
					token = quote
					# eternal loop of lookahead appends until the quote appears without a \ before it
					## single quotes
					if len(quote) == 1:
						counter = 0
						while True:
							next_val = i+1+counter
							if next_val < txtlen:
								char = text[next_val]
								if char == "\n": # explicit break on newline (singles dont accept)
									break
								elif char == quote:
									if token[-1] == "\\": # escaped
										token += char
										counter += 1
									else: # valid end quote - break out
										token += quote
										break
								else: # non-quote
									token += char
									counter += 1
							else: break
						skips += counter+1 # string length + string decl
						result.append(token)
						continue
					## multiline quotes
					elif len(quote) == 3:
						counter = 0
						while True:
							next_val = i+counter+3
							if next_val < txtlen:
								char = text[next_val]
								if char == quote[0]: # quote end?
									if token[-1] == "\\": # escaped
										token += char
										counter += 1
									else:
										if next_val+2 < txtlen:
											if text[next_val:next_val+3] == quote: # valid end quote
												token += quote
												break
											else: # invalid length
												token += char
												counter += 1
										else: break
								else: # non-quote
									token += char
									counter += 1
							else: break
						#! break out even with an unclosed string. warn in validation instead, prioritize avoiding errors
						skips += counter+5 # string length + string decl
						result.append(token)
						continue
				# invalid quote or empty single quoted string
				result.append(quote)
				skips += 1
				# TODO: this may need correction in parsing though. later investigate if this causes issues and nmw add guards
			# arrows, numbers and such
			elif char == "+": #* + +=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "<": #* < <- << <= <<=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == "-":
						token += char
						skips += 1
						result.append(token)
						continue
					char = text[next_val]
					if char == "<":
						token += char
						next_val = i+2
						if next_val < txtlen:
							char = text[next_val]
						skips += 1
					if char == "=": # fails anyways if next char isnt assigned
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == ">": #* > >> >= >>=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char == ">":
						token += char
						next_val = i+2
						if next_val < txtlen:
							char = text[next_val]
						skips += 1
					if char == "=": # fails anyways if next char isnt assigned
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == "-": #* - -> -=
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					if char in ">=":
						token += char
						skips += 1
				result.append(token)
				continue
			elif char == ".": #* .
				result.append(char)
				continue
			elif char in "0123456789": #* 0 0.0 111_22 1_22.0 0b0 0X0 0o7 1e7 3.5E-7
				non_decimal = 0
				hexnum = False
				octnum = False
				binnum = False
				sci_notation = False
				token = char
				next_val = i+1
				if next_val < txtlen:
					char = text[next_val]
					# six segments:
					## check for hex/binary/octal r"[oOxXbB]"
					if token == "0":
						if char.lower() in "obx":
							non_decimal = 1
							token += char
							if char.lower() == "o":
								octnum = True
							elif char.lower() == "b":
								binnum = True
							elif char.lower() == "x":
								hexnum = True
					# define the valid charsets
					decimal_charset = "0123456789_"
					full_charset = decimal_charset
					if binnum: full_charset = "01_"
					elif octnum: full_charset = "01234567_"
					elif hexnum: full_charset = "0123456789abcdef_"
					## detect initial digits
					counter = non_decimal
					while True:
						counter += 1
						next_val = i+counter
						if next_val < txtlen:
							char = text[next_val]
							if char.lower() in full_charset:
								token += char
								continue
						break
					## check for .
					if not non_decimal:
						if char == ".": #? fails anyways if the previous assignment to next_val/char was invalid - thus safe.
							token += char
							# skips += 1
							## check subsequent digits
							while True:
								counter += 1
								next_val = i+counter
								if next_val < txtlen:
									char = text[next_val]
									if char in decimal_charset:
										token += char
										continue
								break
						## check if sci notation
						next_val = i+counter
						if next_val < txtlen:
							char = text[next_val]
							if char in "eE":
								sci_notation = True
								token += char
							next_val = i+counter+1
							if next_val < txtlen:
								char = text[next_val]
								if char in "-+":
									token += char
									counter += 1
					else: skips += 1
					### get remaining digits
					if sci_notation: # inherently depends on non_decimal, is skipped if True
						counter += 1
						while True:
							next_val = i+counter
							if next_val < txtlen:
								char = text[next_val]
								counter += 1
								if char in decimal_charset:
									token += char
									continue
								else:
									skips -= 1
							break
					skips += counter-1-non_decimal
					result.append(token)
				else:
					result.append(char)
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

# shadowing with equivalent signature for imports
def tokenize_str(text :str) -> TokenSeries:
	return funcs.tokenize_str(text)
def tokenize_file(file_path :str|Path) -> TokenSeries:
	return funcs.tokenize_file(file_path)
