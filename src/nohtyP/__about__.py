from nohtyP._buildinfo import BUILD_DATA
_v_base = "0.0.1"
try:
    parts = []
    if BUILD_DATA._BUILD_DATE:
        parts.append(BUILD_DATA._BUILD_DATE)
    if BUILD_DATA._BUILD_DEVMODE:
        parts.append("dev")
    if BUILD_DATA._BUILD_STAGE:
        parts.append(BUILD_DATA._BUILD_STAGE)
    if parts:
        __version__ = _v_base + "+" + "_".join(parts)
    else:
        __version__ = _v_base
except Exception as e:
    print(e)  # useful while debugging
    __version__ = _v_base + "+unknown"
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
