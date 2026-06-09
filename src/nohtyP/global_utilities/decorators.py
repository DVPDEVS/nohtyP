"""Various decorators for fun, actual use, or warnings :3"""

def vibe_check(vibe: str) -> function|type|object|any:
	"""Vibe checking decorator"""
	def wrapper(_obj: object) -> object:
		if not (":3" in vibe): raise ValueError(f"Vibe `{vibe!r}` is NOT silly enough")
		return _obj
	return wrapper

def stub(fn: function) -> function:
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

def api_level(level: int) -> function|type|object|any:
	"""Decorator to mark as internal or public  \n
	`level == 0`: internal  \n
	`level == 1`: public  \n
	This is visible during runtime as a `<OBJ>.__NOHTYP_API_LEVEL` attribute."""
	if level == 0: value = "INTERNAL"
	elif level == 1: value = "PUBLIC"
	else: raise ValueError(f"Unsupported api level: {level}")
	def wrapper(_obj: object) -> object:
		setattr(_obj, "__NOHTYP_API_LEVEL", value)
		return _obj
	return wrapper

def test(_obj: function|type|object|any) -> function|type|object|any:
	"""Test objects are excluded from apilevel markers and SPDX License identifiers in attributes.  \n
	Instead they're to be considered as internal regardless.  \n
	The apilevel and license decorators and their associated attribute marks are for testing only.  \n
	This decorator writes a `<OBJ>._TEST_OBJECT == True` attribute for runtime detection."""
	setattr(_obj, "_TEST_OBJECT",True)
	return _obj

from .types import SPDX_License_Identifers
def license(license: SPDX_License_Identifers) -> function|type|object|any:
	"""Decorator to register an SDPX license ID.  \n
	`<OBJ>.SPDX_LICENSE_IDENTIFIER == "<identifier>"`"""
	def wrapper(_obj: object) -> object:
		setattr(_obj, "SPDX_LICENSE_IDENTIFIER", license)
		return _obj
	return wrapper

#? attributes
def fragile(_obj: function|type|object|any) -> function|type|object|any:
	"""Decorator to mark as fragile."""
	setattr(_obj, "__fragile__",True)
	return _obj
def unstable(_obj: function|type|object|any) -> function|type|object|any:
	"""Decorator to mark as unstable."""
	setattr(_obj, "__unstable__",True)
	return _obj
def regex(_obj: function|type|object|any) -> function|type|object|any:
	"""Decorator to mark use of regex."""
	setattr(_obj, "__regex__", True)
	return _obj
def experimental(_obj: function|type|object|any) -> function|type|object|any:
	"""Decorator to mark as being experimental, in beta, etc."""
	setattr(_obj, "__experimental__", True)
	return _obj
