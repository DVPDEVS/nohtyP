import re, utils
from __future__ import * 

class NohtyPLex:
	...

if __name__ == "__main__":
	# Create the lexer and start scanning
	lexer = NohtyPLex()
	lexer.scan("hello \"world\" ? print() # comment")

