"""godel_peano.py

Central program in the proof of the semantic First Incompleteness Theorem for **Peano**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 6.1
"""

import utilities
from is_theorem_peano import is_theorem_peano  # NOT an oracle
from halting_to_peano import halting_to_peano  # NOT an oracle


def godel_peano(input_str):
    godel_program = utilities.read('godel_peano.py')
    halts_in_peano = halting_to_peano(godel_program)
    does_not_halt_in_peano = 'NOT (' + halts_in_peano + ')'

    if is_theorem_peano(does_not_halt_in_peano) == 'yes':
        return 'halts'
    utilities.loop_forever()
