# Run the tokenizer tests
from .tests import *
from sys import argv

test_set = [
	"Tokenizer.basic",
	"Tokenizer.vnums",
	"Tokenizer.inums",
	"Tokenizer.stress",
	"Tokenizer.realistic_input",
]

if __name__ == "__main__":
	args = argv
	if len(args) >= 2:
		if args[1] == "v":
			modes.verbmode = True
			args.pop(1)
		elif args[1] == "q":
			modes.quietmode = True
			args.pop(1)
	if len(args) >= 2:
		if args[1] == "s":
			modes.showmode = True
			args.pop(1)
	unittest.main(
		argv=args,
		verbosity = 0 if modes.quietmode else 2 if modes.verbmode else 1,
		defaultTest=test_set
		)
