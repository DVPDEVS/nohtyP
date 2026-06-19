# nohtyP  

A superset of Python 3.10+ where whitespace is a suggestion and half the keywords are gone  

## Core ideas  

- No whitespace apart from for token separation (newlines, spaces, tabs, etc.)  
- Only ; separates statements  
- Strictly LTR  
- Flow and declaration change only  
- Barewords are implicitly strings and separated values are implicitly tuples  

## Licensing  

See [./LICENSE](./LICENSE)  

## Syntax  

See [syntax_spec.md](./docs/syntax_spec.md)  

## Reference implementation  

Source code is found under [src/](/src/)  
Documentation and explanations will be under [docs/](/docs/)  

## Quick function examples  

```yp
'Hello, world!' ? print()

0 80 5 ? range() ? ~ { @ % 2 ~ True *~ False ?} ? print()

Exquisite -> s ; 1 s ? :list[int] len() 1 ? range() ? ~ { @ % 3 ~ @ *~ '' ?} ? print() 

*set -e ; unsafe() ; exploding() *? $_setError ? print() ; *set +e ; safe() 
```

## Plans  

As of writing this i have a v0.0.1 of the tokenizer ready.  
I have a bunch of plans for how the lexer and parser should work, which ill summarize here.  
The syntax spec has been updated, too!  

| Directory  | Item         | Responsibility                                                                                          |
|:-----------|:-------------|:--------------------------------------------------------------------------------------------------------|
| lexer/     | Tokenizer    | Accepts a string or file reference and return the contents split according to lexical spec.             |
| lexer/     | Lexer        | Two parts, see below                                                                                    |
| lexer/     | - Identifier | Identify lexical elements in a passed `TokenSeries`. Return a `LexObjectSeries`.                        |
| lexer/     | - Validator  | Validate string quote closing, bracket closing, and emits faults into the `LexObjectSeries`.            |
| lexer/     | Parser       | Identify semantic intent, validate structure, correct previous steps' faults, generate a `ParseObject`. |
| transpile/ | Translator ? | Optional step to convert the structure of the `ParseObject` into valid Pythonic structure.              |
| transpile/ | Transpiler   | Convert the resulting `ParseObject` into Python code.                                                   |

Ill be making more specsheets for what each element aims to generate etc.  

Further plans include a step already taken; Making this a python package. Thus transpiling is just `python -m nohtyP <fileRef>` :3  
Each element is to support outputting just the result of itself too, so its easy to see how your file is parsed in each step.  
