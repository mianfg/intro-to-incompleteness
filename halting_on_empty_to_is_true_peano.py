"""halting_on_empty_to_is_true_peano.py

Implements the reduction of **HaltingOnEmpty** to **IsTruePeano**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 5.1
"""

from is_true_peano import is_true_peano  # oracle
from halting_to_peano import halting_to_peano  # NOT an oracle


def halting_on_empty_to_is_true_peano(program):
    halts_in_peano = halting_to_peano(program)
    return is_true_peano(halts_in_peano)
