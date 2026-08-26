"""utilities.py

Utility functions used across the other programs in this repository.

---
Author: Miguel Ángel Fernández Gutiérrez
"""

import re
from string import printable
from inspect import signature


class TFGException(Exception):
    pass


def read_file(path):
    with open(path) as f:
        return f.read()


def write_file(path, contents):
    with open(path, 'w') as f:
        f.write(contents)


read = read_file
write = write_file


def MAU(*inputs, SEP='::'):
    return SEP.join(inputs)


def UAM(input_str, SEP='::'):
    return input_str.split(SEP)


def in_alphabet(word, alphabet):
    regex = rf"^({'|'.join(alphabet)})*$"
    return bool(re.search(regex, word))


def extract_main_name(program):
    main_regex = r'^def\s+([a-zA-Z0-9_]*)'
    match = re.search(main_regex, program, re.MULTILINE)

    if match:
        return match.group(1)
    return None


def extract_main(program, local_variables):
    main_name = extract_main_name(program)

    if not main_name:
        return lambda _: 'error: no main function defined'

    if main_name in local_variables:
        main = local_variables[main_name]
        num_parameters = len(signature(main).parameters)
        if num_parameters == 1:
            return main
        return lambda _: f"error: function '{main_name}' is not SISO ({num_parameters} parameters)"
    return lambda _: f"error: function '{main_name}' is not defined locally"


PYTHON_ALPHABET = list(str(printable))


def next_string(string, alphabet=PYTHON_ALPHABET):
    first = alphabet[0]
    last = alphabet[-1]
    if string == '':
        return str(first)
    characters = [c for c in string]
    length = len(characters)

    overflows = True
    i = None
    for i in range(length - 1, -1, -1):
        current_char = characters[i]
        if current_char != last:
            overflows = False
            break

    increment_i = i
    alphabet_i = alphabet.index(current_char)

    if overflows:
        return first * (length + 1)

    characters[increment_i] = alphabet[alphabet_i + 1]
    for j in range(increment_i + 1, length):
        characters[j] = first
    return ''.join(characters)


def loop_forever():
    while True:
        pass
