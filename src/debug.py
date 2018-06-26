# ======================================================================
#	@Author: 	Ivan Hazucha
#	@File: 		debug.py
#	@Date: 		10/04/2018
#
#	@Assignment: IPPcode18 3-address code XML representation interpreter
#
#	@brief Debug log messages
#
#	TODO: __blank__
#
# ======================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pprint import pprint
from sys import stderr

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Debug:
	"""Debug log with colored tags (for Linux - Bash)

	This class defines debug operations (if active)
	"""
	_active = False

	DEBUG_TAG = "\033[38;5;202m" + "[ DEBUG ] " + "\033[0m"

	@staticmethod
	def printd(text="", *args):
		"""Debug print

		Method prints debug message
		"""
		if Debug._active:
			print(Debug.DEBUG_TAG + text, file=stderr, end=" " if args else "")
			for arg in args:
				print(arg, end=" ", file=stderr)
			print("\n", end="", file=stderr)

	@staticmethod
	def pprintd(obj):
		"""Pretty debug print

		Method prints out an object
		"""
		hr = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

		if Debug._active:
			print(Debug.DEBUG_TAG + hr, file=stderr)
			pprint(obj, depth=10, stream=stderr)
			print(Debug.DEBUG_TAG + hr, file=stderr)

	@staticmethod
	def active(flag):
		Debug._active = flag
