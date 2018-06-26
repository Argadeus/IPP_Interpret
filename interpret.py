# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		interpret.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Main executable
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sys import stderr

from src.interpreter import Interpreter
from src.exceptions import InterpreterError
from src.arguments import Arguments
from src.debug import Debug

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
	"""Main function
	
	Returns:
		int -- Program's return code
	"""
	
	try:
		Args = Arguments()	
		Interpreter(Args.get_source_file()).run()
	except InterpreterError as e:
		print("[ ERROR ]", e, file=stderr)
		return e.code
	else:
		return 0


if __name__ == '__main__':
	exit(main())
