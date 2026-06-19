from nohtyP._guards import internal, warnings
if not internal:
    warnings.warn(
        "nohtyP._dev is a development module and is not a supported import path.",
        FutureWarning,
        stacklevel=2,
    )
