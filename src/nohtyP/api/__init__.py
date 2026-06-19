from nohtyP._guards import internal, warnings
if not internal:
    warnings.warn(
        "nohtyP.api is an internal compatibility layer and is not a "
        "supported import path. Use nohtyP.internal instead.",
        FutureWarning,
        stacklevel=2,
    )
