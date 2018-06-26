# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		exceptions.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Custom exceptions covering possible interpreter error states
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExitCode:
	"""Interpreter exit codes

	Exit codes for various possible error states
	"""
	
	INVALID_ARGUMENTS	 = 10
	INPUT_FILE_ERROR	 = 11
	OUTPUT_FILE_ERROR	 = 12

	# Static analysis
	INVALID_XML_FORMAT	 = 31
	PARSER_ERROR		 = 32

	# Static semantic analysis
	SEMANTIC_ERROR		 = 52

	# Runtime semantic analysis
	INVALID_OPERAND		 = 53
	UNDEFINED_VARIABLE	 = 54
	UNDEFINED_FRAME		 = 55
	VALUE_MISSING		 = 56
	DIVISION_ZERO		 = 57
	STRING_OPERATION	 = 58
	INTERNAL_ERROR		 = 99


class InterpreterError(Exception):

	def __init__(self, message = "", code = ExitCode.INTERNAL_ERROR):
		self._message = message
		self._code = code

	def __str__(self):
		return self._message

	@property
	def code(self):
		return self._code


class ArgumentsError(InterpreterError):

	def __init__(self, message = ""):
		super().__init__(message)
		self._code = ExitCode.INVALID_ARGUMENTS

	def __str__(self):
		return "Program arguments - {}".format(self._message)


class InputFileError(InterpreterError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.INPUT_FILE_ERROR

	def __str__(self):
		return "Unable to open input file - {}".format(self._message)


class OutputFileError(InterpreterError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.OUTPUT_FILE_ERROR

	def __str__(self):
		return "Unable to open output file - {}".format(self._message)


class XMLFormatError(InterpreterError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.INVALID_XML_FORMAT

	def __str__(self):
		return "XML format error - {}".format(self._message)


class ParserError(InterpreterError):

	def __init__(self, message = ""):
		super().__init__(message)
		self._code = ExitCode.PARSER_ERROR

	def __str__(self):
		return "Source code error - {}".format(self._message)


class InstructionOrderError(ParserError):

	def __str__(self):
		return "Invalid instruction order - {}".format(self._message)


class SemanticError(InterpreterError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.SEMANTIC_ERROR

	def __str__(self):
		return "Semantic error - {}".format(self._message)


class VariableRedefinedError(SemanticError):

	def __str__(self):
		return "Attempt to redefine variable '{}'".format(self._message)


class UndefinedVariableError(SemanticError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.UNDEFINED_VARIABLE

	def __str__(self):
		return "Attempt to assign to an undefined variable '{}'".format(self._message)


class UndefinedFrameError(SemanticError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.UNDEFINED_FRAME

	def __str__(self):
		return "Attempt to use an undefined frame"

class TypeMismatchError(SemanticError):

	def __str__(self):
		return "Type mismatch has occured - {}".format(self._message)

class ValueMissingError(SemanticError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.VALUE_MISSING

	def __str__(self):
		return "Required value is missing {}".format(self._message)

class InvalidOperandError(SemanticError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.INVALID_OPERAND

	def __str__(self):
		return "Invalid operand - {}".format(self._message)

class DivisionZeroError(SemanticError):

	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.DIVISION_ZERO

	def __str__(self):
		return "Division by zero"

class StringOperationError(SemanticError):
	
	def __init__(self, message=""):
		super().__init__(message)
		self._code = ExitCode.STRING_OPERATION

	def __str__(self):
		return "String operation - {}".format(self._message)
