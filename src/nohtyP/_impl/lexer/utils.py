from __future__ import annotations
import os, re, subprocess
from pathlib import Path
from nohtyP._impl.global_utilities.decorators import *

@api_level(0)
class file:
	@staticmethod
	def get_cwd() -> Path:
		return os.path.dirname(os.path.realpath(__file__))

	@staticmethod
	def get_from_cwd(filename :Path) -> Path:
		return os.path.join(file.get_cwd(), filename)

	@staticmethod
	def read_cwd(filename :Path) -> str:
		with open(file.get_from_cwd(filename), 'r') as f:
			return f.read()

	@staticmethod
	def write_cwd(filename :Path, content :str) -> None:
		with open(file.get_from_cwd(filename), 'w') as f:
			f.write(content)

	@staticmethod
	def get(filename :Path) -> Path:
		return os.path(filename)

	@staticmethod
	def read(filename :Path, readtype:str = 'r') -> str:
		with open(file.get(filename), readtype) as f:
			return f.read()

	@staticmethod
	def write(filename :Path, content :str, writetype:str = 'w') -> None:
		with open(file.get(filename), writetype) as f:
			f.write(content)

	@staticmethod
	def delete(filename :Path) -> bool|str:
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


@api_level(0)
class lex_helpers:
	@staticmethod
	def is_whitespace(ch: str) -> bool:
		# return ch in spec.whitespace_ls
		...

	@staticmethod
	def is_digit(ch: str) -> bool:
		return "0" <= ch <= "9"

	@staticmethod
	def is_alpha(ch: str) -> bool:
		return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"

	@staticmethod
	def is_alnum(ch: str) -> bool:
		return lex_helpers.is_alpha(ch) or lex_helpers.is_digit(ch)

