from __future__ import annotations
from nohtyP._impl.global_utilities.decorators import *
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
				if element == TT.ELEM["TOKENIZER_FAIL"]:
					ret = LexObject(element[-2], object)
					ret &= "Tokenizer failure - unknown object"
				if element == TT.ELEM["UNKNOWN"]:
					ret = LexObject(element, object)
					ret &= "Lexer failure - unknown object"
				else:
					return LexObject(element, object)
		return LexObject(element, ...)
	def series(elements :TokenSeries) -> LexObjectSeries:
		result = LexObjectSeries()
		for i in elements:
			result.append(Identify.single_element(i))
		return result
