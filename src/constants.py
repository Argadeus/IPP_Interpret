# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		constants.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 XML representation Interpreter
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


class Constant:

	VAR = 1
	SYMB = 2
	LABEL = 3

	INT = 10
	BOOL = 11
	STRING = 12
	TYPE = 13

	INSTR_LIST = {
		
		# Frame, function call instructions
		'MOVE': (VAR, SYMB),
		'CREATEFRAME': (),
		'PUSHFRAME': (),
		'POPFRAME': (),
		'DEFVAR': (VAR,),
		'CALL': (LABEL,),
		'RETURN': (),

		# Data stack instructions
		'PUSHS': (SYMB,),
		'POPS': (VAR,),

		# Arithmetical, relation, bool and conversion instrictions
		'ADD': (VAR, INT, INT),
		'SUB': (VAR, INT, INT),
		'MUL': (VAR, INT, INT),
		'IDIV': (VAR, INT, INT),

		'LT': (VAR, SYMB, SYMB),
		'GT': (VAR, SYMB, SYMB),
		'EQ': (VAR, SYMB, SYMB),

		'AND': (VAR, BOOL, BOOL),
		'OR': (VAR, BOOL, BOOL),
		'NOT': (VAR, BOOL),

		'INT2CHAR': (VAR, INT),
		'STRI2INT': (VAR, STRING, INT),

		# I/O instructions
		'READ': (VAR, TYPE),
		'WRITE': (SYMB,),

		# String instructions
		'CONCAT': (VAR, STRING, STRING),
		'STRLEN': (VAR, STRING),
		'GETCHAR': (VAR, STRING, INT),
		'SETCHAR': (VAR, INT, STRING),

		# Type instructions
		'TYPE': (VAR, SYMB),

		# Flow control instructions
		'LABEL': (LABEL,),
		'JUMP': (LABEL,),
		'JUMPIFEQ': (LABEL, SYMB, SYMB),
		'JUMPIFNEQ': (LABEL, SYMB, SYMB),

		# Debug instruction
		'DPRINT': (SYMB,),
		'BREAK': ()
	}

	ALLOWED_SYMBOLS = {
		VAR: ('var',),
		SYMB: ('var', 'int', 'bool', 'string'),
		LABEL: ('label',),
		INT: ('var', 'int'),
		BOOL: ('var', 'bool'),
		STRING: ('var', 'string'),
		TYPE: ('type'),
	}

	TYPE_VALUE_REGEX = {
		'var': r"^(GF|LF|TF)@[_\-\$&%\*\w][_\-\$&%\*\w0-9]*$",
		'label': r"^[_\-\$&%\*\w][_\-\$&%\*\w0-9]*$",
		'int': r"^[-+]?\d+$",
		'string': r"^(?!.*\\[^\d])(?!\\[\d]{1}[^\d])(?!\\[\d]{2}[^\d])(?:\w|[ -~]|\d)*(?<!(\\\d{0}))(?<!(\\\d{1}))(?<!(\\\d{2}))(?<!(\\))(?<!\s)$",
		'bool': r"^(true|false)$",
		'type': r"^(int|string|bool)$",
	}
	
