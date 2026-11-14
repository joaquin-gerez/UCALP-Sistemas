# Entender y defender — Joaquín y Facundo

Material de preparación asistida: **leerlo no demuestra aprendizaje**. Cada uno debe ejecutar, modificar y explicar con sus propias palabras. Antes de entregar, revisar juntos que esto represente lo que comprenden y acordar la autoría/asistencia según reglas de la cátedra.

## Árbol del recorrido

1. Objetos del caso: sensor, mediciones y destinatarios.
2. Observer: contrato → suscripción → aviso automático.
3. Strategy: contrato → dos criterios → reemplazo en ejecución.
4. Integración: guardar → avisar → evaluar → estado.
5. UML: estructura (clases), interacción (secuencia), vida del sensor (estados).
6. Ensayo: demo, preguntas y pequeños cambios explicados.

## Bloque 0 — Vocabulario con el mismo ejemplo

| Término | Qué significa aquí |
| --- | --- |
| Clase | Definición de datos y operaciones de un tipo; `Sensor` describe sensores |
| Objeto / instancia | Un ejemplar concreto: `sensor = Sensor(...)` representa Sala A |
| Atributo | Dato de un objeto; `nombre`, `_humedad`, `_estrategia` |
| Método | Operación del objeto; `cambiar_mediciones(...)` modifica y coordina |
| Interfaz / contrato | Operaciones que un colaborador promete ofrecer; todos los observadores tienen `actualizar` |
| ABC | Clase base abstracta de Python: expresa el contrato y no puede instanciarse si faltan métodos abstractos. No es una interfaz Java literal |
| Herencia | Una clase especializa otra; `ObservadorConsola(Observador)` implementa su contrato |
| Composición de comportamiento | Sensor **tiene una referencia a** una estrategia y delega; no **es una** estrategia. En UML dibujamos asociación, no rombo negro, porque no se impone propiedad exclusiva de su ciclo de vida |
| Encapsulación | Cambiar las mediciones por un método que valida y notifica, no editar sus campos directamente |
| Polimorfismo | `evaluar(t,h)` funciona sobre cualquier estrategia que respete la ABC sin preguntar cuál es |
| Notificación | Llamada automática del sujeto al método de un receptor suscrito; no significa email/red |
| Estrategia | Objeto que encapsula una manera de evaluar: temperatura o humedad |
| Estado | Situación actual del sensor: Configurado, Monitoreando o Alerta generada |
| UML | Lenguaje visual de modelado; no es código ejecutable. Cada diagrama responde una pregunta distinta |
| Umbral | Límite para comparar; aquí 30 °C/70 % son elecciones didácticas, no valores exigidos |

**Control oral:** señalar una clase y dos objetos de esa misma clase. Respuesta: `ObservadorConsola` y sus instancias Operador/Supervisor. Tener dos instancias no exige dos definiciones de clase.

## Bloque 1 — Observer (foco Joaquín)

Imaginemos que Sala A tiene dos personas mirando el tablero. Si la consola tuviera que llamar a cada una a mano tras cada modificación, olvidar una llamada dejaría información vieja. Por eso **el sensor** centraliza la colección y se encarga de avisar después de guardar las mediciones. El emisor conoce el contrato, no necesita saber cómo presenta la información cada receptor.

Abrir `monitoreo.py`: leer `Observador`, `ObservadorConsola`, `registrar_observador`, `quitar_observador`, `_notificar` y su llamada en `cambiar_mediciones`. Abrir el test `test_notifica_dos_automaticamente_con_datos_actuales`: verifica las dos listas de avisos, no solo que se imprimió algo.

**Experimento:** desde menú 5 agregar «Visita» y cambiar mediciones. Ahora hay tres líneas, sin editar Sensor. Explicar por qué un cambio idéntico no imprime nada y por qué eliminar una suscripción en la API solo afecta a esa instancia.

Esencial: sujeto, colección, contrato, receptores y disparador automático. **Guion oral:** «El sensor guarda el cambio y llama `actualizar` en cada observador registrado. Operador y Supervisor son objetos diferentes. No tienen que consultar repetidamente ni la consola avisarles a mano».

## Bloque 2 — Strategy (foco Facundo)

31 °C/45 % puede ser anormal si importa temperatura y normal si importa humedad. No cambió el ambiente: cambió **la pregunta**. En vez de crear `SensorTemperatura` y `SensorHumedad`, mantenemos un sensor y le pasamos un objeto que responde esa pregunta con la misma firma.

