import inspect
import warnings

caller = inspect.currentframe().f_back
caller_name = caller.f_globals.get("__name__", "")

if not caller_name.startswith("nohtyP"):
    warnings.warn(
        "nohtyP._dev is an internal development module and is not a "
        "supported import path. This should not be available to you.",
        FutureWarning,
        stacklevel=2,
    )
