# Run the tokenizer tests
from .tests import *
from sys import argv

test_set = [
	"Tokenizer.basic",
	"Tokenizer.vnums",
	"Tokenizer.inums",
	"Tokenizer.stress",
]

if __name__ == "__main__":
	args = argv
	if len(args) >= 2:
		if args[1] == "v":
			verbmode = True
			showmode = True
		elif args[1] == "q":
			quietmode = True
		elif args[1] == "s":
			showmode = True
		args.pop(1)
	unittest.main(
		argv=args,
		verbosity = 0 if quietmode else 2 if verbmode else 1,
		defaultTest=test_set
		)
