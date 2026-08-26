"""simulate_turing.py

Simulates a Turing machine. Use with any machine in the `turing_machines` folder.

---
Author: Miguel Ángel Fernández Gutiérrez
In the thesis: Program 3.2
"""

import utilities
from turing import Turing


def simulate_turing(input_str):
    machine_encoding, machine_input = utilities.UAM(input_str)
    turing_machine = Turing(machine_encoding, machine_input)
    turing_machine.run()
    return str(turing_machine)


def simulate_turing_mult(encoding, input_str):
    return simulate_turing(utilities.MAU(encoding, input_str))
