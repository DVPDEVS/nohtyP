from nohtyP._impl.global_utilities.decorators import api_level
from nohtyP.__about__ import __version__
import sys
from pathlib import Path

__all__ = [
    "entry",
]

@api_level(1)
class _entry_funcs:
    help_text = f"""
NohtyP v{__version__}
"""
    def _print_help() -> None:
        print(_entry_funcs.help_text)
    def _report_option_error(index :int) -> None:
        if index >= 0: raise ValueError("Expected negative index")
        args = sys.argv[1:]
        inv_index = len(args) + index # index should be negative
        error_entry = "'" + " ".join(args) + "'\n\t"
        for i in range(inv_index):
            error_entry += " " * len(args[i]) + "  "
        error_entry += "^" * len(args[index])
        print(f"\nNohtyP:\tArgument not recognized!\n\t{error_entry}")
    def entry() -> bool:
        #? this is called when running this package with "python -m nohtyP"
        # sanitize args and call funcs based on them.
        if len(sys.argv) > 1:
            args = sys.argv[1:] # rm first arg (path to file called to run)
        else: args = []
        print(args)
        #* help requested?
        if args == [] or "-h" in args or "--help" in args:
            _entry_funcs._print_help()
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
            initial = args.pop(0)
            # loop over each entry
            match initial:
                case _ if initial in equiv.keys(): # guarded default for catching OPs
                    op = equiv[initial]
                    # check if next is an in-type
                    if len(args) >= 1:
                        if args[0] in v_in:
                            ti = args.pop(0)
                    continue
                case "-i":
                    if len(args) >= 1:
                        fi = args.pop(0)
                    continue
                case "-o":
                    if len(args) >= 1:
                        fo = args.pop(0)
                    continue
                case _ if Path(initial).exists() and Path(initial).is_file(): # prolly a file
                    if fi == "": fi = initial # infile
                    elif fo == "": fo = initial # outfile
                    continue
                case _:
                    _entry_funcs._report_option_error(-(len(args)+1))
                    break
            break
        #* then check results of argparsing and call the correct apis
        match op:
            case _: return

def entry() ->bool:
    _entry_funcs.entry()

