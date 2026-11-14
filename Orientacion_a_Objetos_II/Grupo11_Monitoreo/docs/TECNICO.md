# Diseño técnico y trazabilidad

## Arquitectura simple

`main.py` conserva un diccionario en memoria de sensores por nombre único. No es un registro global: el modelo permite nombres iguales en objetos independientes; la consola impide duplicados dentro de su sesión. `preparar_sensor` crea sensor, estrategia de temperatura y dos observadores distintos; los registra e inicia. No agrega base de datos, red, GUI ni patrón State innecesario.

`Sensor` conserva datos, colección de observadores, **una** estrategia seleccionada y estado. Las propiedades de medición/estado/resultado/estrategia se consultan sin setters; se cambian mediante operaciones del modelo. La consola nunca escribe directamente esos campos. `nombre` y `ubicacion` son atributos públicos de identificación, sin edición por menú.

`Observador` es una ABC con `actualizar(nombre, ubicacion, temperatura, humedad)`. `ObservadorConsola` implementa ese contrato; Operador y Supervisor son dos instancias de la misma clase, con igual función técnica de presentación pero identificadores/destinatarios diferentes. La consigna exige dos observadores, no dos clases concretas diferentes. Ambos reciben cada cambio efectivo independientemente de que produzca alerta. No guardan historial ni consumen el resultado todavía inexistente de esa evaluación.

`EstrategiaEvaluacion` es una ABC con `evaluar(t,h) -> bool` y `describir() -> str`. `True` significa **hay alerta**, no «condición aceptable». `EvaluacionTemperatura` mira temperatura; `EvaluacionHumedad`, humedad. `describir` permite presentar el criterio sin que `Sensor` pregunte por el tipo concreto. La validación `isinstance(..., EstrategiaEvaluacion)` comprueba el contrato; no es una selección entre las dos clases concretas.

## Flujo integrado, narrado

Sala A comienza a 22 °C/45 %, con temperatura como criterio. El usuario introduce 31 °C/45 %.

1. La consola llama `sensor.cambiar_mediciones(31, 45)`.
2. El sensor valida **ambos** valores antes de modificar nada y guarda el par nuevo.
3. `_notificar()` recorre una copia de la colección y llama `actualizar(...)` en Operador y Supervisor. Ambos ven 31/45: es Observer. No hay llamada manual de la consola a los observadores.
4. `_evaluar()` delega en **el objeto estrategia actual** mediante `evaluar(31,45)`: es Strategy. Devuelve `True` por 31 >30.
5. El sensor guarda resultado y estado `Alerta generada`, devuelve el booleano y la consola imprime `resumen()`.

Al seleccionar humedad sobre el **mismo** sensor, `cambiar_estrategia` reemplaza la referencia y reevalúa 31/45. Ahora `False`, por lo que vuelve a `Monitoreando`. No se notifica: cambió el criterio, no las mediciones. Después, humedad 75 genera alerta y 60 la elimina. El diagrama de secuencia representa el paso 2 de la demo; el de estados cubre todos estos recorridos.

## Patrones: explicación breve para entregar

**Observer (comportamiento)** desacopla al sujeto que cambia de quienes quieren enterarse. `Sensor` es el sujeto concreto; mantiene referencias a `Observador`, permite registro/remoción e invoca el contrato de forma automática al cambiar mediciones. `ObservadorConsola` es el observador concreto. Agregar un observador que guarde datos requeriría implementar esa ABC y registrarlo, sin modificar el bucle del sensor. No se implementó ese extra.

**Strategy (comportamiento)** encapsula criterios intercambiables. `Sensor` es el contexto; `EstrategiaEvaluacion`, la abstracción; temperatura y humedad, las estrategias concretas. El contexto delega en una referencia que puede reemplazarse durante ejecución, sin otra clase de sensor ni otro circuito de notificación. Un criterio adicional requiere implementar el contrato y permitir su selección en el punto de construcción, no reescribir el modelo.

**Diferencia:** Observer responde «¿a quién aviso que algo cambió?» (varios receptores); Strategy, «¿cómo evalúo estos datos?» (un criterio activo). Están integrados por una sola operación del mismo sensor, pero una estrategia no es un observador: primero se avisa, luego se evalúa. No se afirma que los observadores calculen el estado.

## Estados y contratos precisos

| Estado/evento | Efecto |
| --- | --- |
| Construir | Configurado; resultado `None`; estrategia ya seleccionada |
| Configurado + `cambiar_estrategia` | Sigue Configurado, sin evaluar ni notificar |
| Configurado + `iniciar` | Exige al menos dos observadores; evalúa inicial; Monitoreando si normal, Alerta generada si supera límite |
| Configurado + cambiar mediciones | Rechazo, sin cambios |
| Monitoreando/Alerta + cambio efectivo | Guarda, notifica, evalúa; queda Monitoreando/Alerta según resultado |
| Monitoreando/Alerta + cambiar estrategia | Reevalúa datos actuales; puede conservar o cambiar estado, sin avisos |
| Mismos valores | Devuelve último resultado; no notifica ni reevalúa |
| Repetir `iniciar` | Rechazo; no reinicia el ciclo |
| Registro/remoción de observador | No cambia medición, resultado ni estado |

