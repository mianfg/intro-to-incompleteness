"""simulate_turing_decision.py

Variant of `simulate_turing.py` that always returns `yes` or `no`.

---
Author: Miguel Ángel Fernández Gutiérrez
"""

import utilities
from turing import Turing


def turing_decision(input_str):
    machine_encoding, machine_input = utilities.UAM(input_str)
    turing_machine = Turing(machine_encoding, machine_input)
    turing_machine.run()
    return turing_machine.accepts_or_rejects()
