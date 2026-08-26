"""is_theorem_s.py

Proves that **IsTheorem** is decidable for syntactically consistent logical systems.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 6.3
"""

import utilities
from is_proof_S import is_proof_S  # NOT an oracle


def is_theorem_S(formula):
    negated_formula = 'NOT (' + formula + ')'
    proof = ''

    while True:
        if is_proof_S(proof, formula) == 'yes':
            return 'yes'
        if is_proof_S(proof, negated_formula) == 'yes':
            return 'no'
        proof = utilities.next_string(proof)
