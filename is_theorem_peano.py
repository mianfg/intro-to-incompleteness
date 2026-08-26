"""is_theorem_peano.py

Makes **IsTheoremPeano** semi-decidable (Proposition 5.8).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 5.2
"""

import utilities
from is_proof_peano import is_proof_peano  # NOT an oracle


def is_theorem_peano(formula):
    proof = ''

    while True:
        if is_proof_peano(proof, formula) == 'yes':
            return 'yes'
        proof = utilities.next_string(proof)
