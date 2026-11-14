"""Modelo del integrador: Observer distribuye cambios; Strategy los evalúa."""

from abc import ABC, abstractmethod
from enum import Enum
from math import isfinite


def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo}: se requiere texto no vacío")
    return valor.strip()


def numero(valor, campo, minimo=None, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo}: se requiere un número")
    if not isfinite(valor):
        raise ValueError(f"{campo}: debe ser finito")
    if minimo is not None and valor < minimo:
        raise ValueError(f"{campo}: mínimo {minimo}")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo}: máximo {maximo}")
    return float(valor)


class Estado(Enum):
    CONFIGURADO = "Configurado"
    MONITOREANDO = "Monitoreando"
    ALERTA = "Alerta generada"


class Observador(ABC):
    @abstractmethod
    def actualizar(self, nombre, ubicacion, temperatura, humedad):
        """Recibe las nuevas mediciones; aún no hay evaluación de este cambio."""


class ObservadorConsola(Observador):
    def __init__(self, identificador):
        self.identificador = texto(identificador, "Identificador")

    def actualizar(self, nombre, ubicacion, temperatura, humedad):
        print(f"[{self.identificador}] {nombre} ({ubicacion}): "
              f"{temperatura:g} °C / {humedad:g} %")


class EstrategiaEvaluacion(ABC):
    @abstractmethod
    def evaluar(self, temperatura, humedad):
        """Devuelve True si la medición supera el límite de alerta."""

    @abstractmethod
    def describir(self):
        """Devuelve el criterio visible para el usuario."""


class EvaluacionTemperatura(EstrategiaEvaluacion):
    def __init__(self, limite=30):
        self.limite = numero(limite, "Límite de temperatura", -273.15)

    def evaluar(self, temperatura, humedad):
        return temperatura > self.limite

    def describir(self):
        return f"temperatura > {self.limite:g} °C"


class EvaluacionHumedad(EstrategiaEvaluacion):
    def __init__(self, limite=70):
        self.limite = numero(limite, "Límite de humedad", 0, 100)

    def evaluar(self, temperatura, humedad):
        return humedad > self.limite

    def describir(self):
        return f"humedad > {self.limite:g} %"


class Sensor:
    def __init__(self, nombre, ubicacion, temperatura, humedad, estrategia):
        self.nombre = texto(nombre, "Nombre")
        self.ubicacion = texto(ubicacion, "Ubicación")
        self._temperatura = numero(temperatura, "Temperatura", -273.15)
        self._humedad = numero(humedad, "Humedad", 0, 100)
        self._observadores = []
        self._estrategia = self._validar_estrategia(estrategia)
        self._estado = Estado.CONFIGURADO
        self._resultado = None

    @staticmethod
    def _validar_estrategia(estrategia):
        if not isinstance(estrategia, EstrategiaEvaluacion):
            raise ValueError("Se requiere una EstrategiaEvaluacion")
        return estrategia

    @property
    def temperatura(self):
        return self._temperatura

    @property
    def humedad(self):
        return self._humedad

    @property
    def estado(self):
        return self._estado

    @property
    def resultado(self):
        return self._resultado

    @property
    def estrategia(self):
        return self._estrategia

    def registrar_observador(self, observador):
        if not isinstance(observador, Observador):
            raise ValueError("Se requiere un Observador")
        if observador not in self._observadores:
            self._observadores.append(observador)

    def quitar_observador(self, observador):
        """Quitar uno ausente no produce error; permite desuscribirse."""
        if observador in self._observadores:
            self._observadores.remove(observador)

    def iniciar(self):
        if self._estado is not Estado.CONFIGURADO:
            raise ValueError("El sensor ya fue iniciado")
        if len(self._observadores) < 2:
            raise ValueError("Para iniciar se requieren al menos dos observadores")
        self._estado = Estado.MONITOREANDO
        # La medición inicial también se evalúa; podría comenzar en alerta.
        return self._evaluar()

    def _evaluar(self):
        self._resultado = self._estrategia.evaluar(self.temperatura, self.humedad)
        self._estado = Estado.ALERTA if self.resultado else Estado.MONITOREANDO
        return self.resultado

    def cambiar_estrategia(self, estrategia):
        self._estrategia = self._validar_estrategia(estrategia)
        if self.estado is not Estado.CONFIGURADO:
            return self._evaluar()
        return None

    def cambiar_mediciones(self, temperatura, humedad):
        if self.estado is Estado.CONFIGURADO:
            raise ValueError("Primero debe iniciar el monitoreo")
        # Validación completa antes de modificar: una entrada inválida no cambia nada.
        nueva_t = numero(temperatura, "Temperatura", -273.15)
        nueva_h = numero(humedad, "Humedad", 0, 100)
        if (nueva_t, nueva_h) == (self.temperatura, self.humedad):
            return self.resultado
        self._temperatura, self._humedad = nueva_t, nueva_h
        self._notificar()
        return self._evaluar()

    def _notificar(self):
        # Copia: una desuscripción durante un aviso no altera el recorrido actual.
        for observador in tuple(self._observadores):
            observador.actualizar(self.nombre, self.ubicacion,
                                  self.temperatura, self.humedad)

    def resumen(self):
        resultado = ("Sin evaluar" if self.resultado is None else
                     "ALERTA" if self.resultado else "Normal")
        return (f"{self.nombre} | {self.ubicacion} | {self.temperatura:g} °C | "
                f"{self.humedad:g} % | {self.estrategia.describir()} | "
                f"{resultado} | {self.estado.value}")
