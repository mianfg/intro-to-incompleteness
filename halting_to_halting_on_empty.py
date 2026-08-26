"""halting_to_halting_on_empty.py

Implements the reduction of **Halting** to **HaltingOnEmpty**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.12
"""

import utilities
from halting_on_empty import halting_on_empty  # oracle


def halting_to_halting_on_empty(program, input_str):
    utilities.write('disk/program.txt', program)
    utilities.write('disk/input.txt', input_str)
    return halting_on_empty(utilities.read('ignore_input.py'))
