"""c_diagonal.py

If **Diagonal** were decidable, this program would decide **C-Diagonal**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.6
"""

from diagonal import diagonal


def c_diagonal(program):
    output = diagonal(program)

    if output == 'yes':
        return 'no'
    return 'yes'
