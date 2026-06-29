# SPDX-License-Identifier: AGPL-3.0-only
from nohtyP._impl.global_utilities.decorators import api_level, license, SPDX_License_Identifers

__all__ = [
    "internal",
]

@license(SPDX_License_Identifers.AGPL3_o)
@api_level(0)
class internal:
    """Internal APIs"""
    #? this class is imported in __init__.py at root level
    class lexer:
        class objects:
            # class TT:
            #     from nohtyP.lexer.identifier import TT, TT_CTX, TT_NOHTYP, TT_PYTHON, REGEX_TT
            class types:
                from nohtyP._impl.lexer.types import lexer_langs, LexType
            from nohtyP._impl.lexer.utils import file, lex_helpers
