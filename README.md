# IPPcode18 Language Interpreter

Implemented in Python v3.6.5

## Language structure

Input language of the interpreter is a XML representation of assembly like code called IPPcode18 created at VUT Faculty of Information Technology for learning purposes.

This instruction based code with primary focus on its XML representation has a following structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode18">
  <instruction order="1" opcode="DEFVAR">
    <arg1 type="var">GF@counter</arg1>
  </instruction>
</program>
```

**Program** root element with attribute *language* set to **IPPcode18** contains **instruction** child elements with attributes
**order** (since XML parsers do not guarantee to keep the file order) and **opcode** which is name of an instruction.
Instruction element further contains **arg** elements *(arg1, arg2 and arg3 depending on instruction)* which are of a specific **type** and contain value allowed for the specific type in a form of element's text.

## Interpreting

First, the input XML file is parsed and data stored in a form of internal structure along with a list of specific instructions called **LABEL** which is then used as a reference jump table for the interpreter to know where to continue after execution of a jump instruction.

Then, the internal interpreter representation is executed in a proper order using implemented methods of which names correspond with the names of instructions, manipulating the internal memory model and performing actions.

## Usage

Main executable file is **interpret.py**

**Parameters**:

--source=\<file\> - Input file name

--help - Prints out help message
