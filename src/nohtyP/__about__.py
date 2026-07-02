from nohtyP._buildinfo import BUILD_DATA
from re import search

__all__ = [
    "__version__",
    "internal_versions",
]

# dynamic wholesale version for build versioning and dev tag
_v_base = "0.0.1"
try:
    parts = []
    if BUILD_DATA._BUILD_DATE:
        parts.append("r" + BUILD_DATA._BUILD_DATE)
    if BUILD_DATA._BUILD_DEVMODE == True:
        parts.append("dev")
    if BUILD_DATA._BUILD_STAGE:
        parts.append(BUILD_DATA._BUILD_STAGE)
    if parts:
        __version__ = _v_base + "+" + ".".join(parts)
    else:
        __version__ = _v_base + "+unknown"
except Exception as e:
    print(e)  # useful while debugging
    __version__ = _v_base + "+unknown"

class internal_versions:
    # all single versions are static
    #* tbu with versions embedded in the actual modules
    # try:
    #     with open("../../docs/syntax_spec.md", "r") as f:
    #         #? pluck out the version from the syntax doc using regex - https://regex101.com/r/e4qdsk/2
    #         m = search("^Version.{2}(([\d\d{2}])\.([\d\d{2}])\.([\d\d{2}])([\.\-\w]*))\b$", f.read())
    #         # SHOULD be line 5 of the syntax spec
    #         SYNTAX_VERSION: str = m.group(0) if m else "0.0.1-beta"
    # except:
    SYNTAX_VERSION       :str|None = "0.0.1-beta"
    TOKENIZER_VERSION    :str|None = "0.0.1-beta"
    LEXER_IDENT_VERSION  :str|None = "0.0.1-beta"
    LEXER_VAL_VERSION    :str|None = None
    PARSER_VERSION       :str|None = None
    TRANSLATOR_VERSION   :str|None = None
    TRANSPILER_VERSION   :str|None = None
    API_INTERNAL_VERSION :str|None = None
    API_PUBLIC_VERSION   :str|None = None
    BUILD_SCRIPT_VERSION :str|None = "0.0.1-beta"

