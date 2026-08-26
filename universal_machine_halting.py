"""universal_machine_halting.py

Used to prove that **Halting** is undecidable (Proposition 4.6).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.9
"""

import utilities
from universal_machine import universal_machine


def universal_machine_halting(encoded_input):
    program, input_str = utilities.UAM(encoded_input)
    output = universal_machine(program, input_str)

    if output == 'yes':
        return 'yes'
    utilities.loop_forever()
