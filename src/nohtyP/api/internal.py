# SPDX-License-Identifier: AGPL-3.0-only
from nohtyP.global_utilities.decorators import api_level, license, SPDX_License_Identifers

@license(SPDX_License_Identifers.AGPL3_o)
@api_level(0)
class internal:
    """Internal APIs"""
    #? this class is imported in __init__.py at root level
    ...
    class lexer:
        class objects:
            from nohtyP.lexer.lex_tt import TT, TT_CTX, TT_NOHTYP, TT_PYTHON, REGEX_TT