`iniciar` asigna internamente Monitoreando antes de evaluar; el diagrama describe el **estado observable al retornar** (puede ser alerta desde el inicio). No hay apagado/estado final modelado ni reconocimiento manual de alertas: una alerta se elimina al reevaluar con resultado normal.

## Decisiones y límites

- Temperatura >30 °C y humedad >70 %, límites configurables por constructor de estrategia. El menú usa los valores por defecto, sin editor de umbrales. Son ejemplos, no normas ambientales.
- Nombres/ubicación/identificador no vacíos; números finitos, sin booleanos; humedad entre 0 y 100 inclusive; temperatura ≥−273.15 °C (cota física elegida), sin máximo arbitrario. La estrategia presupone mediciones válidas recibidas del sensor; no es una API independiente de validación.
- Los dos observadores son requisito **para iniciar** y están en toda la demo. Se permite desuscribirse luego, incluso quedarse sin observadores. El registro del mismo objeto no duplica avisos; dos objetos con igual identificador siguen siendo dos suscripciones. La consola no incluye remoción, sí la API y sus pruebas.
- Ejecución síncrona, en memoria. No hay concurrencia, persistencia, histórico, autenticación ni sensores reales. Salir pierde los datos. No se notifican la creación, el inicio ni una selección de criterio.
- Se asume que los observadores y estrategias cumplen su contrato y no lanzan errores. No se implementa aislamiento de fallos de plugins: una excepción de un observador externo podría interrumpir la evaluación después de guardar mediciones. Fuera del alcance, no una garantía de tolerancia a fallos.
- `Enum Estado` expresa estados; **no es el patrón State**. ABC impide instanciar contratos incompletos. No se usa herencia para fabricar variantes de Sensor.

## Matriz requisito → código → prueba → UML

Los nombres de pruebas se buscan en [`test_monitoreo.py`](../tests/test_monitoreo.py). `ModeloTests` concentra modelo; `CLITests` ejecuta la consola en subprocesos. La matriz traza evidencia, no una rúbrica inventada.

| Requisito original | Implementación | Prueba (`test_...`) | Diagrama |
| --- | --- | --- | --- |
| Registrar sensores y consultar datos | `Sensor.__init__`, `resumen`, menú 1/2 | `sensores_independientes`, `cli_registrar_cambiar_consultar_y_salir` | Clases: atributos de Sensor |
| Un sensor y dos observadores | `preparar_sensor`, dos `ObservadorConsola` | `dos_observadores_concretos`, `demo_no_interactiva` | Clases 0..*; secuencia O1/O2 |
| Registro/notificación automática | `registrar_observador`, `_notificar`, `cambiar_mediciones` | `notifica_dos_automaticamente_con_datos_actuales`, `registro_duplicado_no_duplica_aviso`, `remocion_y_ausente` | Clases y secuencia |
| Modificar temperatura y humedad | `cambiar_mediciones`, menú 3 | `transiciones_mediciones`, `cambio_estrategia_runtime_reevalua_sin_notificar` | Secuencia y estados |
| Dos estrategias seleccionables | Ambas evaluaciones, menú 4 | `estrategias_limites`, `criterios_independientes` | Clases: generalizaciones |
| Cambio de estrategia sin cambiar estructura | `cambiar_estrategia`, `_evaluar` | `cambio_estrategia_runtime_reevalua_sin_notificar`, `seleccion_en_configurado` | Clases y estados |
| Resultados visibles | `resumen`, consola | `demo_no_interactiva`, `cli_registrar_cambiar_consultar_y_salir` | Secuencia: resumen |
| Flujo usuario → guardar → notificar → evaluar | `cambiar_mediciones` | `orden_guardar_notificar_evaluar` | Secuencia |
| Tres estados y acciones de transición | `Estado`, `iniciar`, `_evaluar` | `configurado_sin_evaluacion`, `inicio_normal`, `inicio_en_alerta`, `transiciones_mediciones`, `cambio_estrategia_puede_generar_alerta` | Estados |
| Clases mínimas y relaciones | Seis clases requeridas + Enum | `interfaces_abstractas`, revisión documental | Clases |
| Aplicación sencilla e integración | `main.py --demo`, único modelo | Las 30 pruebas; demo extraída del ZIP | Los tres UML |
| Código + tres UML + explicación | Paquete y este documento | Auditoría de archivos/links y comparación UML manual, no una aprobación docente | SVG y fuentes Mermaid |

Extras de robustez: `entradas_invalidas_atomicas`, `extremos_validos`, `constructor_invalido`, `limites_invalidos`, `contratos_invalidos`, `cli_errores_recuperables`, `cli_eof_no_cuelga`. No se obtuvo porcentaje de cobertura de líneas; se verifican comportamientos específicos.
