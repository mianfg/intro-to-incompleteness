"""universal_machine.py

Implements a universal machine in Python: a function that accepts a Python program
and an input, and runs the program on that input.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.2
"""

import utilities


def universal_machine(program, input_str):
    try:
        exec(program)
    except Exception as exc:
        return 'error: ' + str(exc)

    main = utilities.extract_main(program, locals())
    return main(input_str)
