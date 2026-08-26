"""c_d.py

Used to prove that if a problem is decidable, its complement is too (Proposition 4.4).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.7
"""

from d import d


def c_d(input_str):
    output = d(input_str)

    if output == 'yes':
        return 'no'
    return 'yes'
