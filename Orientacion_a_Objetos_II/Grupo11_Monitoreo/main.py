"""Consola sin dependencias. Ejecutar: python3 main.py --demo."""

import argparse

from monitoreo import (EvaluacionHumedad, EvaluacionTemperatura,
                       ObservadorConsola, Sensor)


def preparar_sensor(nombre, ubicacion, temperatura, humedad):
    sensor = Sensor(nombre, ubicacion, temperatura, humedad, EvaluacionTemperatura())
    sensor.registrar_observador(ObservadorConsola("Operador"))
    sensor.registrar_observador(ObservadorConsola("Supervisor"))
    sensor.iniciar()
    return sensor


def demo():
    print("DEMO GRUPO 11 — límites didácticos, no oficiales")
    sensor = preparar_sensor("Sala A", "Planta baja", 22, 45)
    print("1. Registrar e iniciar:", sensor.resumen())
    print("2. Cambiar temperatura a 31: dos avisos y alerta por temperatura")
    sensor.cambiar_mediciones(31, 45)
    print(sensor.resumen())
    print("3. Cambiar a humedad: reevaluación sin avisos de medición")
    sensor.cambiar_estrategia(EvaluacionHumedad())
    print(sensor.resumen())
    print("4. Cambiar humedad a 75: dos avisos y alerta por humedad")
    sensor.cambiar_mediciones(31, 75)
    print(sensor.resumen())
    print("5. Cambiar humedad a 60: dos avisos y retorno a Monitoreando")
    sensor.cambiar_mediciones(31, 60)
    print(sensor.resumen())


def leer_numero(mensaje):
    try:
        return float(input(mensaje).replace(",", "."))
    except ValueError:
        raise ValueError("Ingrese un número (ejemplo: 22.5)") from None


def interactivo():
    sensores = {}
    print("Monitoreo ambiental — Grupo 11")
    while True:
        try:
            print("\n1 Registrar sensor | 2 Consultar todos | 3 Cambiar mediciones")
            print("4 Cambiar estrategia | 5 Registrar observador | 0 Salir")
            opcion = input("Opción: ").strip()
            if opcion == "0":
                return
            if opcion == "1":
                nombre = input("Nombre único: ").strip()
                if nombre in sensores:
                    raise ValueError("Ya existe ese nombre")
                ubicacion = input("Ubicación: ")
                temperatura = leer_numero("Temperatura °C: ")
                humedad = leer_numero("Humedad %: ")
                sensor = preparar_sensor(nombre, ubicacion, temperatura, humedad)
                sensores[sensor.nombre] = sensor
                print("Registrados Operador y Supervisor.")
                print(sensor.resumen())
            elif opcion == "2":
                print("\n".join(s.resumen() for s in sensores.values()) or "Sin sensores")
            elif opcion in ("3", "4", "5"):
                print("Sensores:", ", ".join(sensores) or "ninguno")
                nombre = input("Nombre del sensor: ").strip()
                if nombre not in sensores:
                    raise ValueError("Sensor inexistente")
                sensor = sensores[nombre]
                if opcion == "3":
                    temperatura = leer_numero("Nueva temperatura °C: ")
                    humedad = leer_numero("Nueva humedad %: ")
                    sensor.cambiar_mediciones(temperatura, humedad)
                elif opcion == "4":
                    criterio = input("1 Temperatura (>30 °C) | 2 Humedad (>70 %): ").strip()
                    if criterio not in ("1", "2"):
                        raise ValueError("Estrategia inválida")
                    sensor.cambiar_estrategia(EvaluacionTemperatura() if criterio == "1"
                                             else EvaluacionHumedad())
                else:
                    identificador = input("Identificador del nuevo observador: ")
                    sensor.registrar_observador(ObservadorConsola(identificador))
                    print("Observador registrado")
                print(sensor.resumen())
            else:
                print("Opción inválida")
        except ValueError as error:
            print(f"Entrada inválida: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nFin de la sesión; datos en memoria no persistidos.")
            return


def main():
    parser = argparse.ArgumentParser(description="Integrador OOII: Observer + Strategy")
    parser.add_argument("--demo", action="store_true", help="demo reproducible sin interacción")
    argumentos = parser.parse_args()
    if argumentos.demo:
        demo()
    else:
        interactivo()


if __name__ == "__main__":
    main()
