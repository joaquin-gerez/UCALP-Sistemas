"""Trazados UML estáticos sin dependencias; no interpreta las fuentes Mermaid."""

from html import escape
from pathlib import Path


class SVG:
    def __init__(self, ancho, alto, titulo):
        self.partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" '
                       f'height="{alto}" viewBox="0 0 {ancho} {alto}" role="img">',
                       f'<title>{escape(titulo)}</title>',
                       '<defs><marker id="flecha" markerWidth="10" markerHeight="10" '
                       'refX="9" refY="5" orient="auto"><path d="M1,1 L9,5 L1,9" '
                       'fill="none" stroke="#18384c" stroke-width="1.5"/></marker>',
                       '<marker id="herencia" markerWidth="16" markerHeight="16" '
                       'refX="15" refY="8" orient="auto"><path d="M1,1 L15,8 L1,15 Z" '
                       'fill="white" stroke="#18384c"/></marker></defs>',
                       '<rect width="100%" height="100%" fill="white"/>']

    def texto(self, x, y, contenido, tam=20, centro=False, negrita=False):
        self.partes.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" '
                           f'font-size="{tam}" fill="#142f41" '
                           f'text-anchor="{"middle" if centro else "start"}" '
                           f'font-weight="{"bold" if negrita else "normal"}">'
                           f'{escape(contenido)}</text>')

    def caja(self, x, y, ancho, alto, titulo, lineas=()):
        self.partes.append(f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" '
                           'rx="8" fill="#f1f7fa" stroke="#18384c" stroke-width="2"/>')
        self.texto(x + ancho / 2, y + 30, titulo, 21, True, True)
        if lineas:
            self.partes.append(f'<path d="M{x},{y+43} H{x+ancho}" stroke="#18384c"/>')
        for indice, linea in enumerate(lineas):
            self.texto(x + 16, y + 70 + indice * 24, linea, 18)

    def linea(self, puntos, tipo="flecha", discontinua=False):
        marcador = f' marker-end="url(#{tipo})"' if tipo else ""
        guiones = ' stroke-dasharray="8 6"' if discontinua else ""
        self.partes.append(f'<path d="{puntos}" fill="none" stroke="#18384c" '
                           f'stroke-width="2"{marcador}{guiones}/>')

    def guardar(self, nombre):
        ruta = Path(__file__).parent / nombre
        ruta.write_text("\n".join(self.partes + ["</svg>"]), encoding="utf-8")


def clases():
    s = SVG(1500, 1140, "UML de clases — Grupo 11")
    s.texto(750, 32, "CLASES · estructura del modelo", 25, True, True)
    s.caja(440, 60, 600, 450, "Sensor", [
        "+ nombre: str; + ubicacion: str", "− _temperatura: float; − _humedad: float",
        "− _observadores: list; − _estrategia: EstrategiaEvaluacion",
        "− _estado: Estado; − _resultado: bool | None",
        "+ registrar_observador(observador)", "+ quitar_observador(observador)",
        "+ iniciar(): bool", "+ cambiar_mediciones(temperatura, humedad): bool",
        "+ cambiar_estrategia(estrategia): bool | None",
        "− _notificar(); − _evaluar(): bool", "+ resumen(): str"])
    s.caja(35, 70, 330, 160, "«enumeration» Estado", [
        "CONFIGURADO", "MONITOREANDO", "ALERTA"])
    s.linea("M440,160 H365")
    s.texto(372, 145, "estado", 16)
    s.caja(40, 610, 560, 135, "«abstract» Observador", [
        "+ actualizar(nombre, ubicacion,", "  temperatura, humedad) [abstracto]"])
    s.caja(790, 610, 550, 135, "«abstract» EstrategiaEvaluacion", [
        "+ evaluar(temperatura, humedad): bool [abstracto]",
        "+ describir(): str [abstracto]"])
    s.linea("M510,510 V555 H320 V610")
    s.texto(250, 550, "0..* Sensor", 17)
    s.texto(60, 590, "suscripciones → 0..* Observador", 18)
    s.linea("M970,510 V555 H1065 V610")
    s.texto(1080, 550, "0..* Sensor", 17)
    s.texto(1090, 590, "seleccionada → 1", 18)
    s.caja(40, 865, 560, 145, "ObservadorConsola", [
        "+ identificador: str", "+ actualizar(nombre, ubicacion,", "  temperatura, humedad)"])
    s.caja(680, 865, 375, 145, "EvaluacionTemperatura", [
        "+ limite: float = 30", "+ evaluar(t, h): bool", "+ describir(): str"])
    s.caja(1090, 865, 375, 145, "EvaluacionHumedad", [
        "+ limite: float = 70", "+ evaluar(t, h): bool", "+ describir(): str"])
    s.linea("M320,865 V745", "herencia")
    s.linea("M867,865 V800 H1000 V745", "herencia")
    s.linea("M1277,865 V800 H1130 V745", "herencia")
    s.texto(50, 1060, "+ público · − interno · triángulo vacío: herencia hacia ABC · flecha simple: asociación", 20)
    s.texto(50, 1095, "t/h abrevian temperatura/humedad. Propiedades de lectura y auxiliares omitidos. Inicio: exige 2 observadores.", 19)
    s.guardar("clases.svg")


