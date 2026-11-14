"""Verifica sintaxis, enlaces locales y presencia de los PDF."""

import ast
import re
from pathlib import Path
from urllib.parse import unquote


def main():
    raiz = Path(__file__).resolve().parents[1]
    for archivo in raiz.rglob("*.py"):
        ast.parse(archivo.read_text(encoding="utf-8"), filename=str(archivo))
    enlaces = 0
    for archivo in raiz.rglob("*.md"):
        for destino in re.findall(r"\]\(([^)]+)\)", archivo.read_text(encoding="utf-8")):
            if destino.startswith(("https://", "http://", "#")):
                continue
            objetivo = (archivo.parent / unquote(destino.split("#", 1)[0])).resolve()
            assert objetivo.is_relative_to(raiz) and objetivo.exists(), (archivo, destino)
            enlaces += 1
    for nombre in ("clases", "secuencia", "estados"):
        assert (raiz / f"diagramas/{nombre}.pdf").read_bytes().startswith(b"%PDF-")
    print(f"OK: sintaxis Python, {enlaces} enlaces locales y 3 diagramas PDF.")


if __name__ == "__main__":
    main()
