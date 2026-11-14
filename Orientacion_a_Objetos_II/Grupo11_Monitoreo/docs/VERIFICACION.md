# Verificación — 12/11/2026

Estado: borrador implementado/verificado localmente, pendiente revisión humana y entrega. No acredita aprobación ni cobertura exhaustiva.

## Entorno y ejecución

- Linux, **Python 3.14.7**, solo biblioteca estándar para aplicación, pruebas y auditoría.
- Original local de tres páginas leído íntegro, tanto PDF como texto; contrastado con ficha y evidencia de solo lectura del 12/11. No fue necesario volver al navegador ni contactar a nadie.
- Primera ejecución real del modelo y CLI: **30 tests, todos OK**; demo terminada mostrando seis avisos (tres por destinatario), ambas alertas y retorno a normal.
- SVG renderizados con Python estándar; revisados visualmente como PNG temporales. Se corrigieron recorte de cabecera y líneas que cruzaban etiquetas. PDF generados con `rsvg-convert` local, sin instalar paquetes ni servicios externos.
- Comparación manual código/UML: seis clases requeridas + Enum, dos objetos observadores, estrategia única reemplazable, orden guardar→notificar→evaluar, inicio normal o alerta, bucles/retorno por evaluación y ausencia de avisos al seleccionar criterio.

## Comandos reproducibles (desde la raíz del proyecto)

```sh
python3 --version
python3 -B -m unittest discover -s tests -v
python3 -B main.py --demo
python3 -B tools/verificar.py
```

La auditoría verifica sintaxis por AST y compilación en memoria (no genera cachés), enlaces Markdown locales, XML SVG sin scripts/referencias externas, nombres de clases principales y presencia de PDF. No comprueba enlaces remotos ni compila Mermaid; no equivale a validación semántica completa de UML.

## Verificación del paquete extraído

**Resultado real: 30/30 tests OK también desde una extracción nueva en `/tmp/opencode`, demo terminada y auditoría OK**, con las tres órdenes anteriores. Se contrastaron todos los archivos extraídos byte por byte con el proyecto y se comprobó CRC con `ZipFile.testzip()`; sin rutas absolutas ni `..` dentro del ZIP.

Ver transcripción real local y de la extracción candidata en [RESULTADOS.txt](RESULTADOS.txt). Después de incorporar ese registro se reconstruyó el ZIP final y se repitieron tests, demo y auditoría desde otra extracción limpia, sin alterar el contenido del paquete durante esa última ejecución. Los registros de esa última repetición quedan fuera del ZIP, en el temporal de verificación, para no crear un ciclo de «modificar reporte/reempaquetar».

Auditoría: **23 archivos**, cinco Python compilados en memoria, **23 enlaces locales existentes**, siete clases del modelo presentes en fuente/visual UML, tres SVG válidos sin referencias externas y tres PDF de diagramas. Se revisaron visualmente los tres diagramas. Se admite que Mermaid no se compiló con una herramienta externa; fuentes revisadas por lectura.

El ZIP conserva una carpeta raíz `Grupo11_Monitoreo/`, con solo código, tests, docs, UML y la consigna del grupo. Sin `.env`, secretos, cachés, repositorio Git ni documentos ajenos. La copia PDF del original es idéntica al archivo local (154227 bytes; SHA-256 `2e64ab699d0e990617d4a652efc587b66b054b10f35413fa44834da629cfa4c0`); también se verificó igualdad binaria del texto de consulta. Esto no afirma identidad binaria con versiones remotas posteriores.

## Alcance y límites de las pruebas

26 pruebas del modelo + 4 de CLI en subprocesos con timeout de 5 segundos. Cubren normal/alerta y límites, dos receptores, registro/remoción, reemplazo runtime, orden de llamadas, estados, errores atómicos, contratos, demo y consola (incluido EOF). Cada `subTest` adicional no se cuenta como un test separado. No se midió porcentaje de cobertura; no hay ensayos industriales, multihilo ni tolerancia a plugins que fallen.

No se hizo commit/push, cambio de rama, envío al Campus, solicitud de acceso ni mensaje al docente. El reporte describe verificación local, **no entrega**. Si se modifica el proyecto, repetir pruebas y reconstruir ZIP antes de usarlo.
