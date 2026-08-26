"""turing.py

Este programa incluye una clase `Turing` que encapsula la simulación de
`simulate_turing.py`

---
Autor: Miguel Ángel Fernández Gutiérrez
"""

import re

class Turing:
    def __init__(self, codification_mt, entrada=''):
        self.codificacion_mt = codification_mt
        self.entrada = entrada
        self.situacion_actual = 'no cargada'

        # cargamos la configuración inicial
        self.__iniciar()
    
    def run(self):
        while self.next_step():
            pass

    def accepts_or_rejects(self):
        return 'yes' if self.situacion_actual == 'accepts' else 'no'

    def next_step(self):
        if self.situacion_actual == 'has not halted':
            configuracion_actual = self.__configuracion_actual()
            transicion_siguiente = self.__transicion(configuracion_actual)
            configuracion_siguiente = self.__aplicar_transicion(configuracion_actual, transicion_siguiente)
            self.configuraciones.append(configuracion_siguiente)
            self.situacion_actual = self.__situacion(configuracion_siguiente)
            return True

        return False

    def __str__(self):
        if self.situacion_actual in ['has not halted', 'accepts', 'rejects']:
            configuracion_actual = self.__configuracion_actual()
            return f"{configuracion_actual} ({self.situacion_actual})"
        elif self.situacion_actual.startswith('error'):
            return ":\n".join(self.situacion_actual.split(': '))

        return f"({self.situacion_actual})"

    def __repr__(self):
        if self.situacion_actual in ['has not halted', 'accepts', 'rejects']:
            return f"Estados: {sorted(self.estados)}\n" \
                + f"Alfabeto de entrada: {sorted(self.alfabeto_entrada)}\n" \
                + f"Alfabeto de trabajo: {sorted(self.alfabeto_trabajo)}\n" \
                + f"Símbolo blanco: {self.simbolo_blanco}\n" \
                + f"Estado inicial: {self.estado_inicial}\n" \
                + f"Estados finales: {sorted(self.estados_finales)}\n" \
                + "\n----\n\n" \
                + "Transiciones:\n\n" \
                + "\n".join([str(self.transiciones[clave]) for clave in sorted(self.transiciones, key=lambda key: self.transiciones[key].id)]) \
                + "\n\n----\n\n" \
                + f"Entrada: '{self.entrada}'\n" \
                + f"Situación actual: {self.situacion_actual}\n\n" \
                + "Proceso de cálculo:\n\n" \
                + "\n".join([f"{'(C'+str(i)+')':>8} {repr(configuracion)}" for i, configuracion in enumerate(self.configuraciones)])
        elif self.situacion_actual.startswith('error'):
            return ":\n".join(self.situacion_actual.split(': '))
        else:
            return f"Situación actual: {self.situacion_actual}"

    def __iniciar(self):
        # dividimos en líneas
        lineas = self.codificacion_mt.split('\n')

        # eliminamos comentarios
        lineas = [linea.split('#')[0] for linea in lineas]
        # eliminamos líneas vacías
        lineas = [linea for linea in lineas if linea.split()]

        # COMPROBACIÓN SINTÁCTICA
        # ----
        # debe haber al menos 5 líneas
        if len(lineas) < 5:
            self.situacion_actual = 'error semántico: el archivo no tiene las líneas suficientes'
            return

        # las primeras cinco líneas no pueden tener , y : ya que entran en conflicto
        # con la codificación de las transiciones: las eliminamos
        for linea in lineas[:6]:
            linea = linea.replace(':', '').replace(',', '')

        # comprobamos que las líneas a partir de la sexta son transiciones
        for linea in lineas[6:]:
            # eliminamos los espacios
            linea = ''.join(linea.split())
            # comprobamos que obedecen una expresión regular
            if not re.compile('^[^,:]+,[^,:]+:[^,:]+,[^,:]+,[IDS]$').match(linea):
                self.situacion_actual = 'error sintáctico: las transiciones no están bien escritas'
                return
        # ---- [fin COMPROBACIÓN SINTÁCTICA]

        # ESTADOS
        # ----
        # la primera línea son los estados
        # ignoramos , y : (entra en conflicto con la codificación)
        linea_estados = lineas[0].replace(':', '').replace(',', '')
        self.estados = set(linea_estados.split())
        # ---- [fin ESTADOS]

        # ALFABETO DE ENTRADA
        # ----
        self.alfabeto_entrada = set(lineas[1].split())
        # comprobamos que la entrada está en el alfabeto de entrada
        if not set(self.entrada).issubset(self.alfabeto_entrada):
            self.situacion_actual = f"error: la entrada '{self.entrada}' no está en el alfabeto de entrada"
            return
        # ---- [fin ALFABETO DE ENTRADA]

        # ALFABETO DE TRABAJO
        # será la unión de los símbolos expresados en la línea 1 y la 2
        # (esto evita comprobaciones innecesarias y mayor flexibilidad)
        # ----
        self.alfabeto_trabajo = self.alfabeto_entrada.union(set(lineas[2].split()))
        # ---- [fin ALFABETO DE TRABAJO]

        # SÍMBOLO BLANCO
        # será el primer símbolo de la línea 3 (si hay más los ignoramos)
        # ----
        self.simbolo_blanco = lineas[3].split()[0]

        # el símbolo ha de estar en el alfabeto de trabajo
        if self.simbolo_blanco not in self.alfabeto_trabajo:
            self.situacion_actual = f"error semántico: el símbolo blanco '{self.simbolo_blanco}' no está en el alfabeto de trabajo"
            return
        # --- [fin SÍMBOLO BLANCO]

        # ESTADO INICIAL
        # será el primer estado de la línea 4 (si hay más los ignoramos)
        # ----
        self.estado_inicial = lineas[4].split()[0]

        # el estado ha de estar en el conjunto de estados
        if self.estado_inicial not in self.estados:
            self.situacion_actual = f"error semántico: el estado inicial '{self.estado_inicial}' no está en el conjunto de estados"
            return
        # ---- [fin ESTADO INICIAL]

        # ESTADOS FINALES
        # ----
        self.estados_finales = set(lineas[5].split())

        # los estados finales han de estar en el conjunto de estados
        if not self.estados_finales.issubset(self.estados):
            estados_finales_incorrectos = self.estados_finales - self.estados
            if len(estados_finales_incorrectos) == 1:
                self.situacion_actual = f"error semántico: el estado final '{estados_finales_incorrectos[0]}' no está en el conjunto de estados"

            else:
                self.situacion_actual = f"error semántico: los estados finales {estados_finales_incorrectos} no están en el conjunto de estados"
            return
        # ---- [fin ESTADOS FINALES]

        # TRANSICIONES
        # ----
        self.transiciones = dict()

        for i, linea in enumerate(lineas[6:]):
            estado_actual, simbolo_leido, estado_siguiente, simbolo_reemplazo, movimiento = linea.replace(",", " ").replace(":", " ").split()
            if estado_actual not in self.estados:
                self.situacion_actual = f"error semántico: la transición (T{i+1}) tiene como estado actual a '{estado_actual}', que no está en el conjunto de estados"
                return
            if simbolo_leido not in self.alfabeto_trabajo:
                self.situacion_actual = f"error semántico: la transición (T{i+1}) tiene como símbolo leído a '{simbolo_leido}', que no está en el alfabeto de trabajo"
                return
            if estado_siguiente not in self.estados:
                self.situacion_actual = f"error semántico: la transición (T{i+1}) tiene como estado siguiente a '{estado_siguiente}', que no está en el conjunto de estados"
                return
            if simbolo_reemplazo not in self.alfabeto_trabajo:
                self.situacion_actual = f"error semántico: la transición (T{i+1}) tiene como símbolo reemplazo a '{simbolo_reemplazo}', que no está en el alfabeto de trabajo"
                return

            self.transiciones[(estado_actual, simbolo_leido)] = \
                Transicion(
                    i + 1,
                    estado_actual,
                    simbolo_leido,
                    estado_siguiente,
                    simbolo_reemplazo,
                    movimiento
                )
        # --- [fin TRANSICIONES]

        self.configuraciones = []
        self.__insertar_configuracion_inicial()

    def __insertar_configuracion_inicial(self):
        # la insertamos únicamente si la lista de configuraciones está vacía
        if not self.configuraciones:
            self.configuraciones.append(
                Configuracion(
                    self.estado_inicial,
                    self.entrada if len(self.entrada) > 0 else self.simbolo_blanco,
                    0,
                    turing=self
                )
            )

            # actualizamos la situación
            self.situacion_actual = self.__situacion(self.configuraciones[0])

    def __transicion(self, configuracion):
        estado, simbolo = configuracion.estado, configuracion.head_symbol()
        if (estado, simbolo) in self.transiciones:
            return self.transiciones[(estado, simbolo)]
        else:
            return None

    def __situacion(self, configuracion):
        transicion = self.__transicion(configuracion)

        if transicion:
            return 'has not halted'
        else:
            if configuracion.estado in self.estados_finales:
                return 'accepts'
            else:
                return 'rejects'

    def __aplicar_transicion(self, configuracion, transicion):
        estado_actual, simbolo_actual = configuracion.estado, configuracion.head_symbol()
        estado_siguiente, simbolo_reemplazo, movimiento = transicion.estado_siguiente, transicion.simbolo_reemplazo, transicion.movimiento

        # reemplazamos el símbolo
        cinta_siguiente = list(configuracion.cinta)
        cinta_siguiente[configuracion.posicion_cabezal] = simbolo_reemplazo
        cinta_siguiente = "".join(cinta_siguiente)
        posicion_cabezal_siguiente = configuracion.posicion_cabezal

        # si nos movemos a la derecha
        if movimiento == 'D':
            if configuracion.posicion_cabezal == len(cinta_siguiente) - 1:
                # estamos al final: añadimos un símbolo blanco
                cinta_siguiente += self.simbolo_blanco
            posicion_cabezal_siguiente += 1
        if movimiento == 'I':
            if configuracion.posicion_cabezal == 0:
                cinta_siguiente = self.simbolo_blanco + cinta_siguiente
            else:
                posicion_cabezal_siguiente -= 1
        
        return Configuracion(
            estado_siguiente,
            cinta_siguiente,
            posicion_cabezal_siguiente,
            self.transiciones[(estado_actual, simbolo_actual)].id,
            turing=self
        )

    def __configuracion_actual(self):
        return self.configuraciones[-1] if self.configuraciones else None


