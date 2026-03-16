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

0 80 5 ? range() ? ~ { @ % 2 ~ True *~ False ?} ? print()

Exquisite -> s ; 1 s ? len() 1 :list[int] ? range() ? ~ { @ % 3 ~ @ *~ '' ?} ? print() 

*set -e ; unsafe() ; exploding() ; $_setError ? print() ; *set +e ; safe() 
```

## Plans

To begin with, i need to make the lexer and tokenizer functional.  
Next the translator should use the result to transpile into a standard python script and run it.  
Once more of the syntax is locked in, a runtime should be made, as well as a script to generate it.  
At some point the code should also get a version written in nohtyP!  
Ill also want to make a wheel package to support the nohtyP syntax inside python scripts.  

At a later point i might remake it to compile directly to .pyc files :3  
