# MoreAsThanBs
# ---
# Esta máquina de Turing resuelve el problema MásAQueB, que
# dada una palabra del alfabeto {'a', 'b'} acepta si tiene
# más 'a' que 'b'


q_0 q_a q_b q_R q_F     # estados
a b                     # alfabeto de entrada
a b X _                 # alfabeto de trabajo
_                       # símbolo blanco
q_0                     # estado inicial
q_F                     # estados finales

# transiciones
q_0, a : q_a, X, D
q_0, b : q_b, X, D
q_0, X : q_0, X, D
q_a, a : q_a, a, D
q_a, b : q_R, X, I
q_a, X : q_a, X, D
q_a, _ : q_F, _, S
q_b, a : q_R, X, I
q_b, b : q_b, b, D
q_b, X : q_b, X, D
q_R, a : q_R, a, I
q_R, b : q_R, b, I
q_R, X : q_R, X, I
q_R, _ : q_0, _, D