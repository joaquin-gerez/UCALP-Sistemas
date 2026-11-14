import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path

from monitoreo import (Estado, EstrategiaEvaluacion, EvaluacionHumedad,
                       EvaluacionTemperatura, Observador, ObservadorConsola, Sensor)


class Espia(Observador):
    def __init__(self, eventos=None):
        self.avisos = []
        self.eventos = eventos if eventos is not None else []

    def actualizar(self, *datos):
        self.avisos.append(datos)
        self.eventos.append("aviso")


class ModeloTests(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor("Sala A", "Planta baja", 22, 45, EvaluacionTemperatura())
        self.uno, self.dos = Espia(), Espia()
        self.sensor.registrar_observador(self.uno)
        self.sensor.registrar_observador(self.dos)

    def iniciar(self):
        self.sensor.iniciar()

    def test_configurado_sin_evaluacion(self):
        self.assertEqual(self.sensor.estado, Estado.CONFIGURADO)
        self.assertIsNone(self.sensor.resultado)
        self.assertIn("Sin evaluar", self.sensor.resumen())

    def test_inicio_normal(self):
        self.assertFalse(self.sensor.iniciar())
        self.assertEqual(self.sensor.estado, Estado.MONITOREANDO)
        self.assertEqual(self.uno.avisos, [])

    def test_inicio_en_alerta(self):
        sensor = Sensor("Caldera", "Sur", 40, 45, EvaluacionTemperatura())
        sensor.registrar_observador(self.uno)
        sensor.registrar_observador(self.dos)
        self.assertTrue(sensor.iniciar())
        self.assertEqual(sensor.estado, Estado.ALERTA)

    def test_inicio_exige_dos_observadores(self):
        self.sensor.quitar_observador(self.dos)
        with self.assertRaises(ValueError):
            self.iniciar()
        self.assertEqual(self.sensor.estado, Estado.CONFIGURADO)

    def test_no_reiniciar(self):
        self.iniciar()
        with self.assertRaises(ValueError):
            self.iniciar()

    def test_no_cambiar_antes_de_iniciar(self):
        with self.assertRaises(ValueError):
            self.sensor.cambiar_mediciones(31, 45)
        self.assertEqual(self.sensor.temperatura, 22)

    def test_notifica_dos_automaticamente_con_datos_actuales(self):
        self.iniciar()
        self.assertTrue(self.sensor.cambiar_mediciones(31, 45))
        esperado = [("Sala A", "Planta baja", 31, 45)]
        self.assertEqual(self.uno.avisos, esperado)
        self.assertEqual(self.dos.avisos, esperado)

    def test_orden_guardar_notificar_evaluar(self):
        eventos = []
        sensor = self.sensor

        class Inspeccion(Observador):
            def actualizar(self, nombre, ubicacion, temperatura, humedad):
                self_test.assertEqual(sensor.temperatura, temperatura)
                eventos.append("aviso")

        class Criterio(EstrategiaEvaluacion):
            def evaluar(self, temperatura, humedad):
                eventos.append("evaluacion")
                return temperatura > 30

            def describir(self):
                return "criterio de prueba"

        self_test = self
        sensor.quitar_observador(self.uno)
        sensor.quitar_observador(self.dos)
        sensor.registrar_observador(Inspeccion())
        sensor.registrar_observador(Inspeccion())
        sensor.cambiar_estrategia(Criterio())
        sensor.iniciar()
        eventos.clear()
        sensor.cambiar_mediciones(31, 45)
        self.assertEqual(eventos, ["aviso", "aviso", "evaluacion"])

    def test_registro_duplicado_no_duplica_aviso(self):
        self.sensor.registrar_observador(self.uno)
        self.iniciar()
        self.sensor.cambiar_mediciones(23, 45)
        self.assertEqual(len(self.uno.avisos), 1)

    def test_remocion_y_ausente(self):
        self.iniciar()
        self.sensor.quitar_observador(self.uno)
        self.sensor.quitar_observador(self.uno)
        self.sensor.cambiar_mediciones(23, 45)
        self.assertEqual(self.uno.avisos, [])
        self.assertEqual(len(self.dos.avisos), 1)

    def test_sin_cambio_no_notifica(self):
        self.iniciar()
        self.assertFalse(self.sensor.cambiar_mediciones(22, 45))
        self.assertEqual(self.uno.avisos, [])
        self.assertEqual(self.dos.avisos, [])

    def test_transiciones_mediciones(self):
        self.iniciar()
        for temperatura, esperado in [(23, Estado.MONITOREANDO), (31, Estado.ALERTA),
                                      (32, Estado.ALERTA), (29, Estado.MONITOREANDO)]:
            with self.subTest(temperatura=temperatura):
                self.sensor.cambiar_mediciones(temperatura, 45)
                self.assertEqual(self.sensor.estado, esperado)

    def test_cambio_estrategia_runtime_reevalua_sin_notificar(self):
        self.iniciar()
        self.sensor.cambiar_mediciones(31, 45)
        self.assertFalse(self.sensor.cambiar_estrategia(EvaluacionHumedad()))
        self.assertEqual(self.sensor.estado, Estado.MONITOREANDO)
        self.assertEqual(len(self.uno.avisos), 1)
        self.assertEqual(len(self.dos.avisos), 1)
        self.assertTrue(self.sensor.cambiar_mediciones(31, 75))
        self.assertEqual(self.sensor.estado, Estado.ALERTA)
        self.assertFalse(self.sensor.cambiar_mediciones(31, 60))
        self.assertEqual(self.sensor.estado, Estado.MONITOREANDO)

    def test_cambio_estrategia_puede_generar_alerta(self):
        self.iniciar()
        self.sensor.cambiar_mediciones(22, 75)
        self.assertTrue(self.sensor.cambiar_estrategia(EvaluacionHumedad()))
        self.assertEqual(self.sensor.estado, Estado.ALERTA)
        self.assertTrue(self.sensor.cambiar_estrategia(EvaluacionHumedad(60)))
        self.assertFalse(self.sensor.cambiar_estrategia(EvaluacionTemperatura()))

    def test_seleccion_en_configurado(self):
        self.assertIsNone(self.sensor.cambiar_estrategia(EvaluacionHumedad()))
        self.assertEqual(self.sensor.estado, Estado.CONFIGURADO)
        self.assertIsNone(self.sensor.resultado)

    def test_estrategias_limites(self):
        for estrategia, valores in [(EvaluacionTemperatura(), [(29, 45), (30, 45), (31, 45)]),
                                     (EvaluacionHumedad(), [(22, 69), (22, 70), (22, 71)])]:
            for datos, esperado in zip(valores, [False, False, True]):
                with self.subTest(criterio=estrategia.describir(), datos=datos):
                    self.assertEqual(estrategia.evaluar(*datos), esperado)

    def test_criterios_independientes(self):
        self.assertFalse(EvaluacionTemperatura().evaluar(22, 100))
        self.assertFalse(EvaluacionHumedad().evaluar(50, 45))

    def test_limites_personalizados(self):
        self.assertTrue(EvaluacionTemperatura(25).evaluar(26, 0))
        self.assertTrue(EvaluacionHumedad(60).evaluar(0, 61))

    def test_entradas_invalidas_atomicas(self):
        self.iniciar()
        for t, h in [(31, -1), (31, 101), (-274, 45), (float("nan"), 45),
                     (22, float("inf")), (True, 45), ("22", 45), (22, None)]:
            with self.subTest(t=t, h=h), self.assertRaises(ValueError):
                self.sensor.cambiar_mediciones(t, h)
            self.assertEqual((self.sensor.temperatura, self.sensor.humedad), (22, 45))
            self.assertEqual(self.sensor.estado, Estado.MONITOREANDO)
        self.assertEqual(self.uno.avisos, [])

    def test_extremos_validos(self):
        self.iniciar()
        self.sensor.cambiar_mediciones(-273.15, 0)
        self.sensor.cambiar_mediciones(22, 100)
        self.assertEqual(self.sensor.humedad, 100)

    def test_constructor_invalido(self):
        for nombre, ubicacion, t, h in [(" ", "Sur", 22, 45), ("A", "", 22, 45),
                                       ("A", "Sur", -300, 45), ("A", "Sur", 22, 101)]:
            with self.subTest(nombre=nombre, h=h), self.assertRaises(ValueError):
                Sensor(nombre, ubicacion, t, h, EvaluacionTemperatura())

    def test_limites_invalidos(self):
        for clase, valor in [(EvaluacionHumedad, 101), (EvaluacionHumedad, -1),
                              (EvaluacionTemperatura, -274), (EvaluacionTemperatura, float("inf"))]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                clase(valor)

    def test_contratos_invalidos(self):
        with self.assertRaises(ValueError):
            self.sensor.registrar_observador(object())
        anterior = self.sensor.estrategia
        with self.assertRaises(ValueError):
            self.sensor.cambiar_estrategia(object())
        self.assertIs(self.sensor.estrategia, anterior)
        with self.assertRaises(ValueError):
            Sensor("A", "Sur", 22, 45, None)
        with self.assertRaises(ValueError):
            ObservadorConsola(" ")

    def test_interfaces_abstractas(self):
        for clase in (Observador, EstrategiaEvaluacion):
            with self.assertRaises(TypeError):
                clase()

    def test_dos_observadores_concretos(self):
        sensor = Sensor("A", "Sur", 22, 45, EvaluacionTemperatura())
        for nombre in ("Operador", "Supervisor"):
            sensor.registrar_observador(ObservadorConsola(nombre))
        sensor.iniciar()
        with contextlib.redirect_stdout(io.StringIO()) as salida:
            sensor.cambiar_mediciones(31, 45)
        self.assertIn("[Operador] A (Sur): 31 °C / 45 %", salida.getvalue())
        self.assertIn("[Supervisor] A (Sur): 31 °C / 45 %", salida.getvalue())

    def test_sensores_independientes(self):
        otro = Sensor("B", "Norte", 10, 20, EvaluacionHumedad())
        self.iniciar()
        self.sensor.cambiar_mediciones(31, 45)
        self.assertEqual(otro.estado, Estado.CONFIGURADO)
        self.assertEqual(otro.temperatura, 10)


class CLITests(unittest.TestCase):
    def ejecutar(self, argumentos=(), entrada=""):
        return subprocess.run([sys.executable, "-B", "main.py", *argumentos],
                              cwd=Path(__file__).resolve().parents[1], input=entrada,
                              text=True, capture_output=True, timeout=5, check=True)

    def test_demo_no_interactiva(self):
        salida = self.ejecutar(["--demo"]).stdout
        self.assertEqual(salida.count("[Operador]"), 3)
        self.assertEqual(salida.count("[Supervisor]"), 3)
        self.assertIn("temperatura > 30 °C | ALERTA | Alerta generada", salida)
        self.assertIn("humedad > 70 % | ALERTA | Alerta generada", salida)
        self.assertTrue(salida.strip().endswith("Normal | Monitoreando"))

    def test_cli_registrar_cambiar_consultar_y_salir(self):
        entrada = "1\nSala A\nSur\n22\n45\n3\nSala A\n31\n45\n4\nSala A\n2\n5\nSala A\nVisita\n3\nSala A\n31\n75\n2\n0\n"
        salida = self.ejecutar(entrada=entrada).stdout
        self.assertIn("[Visita] Sala A (Sur): 31 °C / 75 %", salida)
        self.assertIn("humedad > 70 % | ALERTA | Alerta generada", salida)

    def test_cli_errores_recuperables(self):
        entrada = "9\n3\nNo existe\n1\nA\nSur\nno-numero\n2\n0\n"
        salida = self.ejecutar(entrada=entrada).stdout
        self.assertIn("Opción inválida", salida)
        self.assertIn("Sensor inexistente", salida)
        self.assertIn("Ingrese un número", salida)
        self.assertIn("Sin sensores", salida)

    def test_cli_eof_no_cuelga(self):
        self.assertIn("Fin de la sesión", self.ejecutar().stdout)


if __name__ == "__main__":
    unittest.main()
