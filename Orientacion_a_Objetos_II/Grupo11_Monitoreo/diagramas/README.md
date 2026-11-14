# UML — fuentes y visuales autocontenidos

| Pregunta | Fuente editable | Visual estático | PDF imprimible |
| --- | --- | --- | --- |
| ¿Qué clases hay y cómo colaboran? | [clases.mmd](clases.mmd) | [clases.svg](clases.svg) | [clases.pdf](clases.pdf) |
| ¿Qué ocurre cuando cambia la temperatura? | [secuencia.mmd](secuencia.mmd) | [secuencia.svg](secuencia.svg) | [secuencia.pdf](secuencia.pdf) |
| ¿Cómo evoluciona el sensor? | [estados.mmd](estados.mmd) | [estados.svg](estados.svg) | [estados.pdf](estados.pdf) |

Abrir los SVG en cualquier navegador; contienen solo formas/texto, sin scripts, red, fuentes remotas ni imágenes externas. Se pueden ampliar e imprimir desde el navegador. Los `.mmd` son Mermaid, no requieren ejecutarse para estudiar los visuales. No se subió el repositorio a servicios de diagramado.

**Clases:** `+` público y `-` interno; triángulo vacío = herencia hacia la ABC. Flechas simples = asociaciones navegables. `0..*` junto a Observador permite registrar/remover; el método `iniciar` exige dos. Un observador puede suscribirse a varios sensores; una estrategia puede compartirse entre varios sensores; por eso ambos extremos del lado Sensor son `0..*`, no propiedad exclusiva. Cada sensor tiene exactamente una estrategia (`1`). `Estado` es un Enum. Se omiten constructores, getters, validadores auxiliares y consola para mantener foco en clases principales; propiedades de lectura exponen temperatura, humedad, estado, resultado y estrategia.

**Secuencia:** lectura de arriba abajo; seis participantes y llamadas del caso real de la demo paso 2. Retornos discontinuos y autoenvíos para operaciones internas. Dos objetos de la misma clase no se dibujan como una sola línea de vida. Las impresiones de cada observador se indican en nota para evitar dos participantes de salida adicionales. `resumen()` es una llamada posterior de consola; no calcula de nuevo ni notifica.

**Estados:** flechas con evento/condición; `[normal]` significa resultado `False`, `[alerta]` resultado `True`. «reevaluar» es una **abreviatura gráfica**, no un método público adicional: representa el final de `cambiar_mediciones` efectivo o `cambiar_estrategia`, mediante `_evaluar`. Los efectos anteriores difieren y están aclarados. La transición desde Configurado refleja el estado al terminar `iniciar`; internamente se pasa por Monitoreando antes de evaluar la medición inicial. No se introduce un estado final inexistente.

Los SVG son trazados estáticos equivalentes, generados por [render_svg.py](render_svg.py), **no salida de un compilador Mermaid** (no había uno instalado). Las fuentes Mermaid se revisaron por lectura, no se afirma validación con `mmdc`. El generador usa solo Python estándar y coordenadas explícitas para mantener legibilidad sin descargar herramientas:

```sh
python3 -B diagramas/render_svg.py
```

También se incluyen PDF de una página por diagrama, convertidos localmente con `rsvg-convert` ya instalado (herramienta opcional de preparación, **no necesaria para ejecutar el proyecto**). Si está disponible, regenerar cada PDF después de cambiar el SVG, por ejemplo: `rsvg-convert -f pdf -o diagramas/clases.pdf diagramas/clases.svg`.

Si cambia el modelo, actualizar **ambas representaciones** y revisar que mensajes, clases, multiplicidades y transiciones coincidan. Las dos fuentes no se sincronizan automáticamente. Los tests verifican el comportamiento del modelo; la concordancia UML requiere también revisión humana.
