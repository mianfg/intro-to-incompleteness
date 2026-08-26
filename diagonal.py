"""diagonal.py

If **Universal** were decidable, this program would decide **Diagonal**.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.5
"""

from universal import universal


def diagonal(program):
    return universal(program, program)
