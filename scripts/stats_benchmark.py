# Resources for benchmarking and generating stats
# Might use matplotlib or pygame later but ill start with shell scripts, numpy, and pympler.asizeof
from pympler.asizeof import asizeof
import numpy as np
from lex_tt import TT

class memoryUsage():
    # Objects to check first
    __TEMPLATE__ = {'obj':object, 'val':np.uint64, 'name':str } # As { getattr(parent/class, '_parent/classOBJECT').copy(), ram_usage, "variable name"}
    def __init__(self):
        self._OBJECTS: list[dict[object, np.uint64]] = [
        # I suspect this object would be the worst tbh.
            { 
                'obj': getattr(TT, '_TT__DIFF').copy(), # Actaully refers to `TT.__DIFF` but safely (name mangling)
                'val': np.uint64, 
                'name': "TT.__DIFF" },
        ]

        # Get ram usage of all the types
        for i in self._OBJECTS: i['val'] = np.uint64(asizeof(i['obj']))

if __name__ == "__main__":
    print("\n".join([f"{i['name']} ({type(i['obj']).__name__}): {i['val']}" for i in memoryUsage()._OBJECTS]))

