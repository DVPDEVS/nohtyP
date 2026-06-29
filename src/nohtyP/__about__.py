from __future__ import annotations
v_base = "0.0.1+"
__version__ = v_base + _BUILD_DATE + "_dev" if _BUILD_DEVMODE else ''
class internal_versions:
    __syntax_version__       :str|None = "0.0.1-beta"
    __tokenizer_version__    :str|None = "0.0.1-beta"
    __lexer_ident_version__  :str|None = "0.0.1-beta"
    __lexer_val_version__    :str|None = None
    __parser_version__       :str|None = None
    __translator_version__   :str|None = None
    __transpiler_version__   :str|None = None
    __api_internal_version__ :str|None = None
    __api_public_version__   :str|None = None

_g = globals().keys()
if "_BUILD_DEVMODE" not in _g:
    _BUILD_DEVMODE = False
if "_BUILD_DATE" not in _g:
    _BUILD_DATE = "UNSET"

# area for build script to append devmode and build date:
