"""Auditoría estándar: sintaxis, enlaces locales, SVG y nombres UML principales.

No reemplaza las pruebas de comportamiento ni la revisión visual de diagramas.
"""

import ast
import re
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET


def main():
    raiz = Path(__file__).resolve().parents[1]
    archivos = [p for p in raiz.rglob("*") if p.is_file()]
    for archivo in archivos:
        assert not archivo.is_symlink(), f"Enlace simbólico no esperado: {archivo}"
        assert not any(parte.startswith(".") or parte == "__pycache__"
                       for parte in archivo.relative_to(raiz).parts), archivo
        assert archivo.suffix in (".py", ".md", ".mmd", ".svg", ".pdf", ".txt"), archivo
    python = list(raiz.rglob("*.py"))
    for archivo in python:
        contenido = archivo.read_text(encoding="utf-8")
        ast.parse(contenido, filename=str(archivo))
        compile(contenido, str(archivo), "exec")
    enlaces = 0
    for archivo in raiz.rglob("*.md"):
        for destino in re.findall(r"\]\(([^)]+)\)", archivo.read_text(encoding="utf-8")):
            if destino.startswith(("https://", "http://", "#")):
                continue
            relativo = unquote(destino.split("#", 1)[0])
            objetivo = (archivo.parent / relativo).resolve()
            assert objetivo.is_relative_to(raiz) and objetivo.exists(), (archivo, destino)
            enlaces += 1
    for archivo in raiz.glob("diagramas/*.svg"):
        arbol = ET.parse(archivo)
        assert arbol.getroot().tag.endswith("svg"), archivo
        for nodo in arbol.iter():
            assert not nodo.tag.endswith("script"), archivo
            assert not any("href" in atributo for atributo in nodo.attrib), archivo
    modelo = ast.parse((raiz / "monitoreo.py").read_text(encoding="utf-8"))
    clases = {n.name for n in modelo.body if isinstance(n, ast.ClassDef)}
    fuente = (raiz / "diagramas/clases.mmd").read_text(encoding="utf-8")
    visual = (raiz / "diagramas/clases.svg").read_text(encoding="utf-8")
    for clase in clases:
        assert f"class {clase}" in fuente and clase in visual, clase
    for nombre in ("clases", "secuencia", "estados"):
        pdf = raiz / f"diagramas/{nombre}.pdf"
        assert pdf.read_bytes().startswith(b"%PDF-"), pdf
    print(f"OK: {len(python)} archivos Python compilan; {enlaces} enlaces locales existen;")
    print(f"{len(clases)} clases del modelo presentes en UML; 3 SVG XML válidos sin recursos externos;")
    print(f"3 PDF presentes; {len(archivos)} archivos con extensiones permitidas y sin basura oculta.")
    print("Limitación: no valida enlaces remotos ni compila Mermaid; UML requiere revisión humana.")


if __name__ == "__main__":
    main()
