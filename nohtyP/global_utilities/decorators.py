def regex(fn):
	"""Regex adjacent function decorator"""
	return fn

def vibe_check(vibe: str):
	"""Vibe checking decorator"""
	def wrapper(fn):
		if not (":3" in vibe): raise ValueError(f"Vibe `{vibe!r}` is NOT silly enough")
		return fn
	return wrapper

def stub(fn):
	"""Stub function generator.  \n
	Syntax:
	```python
	@stub
	def a_func() -> T: ...
	```  \n
	Ovverwrites any function to return an empty instance of its return type `T`"""
	from typing import get_type_hints, get_origin
	t = get_type_hints(fn).get("return")
	ot = get_origin(t) or t
	def wrapper(*args, **kwargs):
		try: return ot()
		except: return None
	return wrapper

def api_level(level: int):
	"""Decorator to mark as internal or public  \n
	`level == 0`: internal  \n
	`level == 1`: public"""
	if level == 0: value = "INTERNAL"
	elif level == 1: value = "PUBLIC"
	else: raise ValueError(f"Unsupported api level: {level}")
	def wrapper(_obj):
		_obj.__setattr__("__NOHTYP_API_LEVEL", value)
		return _obj
	return wrapper


