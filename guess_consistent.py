"""guess_consistent.py

Used in the proof of Theorem 6.3: if the logical system were complete, this program
would decide **GuessConsistent**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 6.4
"""

import utilities
from halting_to_S import halting_to_S  # NOT an oracle
from is_theorem_s import is_theorem_S  # NOT an oracle
from universal_machine import universal_machine  # NOT an oracle


def guess_consistent(program):
    program_formula = halting_to_S(program)
    is_theorem = is_theorem_S(program_formula)

    if is_theorem == 'yes':
        output = universal_machine(program, '')
        if output == 'yes':
            return 'yes'
        return 'no'
    return 'no'
