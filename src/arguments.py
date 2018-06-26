# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		arguments.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 XML representation Interpreter
#
#	@Brief: Command line argument parsing and validation
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sys import argv
from argparse import ArgumentParser

from src.exceptions import InterpreterError, ArgumentsError
from src.debug import Debug

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Arguments:
	"""Argument parser

	This class is used as an argument parser and validator
	"""

	helpMessage = (
		"-----------------------------------------------------------------------------------\n"
		"Usage: interpret.py --file=file\n"
		"-----------------------------------------------------------------------------------\n"
		"Program reads XML representation of a program from a given file and which\n"
		"it then interprets using standard intput and output. Input XML representation\n"
		"is generated may be generated by script 'parse.php' from an IPPcode18 source code.\n"
		"-----------------------------------------------------------------------------------"
	)

	def __init__(self):
		self.__parse()
		self.__handle()

	def __parse(self):
		"""Parse Arguments

		Defines and parses command line arguments
		"""

		parser = ArgumentParser(add_help=False)
		parser.add_argument('-f', '--source', type=str, default="")
		parser.add_argument('-h', '--help', action='store_true')
		parser.add_argument('-d', '--debug', action='store_true', default=False)

		try:
			self.args = vars(parser.parse_args())
		except SystemExit:
			raise ArgumentsError("parsing error")

	def __handle(self):
		"""Handle passed arguments

		Validates arguments and takes corresponding actions
		"""

		if self.args['help']:
			if len(argv) > 2:		
				raise ArgumentsError("invalid combination")		
			print(Arguments.helpMessage)
			exit(0)
		
		if self.args['source'] == "":
			raise ArgumentsError("source file is required")

		if self.args['debug']:
			Debug.active(True)

	def get_source_file(self):
		return self.args['source']