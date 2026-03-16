import os
from __future__ import *
class PathLike(str, os.PathLike, os.path):
	... # Holder class for path types, not used except for type hints

class file:
	@staticmethod
	def get_cwd() -> PathLike:
		return os.path.dirname(os.path.realpath(__file__))

	@staticmethod
	def get_cwd(filename :PathLike) -> PathLike:
		return os.path.join(file.get_current_dir(), filename)

	@staticmethod
	def read_cwd(filename :PathLike) -> str:
		with open(file.get_file_from_cwd(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write_cwd(filename :PathLike, content :str) -> None:
		with open(file.get_file_from_cwd(filename), 'w') as f:
			f.write(content)

	@staticmethod
	def get(filename :PathLike) -> PathLike:
		return os.path(filename)

	@staticmethod
	def read(filename :PathLike) -> str:
		with open(file.get_file(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write(filename :PathLike, content :str) -> None:
		with open(file.get_file(filename), 'w') as f:
			f.write(content)

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

	# String quote characters
	string_quotes_ls:list[str] = [ "'", '"', '´', '`', ]

class regex_patterns:
	whitespace 		= r'[' + spec.whitespace_ls + r']+' # Any postitive non-zero amount of whitespace chars defined in utils.spec
	comment 		= r'#.*$' 							# End of line comments
	string_quote 	= r'|'.join(spec.string_quotes_ls)	# Eligible quotes

