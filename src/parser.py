# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		parser.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Parser module used to load, validate and process source code file
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import xml.etree.ElementTree as ET
import re

from src.exceptions import *
from src.debug import Debug
from src.constants import Constant

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Parser():
	def __init__(self, source_file: str):
		self._source_file = source_file
		self._program_root = None
		self._instruction_list = dict()
		self._jump_label_list = dict()

	def run(self):
		"""Executes parsing process
		"""

		Debug.printd("Parser -> START")
		try:
			self.__load_source()
			self.__parse_source()
			Debug.pprintd(self._instruction_list)
		except InterpreterError:
			raise
	
	def __load_source(self):
		"""Loads source XML file
		
		Raises:
			InputFileError -- File not found
			XMLFormatError -- Unable to parse
		"""

		try:
			element_tree = ET.parse(self._source_file)
			self._program_root = element_tree.getroot()
		except FileNotFoundError:
			raise InputFileError("not found")
		except ET.ParseError:
			raise XMLFormatError("unable to parse")

	def __parse_source(self):
		"""Parses source file

		Performs static lexical, syntactic and semantic
		checks along with instruction list construction
		and list of labels
		"""

		try:
			self.__check_source_root()
			self.__add_instructions()
		except InterpreterError:
			raise

	def __check_source_root(self):
		"""Checks XML root tag (program)
		
		Raises:
			XMLFormatError -- invalid root tag
			XMLFormatError -- language attribute missing
			ParserError -- unknown language
		"""

		root_tag = self._program_root.tag
		source_language = self._program_root.get("language")

		if root_tag != "program":
			raise XMLFormatError("invalid root tag '{}'".format(root_tag))
		if source_language == None:
			raise XMLFormatError("language attribute missing")	
		if source_language != "IPPcode18":
			raise ParserError("unknown language '{}'".format(source_language))

	def __add_instructions(self):
		"""Loops through instructions in file
		"""

		for instr in self._program_root:
			Debug.printd("Processing instruction '{}'".format(instr.get("opcode")))
			try:
				self.__add_instruction(instr)
			except InterpreterError:
				raise

	def __add_instruction(self, instr: object):
		"""Checks individual instructions
		
		Arguments:
			instr XMLobject -- XML structure of an instruction
		"""

		if instr.tag != "instruction":
			raise XMLFormatError("unknown tag '{}'".format(instr.tag))

		if len(instr.items()) != 2:
			raise XMLFormatError("wrong number of attributes, expected 'order' and 'opcode'")

		try:
			order = self.__extract_instr_order(instr)
			opcode = self.__extract_instr_opcode(instr)
			arguments = self.__extract_instr_arguments(instr)
		except InterpreterError:
			raise

		self._instruction_list[order] = (opcode, arguments)	

	def __extract_instr_order(self, instr: object) -> int:
		"""Checks and returns valid instruction order value
		
		Arguments:
			instr {XMLobject} -- instruction element
		
		Raises:
			XMLFormatError -- order attribute missing
			ParserError -- invalid order value
			ParserError -- order value already exists
		
		Returns:
			str -- instruction order value
		"""

		order = instr.get('order')

		if order == None:
			raise XMLFormatError("required instruction argument 'order' is missing")
		try:
			order = int(order)
		except Exception:
			raise ParserError("invalid instruction order value '{}'".format(order))
		if order in self._instruction_list:
			raise ParserError("instruction with order value '{}' already exists".format(
				order
			))

		return order

	def __extract_instr_opcode(self, instr: object) -> str:
		"""Checks and returns valid opcode value
		
		Arguments:
			instr {XMLobject} -- instruction element
		
		Raises:
			XMLFormatError -- opcode attribute missing
			ParserError -- invalid opcode
		
		Returns:
			str -- instruction opcode
		"""

		opcode = instr.get('opcode')

		if opcode == None:
			raise XMLFormatError("required argument 'opcode' is missing")
		if opcode not in Constant.INSTR_LIST:
			raise ParserError("invalid opcode '{}' on instruction {}".format(
				opcode, instr.get('order')
			))

		return opcode

	def __extract_instr_arguments(self, instr: object) -> list:
		"""Extracts and checks instruction arguments
		
		Arguments:
			instr {object} -- instruction xml object
		
		Raises:
			ParserError -- Invalid number of arguments
		
		Returns:
			list -- A list of instruction arguments
		"""

		opcode = instr.get('opcode')
		ref_opcode_args = Constant.INSTR_LIST[opcode]
		arguments = list()

		instr_arg_count = len(list(instr))
		ref_arg_count = len(ref_opcode_args)

		if instr_arg_count != ref_arg_count:
			raise ParserError("invalid number of arguments for instruction {}".format(
				instr.get("order")
			))

		for i in range(instr_arg_count):
			operand_type = ref_opcode_args[i]
			try:
				arg = self.__find_instr_arg(instr, str(i + 1))
				arg_type = self.__extract_arg_type(instr, arg, operand_type)
				arg_text = self.__extract_arg_value(instr, arg, arg_type)
			except InterpreterError:
				raise

			arguments.append((arg_type, arg_text))
		
		# If instruction is LABEL, add record to the list of jump labels
		if opcode == "LABEL":
			if arg_text in self._jump_label_list:
				raise SemanticError("redefinition of label '{}' on instruction {}".format(
					arg_text, instr.get("order")
				))
			self._jump_label_list[arg_text] = int(instr.get("order"))

		return arguments

	def __find_instr_arg(self, instr: object, index: str) -> object:
		"""Finds and returns a specific instruction argument
		
		Arguments:
			instr {object} -- instruction xml object
			index {str} -- argument index <1|2|3>
		
		Raises:
			ParserError -- Argument not found
			ParserError -- Invalid number of arguments
		
		Returns:
			object -- argument xml object
		"""

		arg = instr.find("arg" + index)
		
		if arg == None:
			raise ParserError("argument 'arg{}' not found on instruction {}".format(
				index, instr.get("order")
			))
		if len(arg.items()) != 1:
			raise ParserError("invalid number of attributes for instruction {}".format(
				instr.get("order")
			))

		return arg

	def __extract_arg_type(self, instr: object, arg: object, operand_type: int) -> str:
		"""Extracts and checks instruction's argument type
		
		Arguments:
			instr {object} -- instruction xml object
			arg {object} -- argument xml object
			operand_type {int} -- type of operand
		
		Raises:
			ParserError -- The 'type' attribute is missing
			ParserError -- Invalid type value for a given opcode
		
		Returns:
			str -- argument type
		"""

		# Value of the 'type' attribute of an argument
		ref_valid_types = Constant.ALLOWED_SYMBOLS[operand_type]
		arg_type = arg.get("type")

		if arg_type == None:
			raise ParserError("argument attribute 'type' missing on instruction {}".format(
				instr.get("order")
			))
		if arg_type not in ref_valid_types:
			raise ParserError(
				"argument's type value '{}' is incompatible with opcode '{}' on instruction {}"
				.format(arg_type, instr.get("opcode"), instr.get("order"))
			)

		return arg_type

	def __extract_arg_value(self, instr: object, arg: object, arg_type: str) -> str:
		"""Extracts and checks instruction's argument value
		
		Arguments:
			instr {object} -- instruction xml object
			arg {object} -- argument xml object
			arg_type {str} -- type of an argument
		
		Raises:
			ParserError -- Invalid argument's content
		
		Returns:
			str -- argument value
		"""

		arg_value_regex = Constant.TYPE_VALUE_REGEX[arg_type]
		arg_value = arg.text if arg.text != None else ""

		if not re.match(arg_value_regex, arg_value):
			raise ParserError(
				"content of an argument does not match its type '{}' on instruction {}".format(
					arg_type, instr.get("order"))
			)
		
		if arg_type == "int":
			return int(arg_value)
		elif arg_type == "string":
			return self.__replace_escapes(arg_value)
		else:
			return arg_value

	def __replace_escapes(self, string: str) -> str:
		"""Substitutes all escape sequences within a string for corresponding characters
		
		Arguments:
			string {str} -- Input string with escape sequences
		
		Returns:
			str -- String with replaced escape sequences
		"""

		pattern = re.compile(r"\\\d{3}")
		matches = pattern.findall(string)
		for match in matches:
			replacement = chr(int(match[2:]))
			string = pattern.sub(replacement, string)

		return string

	@property
	def instruction_list(self):
		return self._instruction_list

	@property
	def jump_label_list(self):
		return self._jump_label_list
