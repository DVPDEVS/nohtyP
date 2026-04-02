import os, re, subprocess
from __future__ import *
from re import Match

class PathLike(str, os.PathLike, os.path):
	"""Holder class for path types, used for type hints"""
	...


class types(): 
	"""Contains references to other types used in `utils`"""
	PathLike:type = PathLike


class file:
	@staticmethod
	def get_cwd() -> PathLike:
		return os.path.dirname(os.path.realpath(__file__))

	@staticmethod
	def get_from_cwd(filename :PathLike) -> PathLike:
		return os.path.join(file.get_cwd(), filename)

	@staticmethod
	def read_cwd(filename :PathLike) -> str:
		with open(file.get_from_cwd(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write_cwd(filename :PathLike, content :str) -> None:
		with open(file.get_from_cwd(filename), 'w') as f:
			f.write(content)

	@staticmethod
	def get(filename :PathLike) -> PathLike:
		return os.path(filename)

	@staticmethod
	def read(filename :PathLike, readtype:str = 'r') -> str:
		with open(file.get(filename), readtype) as f:
			return f.read()

	@staticmethod
	def write(filename :PathLike, content :str, writetype:str = 'w') -> None:
		with open(file.get(filename), writetype) as f:
			f.write(content)

	@staticmethod
	def delete(filename :PathLike) -> bool|str:
		if os.path.exists(filename):
			try:
				if os.name.lower()=='nt':
					subprocess.run(['delete', str(filename)], shell=True) # Windows #? iirc its `delete` or `del`
				elif os.name.lower() == 'posix': 
					subprocess.run(['rm', str(filename)], shell=True) # Linux, MacOS, Unix OSes
				else: raise SystemError('unknown os')
				return True
			except FileNotFoundError as e:
				return "File doesnt exist"
			except Exception as e:
				return e.__repr__() # Return a string repr of the error
		return "File doesnt exist"



class spec:
	# Define the spec for translating the syntax
	tokens:dict[str, str] = {
		'set_operator'						: "*set",
		'group_or_call'					 	: "()"	,
		'block'							 	: "{}"	,
		'compund_error_value_assingment'	: "*$"	,
		'compound_error_pipe'				: "*?"	,
		'compound_complex_assignment'		: "#?"	,
		'unary_flow'						: "?"	,
		'unary_continuous_flow'				: "?="	,
		'conditional'						: "~"	,
		'conditional_fail'					: "*~"	,
		'boundary'							: ";"	,
	}

	# replacement blocks for nohtyP syntax
	replacements:dict[str, str] = {
	}

	# whitespace eligible characters
	whitespace_ls:list[str] = [ ' ', '\n', '\t',  ]
	whitespace_str:str = ''.join(whitespace_ls)

	# String quote character sets
	string_quotes_ls:list[str] = [ "'", '"', '´', '`', '"""', "'''", ]


class regex_patterns:
	whitespace 		= r'[' + spec.whitespace_str + r']+' 	# Any postitive non-zero amount of whitespace chars defined in utils.spec
	comment 		= r'#(?!\?)[^\n]*$'						# End of line comments not matching compund assignments (https://regex101.com/r/b9wdL5/2)
	string_quote 	= r'|'.join(spec.string_quotes_ls)		# Eligible quotes
	# All possible formats of native python strings (https://regex101.com/r/Hhihv5/1) [requires case insens flag `re.INSENSITIVE`]
	native_string   = rf'((rf|fr|r|f)?u?|u?(rf|fr|r|f)?|(fur|ruf)|r?b)?({string_quote})([.\n]*)\5(\..+\(\)*'
	# This matches all valid format tags, content, and any number of tacked-on method calls with a backref for dynamic quote matching.
	# Does also allow newlines in non-triple quotes but eh
	@classmethod
	def check_for_valid_newline(match_obj:Match) -> bool:
		""" Verify whether the quote type is valid for the content.  \n
		Checks for newlines in single-quoted strings.  \n
		Returns `False` if invalid, `True` if valid.  \n
		Requires a `re.Match` object of `utils.regex_patterns.native_string`"""
		qt = len(match_obj.group(5)) ; sc = match_obj.group(6)
		if qt == 1 and '\n' in sc:
			return False
		return True


class lex_helpers:
	@staticmethod
	def is_whitespace(ch: str) -> bool:
		return ch in spec.whitespace_ls

	@staticmethod
	def is_digit(ch: str) -> bool:
		return "0" <= ch <= "9"

	@staticmethod
	def is_alpha(ch: str) -> bool:
		return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"

	@staticmethod
	def is_alnum(ch: str) -> bool:
		return lex_helpers.is_alpha(ch) or lex_helpers.is_digit(ch)

