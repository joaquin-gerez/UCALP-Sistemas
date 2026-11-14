# TP integrador — Monitoreo ambiental

Aplicación de consola para registrar sensores de temperatura y humedad, notificar sus cambios con **Observer** y evaluar las mediciones con **Strategy**.

## Entregable

[Descargar ZIP para entregar o llevar a la exposición](consigna/ENTREGABLE_Grupo11_Monitoreo.zip).

Incluye código fuente, tres diagramas PDF y un README con los requisitos, las instrucciones y la explicación de Observer y Strategy. Extraer el ZIP y abrir su README para empezar.

## Ejecutar

Requiere Python 3.10 o superior y solo usa la biblioteca estándar. Desde esta carpeta:

```sh
python3 -B main.py --demo
python3 -B main.py
```

En Windows se puede usar `py -3` en lugar de `python3`.

`--demo` muestra un recorrido automático. Sin esa opción se abre el menú para registrar sensores, consultar datos, modificar mediciones, cambiar estrategias y agregar observadores. La opción `0` sale.

## Probar

```sh
python3 -B -m unittest discover -s tests -v
```

## Contenido

- [`monitoreo.py`](monitoreo.py): sensores, observadores, estrategias y estados.
- [`main.py`](main.py): menú y demo.
- [Guía de estudio](docs/GUIA_ESTUDIO.md): diseño, patrones y ejercicios.
- [Diagramas UML](diagramas/README.md): clases, secuencia y estados.
- [Consigna](consigna/CONSIGNA.md): requisitos del trabajo.
- [`tests/test_monitoreo.py`](tests/test_monitoreo.py): pruebas del modelo y la consola.

## Recorrido de la demo

Cada sensor tiene dos observadores: Operador y Supervisor.

| Acción | Mediciones | Criterio activo | Resultado | Avisos |
| --- | --- | --- | --- | --- |
| Registrar e iniciar | 22 °C / 45 % | Temperatura >30 °C | Normal | 0 |
| Cambiar temperatura | 31 °C / 45 % | Temperatura >30 °C | Alerta | 2 |
| Seleccionar humedad | 31 °C / 45 % | Humedad >70 % | Normal | 0 |
| Cambiar humedad | 31 °C / 75 % | Humedad >70 % | Alerta | 2 |
| Cambiar humedad | 31 °C / 60 % | Humedad >70 % | Normal | 2 |

Los umbrales son valores de ejemplo. La comparación es estricta: 30 °C y 70 % exactos no generan alerta. Los datos se conservan en memoria y se pierden al salir.
