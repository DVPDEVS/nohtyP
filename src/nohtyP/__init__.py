#? init point of the package
# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package 
# https://docs.python.org/3/library/distribution.html 

# show the public api surfaces here

from nohtyP.api.public import *
from nohtyP.api.internal import internal

__all__ = [
    "decorators",
    "types",
    "internal",
]

#* type shi
