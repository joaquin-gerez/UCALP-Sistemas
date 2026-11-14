# Guía de estudio — Observer y Strategy

## Qué resuelve el sistema

Un sensor guarda nombre, ubicación, temperatura y humedad. Cuando cambian sus mediciones, avisa a los observadores registrados y evalúa los datos con el criterio seleccionado.

El código se divide en modelo (`monitoreo.py`) y consola (`main.py`). La consola recibe las opciones y llama al modelo; las reglas están en el modelo.

## Observer: avisar de un cambio

- **Sujeto:** `Sensor`.
- **Contrato:** `Observador`, con el método `actualizar`.
- **Implementación:** `ObservadorConsola`.
- **Suscripción:** `registrar_observador` y `quitar_observador`.

Operador y Supervisor son dos objetos de la misma clase. El sensor guarda sus referencias y llama a `actualizar` después de guardar mediciones nuevas. Así puede agregar receptores sin conocer cómo muestra los datos cada uno.

Los avisos ocurren ante cualquier cambio efectivo, haya alerta o no. Repetir los mismos valores no genera avisos.

**Para practicar:** agregar un tercer observador desde el menú y cambiar una medición. Explicar por qué aparecen tres avisos sin modificar la clase `Sensor`.

## Strategy: cambiar cómo se evalúan los datos

- **Contexto:** `Sensor`.
- **Contrato:** `EstrategiaEvaluacion`, con `evaluar` y `describir`.
- **Alternativas:** `EvaluacionTemperatura` y `EvaluacionHumedad`.

El sensor conserva una estrategia y delega en su método `evaluar`. El resultado `True` significa alerta. `cambiar_estrategia` reemplaza ese objeto y reevalúa las mediciones actuales sin crear otro sensor.

Con 31 °C y 45 % de humedad, el criterio de temperatura genera alerta y el de humedad da normal. Los datos son iguales; cambió el criterio. Cambiar estrategia no notifica a los observadores porque las mediciones no cambiaron.

**Para practicar:** ejecutar la demo y predecir el resultado antes de cada cambio de estrategia.

## Cómo se integran

Al ejecutar `cambiar_mediciones`:

1. Valida ambos valores y guarda las mediciones.
2. Notifica a los observadores: **Observer**.
3. Delega la evaluación en la estrategia: **Strategy**.
4. Actualiza el resultado y el estado del sensor.

Observer responde «¿a quién aviso?» y Strategy responde «¿cómo evalúo?». Los observadores reciben las mediciones; el resultado se calcula después.

## Estados y decisiones

| Estado | Significado |
| --- | --- |
| Configurado | Sensor creado, todavía sin iniciar. |
| Monitoreando | Iniciado y con evaluación normal. |
| Alerta generada | La medición supera el umbral del criterio activo. |

`iniciar` requiere al menos dos observadores y evalúa los valores iniciales. Una nueva medición o estrategia puede activar o quitar la alerta. `Estado` es un enum; no se implementa el patrón State.

La humedad debe estar entre 0 y 100; la temperatura no puede ser inferior a −273.15 °C. Los números deben ser finitos. Una entrada inválida se rechaza sin guardar cambios parciales.

La aplicación funciona en memoria y de forma síncrona, sin sensores físicos ni persistencia. Supone que los observadores registrados cumplen su contrato sin lanzar errores.

## Leer los diagramas

Abrir los [diagramas UML](../diagramas/README.md).

- **Clases:** estructura y relaciones. `Sensor` tiene observadores y una estrategia; las clases concretas implementan sus contratos mediante clases base abstractas (ABC).
- **Secuencia:** orden de llamadas al cambiar una medición. Seguir guardar → notificar → evaluar → mostrar resultado.
- **Estados:** cambios entre Configurado, Monitoreando y Alerta generada.

En clases, `0..*` permite registrar y quitar observadores. La condición de tener dos se exige al iniciar. La estrategia tiene multiplicidad `1`: siempre hay una seleccionada.

## Preguntas para repasar

1. ¿Por qué dos observadores no requieren dos clases distintas?
2. ¿Dónde se ve que el aviso es automático?
3. ¿Qué cambia al seleccionar otra estrategia y qué se conserva?
4. ¿Por qué cambiar estrategia no produce avisos?
5. ¿Qué pasa con humedad de 70 % exactos? ¿Y con 71 %?
6. ¿Cómo agregarías una tercera estrategia sin cambiar la evaluación del sensor?
7. ¿Dónde se integran ambos patrones en el código?

Para preparar una explicación breve: presentar el problema, ejecutar la demo, señalar ambos patrones en el código y recorrer los tres diagramas. Ejecutar las pruebas y elegir una para explicar qué comportamiento verifica.
