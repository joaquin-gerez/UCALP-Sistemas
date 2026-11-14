# Grupo 11 — Monitoreo ambiental

**Borrador implementado y verificado localmente el 12/11/2026. Revisión humana, estudio, adaptación conjunta y entrega pendientes.** No acredita aprobación ni envío.

Integrantes asignados: **Joaquín Gerez — Observer; Facundo Gómez — Strategy**. Código y documentación preparados con asistencia de IA: el reparto que sigue es para comprender, revisar y adaptar; no afirma que los integrantes ya hayan escrito o defendido estas partes.

## Ejecutar en dos minutos

Solo biblioteca estándar; sin instalar paquetes ni conexión a Internet. Verificado realmente con **Python 3.14.7 en Linux**. Se usa sintaxis compatible con Python 3.10+, pero otras versiones/plataformas no fueron ejecutadas. En Windows puede usarse `py -3` en lugar de `python3` si está instalado.

Abrir una terminal **dentro de la carpeta `Grupo11_Monitoreo`** (también después de extraer el ZIP):

```sh
python3 --version
python3 -B main.py --demo
python3 -B main.py
python3 -B -m unittest discover -s tests -v
```

`--demo` no pide datos y termina. Sin esa opción aparece el menú: registrar uno o más sensores, consultar todos, modificar ambas mediciones, seleccionar estrategia o agregar observadores. Se crean **dos objetos distintos `ObservadorConsola`**, Operador y Supervisor, por cada sensor; ambos muestran los cambios para sus respectivos destinatarios (no hay archivo de registro ni observador de alertas ficticio). La opción 5 permite agregar más. `0` sale; EOF/Ctrl+C también termina sin bucle.

Ejemplo manual: opción `1`, nombre `Sala A`, ubicación `Planta baja`, temperatura `22`, humedad `45`; opción `3`, `Sala A`, `31`, `45`; opción `4`, `Sala A`, `2`; opción `3`, `Sala A`, `31`, `75`. Consultar con `2` y salir con `0`. Se aceptan decimales con punto o coma en la consola.

## Qué incluye

- [`monitoreo.py`](monitoreo.py): modelo, contratos Observer/Strategy y estados.
- [`main.py`](main.py): consola y demostración reproducible.
- [`tests/test_monitoreo.py`](tests/test_monitoreo.py): 30 pruebas automatizadas, incluidas cuatro de procesos CLI.
- [Arquitectura, patrones, decisiones y matriz de requisitos](docs/TECNICO.md).
- [Guía sencilla de estudio y defensa para ambos integrantes](docs/GUIA_ESTUDIO.md).
- [Diagramas UML y su lectura](diagramas/README.md): fuentes Mermaid y SVG estáticos, sin servicios externos.
- [Consigna original completa, tres páginas](consigna/TIF-OO2-G11.pdf) y [texto de consulta](consigna/TIF-OO2-G11.txt).
- [Verificación local real](docs/VERIFICACION.md) y [checklist de preparación de entrega](docs/ENTREGA.md).

## Resultado esperado de la demo

| Paso | Valores | Estrategia | Resultado / estado | Avisos |
| --- | --- | --- | --- | --- |
| 1 Registrar e iniciar | 22 °C / 45 % | temperatura >30 °C | Normal / Monitoreando | 0 |
| 2 Modificar temperatura | 31 °C / 45 % | temperatura >30 °C | ALERTA / Alerta generada | 2 |
| 3 Cambiar estrategia | 31 °C / 45 % | humedad >70 % | Normal / Monitoreando | 0 |
| 4 Modificar humedad | 31 °C / 75 % | humedad >70 % | ALERTA / Alerta generada | 2 |
| 5 Modificar humedad | 31 °C / 60 % | humedad >70 % | Normal / Monitoreando | 2 |

Los umbrales **30 °C y 70 %**, el comparador estricto `>` y las validaciones son **decisiones de implementación, no exigencias numéricas del docente**. A 30 °C o 70 % exactos no hay alerta. No es un instrumento de seguridad ambiental ni usa sensores físicos.

## Consigna y fechas: no confundir

El original pide registrar sensores con nombre, ubicación, temperatura/humedad; dos observadores, notificación automática, dos estrategias intercambiables y resultados; código, UML de clases/secuencia/estados y explicación breve de patrones integrados. Permite consola; no impone lenguaje ni framework.

**Defensa prevista: 17/11/2026**, según planilla leída el 08/11; el 12/11 la planilla exigía acceso y no pudo revalidarse. Hora/modalidad por confirmar. **Fecha/hora/zona, canal, formato y responsable de ENTREGA: no verificados.** El 27/11 de Builder es otro TP, ya enviado; no es el vencimiento de este integrador. Confirmar también si hay un oral adicional/final posterior.

Fuente primaria: [PDF del docente en Drive](https://drive.google.com/file/d/1mR7vjdqdwZUOtO3XgYiMJLV_qCDaGAPS/view), mensaje del 03/11. [Campus OOII](https://campus.ucalp.edu.ar/course/view.php?id=2930), [recurso de requisitos generales](https://campus.ucalp.edu.ar/mod/url/view.php?id=103453), [planilla](https://docs.google.com/spreadsheets/d/15ChGERAd6K0q5hxfKnGClzGaSH45R7gCqvk-7I0q7UU/edit). Los enlaces pueden exigir cuenta/permisos; la copia de la consigna es autocontenida para preparación privada. No se incluyen datos de sesiones ni otros documentos personales.
