# nohtyP Syntax Specification (.yp files)

File Extension: .yp
*nohtyP* source code files. FULLY INTERCOMPATIBLE with standard Python 3.10+

## CORE PRINCIPLES

1. Whitespace is lexically irrelevant - newlines, tabs, spaces are cosmetic only
2. Semicolons (;) separate statements - ONLY hard delimiter  
3. Strict left-to-right evaluation within statements
4. Standard Python code works VERBATIM - imports, functions, classes, literals
5. New operators extend flow without breaking Python semantics
6. Barewords implicitly evaluate as strings unless shadowed by an in-scope variable, builtin, or known type.

## LEXER RULES

Whitespace (spaces/tabs/newlines) = token separation only, never syntax

```txt
h h           -> ["h", "h"]
h, h          -> ["h", "h"]     (comma+whitespace = separator like space)
h,h           -> ["h,h"]        (no whitespace = single token)
"h,",h        -> ["h,", "h"]    
"h","h"       -> ["h", "h"]
```

RULE: Comma separates ONLY if surrounded by whitespace on at least one side

Special tokens:
@ - iteration variable (current item in ? ~ {})

### Bareword Resolution

Unquoted identifiers (barewords) are parsed as string literals *unless*:

1. A variable with that name exists in local or global scope,
2. The name matches a builtin or imported type,
3. It appears in a syntactic context where a keyword or known symbol is required.

Otherwise, the bareword is treated as `"bareword"`.

Examples:

```yp
count = 5  
world ? print()       -> print("world")  
count ? print()       -> print(count)  
int ? print()         -> print(<class 'int'>)  
```

Lexers MAY issue warnings when a bareword string appears in ambiguous positions (e.g., where an expression, not a literal, is expected).

## OPERATORS (left-to-right precedence)

1. () - function calls, grouping
2. { ... } - blocks of execution, ignores semicolon frame delimiting
3. \*$ \*? #? - compound operators  
4. ? ?= ~ \*~ - unary flow operators
5. ; - statement boundary

## SYNTAX BY CATEGORY

### FLOW OPERATOR (?)
Pipe previous value into next object

```yp
Python: print("Hello, world!")
nohtyP: "Hello, world!" ? print()

Python: print("Hello"); input("nem > ")
nohtyP: "Hello" ? print(); "nem > " ? input()
```

### ASSIGNMENT & TYPES

```yp
Python: num:int = 80085
nohtyP: 80085 = num:int
nohtyP: 80085 -> num:int
nohtyP: 80085 ? num:int
```

### COMPOSITE LITERALS (#?)
No brackets - type annotation defines container

```yp
nohtyP: ls:dict #? "type":"dict""val":8
Python: ls:dict = {"type": "dict", "val": 8}

nohtyP: "type":"dict" "val":8 #? ls:dict
nohtyP: string1 string2 :list ? print()
nohtyP: value1 30 val2 hi :dict[str[int], str[str]] ? print()
```

### CONTROL FLOW

WHILE:

```yp
Python: while(True): print("loop")
nohtyP: True ?= { 'loop' ? print() }
```

ITERATION (? ~ {}) (@ = current item):

```yp
Python: for i in range(1, 20, 3): print(i)
nohtyP: 1, 20, 3 ? range() ? ~ { @ ? print() }
```

CONDITIONALS (~ *~) (NO if/elif/else):

```yp
Python: if True == 1: print("yes") else: print("no")
nohtyP: True == 1 ~ yes ? print() *~ no ? print()
```

MATCH:

```yp
Python: test = ""; match test: case "": ... case _: ...
nohtyP: "" = test; test ? match { "" ~ ... *~ _ ~ ... }
```

### FUNCTIONS (reversed declaration)

```yp
Python: def check(number1:int = 0) -> bool: return bool(number1)
nohtyP: { number1 ? bool() ? return } <- 0 ? number1:int ? check -> bool <- def
```

### ERROR HANDLING (* family) - Frame-local

Frame scope = all operations left of *? up to the nearest semicolon (;). Each semicolon boundary creates a new exception frame. Exception state does not cross semicolon delimiters unless explicitly passed via variable.

STORE EXCEPTION:

```yp
nohtyP: unsafe() *$e
Python: try: unsafe() except Exception as e: $e = e
```

HANDLE w/o STORE:

```yp
nohtyP: unsafe() *? "EXCEPTION" ? print()
Python: try: unsafe() except Exception: print("EXCEPTION")
```

CAPTURE + CONTINUE + HANDLE:

```yp
nohtyP: unsafe() *$e ? safe() *? $e ? print()
```

FULL NESTED (3 try/excepts, 68 chars):

```yp
nohtyP: unsafe() *$e *? $e ? print() *? "couldnt print exception!" ? print()
```

RULES:

- *$name captures Exception object into variable
- *? triggers ONLY for leftward exceptions in same frame
- Handlers can fail (not protected by own *?)
- Variables persist (normal Python scope)

### GLOBAL ERROR MODE

```yp
nohtyP: *set -e ; risky() ; *set +e
```

Effect: All expressions auto-wrapped try: expr except: $_setError = e

*set +e clears $_setError  
*? needs local exception to trigger, can read $_setError for diagnostics

### META ACTIONS

```yp
Python: import subprocess
nohtyP: subprocess ? go fetch
```

## INTERCOMPATIBILITY WITH STANDARD PYTHON

Standard Python syntax may appear interleaved with nohtyP syntax in .yp source. Mixed-mode parsing is supported; unrecognized constructs are passed through unchanged to the Python compiler.

ALL THESE WORK VERBATIM IN .yp:

```py
import sys
def normal_python(x): return x * 2
class MyClass: pass
x = [1, 2, 3]
for i in x: print(i)
try: risky() except: pass
```

## COMPRESSION EXAMPLE

```py
nohtyP (68 chars): unsafe() *$e *? $e ? print() *? "couldnt print exception!" ? print()
Python (262 chars): 3 nested try/except blocks w/ value handling + feedback 

__value = None
__exit = None
try:
    try:
        try:
            __value = unsafe()
        except Exception as e:
            __exit = e
        safe(__value)
    except Exception:
        print(__exit)
except Exception:
    print("couldnt print exception!")
```

## WHITESPACE EXAMPLE (identical parsing)

```yp
unsafe() *$e ? safe() *? $e ? print()
```

```yp
            unsafe()
        *$e
?
                                            safe()
    *?
$e
                ?
                    print()
```

## RUNTIME

Pure Python 3.10+ superset. Transpiles to standard Python AST. No VM changes.  

The translator performs bareword resolution and whitespace normalization before AST translation. It preserves all standard Python semantics during mixed-syntax parsing.  
