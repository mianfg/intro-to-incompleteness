"""ignore_input.py

Ignores the input and runs a program and input stored on disk.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.11
"""

import utilities
from universal_machine import universal_machine


def ignore_input(ignored_input):
    program = utilities.read('disk/program.txt')
    input_str = utilities.read('disk/input.txt')
    return universal_machine(program, input_str)
