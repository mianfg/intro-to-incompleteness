"""binary_addition.py

Este programa decide los problemas _EsTeorema_ y _EsVerdadero_ para todos los
sistemas lógicos derivados del sistema formal ***SumaBinaria*** (incluyendo la
decidibilidad del problema _EsTeorema_ de este sistema formal)

---
Autor: Miguel Ángel Fernández Gutiérrez
"""

import utilities
import re

axioma = '1=1'

regex_numero_binario = re.compile(r'[01]+')
regex_suma_numero_binario = re.compile(r'^[01]+(\+[01]+)*$')
regex_formula_bien_formada = re.compile(r'^[01]+(\+[01]+)*=[01]+(\+[01]+)*$')
regex_R2 = re.compile(r'([=+]|^)([01]+)(?=\+\2([=+]|$))')
regex_R3 = re.compile(r'([=+]|^)1\+([01]+)0([=+]|$)')

def _bien_formada(formula):
    if regex_formula_bien_formada.match(formula):
        return True
    else:
        return False

def R1(formula):
    consecuencias = set()
    # si la fórmula no está bien formada, no puede haber consecuencias
    if not _bien_formada(formula):
        return consecuencias
    
    (left_side, right_side) = formula.split('=')
    nueva_formula = f'1+{left_side}=1+{right_side}'
    consecuencias.add(nueva_formula)

    return consecuencias

def R2(formula):
    consecuencias = set()
    # si la fórmula no está bien formada, no puede haber consecuencias
    if not _bien_formada(formula):
        return consecuencias

    # con finditer comprobamos todas las posibles coincidencias (matches)
    for match in regex_R2.finditer(formula):
        # N está en el grupo 2 del match
        N = match.group(2)

        # N ha de ser un número binario
        assert regex_numero_binario.match(N)

        # tomamos las posiciones de inicio y final de N (el segundo grupo del match)
        N_start = match.start(2)
        N_end = match.end(2)

        # longitud de N
        N_len = N_end - N_start

        # el nuevo N será N0
        N_new = f'{N}0'

        # N+N es el string siendo reemplazado, luego su longitud es 2*N_len+1
        replace_len = 2 * N_len + 1
        
        # creamos la nueva fórmula
        nueva_formula = formula[:N_start] + N_new + formula[N_start+replace_len:]
        
        # añadimos la fórmula al conjunto de posibles consecuencias
        consecuencias.add(nueva_formula)
    
    return consecuencias

def R3(formula):
    consecuencias = set()
    # si la fórmula no está bien formada, no puede haber consecuencias
    if not _bien_formada(formula):
        return consecuencias

    # con finditer comprobamos todas las posibles coincidencias (matches)
    for match in regex_R3.finditer(formula):
        # N está en el grupo 2 del match
        N = match.group(2)

        # N ha de ser un número binario
        assert regex_numero_binario.match(N)

        # tomamos las posiciones de inicio y final de N (el segundo grupo del match)
        N_start = match.start(2)
        N_end = match.end(2)

        # longitud de N
        N_len = N_end - N_start

        # el nuevo N será N1
        N_new = f'{N}1'

        # 1+N0 es el string siendo reemplazado, luego su longitud es N_len+3
        replace_len = N_len + 3

        # empezamos reemplazando 2 caracteres antes de N (al 1 en 1+N0)
        replace_start = N_start - 2

        # creamos la nueva fórmula
        nueva_formula = formula[:replace_start] + N_new + formula[replace_start+replace_len:]

        # añadimos la fórmula al conjunto de posibles consecuencias
        consecuencias.add(nueva_formula)

    return consecuencias

def R1b(formula):
    consecuencias = set()
    # si la fórmula no está bien formada, no puede haber consecuencias
    if not _bien_formada(formula):
        return consecuencias
    
    (left_side, right_side) = formula.split('=')
    nueva_formula = f'1+{left_side}={right_side}'
    consecuencias.add(nueva_formula)

    return consecuencias

def _suma_binaria(string):
    # debe ser una suma de números binarios
    assert regex_suma_numero_binario.match(string)

    numeros = [int(x, 2) for x in string.split('+')]
    return sum(numeros)

def _sumas_formula(formula):
    assert regex_formula_bien_formada.match(formula)

    (left_side, right_side) = formula.split('=')
    left_sum = _suma_binaria(left_side)
    right_sum = _suma_binaria(right_side)

    return left_sum, right_sum

def _es_verdadero(formula):
    # si la fórmula no está bien formada, no es verdadero
    if not _bien_formada(formula):
        return False
    
    left_sum, right_sum = _sumas_formula(formula)
    
    return left_sum == right_sum

def _es_verdadero_geq(formula):
    # si la fórmula no está bien formada, no es verdadero
    if not _bien_formada(formula):
        return False
    
    left_sum, right_sum = _sumas_formula(formula)
    
    return left_sum >= right_sum

def _aplicar_reglas(formula, reglas):
    """
    Aplicar todas las reglas a una fo4rmula

    Argumentos
    ----------
    formula (str): una fórmula
    reglas (List<function>): las reglas a aplicar

    Return
    ------
    set<str>: conjunto de fórmulas que pueden producirse aplicando las reglas.
        Será vacío si la fórmula no está bien formada
    """

    nuevas_formulas = set()

    for regla in reglas:
        # | es el operador de unión, y x |= y es equivalente a x = x | y
        nuevas_formulas |= set([(f, regla.__name__) for f in regla(formula)])
    
    return nuevas_formulas

