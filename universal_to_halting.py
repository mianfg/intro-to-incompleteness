"""universal_to_halting.py

Implements the reduction of **Universal** to **Halting**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.10
"""

import utilities
from halts import halts  # oracle


def universal_to_halting(program, input_str):
    encoded_input = utilities.MAU(program, input_str)
    halting_program = utilities.read('universal_machine_halting.py')
    return halts(halting_program, encoded_input)