Leer `EstrategiaEvaluacion`, ambas evaluaciones y `cambiar_estrategia`. Después seguir `_evaluar`: solo aparece `self._estrategia.evaluar(...)`, no una lista de `if` de criterios concretos. El `if` del menú sirve para construir la selección del usuario; no vuelve al modelo dependiente del criterio elegido.

**Experimento:** ejecutar demo y detenerse mentalmente entre pasos 2 y 3. Predecir qué pasa al elegir humedad: los valores siguen 31/45, el resultado pasa a normal, no hay nuevos avisos. Revisar el test de reemplazo en ejecución. Luego cambiar temporalmente el límite a 25 en una copia y predecir el resultado a 26 °C.

Esencial: contexto, contrato, alternativas y delegación. **Guion oral:** «Sensor es el contexto. Se intercambia el objeto que evalúa, no la clase del sensor. Temperatura y humedad cumplen el mismo contrato; `True` significa alerta».

## Bloque 3 — Integración y estados (ambos)

Observer no determina si 31 °C es peligroso: reparte datos. Strategy no avisa a dos personas: decide un resultado. `cambiar_mediciones` une ambas responsabilidades en orden: **validar y guardar → notificar → evaluar → actualizar estado**. Por eso los observadores reciben mediciones y no el nuevo resultado. `resumen()` se imprime después, cuando sí existe el resultado actualizado.

Leer el Enum y ejecutar la demo. Dibujar una línea con estados: Configurado al construir, Monitoreando al iniciar normal, Alerta al poner 31, Monitoreando al elegir humedad, Alerta al poner 75 %, Monitoreando al volver a 60 %. Si los datos iniciales ya exceden el criterio, iniciar termina en Alerta; también se prueba. No hay que implementar State: se modelan estados del objeto, no necesariamente ese patrón de diseño.

**Ejercicio sin computadora:** con humedad seleccionada, temperatura 40 y humedad 70 exacta, ¿alerta? No: se evalúa solo humedad y `70 >70` es falso. Con 71 sí. Si escribir humedad 150, se rechaza todo el cambio: ni siquiera se guarda la nueva temperatura.

**Guion oral conjunto:** «El estado expresa el resultado de la estrategia actual. No se elimina una alerta pulsando aceptar: se elimina al obtener una evaluación normal, sea por datos nuevos o por cambiar el criterio».

## Bloque 4 — Leer y defender los tres UML

Abrir [los diagramas](../diagramas/README.md) y sus SVG; se pueden ver en navegador sin Internet.

- **Clases** = foto de la estructura: rectángulos con nombre, atributos y métodos. Una flecha con triángulo vacío apunta a la abstracción heredada. La asociación Sensor–Observador tiene `0..*` porque se configura/remueve; el inicio requiere dos por regla del método. La de estrategia tiene `1`: siempre hay un criterio seleccionado. No representa el orden temporal.
- **Secuencia** = película de una operación: participantes arriba, líneas de vida hacia abajo y mensajes ordenados de arriba a abajo. Líneas discontinuas son retornos; el autoenvío expresa una operación interna. Seguir desde usuario que cambia temperatura hasta `resumen`; identificar exactamente dónde aparecen los dos patrones. Es un caso representativo con dos observadores, no limita el máximo.
- **Estados** = mapa de situaciones de **un sensor**: nodo inicial y transiciones con `evento [condición] / acción`. Una flecha a sí mismo significa que hubo una operación pero no cambió el estado. Un cambio de estrategia puede producir los mismos cuatro caminos que un cambio de medición; lo que difiere es que no notifica. No mezcla estados de la aplicación y del sensor.

**Prueba de comprensión:** tapar el código y explicar por qué no corresponde dibujar la estrategia como subclase de Sensor, ni los observadores recibiendo una alerta calculada antes de `_evaluar`.

## Reparto para revisar/adaptar y preparar defensa

| Persona | Recorrido principal | Debe poder mostrar |
| --- | --- | --- |
| Joaquín | Observer, registro/remoción, colección y aviso | Dos receptores automáticos, tercero sin tocar Sensor, tests de notificación |
| Facundo | Strategy, umbrales, resultado y reemplazo | Dos criterios en mismo sensor, comparador, reevaluación sin aviso |
| Ambos | Releer consigna, ajustar juntos código/UML, consola, estados y documentación | Demo completa, pruebas, decisiones, límites y entrega correcta |

