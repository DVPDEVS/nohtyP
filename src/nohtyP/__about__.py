from nohtyP._buildinfo import BUILD_DATA
from re import search
"""
Construct version numbers based on _buildinfo.py  

Follows https://packaging.python.org/en/latest/specifications/version-specifiers/  
and https://peps.python.org/pep-0440/#public-version-identifiers  

That is, this scheme is followed:

```txt
[N!]N(.N)*[{a|b|rc}N][.postN][.devN]
```
"""

# exports
__all__ = [
    "__version__",
    "VERSIONS",
]
# wholesale version number
_v_base = "0.0.1"

try:
    _parts :list[str] = _v_base.split('.')
    # reconstruct as {date}.X.X.X[{stage}0][.dev0]
    _dm = "dev" if BUILD_DATA._BUILD_DEVMODE == True else ""
    _dm += BUILD_DATA._BUILD_DATE
    _s = BUILD_DATA._BUILD_STAGE[0] or '.'
    #* recombine and assign
    _partlist = [
        BUILD_DATA._BUILD_DATE,
        _parts[0],
        _parts[1],
        _parts[2],
    ]
    if BUILD_DATA._BUILD_STAGE:
        _partlist[-1] += _s + "0"
    if BUILD_DATA._BUILD_DEVMODE:
        _partlist.append("dev0")
    __version__ = '.'.join(_partlist)
except Exception as e:
    print(e)  # useful while debugging
    #? mark with an epoch in case of error. i dont plan to change this scheme so it should be fine
    __version__ = "1!" + _v_base

_split = __version__.split('.')

class VERSIONS:
    # static singleton versions. follow X.X.X+stage
    #* tbu with versions embedded in the actual modules
    BUILD_DATE           :str|None = f"{_split[0][6:]}.{_split[0][4:6]}.{_split[0][0:4]} (ddMMyyyy)"
    PACKAGE_VERSION      :str|None = __version__[9:]
    SYNTAX_VERSION       :str|None = "0.0.1+beta"
    TOKENIZER_VERSION    :str|None = "0.0.1+beta"
    LEXER_IDENT_VERSION  :str|None = "0.0.1+beta"
    LEXER_VAL_VERSION    :str|None = None
    PARSER_VERSION       :str|None = None
    TRANSLATOR_VERSION   :str|None = None
    TRANSPILER_VERSION   :str|None = None
    API_INTERNAL_VERSION :str|None = None
    API_PUBLIC_VERSION   :str|None = None
    BUILD_SCRIPT_VERSION :str|None = "0.0.1+beta"

