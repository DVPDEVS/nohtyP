v_base = "0.0.1"
__version__ = v_base+"+dev" if __import__("os").getenv("_YP_HATCH_BUILD_MODE", "release") == "dev" else v_base
class internal_versions:
    __syntax_version__      :str|None = "0.0.1-beta"
    __tokenizer_version__   :str|None = "0.0.1-beta"
    __lexer_ident_version__ :str|None = "0.0.1-beta"
    __lexer_val_version__   :str|None = None
    __parser_version__      :str|None = None
    __translator_version__  :str|None = None
    __transpiler_version__  :str|None = None

