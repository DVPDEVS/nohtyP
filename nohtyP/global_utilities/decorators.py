"""Various decorators for fun, actual use, or warnings :3"""

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
	Overwrites any function to return an empty instance of its return type `T`"""
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
	`level == 1`: public  \n
	This is visible during runtime as a `<OBJ>.__NOHTYP_API_LEVEL` attribute."""
	if level == 0: value = "INTERNAL"
	elif level == 1: value = "PUBLIC"
	else: raise ValueError(f"Unsupported api level: {level}")
	def wrapper(_obj):
		_obj.__setattr__("__NOHTYP_API_LEVEL", value)
		return _obj
	return wrapper

def SPDX_license_mark():
	...

#? attributes
def fragile(_obj):
	"""Decorator to mark as fragile."""
	_obj.__setattr__("__fragile__",True)
	return _obj
def unstable(_obj):
	"""Decorator to mark as unstable."""
	_obj.__setattr__("__unstable__",True)
	return _obj
def regex(_obj):
	"""Decorator to mark use of regex."""
	_obj.__setattr__("__regex__", True)
	return _obj
def experimental(_obj):
	"""Decorator to mark as being experimental, in beta, etc."""
	_obj.__setattr__("__experimental__", True)
	return _obj
