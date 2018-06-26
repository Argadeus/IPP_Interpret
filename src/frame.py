# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		frame.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Frame module is used as a part of the interpreter as an abstract
#          data type for storing and manipulating variables
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.constants import Constant
from src.exceptions import *
from src.debug import Debug

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Frame():

	def __init__(self, defined = False):
		self._defined = defined
		self._variables = dict()

	def define_variable(self, var: str):
		"""Defines a variable of a given name within the frame
		
		Arguments:
			var {str} -- variable name
		
		Raises:
			UndefinedFrameError -- Attempt to use an undefined frame
			VariableRedefinedError -- Attempt to redefine variable
		"""

		if not self._defined:
			raise UndefinedFrameError()
		if var in self._variables:
			raise VariableRedefinedError(var)

		self._variables[var] = None

	def assign_value(self, var: str, value: tuple):
		"""Assigns value to a given variable
		
		Arguments:
			var {str} -- variable name
			value {tuple} -- value to be assigned
		
		Raises:
			UndefinedFrameError -- Attempt to use an undefined frame
			UndefinedVariableError -- Attempt to assign to an undefined variable
		"""

		if not self._defined:
			raise UndefinedFrameError()
		if var not in self._variables:
			raise UndefinedVariableError(var)

		self._variables[var] = value

	def get_value(self, var: str) -> tuple:
		"""Returns value stored in the given variable
		
		Arguments:
			var {str} -- variable name
		
		Raises:
			UndefinedFrameError -- Attempt to use an undefined frame
			UndefinedVariableError -- Attempt to assign to an undefined variable
		
		Returns:
			tuple -- variable value
		"""

		if not self._defined:
			raise UndefinedFrameError()
		if var not in self._variables:
			raise UndefinedVariableError(var)
		
		value = self._variables[var]

		if not value:
			return (None, None)
		else:
			return value 


	@property
	def defined(self):
		return self._defined

	@defined.setter
	def defined(self, state: bool):
		self._defined = state

	@property
	def variables(self):
		return self._variables
	
	@variables.setter
	def variables(self, value):
		self._variables = value

	def __repr__(self):
		frame_dump = ""
		for key, value in self._variables.items():
			if value == None:
				frame_dump += "{} =".format(key)
			else:
				frame_dump += "{} = <{}> {}\n".format(key, value[0], value[1])

		return frame_dump
