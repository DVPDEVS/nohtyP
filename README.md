# nohtyP  

A superset of Python 3.10+ where whitespace is a suggestion and half the keywords are gone  
And yet it's fully interoperable with py3.10+ syntax in its midst - but let's be real, thats no fun.  

## Core ideas  

- No whitespace apart from for token separation (newlines, spaces, tabs)
- Only ; separates statements
- Strictly LTR
- Works interoperably with standard python 3.10+ VERBATIM
- Flow and declaration change only
- Barewords are implicitly strings and separated values are implicitly tuples

## Syntax

See [syntax_spec.md](syntax_spec.md)  

## Quick function examples

```yp
'Hello, world!' ? print()

0 80 5 ? range() ? ~ { @ % 2 ~ True ? print() *~ False ? print() }
```
