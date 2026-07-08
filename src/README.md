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

Base version (base_version) follows Major.Minor.Micro  
The encoded build date (build_date) is in yyyyMMdd  
Project stage (project_stage) is the first character of "alpha" or "beta", or nothing.  

Version numbers follow this scheme:  

```txt
{build_date}.{base_version}[{project_stage}0][.dev0]
```

No version information is to succeed stage marker or devloper release marker.  
Therefore they are to be followed by a '0' to comply with PEP440.  

Should the version number creation fail for any reason it will instead be marked with an epoch:  

```txt
1!{base_version}
```

Examples:

```txt
08072026.0.0.1b0.dev0 -> package version 0.0.1, packaged 8th of July 2026, developer package, beta stage of development
32053072.0.2.3        -> package version 0.2.3, packaged 32nd of May 3072, release package, mature stage of development
1!1.4.2               -> build failure - you should not see this, assumedly unstable
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
