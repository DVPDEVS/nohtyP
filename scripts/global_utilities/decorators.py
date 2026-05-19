def regex(fn):
    """Regex adjacent function decorator"""
    return fn
def vibe_check(fn, vibe):
    """Vibe checking decorator"""
    if not (":3" in vibe): raise ValueError(f"Vibe `{vibe!r}` is NOT silly enough")
    return fn


