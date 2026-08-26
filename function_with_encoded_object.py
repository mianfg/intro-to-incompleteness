"""function_with_encoded_object.py

Shows that SISO programs impose no restriction on encoded input/output (via `pickle`).

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 3.1
"""

import pickle


def function_with_encoded_object(encoded):
    decoded = pickle.loads(encoded)


adjacencies = {1: 2, 3: 4, 5: 3, 4: 2}
adjacencies_encoded = pickle.dumps(adjacencies)
function_with_encoded_object(adjacencies_encoded)
