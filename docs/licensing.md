# Licensing, Copyright, and Attribution  

At present, this project is licensed under the GNU AGPL v3.0 only  
for the duration of active development.  

The licensing structure may change in later releases or after beta.  
The current intended structure is roughly as follows:  

| Part                               | License                            |
| ---------------------------------- | ---------------------------------- |
| Transpiler, core and tooling APIs  | [AGPLv3](../LICENSES/AGPL-3.0.txt) |
| Public runtime libraries/helpers   | LGPLv3 or MPL-2.0                  |
| Internal transpiler modules        | [AGPLv3](../LICENSES/AGPL-3.0.txt) |
| Specifications, docs, tutorials    | CC BY 4.0                          |
| Generated ordinary code            | Exempt                             |
| Generated code embedding internals | Not exempt                         |

## Generated Code  

Generated code is generally considered exempt from the AGPLv3.  

However, this exemption does **not** apply where generated code:  

- embeds compiler internals,  
- ships substantial implementation components,  
- uses internal AST/compiler APIs,  
- integrates deeply with transpiler internals,  
- redistributes portions of the implementation.  

Use of documented public APIs alone does not, by itself,  
create a derivative work.  

## API Boundaries  

All APIs, modules, and implementation components are intended to  
be classified as either public or internal. These classifications  
will be documented in the codebase and are intended to guide  
correct usage and licensing boundaries. They should be treated  
as authoritative within the context of this project.  

## Intent and Design  

This structure is designed to protect the implementation and  
tooling ecosystem while still allowing community and  
commercial development using the language itself.  

## Attribution  

Attributions may change over time and currently include, but  
are not limited to, the following:  

- [DVP-F/Carnx00](https://github.com/DVP-F)  
- [nohtyP](https://github.com/DVPDEVS/nohtyP)  

## License Files  

All applicable licenses are located under: [../LICENSES/](../LICENSES)  

## Component Licensing  

Each source file, module, API surface, and implementation component  
is intended to include an appropriate copyright and licensing notice,  
or a reference to the applicable license where appropriate.  

## SPDX Identifiers  

This project intends to use [SPDX license identifiers](https://spdx.org/) to  
clearly indicate licensing within source files and other  
relevant components.  