No separar el proyecto en dos demos. No memorizar únicamente la parte propia: la defensa debe explicar **el enlace** entre las dos.

## Preguntas y respuestas para el oral

1. **¿Quién es el sujeto observado?** El Sensor; conserva observadores y emite avisos ante cambios efectivos.
2. **¿Cuáles son los dos observadores?** Operador y Supervisor, instancias distintas de ObservadorConsola. No son dos estrategias.
3. **¿Para qué la ABC?** Expresa operaciones comunes y obliga a implementarlas; el sensor usa ese contrato.
4. **¿Qué modifica un cambio de estrategia?** La referencia `_estrategia`; se reevalúan datos actuales y puede cambiar el estado. No se reconstruye el sensor.
5. **¿Por qué ambos patrones son de comportamiento?** Organizan colaboración/notificación y selección de algoritmos, no creación de objetos ni adaptación de estructuras.
6. **¿Dónde están integrados?** En `cambiar_mediciones`, que primero notifica y luego delega la evaluación dentro del mismo Sensor.
7. **¿Puedo agregar otra estrategia?** Sí, otra clase que implemente `evaluar` y `describir`; se selecciona al construir o con `cambiar_estrategia`. Si se quiere en el menú, se agrega su opción allí.
8. **¿Se avisa solo si hay alerta?** No: por cada cambio efectivo, sea normal o alerta. No se avisa si los dos valores son idénticos.
9. **¿Por qué 30 y 70?** Decisiones de ejemplo documentadas; el original no fija números. Se usa `>`; en igualdad es normal.
10. **¿Cómo vuelve desde alerta?** Una evaluación normal, causada por nuevos datos o una estrategia diferente. No hay botón de reconocimiento.
11. **¿Por qué 0..* observadores si se piden dos?** La colección puede estar vacía al configurar o tras desuscripciones. `iniciar` exige al menos dos y la demo siempre mantiene dos.
12. **¿Se pueden iniciar datos ya anormales?** Sí: iniciar los evalúa y termina en Alerta generada, sin avisar un cambio que no ocurrió.
13. **¿Qué pasa con un dato inválido?** ValueError, mensaje en consola y ningún cambio parcial; humedad 101 no es aceptada.
14. **¿Tiene límites?** Datos solo en memoria; síncrono; sin tolerancia a errores de observadores externos. No es monitoreo industrial real.
15. **¿Qué diferencia clase, secuencia y estados?** Estructura de tipos, orden de llamadas de un caso y evolución de un objeto, respectivamente.
16. **¿Cómo saben que funciona?** 30 pruebas reales y demo, también tras extraer el ZIP; no equivalen a certificación ni calificación docente.
17. **¿Quién escribió esto?** Borrador preparado con asistencia de IA; cada integrante debe revisar/adaptar y poder explicar lo que finalmente presente. No inventar una historia de implementación propia.

## Sesión de estudio concreta (70–90 minutos, ajustable)

1. **10 min juntos:** leer original de tres páginas, marcar requisitos y comparar la matriz.
2. **10 min:** ejecutar demo y predecir cada siguiente estado antes de leerlo.
3. **15 min Joaquín / 15 min Facundo:** seguir el bloque propio y explicárselo al otro señalando código real.
4. **15 min juntos:** recorrer los tres SVG y señalar la línea de código de cada flecha relevante.
5. **10 min:** ejecutar pruebas, elegir dos tests y explicar qué error detectarían. Alterar un umbral en una **copia** para ver un fallo esperado; restaurar la copia, no el trabajo ajeno.
6. **10 min:** ensayo sin apuntes: caso, patrones, integración, estados y decisiones. Volver a lo que no se pudo justificar.

**Guion de demo de 5 minutos:** 30 s contexto; 1 min Joaquín Observer; 1 min Facundo Strategy; 1 min demo de ambas alertas y retorno; 1 min tres UML; 30 s tests y límites. El lunes 16/11 puede usarse para ensayo, como plan propio, no plazo docente.

**Criterio de preparación:** cada uno puede predecir resultados nuevos, localizar métodos y justificar flechas sin leer de corrido. Si solo pueden repetir definiciones, falta estudio aunque el ZIP funcione.
