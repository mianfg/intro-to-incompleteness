"""more_as_than_b_v2.py

Decides **MoreAsThanBs**, accepting any word as input.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 4.3
"""


def more_as_than_b_v2(word):
    if word.count('a') > word.count('b'):
        return 'yes'

    return 'no'
