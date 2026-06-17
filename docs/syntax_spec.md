# nohtyP Syntax Specification (.yp files)  

Superset of Python designed to transpile into standard python.  

File Extension: .yp  
*nohtyP* source code files.  

Design Python version: 3.10+  
*Due to support for `match` statements: see [PEP-634](https://peps.python.org/pep-0634/)*  

## Undecided syntax  

- Walrus operator  
- With/open  

## Optional features  

- Interoperability with standard Python  

## CORE PRINCIPLES  

1. Whitespace is lexically irrelevant - newlines, tabs, spaces are cosmetic only  
2. Semicolons (;) separate statements - ONLY hard delimiter  
3. Strict left-to-right evaluation within statements  
4. New operators extend flow without breaking Python semantics  
5. Barewords implicitly evaluate as strings unless shadowed by an in-scope variable, builtin, or known type.  

## LEXER RULES  

Whitespace (spaces/tabs/newlines) = token separation only, never syntax  

```txt
h h           -> ["h", "h"]
h, h          -> ["h", "h"]  (comma or whitespace = separator)
h,h           -> ["h", "h"]
"h,",h        -> ["h,", "h"]
"h","h"       -> ["h", "h"]
```

RULE: Comma separates ONLY if surrounded by whitespace on at least one side  

Special tokens:  
@ - iteration variable (current item in for loops / comprehensions)  

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

Barewords have to follow this regex:

```regex
^(?![0-9])\w+$
```

Which expands to the entire symbol being:

1. First character is alphabetical or an underscore '\_'  
    *Valid characters:*  
    *a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z \_*  
2. All following characters are alphanumericals or an underscore '\_'  
    *Valid characters:*  
    *a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 \_*  
3. The entire symbol is at least one character long  

Lexers MAY issue warnings when a bareword string appears in ambiguous positions (e.g., where an expression, not a literal, is expected).  

### Token separation  

Token separation is supported either through brackets `{}()`, whitespace, commas, or colons.  

Colon is, however, exclusively for type declarations and dictionaries.  
This may change in later specification versions.  

Since python will natively consider values in brackets to be dictionaries or tuples, nohtyP will not assume types for anything.  
Thus `(1,2)` is the same as `1 2` and dictionaries and tuples need a type declaration like this:  

```yp
tuple: (1,2) #? nums
```

This allows using zero whitespace in scripts :3  
This also means no operator characters can be used in most contexts:  
But thats a small loss for this being syntactically valid:  

```yp
10?range()?~{@%2~@*2?str()?}=*list[str]:res?print()
```

### Supported whitespace  

| Name                      | Escape   | Python shorthand |
|:--------------------------|:---------|:-----------------|
| Space                     | `\u0020` | `" "`            |
| Tab                       | `\u0009` | `\t`             |
| Line Feed                 | `\u000A` | `\n`             |
| Vertical Tab              | `\u000B` | `\v`             |
| Form Feed                 | `\u000C` | `\f`             |
| Carriage Return           | `\u000D` | `\r`             |
| File Separator            | `\u001C` |                  |
| Group Separator           | `\u001D` |                  |
| Record Separator          | `\u001E` |                  |
| Unit Separator            | `\u001F` |                  |
| Next Line                 | `\u0085` |                  |
| No-Break Space            | `\u00A0` |                  |
| Ogham Space Mark          | `\u1680` |                  |
| En Quad                   | `\u2000` |                  |
| Em Quad                   | `\u2001` |                  |
| En Space                  | `\u2002` |                  |
| Em Space                  | `\u2003` |                  |
| Three-Per-Em Space        | `\u2004` |                  |
| Four-Per-Em Space         | `\u2005` |                  |
| Six-Per-Em Space          | `\u2006` |                  |
| Figure Space              | `\u2007` |                  |
| Punctuation Space         | `\u2008` |                  |
| Thin Space                | `\u2009` |                  |
| Hair Space                | `\u200A` |                  |
| Line Separator            | `\u2028` |                  |
| Paragraph Separator       | `\u2029` |                  |
| Narrow No-Break Space     | `\u202F` |                  |
| Medium Mathematical Space | `\u205F` |                  |
| Ideographic Space         | `\u3000` |                  |

In Python:  

```py
whitespace: str = " \t\n\v\f\r\u001C\u001D\u001E\u001F\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"

string_token in whitespace
__import__('re').match(r"\s", string_token)
__import__('re').match(f"{"|".join(whitespace.split(''))}", string_token)
```

## Precendence layering and priority  

! Subject to review !  

| Layer | Operators                | Scope                   | Example -> Desugaring                                    |
|:------|:-------------------------|:------------------------|:---------------------------------------------------------|
| 1     | () [] . \*\*             | Python atoms/access     | lst\[0]                                                  |
| 2     | \* / // % + - << >> etc. | All Python binary/unary | 2 \*\* 3 \* 4 // 2 -> ((2 \*\* 3) \* 4) // 2             |
| 3     | Comparisons == in and or | Python logic            | x > 5 and y == 3                                         |
| 4     | {} blocks                | nohtyP execution        | {x?print()}                                              |
| 5     | ? =? ~ \*~ \*$ \*? #?    | nohtyP flow             | x \* 2 ? print() \*~ y -> if print(x \* 2) else y        |
| 6     | ;                        | Statement boundary      | a?b; c?d                                                 |

### {} Semantics  

- Executes statements until ;  
- If the block ends with a `?` flow operator, pipes the last value out  
- Otherwise returns None (like Python bare block)  
- REQUIRES terminal flow op for chainable results  

Example:   

```yp  
{ x > 0 ~ "pos" *~ "neg" ? } ? print()      # ✓ block yields value -> print  
{ x > 0 ~ "pos" *~ "neg" } ? print()        # ✗ block yields None -> print(None)  

{ x == 32 ~ True *~ False ?} -> val         # `val` is assigned a bool through a ternary  
{ risky() *? "fallback" ? } ? process()     # exception-safe value -> process  
```  

## REAL-WORLD COMPRESSION  

Example function:  

! To be remade !  

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

Additionally pipes the result of a block out of the block  

```yp
; { 1 5 :*list ? range() ?} ? print() ;
```

Non-assignable/non-pipable objects cannot succeed flow operators, eg.:  

```yp
*: 0 5 1 ? range() ? ; nums
```

`nums` does NOT recieve the output of `range(0, 5, 1)` here.  
This is equivalent to the following python:  

```py
range(0, 5, 1)
nums
```

### ASSIGNMENT & TYPES  

```yp
Python: num:int = 80085
nohtyP: int: 80085 = num
nohtyP: int: 80085 -> num
nohtyP: int: 80085 ? num
```

Additionally, any Python native augmented assignment is also applicable, such as:  

```py
num1, num2 = 0x12
num2 |= 3
num1 *= 4
```

### COMPOSITE LITERALS (#?)  

Assign a composite type (tuples, lists, sets, dictionaries) to the following object  
No brackets - type annotation defines container  

```yp
Python: ls:dict = {"type": "dict", "val": 8}
nohtyP: dict:"type":"dict","val":8 #? ls

nohtyP: list: string1 string2 #? print()
nohtyP: dict[str[int], str[str]]: value1 30 val2 hi #? print()
```

As a complication, lists and tuples passed into functions like range() need to be unpacked:  

```py
range(*[1,2,1])
```

This is marked in the type declaration as such:  

```yp
*: 1 2 1 ? range()
list: 2 45 3 #? var1 ; *: var1 ? range()
```

Notice that `?` is used for flowing the list as an argument, and not `#?`-assigning.  

Lest `range()` throws an exception. That's the price to pay for not passing arguments normally :)  
If it's declared to be unpacked, the translator will mark the passed object for unpacking at the next operation using the object.  
Else it's passed wholesale and *will* break.  

This 'unpacking mark' lasts ONLY until the next operation using the object takes place.  

On the upside, this forces type declaring in some capacity and is just good practice :3  

### CONTROL FLOW  

WHILE:  

```yp
Python: while(True): print("loop")
nohtyP: True ?= { 'loop' ? print() }
```

ITERATION (? ~ {}) (@ = current item):  

```yp
Python: for i in range(1, 20, 3): print(i)
nohtyP: *list: 1, 20, 3 ? range() ? ~ { @ ? print() }
```

CONDITIONALS (~ *~):  

```yp
Python: if True == 1: print("yes")
        else: print("no")
nohtyP: True == 1 ~ yes ? print() *~ no ? print()

Python: print( "yes" if True == 1 else "no" )
nohtyP: { True == 1 ~ yes *~ no ? } ? print()
```

COMPREHENSIONS (? ~ { ? })  

```yp
Python: list = [x*2 for x in range(10) if x % 2]
nohtyP: 10 ? range() ? ~ { @ % 2 ~ @ * 2 ?} -> list
```

MATCH:  

```yp
Python: test = "";
        match test:
            case "": ...
            case _: ...
nohtyP: "" = test; test ? match { "" ~ ... *~ _ ~ ... }

nohtyP: test ? match { 1, "s", *rest ~ ... }
```

### FUNCTIONS (reversed declaration)  

The function **body** appears first within a block, `{}`, followed by parameters (with optional defaults and type annotations), then the function name, optionally a return type, ending with `<- def`.  

```yp
Python:
def check(number1:int = 0) -> bool:
    return bool(number1)

nohtyP:
{ number1 ? bool() ? return } <- int: 0 ? number1 <- check -> bool <- def
```

#### Rules for functions  

- `{ ... }` always encloses the full function body.  
- Parameters appear after `<-`  
- Default values appear before the parameter they belong to, piped with `?`.  
- The function name follows the parameter list after `<-`.  
- Return type annotations use `->` as in Python.  
- Function types follow `def` declaration (async, etc.)  
- Decorators follow last in line as `<- <decorator>`  
- You may omit parameters entirely for zero‑argument functions:  

```yp
{ "hello" ? print() } <- greet <- def <- @staticmethod
```

- The body is fully composable - any valid nohtyP statements work inside.  
- Within a function body, reversed definitions, assignments, and flow operators behave identically to top‑level code.  

Example:  

```yp
{ * : a b ? add() ? return } <- int : a int : b <- sum -> int <- def
```

Equivalent Python:  

```py
def sum(a: int, b: int) -> int:
    return add(a, b)
```

Lambda functions have the following equivalent syntax:  

```yp
Python: lambda x: *2
nohtyP: { @ * 2 } <- x <- lambda
```

Where once again, `@` holds the passed value.  

Async operates similarly, too:  

```yp
Python: async def func() {
            await something()
        }

nohtyP: {something() ? await} <- func <- def async
```

### CLASSES (reversed declaration)  

Classes use the same directional logic as functions.  
The class **body** appears first within a block, `{}`, followed by optional base classes or mixins, then the name, ending with `<- class`.  

```yp
Python:
class MyThing(Base1, Base2):
    def hi(self):
        print("hi")
        return

nohtyP:
{ { "hi" ? print() ; return } <- self ? hi <- def } <- Base1, Base2 ? MyThing <- class
```

#### Rules for classes  

- `{ ... }` always encloses the full class body (methods, attributes, inner definitions).  
- Base classes follow `<-` just like default arguments or type hints in function form.  
- You may omit base list:  

  ```yp
  { pass } <- MyPlain <- class
  ```

- The body is fully composable - any valid nohtyP statements work inside.  
- Within a class body, reversed function or attribute assignments behave identically to top‑level definitions.  
- Decorators follow last in line as `<- <decorator>`  

#### Example  

```yp
{ "init" ? print(); { name ? print() ? return } <- self, str:name ? greet <- def } <- Friendly <- class
```

Equivalent Python:  

```py
class Friendly:
    print("init")
    def greet(self, name: str):
        print(name)
        return
```

Dataclasses:  

```yp
int:x int:y ? Point <- class <- @dataclass
```

## TODO: update

### ERROR HANDLING (* family) - Frame-local  

Frame scope = all operations left of *? up to the nearest semicolon (;) which is not within a block contained inside the current frame or block. Each semicolon boundary creates a new exception frame. Exception state does not cross semicolon delimiters unless explicitly passed via variable.  

Examples of scope:  
`'e' -> ltr ; { ... } ; smn() *$e *? $e ? print()` - Scope includes `smn()`  
`{ { 0 -> truth ; truth ? print() } *? woag ? print() }` - Scope includes the entire inner block `{}` including the assignment `0 -> truth` and not the rightwards `woag ? print()` call  

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

Python:   
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

## COMPRESSION EXAMPLES  

nohtyP (68 chars):  

```yp  
unsafe() *$e *? $e ? print() *? "couldnt print exception!" ? print()  
```  

Python (262 chars): 3 nested try/except blocks w/ value handling + feedback  

```py  
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

Example function 2:  

```py  
class Genes:  
    stats = [  
        "agr"   ,   # Aggression  
        "str"   ,   # Strength  
        "mut"   ,   # Mutation  
        "val"   ,   # Value  
        "sth"   ]   # Stealth  
    @staticmethod  
    def _make_stats_dict(*, values: list[float,] = None):  
        ret = {}  
        for i in Genes.stats: # maps values and Genes.stats one-to-one  
            ret += {Genes.stats[i]: 0.0 if values is None else float(abs(values[i])) if len(values) >= i-1 else 0.0,}  
        return ret  
```  

Equivalent in nohtyP:  

```yp  
{ agr str mut val sth :list #? stats ; { ret :dict[str, float] ; Genes.stats ? ~ { Genes.stats[@] values == None ~ 0.0 *~ values ? len() >= @-1 values[@] ? abs() ? float() *~ 0.0 :dict[str, float] += ret } ; ret ? return } <- (* None ? values :list[float,] ) ? _make_stats_dict <- def <- @staticmethod } <- Genes <- class  
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
