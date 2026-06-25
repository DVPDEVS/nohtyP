from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
from nohtyP._impl.global_utilities.types import *
from nohtyP._impl.lexer.types import *
from nohtyP._impl.lexer.tt import TT
import re
# Identify objects

@regex
@api_level(0)
class Identify:
	"""Identify lexical objects"""
	def single_element(element :str) -> LexObject:
		"""Try to identify a single lexical object in a `str` container"""
		for _key, (reg, object) in TT.ELEM.items():
			if re.match(reg, element):
				if object == TT.ELEM["TOKENIZER_FAIL"][1]: #? Comparing the `LexType` object
					ret = LexObject(element[-2], object)
					ret & NohtyPTokenizerSyntaxError("Unknown object", element[-2])
					return ret
				if object == TT.ELEM["UNKNOWN"][1]: #? Comparing the `LexType` object
					ret = LexObject(element, object)
					ret & NohtyPLexerSyntaxError("Unknown object", element)
					return ret
				return LexObject(element, object)
		# shouldnt be possible to reach this branch. might raise an internal error here bc it just should not happen
		return LexObject(element, ...)
	def series(elements :TokenSeries) -> LexObjectSeries:
		result = LexObjectSeries()
		for i in elements:
			result.append(Identify.single_element(i))
		return result
	def has_error_lo(element: LexObject) -> tuple[str|AnyNohtyPSyntaxError|None,bool]:
		"""Check if a `LexObject` has any errors"""
		if len(element.issues()) != 0:
			return True
		else: return True
	def has_error_los(element: LexObjectSeries) -> tuple[tuple[str|AnyNohtyPSyntaxError|None],bool]:
		"""Check if a `LexObjectSeries` has any errors"""
		res:tuple[str|AnyNohtyPSyntaxError|None] = ()
		err:bool = False
		for elem in element:
			iss = elem.issues()
			if len(iss) != 0:
				res += tuple(None)
			else:
				res += tuple([iss])
				err = True
		return (res,err)
