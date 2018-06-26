# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		interpret.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Interpreter execution core, defining internal behaviour and
#		   generates corresponding output	
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
import re

from src.parser import Parser
from src.frame import Frame
from src.constants import Constant
from src.exceptions import *
from src.debug import Debug

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Interpreter:

	def __init__(self, source_file):		
		self._source_file = source_file
		
		self._instr_list = dict()
		self._instr_order_list = list()
		self._jump_label_list = dict()	
		
		self._instr_index = 0
		self._instr_args = list()

		self._tmp_frame = Frame(False)
		self._global_frame = Frame(True)
		self._local_frame = Frame(False)

		self._call_stack = list()
		self._data_stack = list()
		self._local_frame_stack = list()

	def run(self):
		"""Runs the interpreter
		"""

		Debug.printd("Interpreter -> START")
		
		try:
			self.__parse()
			self.__process()
		except InterpreterError:
			raise

	def __parse(self):
		"""Parses and sets up interpreter variables
		"""

		Debug.printd("Interpreter -> PARSING..")
		parser = Parser(self._source_file)
		
		try:
			parser.run()
		except InterpreterError:
			raise

		self._instr_list = parser.instruction_list
		self._jump_label_list = parser.jump_label_list
		self._instr_order_list = list(self._instr_list.keys())
		self._instr_order_list.sort()

	def __process(self):
		"""Interpreter loop executes parsed instructions
		"""

		Debug.printd("Interpreter -> PROCESSING..")
		instr_count = len(self._instr_order_list)

		while self._instr_index < instr_count:
			try:
				self.__execute_instr()
			except InterpreterError:
				raise

			self._instr_index += 1

	def __execute_instr(self):
		"""Executes instruction based on its opcode
		
		Raises:
			InterpreterError -- Raised exception with added order of an instruction
								on which an error has occured
		"""

		instr_order = self._instr_order_list[self._instr_index]	
		instr = self._instr_list[instr_order]
		instr_opcode = instr[0]
	
		self._instr_args = instr[1]

		try:
			# Execute method based on instruction's opcode
			getattr(self, instr_opcode)()
		except InterpreterError as e:
			raise InterpreterError(str(e) + " on instruction {}".format(instr_order), e.code)
	

	def MOVE(self):
		value = self.__get_arg_value(self._instr_args[1])
	
		try:
			self.__write_var(self._instr_args[0], value)
		except InterpreterError:
			raise

	def CREATEFRAME(self):
		self._tmp_frame.defined = True
		self._tmp_frame.variables = {}

	def PUSHFRAME(self):
		if not self._tmp_frame.defined:
			raise UndefinedFrameError()

		self._local_frame = self._tmp_frame
		self._local_frame_stack.append(self._local_frame)
		self._tmp_frame = Frame()

	def POPFRAME(self):
		if not self._local_frame_stack:
			raise UndefinedFrameError()
		self._local_frame_stack.pop(-1)

	def DEFVAR(self):
		frame, var_name = self.__resolve_var(self._instr_args[0])
		try:
			frame.define_variable(var_name)
		except InterpreterError:
			raise
		
	def CALL(self):
		# Save the current instruction index
		self._call_stack.append(self._instr_index)

		try:
			self.__label_jump()
		except InterpreterError:
			raise

	def RETURN(self):
		if not self._call_stack:
			raise ValueMissingError("call stack position")

		self._instr_index = self._call_stack.pop(-1) 

	def PUSHS(self):
		try:
			value = self.__get_arg_value(self._instr_args[0])
		except InterpreterError:
			raise

		self._data_stack.append(value) 

	def POPS(self):
		try:
			value = self._data_stack.pop(-1)
			self.__write_var(self._instr_args[0], value)
		except InterpreterError:
			raise
		except Exception:
			raise ValueMissingError("data stack value")

	def ADD(self):
		try:
			new_value = self.__arithmetic_calc("+")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def SUB(self):
		try:
			new_value = self.__arithmetic_calc("-")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def MUL(self):
		try:
			new_value = self.__arithmetic_calc("*")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def IDIV(self):
		try:
			new_value = self.__arithmetic_calc("//")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def LT(self):
		try:
			new_value = self.__comparation_calc("<")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def GT(self):
		try:
			new_value = self.__comparation_calc(">")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def EQ(self):
		try:
			new_value = self.__comparation_calc("=")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def AND(self):
		try:
			new_value = self.__logic_calc("&")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def OR(self):
		try:
			new_value = self.__logic_calc("|")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def NOT(self):
		try:
			new_value = self.__logic_calc("^")
			self.__write_var(self._instr_args[0], new_value)
		except InterpreterError:
			raise

	def INT2CHAR(self):
		int_arg = self.__get_arg_value(self._instr_args[1])
		
		if int_arg[0] != "int":
			raise InvalidOperandError("has to be a type of integer")
		
		try:
			char = chr(int_arg[1])
			self.__write_var(self._instr_args[0], ("string", char))
		except InterpreterError:
			raise
		except Exception:
			raise StringOperationError("value can not be converted into a character")

	def STRI2INT(self):
		string_arg = self.__get_arg_value(self._instr_args[1])
		position_arg = self.__get_arg_value(self._instr_args[2])

		if string_arg[0] != "string":
			raise InvalidOperandError("has to be a type of string")
		if position_arg[0] != "int":
			raise InvalidOperandError("has to be a type of integer")

		index = position_arg[1]
		string_list = list(string_arg[1]) 

		try:
			value = ord(string_list[index])
			self.__write_var(self._instr_args[0], ("int", value))
		except InterpreterError:
			raise
		except Exception:
			raise StringOperationError("index '{}' out of range".format(position_arg))

	def READ(self):
		input_type = self.__get_arg_value(self._instr_args[1])[1]
		pattern = Constant.TYPE_VALUE_REGEX[input_type]
		
		value = input()

		if input_type == "int":
			try:
				value = int(value)
			except Exception:
				value = 0	
		elif input_type == "string":
			if not re.match(pattern, value):
				value = ""				
		elif input_type == "bool":
			value = value.lower()
			if not re.match(pattern, value):
				value = "false"

		try:
			self.__write_var(self._instr_args[0], (input_type, value))
		except InterpreterError:
			raise		 

	def WRITE(self):
		arg_val = self.__get_arg_value(self._instr_args[0])
		print(arg_val[1], end='')
		
	def CONCAT(self):
		string1 = self.__get_arg_value(self._instr_args[1])
		string2 = self.__get_arg_value(self._instr_args[2])

		if string1[0] != "string":
			raise InvalidOperandError("types have to be strings")
		if string1[0] != string2[0]:
			raise InvalidOperandError("types have to match")

		new_string = string1[1] + string2[1]

		try:
			self.__write_var(self._instr_args[0], ("string", new_string))
		except InterpreterError:
			raise

	def STRLEN(self):
		string = self.__get_arg_value(self._instr_args[1])

		if string[0] != "string":
			raise InvalidOperandError("type has to be string")

		string_len = len(string[1])

		try:
			self.__write_var(self._instr_args[0], ("int", string_len))
		except InterpreterError:
			raise

	def GETCHAR(self):
		string_arg = self.__get_arg_value(self._instr_args[1])
		position_arg = self.__get_arg_value(self._instr_args[2])

		if string_arg[0] != "string":
			raise InvalidOperandError("has to be a type of string")
		if position_arg[0] != "int":
			raise InvalidOperandError("has to be a type of integer")

		index = position_arg[1]
		string_list = list(string_arg[1])

		try:
			value = string_list[index] 
			self.__write_var(self._instr_args[0], ("string", value))
		except InterpreterError:
			raise
		except Exception:
			raise StringOperationError("index '{}' out of range".format(position_arg))

	def SETCHAR(self):
		old_string_arg = self.__get_arg_value(self._instr_args[0])
		index_arg = self.__get_arg_value(self._instr_args[1])
		char_arg = self.__get_arg_value(self._instr_args[2])

		if old_string_arg[0] != "string":
			raise InvalidOperandError("has to be a type of string")
		if index_arg[0] != "int":
			raise InvalidOperandError("has to be a type of integer")
		if char_arg[0] != "string":
			raise InvalidOperandError("has to be a type of string")

		try:
			old_string_list = list(old_string_arg[1])
			replace_char = list(char_arg[1])[0]
			index = index_arg[1]

			old_string_list[index] = replace_char
			new_string = "".join(old_string_list)

			self.__write_var(self._instr_args[0], ("string", new_string))

		except InterpreterError:
			raise
		except Exception:
			raise StringOperationError("index out of range")

	def TYPE(self):
		symb_arg = self.__get_arg_value(self._instr_args[1])

		try:
			self.__write_var(self._instr_args[0], ("string", symb_arg[0]))
		except InterpreterError:
			raise
		
	def LABEL(self):
		pass

	def JUMP(self):
		try:
			self.__label_jump()
		except InterpreterError:
			raise

	def JUMPIFEQ(self):
		value1 = self.__get_arg_value(self._instr_args[1])
		value2 = self.__get_arg_value(self._instr_args[2])

		if value1[0] != value2[0]:
			raise InvalidOperandError("types have to match")

		if value1[1] == value2[1]:
			try:
				self.__label_jump()
			except InterpreterError:
				raise

	def JUMPIFNEQ(self):
		value1 = self.__get_arg_value(self._instr_args[1])
		value2 = self.__get_arg_value(self._instr_args[2])

		if value1[0] != value2[0]:
			raise InvalidOperandError("types have to match")

		if value1[1] != value2[1]:
			try:
				self.__label_jump()
			except InterpreterError:
				raise

	def DPRINT(self):
		pass

	def BREAK(self):
		pass


	def __get_arg_value(self, arg: tuple) -> tuple:
		"""Extracts and returns value of an argument
		
		Arguments:
			arg {tuple} -- argument
		
		Returns:
			tuple -- argument's value
		"""

		if arg[0] == "var":
			return self.__read_var(arg)
		else:
			return arg

	def __write_var(self, var_arg: tuple, value: tuple):
		"""Writes value to a given variable
		
		Arguments:
			var_arg {tuple} -- variable argument
			value {tuple} -- value to be stored
		"""

		frame, var_name = self.__resolve_var(var_arg)
		try:
			frame.assign_value(var_name, value)
		except InterpreterError:
			raise

	def __read_var(self, var_arg: tuple) -> tuple:
		"""Reads value from a variable
		
		Arguments:
			var_arg {tuple} -- variable argument
		
		Returns:
			tuple -- variable's value
		"""

		frame, var_name = self.__resolve_var(var_arg)
		try:
			return frame.get_value(var_name)
		except InterpreterError:
			raise

	def __resolve_var(self, var_arg: tuple) -> tuple:
		"""Resolves variable's frame and name
		
		Arguments:
			var_arg {tuple} -- variable argument
		
		Returns:
			tuple -- frame object and variable name
		"""

		var = var_arg[1]
		frame_type, var_name = var.split('@')
		frame = self.__select_frame(frame_type)
		
		return (frame, var_name)

	def __select_frame(self, frame_type: str) -> object:
		"""Selects frame based on a given frame type string
		
		Arguments:
			frame_type {str} -- type of frame as a string
		
		Raises:
			ValueError -- invalid frame type
		
		Returns:
			object -- frame
		"""

		if frame_type == "GF":
			return self._global_frame
		elif frame_type == "LF":
			return self._local_frame
		elif frame_type == "TF":
			return self._tmp_frame
		else:
			raise ValueError("Unknown frame '{}'".format(frame_type))

	def __arithmetic_calc(self, operator: str) -> tuple:
		"""Performs an arithmetical operation and returns result
		
		Arguments:
			operator {str} -- operator sign
		
		Raises:
			InvalidOperandError -- Invalid operand type(s)
			DivisionZeroError -- An attempt to division by zero
			ValueError -- Invalid operator
		
		Returns:
			tuple -- result (type, value)
		"""

		value1 = self.__get_arg_value(self._instr_args[1])
		value2 = self.__get_arg_value(self._instr_args[2])

		if value1[0] != "int":
			raise InvalidOperandError("types have to be integers")
		if value1[0] != value2[0]:
			raise InvalidOperandError("types have to match")

		if operator == "+":
			result = value1[1] + value2[1]
		elif operator == "-":
			result = value1[1] - value2[1]
		elif operator == "*":
			result = value1[1] * value2[1]
		elif operator == "//":
			try:			
				result = value1[1] // value2[1]
			except ZeroDivisionError:
				raise DivisionZeroError()
		else:
			raise ValueError("invalid arithmetic operation")

		return (value1[0], result)
	
	def __comparation_calc(self, operator: str) -> tuple:
		"""Performs and comparative operation and returns result
		
		Arguments:
			operator {str} -- operator sign 
		
		Raises:
			InvalidOperandError -- operand types have to match
			ValueError -- invalid operations
		
		Returns:
			tuple -- result (type, value)
		"""

		value1 = self.__get_arg_value(self._instr_args[1])
		value2 = self.__get_arg_value(self._instr_args[2])

		if value1[0] != value2[0]:
			raise InvalidOperandError("types have to match")

		if operator == "<":
			result = value1[1] < value2[1]
		elif operator == ">":	
			result = value1[1] > value2[1]
		elif operator == "=":	
			result = value1[1] == value2[1]
		else:
			raise ValueError("invalid comparation operation")

		result_value = "true" if result else "false"

		return ("bool", result_value)

	def __logic_calc(self, operator: str) -> tuple:
		"""Performs logical operation and returns result
		
		Arguments:
			operator {str} -- operator sign
		
		Raises:
			InvalidOperandError -- Invalid operand type(s)
			ValueError -- invalid operator
		
		Returns:
			tuple -- value (type, value)
		"""

		value1 = self.__get_arg_value(self._instr_args[1])
		tmp_value1 = True if value1[1] == "true" else False
		
		value2 = None
		tmp_value2 = None
		
		if len(self._instr_args) == 3:
			value2 = self.__get_arg_value(self._instr_args[2])
			tmp_value2 = True if value1[1] == "true" else False
			
			if value1[0] != value2[0]:
				raise InvalidOperandError("types have to match")

		if value1[0] != "bool":
			raise InvalidOperandError("types have to be booleans")

		if operator == "&":
			result = tmp_value1 & tmp_value2
		elif operator == "|":
			result = tmp_value1 | tmp_value2
		elif operator == "^":
			result = not tmp_value1
		else:
			raise ValueError("invalid logic operation")

		result_value = "true" if result else "false"

		return ("bool", result_value)

	def __label_jump(self):
		"""Sets the instruction head to the index of label given by an instruction
		   argument 
		
		Raises:
			SemanticError -- label doesn't exist
		"""

		label = self._instr_args[0][1]
		
		try:
			jump_order = self._jump_label_list[label]
		except Exception:
			raise SemanticError("undefined label '{}'".format(label))

		self._instr_index = self._instr_order_list.index(jump_order)
