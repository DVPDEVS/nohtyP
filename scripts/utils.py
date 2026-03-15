import os

class file:
	@staticmethod
	def get_current_dir() -> os.path:
		return os.path.dirname(os.path.realpath(__file__))

	@staticmethod
	def get_file_from_cwd(filename :os.path.__path__|str) -> os.path:
		return os.path.join(file.get_current_dir(), filename)

	@staticmethod
	def read_file_cwd(filename :os.path.__path__|str) -> str:
		with open(file.get_file_from_cwd(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write_file_cwd(filename :os.path.__path__|str, content :str) -> None:
		with open(file.get_file_from_cwd(filename), 'w') as f:
			f.write(content)

	@staticmethod
	def get_file(filename :os.path.__path__|str) -> os.path:
		return os.path(filename)

	@staticmethod
	def read_file(filename :os.path.__path__|str) -> str:
		with open(file.get_file(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write_file(filename :os.path.__path__|str, content :str) -> None:
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
	whitespace:list[str] = [ ' ', '\n', '\t',  ]

