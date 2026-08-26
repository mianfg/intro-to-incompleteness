"""modify_guess_consistent.py

Used to prove the undecidability of **GuessConsistent** (Proposition 4.8).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.13
"""

import utilities
from guess_consistent import guess_consistent  # NOT an oracle
from ignore_input import ignore_input


def modify_guess_consistent(program):
    utilities.write('disk/program.txt', program)
    utilities.write('disk/input.txt', program)
    output = guess_consistent(utilities.read('ignore_input.py'))

    if output == 'yes':
        return 'no'
    if output == 'no':
        return 'yes'
