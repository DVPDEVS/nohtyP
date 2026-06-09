from __future__ import annotations
from nohtyP.global_utilities.decorators import *
from nohtyP.lexer.types import *
# from nohtyP.lexer.tt import TT, PY
import re
# Identify objects

@regex
@api_level(0)
class Identify:
	"""Identify lexical objects"""
	def single_element(element :str) -> LexObject:
		"""Try to identify a single lexical object in a `str` container"""
		for key, (reg, object) in TT.YP.items():
			if re.match(reg, element):
				return LexObject(element, object)
		for key, regex in PY.REGEX:
			if re.match(regex, element):
				return LexObject(element, PY.ELEM[key])
		return LexObject(element, ...)
	def series(elements :TokenSeries) -> LexObjectSeries:
		result = LexObjectSeries()
		for i in elements:
			result.append(Identify.single_element(i))
		return result

from typing import reveal_type

reveal_type(TT)
reveal_type(TT.G)
