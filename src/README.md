# nohtyP  

A superset of Python 3.10+  

## License

See [./LICENSES/notice.md](./LICENSES/notice.md)  
... To be updated post-beta  

## Table of Contents  

- [Header](#nohtyp)
  - [License](#license)
  - [TOC](#table-of-contents)
  - [Links](#links)
  - [Usage](#usage)
    - [Python](#python)
    - [Commandline](#commandline)

## Links  

...  

## Versioning scheme  

Version numbers follow this scheme:  

```plaintext
{base_version (eg. 0.0.1)}+r{build_date as ddmmyyyy}[.dev][.{project_stage}]
```

Should the version number creation fail for any reason this will instead become:  

```plaintext
{base_version (eg. 0.0.1)}+unknown
```

Examples:

```plaintext
0.0.1+r01072026.dev.beta -> package version 0.0.1, packaged 1st of June 2026, developer package, beta stage of development
0.2.3+r32053072          -> package version 0.2.3, packaged 32nd of May 3072, release package, mature stage of development
```

This build date acts as a build number.  
For the actual internals' versions, check with the help option or read the `__about__.py` file.  

## Usage  

### Python

Supported APIs are all made available at top-level:  

```py
from nohtyP import *
from nohtyP import transpile
from nohtyP import internal
```

All other APIs are to be considered unstable and will emit `FutureWarning` should you use them anyways.  
This includes but is not limited to:  

- `nohtyP.api.*`
- `nohtyP._impl.*`
- `nohtyP._dev.*`   (only available in dev wheels and source)

Normal usage should be through CLI (see [below](#commandline)).  
The equivalent functions are, however, available as:  

- `nohtyP.tokenize`
- `nohtyP.lex`
- `nohtyP.parse`
- `nohtyP.transpile`

And have descriptions for use in heredocs.  

The internal implementation is to be considered SEMI-stable if it is available through `nohtyP.internal`  
This is a structured API surface and the only supported way to interact with internal implementations.  

### Commandline  

```sh
python -m nohtyP [ [<operation> [<in-type>] ] [-i] <in-file> [-o] [<out-file>] | ( -h | --help ) ]
```

Where `<operation>` is one of the following:

- -T
  - Tokenize the input file
- -L
  - `-T` + lexically identify and validate the input file
- -P
  - `-L` + syntactically parse and validate the input file
- -C
  - `-P` + transpile the input file
- -R
  - `-C` and run the output file

If `<in-type>` is given, `<operation>` will skip earlier steps based on it.  
Valid options:  

- `token`
- `lex`
- `parse`

`<in-type>` cannot be the same as or a later step than `<operation>`.  

Already transpiled files should be run directly with python.  