def secuencia():
    s = SVG(1550, 1220, "UML de secuencia — modificar temperatura")
    s.texto(775, 32, "SECUENCIA · cambio de temperatura en Sala A", 25, True, True)
    nombres = [(100, "Usuario"), (330, "Consola"), (580, "Sensor Sala A"),
               (855, "Operador"), (1110, "Supervisor"), (1400, "Estrategia activa")]
    for x, nombre in nombres:
        if x == 100:
            s.caja(10, 65, 180, 75, nombre)
        else:
            s.caja(x - 110, 65, 220, 75, nombre)
        s.linea(f"M{x},140 V1100", tipo=None, discontinua=True)
        if x in (855, 1110):
            s.texto(x, 121, "ObservadorConsola", 16, True)
        elif x == 1400:
            s.texto(x, 121, "EvaluacionTemperatura", 16, True)
    s.texto(775, 175, "Precondición: 22 °C / 45 %, iniciado, dos observadores, criterio temperatura >30 °C", 20, True)

    def mensaje(a, b, y, texto, retorno=False):
        s.linea(f"M{a},{y} H{b}", discontinua=retorno)
        s.texto((a+b)/2, y-10, texto, 18, True)

    def propio(y, texto):
        s.linea(f"M580,{y} H630 V{y+32} H580")
        s.texto(650, y+18, texto, 18)

    mensaje(100, 330, 220, "Cambiar a 31 °C")
    mensaje(330, 580, 295, "cambiar_mediciones(31,45)")
    propio(340, "Validar y guardar 31 °C / 45 %")
    propio(400, "_notificar()")
    mensaje(580, 855, 480, "actualizar(nombre,ubicacion,31,45)")
    mensaje(580, 1110, 555, "actualizar(nombre,ubicacion,31,45)")
    s.texto(1050, 600, "Cada observador imprime el nuevo par de valores", 18, True)
    propio(645, "_evaluar()")
    mensaje(580, 1400, 725, "evaluar(31,45)")
    mensaje(1400, 580, 790, "True (31 >30)", True)
    propio(840, "Guardar resultado=True; estado=Alerta generada")
    mensaje(580, 330, 920, "True", True)
    mensaje(330, 580, 980, "resumen()")
    mensaje(580, 330, 1040, "datos, criterio, ALERTA, estado", True)
    mensaje(330, 100, 1100, "Mostrar resultado", True)
    s.texto(50, 1160, "Observer: dos llamadas actualizar. Strategy: delegación evaluar. El orden es guardar → avisar → evaluar.", 20)
    s.texto(50, 1195, "Retornos discontinuos. nombre/ubicacion = Sala A / Planta baja. La secuencia no notifica el resultado posterior.", 19)
    s.guardar("secuencia.svg")


def estados():
    s = SVG(1500, 1030, "UML de estados — ciclo del Sensor")
    s.texto(750, 32, "ESTADOS · un Sensor (estado observable al retornar)", 25, True, True)
    s.partes.append('<circle cx="750" cy="70" r="9" fill="#18384c"/>')
    s.linea("M750,79 V150")
    s.texto(440, 115, "construir / resultado=None", 19)
    s.caja(530, 150, 440, 70, "Configurado")
    s.linea("M970,185 H1300 V95 H920 V150")
    s.texto(1050, 135, "cambiar_estrategia", 19)
    s.texto(1050, 163, "/ seleccionar sin evaluar", 18)
    s.caja(120, 470, 450, 80, "Monitoreando")
    s.caja(930, 470, 450, 80, "Alerta generada")
    s.linea("M580,220 V300 H345 V470")
    s.texto(50, 345, "iniciar [2+ observadores", 19)
    s.texto(50, 375, "y evaluación normal]", 19)
    s.linea("M920,220 V300 H1155 V470")
    s.texto(850, 345, "iniciar [2+ observadores", 19)
    s.texto(850, 375, "y evaluación alerta]", 19)
    s.linea("M570,490 H930")
    s.texto(750, 453, "reevaluar [alerta]", 19, True)
    s.texto(750, 477, "/ resultado=True", 18, True)
    s.linea("M930,535 H570")
    s.texto(750, 570, "reevaluar [normal]", 19, True)
    s.texto(750, 596, "/ resultado=False", 18, True)
    s.linea("M120,510 H55 V660 H345 V550")
    s.texto(85, 700, "reevaluar [normal] / resultado=False", 18)
    s.linea("M1380,510 H1445 V660 H1155 V550")
    s.texto(1020, 700, "reevaluar [alerta] / resultado=True", 18)
    s.texto(60, 770, "«reevaluar» abrevia dos eventos públicos (no es un método adicional):", 22, negrita=True)
    for i, linea in enumerate([
        "• cambiar_mediciones [par diferente] / validar → guardar → notificar → _evaluar",
        "• cambiar_estrategia / seleccionar → _evaluar (sin avisos de medición)",
        "Mismos datos: mismo estado, no notifica ni evalúa. Registrar/remover observadores: no cambia estado.",
        "Rechazos sin transición: iniciar con menos de dos; cambiar datos en Configurado; volver a iniciar.",
        "No hay estado final ni botón de reconocimiento: se vuelve a Monitoreando con una evaluación normal.",
        "Normal = False; alerta = True. iniciar evalúa la medición inicial (paso interno por Monitoreando omitido)."]):
        s.texto(60, 815 + i*33, linea, 20)
    s.guardar("estados.svg")


if __name__ == "__main__":
    clases()
    secuencia()
    estados()
