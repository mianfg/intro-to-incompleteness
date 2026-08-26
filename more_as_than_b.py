"""more_as_than_b.py

Decides the **MoreAsThanBs** problem (Proposition 4.1).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.1
"""

import utilities


def more_as_than_b(word):
    if not utilities.in_alphabet(word, {'a', 'b'}):
        return 'no'

    if word.count('a') > word.count('b'):
        return 'yes'

    return 'no'
