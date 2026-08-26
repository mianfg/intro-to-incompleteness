"""diagonal_to_universal.py

Implements the reduction of **Diagonal** to **Universal**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.8
"""

from universal import universal  # oracle


def diagonal(program):
    output = universal(program, program)

    if output == 'yes':
        return 'yes'
    return 'no'
