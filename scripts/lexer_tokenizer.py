import re
from lex import Lexer

class NohtyPLex(Lexer):
    # Define regular expressions for tokens
    whitespace = r'\s+'
    comment = r'#.*$'  # End of line comments
    string_quote = r"'|\""
    identifier = r'[a-zA-Z_][a-zA-Z0-9_]*'
    keyword = r'print|try|except'  # Initial set of keywords

    def __init__(self):
        super().__init__()
        self.add_pattern(self.whitespace, whitespace_token)
        self.add_pattern(self.comment, comment_token)
        self.add_pattern(self.string_quote, string_token)
        self.add_pattern(self.identifier, identifier_token)
        self.add_pattern(self.keyword, keyword_token)

    # Token functions
    def whitespace_token(self):
        return 'WS'

    def comment_token(self):
        return 'COMMENT'

    def string_token(self):
        return 'STRING'

    def identifier_token(self):
        return 'IDENTIFIER'

    def keyword_token(self):
        return 'KEYWORD'

# Define token actions
def WS(token):
    pass  # Ignore whitespace

def COMMENT(token):
    pass  # Ignore comments

def STRING(token):
    print(f"Found string: {token.value}")

def IDENTIFIER(token):
    print(f"Found identifier: {token.value}")

def KEYWORD(token):
    print(f"Found keyword: {token.value}")

# Create the lexer and start scanning
lexer = NohtyPLex()
lexer.scan("hello *? \"world\" ? print() # comment")