class Transicion:
    def __init__(self, id, estado_actual, simbolo_leido, estado_siguiente, simbolo_reemplazo, movimiento):
        self.id = id
        self.estado_actual = estado_actual
        self.simbolo_leido = simbolo_leido
        self.estado_siguiente = estado_siguiente
        self.simbolo_reemplazo = simbolo_reemplazo
        self.movimiento = movimiento

    def __str__(self):
        return f"{'(T'+str(self.id)+')':>8}  δ({self.estado_actual}, {self.simbolo_leido})" \
            + f" = ({self.estado_siguiente}, {self.simbolo_reemplazo}, {self.movimiento})"

class Configuracion:
    def __init__(self, estado, cinta, posicion_cabezal, id_transicion_causa=None, turing=None):
        # eliminamos los símbolos blancos a la derecha y a la izquierda
        if turing:
            # debemos eliminar a la izquierda tantos símbolos como
            # min([numero de blancos a la izquierda], posición del cabezal)
            eliminar_izquierda = min(len(cinta)-len(cinta.lstrip(turing.simbolo_blanco)), posicion_cabezal)
            cinta = cinta[eliminar_izquierda:]
            posicion_cabezal -= eliminar_izquierda

            # debemos eliminar a la derecha tantos símbolos como
            # min([numero de blancos a la derecha], longitud de la cinta - posición del cabezal - 1)
            eliminar_derecha = min(len(cinta)-len(cinta.rstrip(turing.simbolo_blanco)), len(cinta) - posicion_cabezal - 1)
            cinta = cinta[:-eliminar_derecha] if eliminar_derecha > 0 else cinta

        self.estado = estado
        self.cinta = cinta
        self.posicion_cabezal = posicion_cabezal
        self.id_transicion_causa = id_transicion_causa

    def __str__(self):
        repr_cinta = ""
        for i, simbolo in enumerate(self.cinta):
            repr_cinta += f"[{simbolo}]" if i == self.posicion_cabezal else simbolo
            repr_cinta += " "
        return f"{self.estado} : {repr_cinta}"[:-1]

    def __repr__(self):
        return f"{self.__str__()}" \
            + (f"\t- aplicando (T{self.id_transicion_causa})" if self.id_transicion_causa else "")

    def head_symbol(self):
        return self.cinta[self.posicion_cabezal]