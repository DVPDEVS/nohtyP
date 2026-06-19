import inspect
import warnings

caller = inspect.currentframe().f_back
caller_name = caller.f_globals.get("__name__", "")

if not caller_name.startswith("nohtyP"):
    warnings.warn(
        "nohtyP.api is an internal compatibility layer and is not a "
        "supported import path. Use nohtyP.internal instead.",
        FutureWarning,
        stacklevel=2,
    )
