from nohtyP._guards import internal, warnings
if not internal:
    warnings.warn(
        "nohtyP._impl is an internal implementation module and is not a "
        "supported import path. Use nohtyP.internal instead.",
        FutureWarning,
        stacklevel=2,
    )
