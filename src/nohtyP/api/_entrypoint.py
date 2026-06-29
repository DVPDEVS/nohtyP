from nohtyP._impl.global_utilities.decorators import api_level
from nohtyP.__about__ import __version__
import sys

__all__ = [
    "entry",
]

@api_level(1)
class _entry_funcs:
    help_text = """
"""
    def _print_help() -> None:
        print(_entry_funcs.help_text)
    def entry() -> bool:
        #? this is called when running this package with "python -m nohtyP"
        # sanitize args and call funcs based on them.
        if len(sys.argv) > 0:
            args = sys.argv[1:] # rm first arg (path to file called to run)
        else: args = []
        print(args)
        #* help requested?
        if len(args) == 0 or"-h" in args or "--help" in args:
            _entry_funcs._print_help
            return True
        #* else
        op :str = ""
        fi = ""
        fo = ""
        ti = ""
        equiv = {
            "-T" : "tok",
            "-L" : "lex",
            "-P" : "par",
            "-C" : "com",
            "-R" : "run",
        }
        v_in = [
            "token",
            "lex",
            "parse",
        ]
        while True:
            if len(args) <= 0: break
            initial = args.pop(0).upper()
            # loop over each entry
            match initial:
                case _ if initial in equiv.keys(): # guarded default for catching OPs
                    op = equiv[initial]
                    # check if next is an in-type
                    if len(args) >= 1:
                        if args[1] in v_in:
                            ti = args.pop(0)
                case "-i":
                    if len(args) >= 1:
                        fi = args.pop(0)
                case "-o":
                    if len(args) >= 1:
                        fo = args.pop(0)
                case _ if len(args) >= 1: # prolly a file
                    if fi == "": fi = initial # infile
                    elif fo == "": fo = initial # outfile
                case _: break
            break
        #* then check results of argparsing and call the correct apis
        match op:
            case _: return

def entry() ->bool:
    _entry_funcs.entry()