def _aplicar_reglas_a_frontera(probadas, frontera, reglas, predecesores=None):
    """
    Aplica las reglas a un conjunto de fórmulas en la frontera

    Esta fórmula aplicará todas las reglas de inferencia a la frontera, añadiendo
    las fórmulas nuevas probables a probadas y devolviendo una nueva frontera
    que consiste únicamente en las fórmulas añadidas. Un diccionario de fórmulas
    predecesoras, si se proporciona, se actualiza

    Argumentos
    ----------
    probados (set<str>): un conjunto de fórmulas que ya han sido probadas. Las
        fórmulas de este conjunto pueden haber sido usadas o no para generar otras
        fórmulas mediante reglas de inferencia. Este conjunto se actualizará,
        produciendo un conjunto que contiene todas las nuevas fórmulas probadas
    frontera (set<str>): un conjunto de fórmulas a las que las reglas de inferencia
        no han sido aplicadas todavía. Por definición, frontera es un subconjunto de
        probados y la función devolverá un error si este no es el caso
    predecersores(dict<str,str>): un diccionario en el cual la clave es una fórmula
        f y el valor es una fórmula f' que se usa para generar f a través de una regla
        de inferencia. Este parámetro es opcional pero, en caso de que exista, el
        diccionario será actualizado
    
    Return
    ------
    set<str>: una nueva frontera que consiste únicamente en las nuevas fórmulas probadas
    """

    assert frontera <= probadas

    nueva_frontera = set()

    # la función sorted no se usa para corrección, es necesaria para obtener los mismos
    # predecesores cada vez (en otro caso habrá ambigüedad)
    for f in sorted(frontera):
        nuevas_formulas = _aplicar_reglas(f, reglas)
        nueva_frontera |= {f[0] for f in nuevas_formulas}
        #nueva_frontera |= nuevas_formulas
        if predecesores:
            # la función sorted aparece por el mismo motivo que la anterior
            for nueva_formula in sorted(nuevas_formulas):
                if nueva_formula[0] not in predecesores:
                    predecesores[nueva_formula[0]] = (f, nueva_formula[1])
    ya_probado = nueva_frontera & probadas
    nueva_frontera -= ya_probado
    probadas |= nueva_frontera

    return nueva_frontera

def _prueba_desde_predecesores(formula, predecesores, max_predecesores = 1000):
    """
    Generar una prueba de formula

    Esta función genera una prueba para la fórmula formula, dada la información
    de los predecesores en el diccionario predecesores. 
    """

    prueba = [(formula, predecesores[formula][1])]
    predecesor = predecesores[formula][0]
    count = 0
    while predecesor != '' and count <= max_predecesores:
        prueba.append((predecesor, predecesores[predecesor][1]))
        predecesor = predecesores[predecesor][0]
        count += 1
    if count > max_predecesores:
        print('WARN: ciclo inesperado o cadena larga de predecesores:')
        print(prueba)
    prueba.reverse()

    return prueba

def _prueba_a_printstring(prueba):
    # para estilizar, tomamos la longitud de la mayor de las fórmulas
    len_max = max([len(paso[0]) for paso in prueba])
    len_max_num = len(str(int(len(prueba)))) + 2
    return '\n'.join([f' {"  " if i==0 else "->"} {f"(F{i+1})":>{len_max_num}} {paso[0]:<{len_max}}  ({paso[1]})' for i, paso in enumerate(prueba)])


def _es_teorema(formula, reglas=[R1, R2, R3], max_formulas=100000):
    """
    Intenta determinar si formula es un teorema, y devuelve una demostración

    Argumentos
    ----------
    formula (str): un string representando una fórmula
    reglas (List<function>): el conjunto de reglas a aplicar
    max_formulas (int): una cota superior (aproximada) del número de fórmulas
        probables que serán generadas intentando demostrar formula
    
    Returns
    -------
    resultado (str): un string describiendo lo que ha pasado, uno de entre
        ['theorem', 'not proved...', 'ill-formed']
    demostracion (List<str>): una lista ordenada de las fórmulas usadas para
        probar formula. Si no se encuentra una prueba, es None
    """

    prueba = None
    if not _bien_formada(formula):
        resultado = 'ill-formed'
    else:
        probado = set([axioma])
        frontera = probado
        predecesores = {axioma: ('', 'Axioma')}

        while len(probado) < max_formulas:
            frontera = _aplicar_reglas_a_frontera(probado, frontera, reglas, predecesores)
            if formula in probado:
                break
        if formula in probado:
            resultado = 'theorem'
            prueba = _prueba_desde_predecesores(formula, predecesores)
        else:
            resultado = f'not proved in the first {len(probado)} generated formulas'

    return resultado, prueba

def is_theorem(logical_system, formula, max_formulas=100000):
    if logical_system == 'BinarySumLogical' or logical_system == 'BinarySum':
        reglas = [R1, R2, R3]
    elif logical_system == 'BinarySumLogicalBroken':
        reglas = [R1, R2, R3, R1b]
    elif logical_system == 'BinarySumLogicalRestricted':
        reglas = [R1, R2]
    elif logical_system == 'BinarySumLogicalFixed':
        reglas = [R1, R2, R3, R1b]
    else:
        return 'the system does not exist'

    resultado, prueba = _es_teorema(formula, reglas, max_formulas)

    if prueba:
        print(_prueba_a_printstring(prueba))
    return resultado

def is_true(logical_system, formula):
    if logical_system == 'BinarySumLogical':
        interpretacion = _es_verdadero
    elif logical_system == 'BinarySumLogicalBroken':
        interpretacion = _es_verdadero
    elif logical_system == 'BinarySumLogicalRestricted':
        interpretacion = _es_verdadero
    elif logical_system == 'BinarySumLogicalFixed':
        interpretacion = _es_verdadero_geq
    else:
        return 'the system does not exist or is not a logical system'

    return interpretacion(formula)
