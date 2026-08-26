"""semantic_incomplete.py

Central program in the proof of the semantic First Incompleteness Theorem (general case).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 6.2
"""

import utilities
from is_theorem_G import is_theorem_G  # NOT an oracle
from halting_to_G import halting_to_G  # NOT an oracle


def semantic_incomplete(input_str):
    program = utilities.read('semantic_incomplete.py')
    halts_in_G = halting_to_G(program)
    does_not_halt_in_G = 'NOT (' + halts_in_G + ')'

    if is_theorem_G(does_not_halt_in_G) == 'yes':
        return 'halts'
    utilities.loop_forever()
