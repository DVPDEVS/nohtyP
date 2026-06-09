# note: has to handle sep by whitespace AND semicolon

from nohtyP.lexer.types import TokenSeries
from nohtyP.global_utilities.decorators import api_level
from pathlib import Path

__all__ = [
    "whitespace",
    "tokenize",
]

whitespace :str = " \t\n\v\f\r\u001C\u001D\u001E\u001F\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"

@api_level(0)
class funcs:
    def tokenize(text :str) -> TokenSeries:
        result = TokenSeries()
        #* loop over text, check for whitespace / semicolon, append to result
        #* separate on all valid operators, too
        token = ""
        for i in range(len(text)):
            char = text[i]
            if char in whitespace and char == token[-1]:
                continue
            if char == ":":
                token += char + text[i+1]
                continue
            if char in whitespace:
                result.append(token)
                token = ""
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
