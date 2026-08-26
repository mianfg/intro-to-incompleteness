"""universal.py

Makes **Universal** semi-decidable. Not proved in the thesis; left for experimentation.

---
Author: Miguel Ángel Fernández Gutiérrez
"""

from universal_machine import universal_machine


def universal(program, input_str):
    output = universal_machine(program, input_str)

    if output == 'yes':
        return 'yes'
    return 'no'
