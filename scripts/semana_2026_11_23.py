"""Imágenes de Instagram para la semana del 23 al 29 de noviembre de 2026."""
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

from estilo import *  # noqa: F401,F403

SALIDA = RAIZ / "publicaciones" / "2026-11-23_semana"
R = RECURSOS
N = RECURSOS / "novedades"


# ------------------------------------------------ lunes 23: Makt myrkranna (CONSULTA)
def makt_anuncio():
    img = lienzo(brillo_verde=(0.5, 0.5), intensidad=0.6, semilla=61)
    fondo = sepia_grabado(R / "drac_huesped.png", (0, 0, 1024, 1536), (W, H), oscuro=(0, 0, 0), claro=(150, 120, 80))
    fondo.putalpha(26)
    img.alpha_composite(fondo)
    marco(img)
    rotulo(img, (W / 2, 118), "Novedad  ·  Límite Abisal  ·  Vol. XIX", 22)
    texto_dorado(img, (W / 2, 205), "Creías conocer Drácula", fuente("titulo", 78))
    separador(img, W / 2, 268)
    portada(img, N / "makt-myrkranna_portada.jpg", (W / 2, 662), 690)
    parrafo(img, W / 2, 1045, "En Islandia lo leyeron de otra manera.", fuente("cursiva", 44), color=DORADO_CLARO)
    rotulo(img, (W / 2, 1150), "Makt myrkranna  ·  Los poderes de la oscuridad", 21, color=CREMA, espaciado=3)
    logo_pie(img, y=1262, ancho=210)
    return img


# ------------------------------------------------ martes 24: El Horla (HABITUAL)
def horla():
    img = lienzo(brillo_verde=(0.5, 0.42), intensidad=0.7, semilla=62)
    marco(img)
    rotulo(img, (W / 2, 118), "Colección Cámara Sellada", 24)
    portada(img, R / "horla.jpg", (W / 2, 560), 760)
    texto_dorado(img, (W / 2, 1010), "Guy de Maupassant", fuente("titulo", 70))
    parrafo(img, W / 2, 1060, "Un diario. Un velero brasileño que pasa de largo.\nY alguien en la habitación que nadie ve.",
            fuente("cursiva", 36), ancho_max=860)
    logo_pie(img, y=1262, ancho=210)
    return img


# ------------------------------------------------ miércoles 25: El peligro azul (CONSULTA)
def peligro_azul():
    img = lienzo(brillo_verde=(0.5, 0.5), intensidad=0.55, semilla=63)
    marco(img)
    rotulo(img, (W / 2, 118), "Límite Abisal  ·  Vol. XX  ·  Próximamente", 22)
    texto_dorado(img, (W / 2, 205), "Tres rastros suben.", fuente("titulo", 80))
    texto_dorado(img, (W / 2, 300), "Ninguno baja", fuente("titulo", 80))
    separador(img, W / 2, 368)
    # croquis de 1911 en papel sepia, como lámina
    cro = Image.open(N / "el-peligro-azul_croquis_1911.png").convert("L")
    cro = ImageOps.autocontrast(cro, cutoff=1)
    lw = 880
    cro = cro.resize((lw, int(cro.height * lw / cro.width)), Image.LANCZOS)
    a = np.asarray(cro).astype(np.float32) / 255
    tinta, papel = np.array((52, 36, 20), np.float32), np.array((226, 211, 178), np.float32)
    rgb = tinta + (papel - tinta) * a[..., None]
    rng = np.random.default_rng(5)
    rgb += rng.normal(0, 3, rgb.shape[:2])[..., None]
    lam = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    x, y = (W - lw) // 2, 410
    sombra = Image.new("RGBA", (lw + 80, lam.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle([40, 54, lw + 40, lam.height + 54], fill=(0, 0, 0, 210))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40))
    img.alpha_composite(lam, (x, y))
    d = ImageDraw.Draw(img)
    d.rectangle([x - 1, y - 1, x + lw, y + lam.height], outline=DORADO + (220,), width=2)
    yb = y + lam.height
    parrafo(img, W / 2, yb + 34, "Croquis de la edición de 1911", fuente("cursiva", 30), color=DORADO_CLARO)
    parrafo(img, W / 2, yb + 96, "El peligro azul  ·  Maurice Renard", fuente("texto_bold", 40), color=CREMA)
    logo_pie(img, y=1262, ancho=210)
    return img


# ------------------------------------------------ jueves 26: Drácula vs. Makt (CONSULTA)
def makt_comparativa():
    img = lienzo(brillo_verde=(0.5, 0.55), intensidad=0.55, semilla=64)
    marco(img)
    rotulo(img, (W / 2, 118), "Límite Abisal  ·  Vol. XIX", 22)
    texto_dorado(img, (W / 2, 200), "Dos novelas, un conde", fuente("titulo", 80))
    separador(img, W / 2, 262)
    xi, xd = 300, 780
    rotulo(img, (xi, 318), "Drácula", 30, color=DORADO, espaciado=4)
    rotulo(img, (xd, 318), "Makt myrkranna", 30, color=DORADO, espaciado=4)
    parrafo(img, xi, 346, "Londres, 1897", fuente("cursiva", 30), color=CREMA)
    parrafo(img, xd, 346, "Reikiavik, 1900-1901", fuente("cursiva", 30), color=CREMA)
    filas = [
        ("El protagonista", "Jonathan Harker", "Thomas Harker"),
        ("El castillo", "Los primeros capítulos", "Mucho más tiempo entre sus muros"),
        ("Los personajes", "Los que escribió Stoker", "Aparecen otros que Stoker nunca escribió"),
        ("El conde", "Un depredador que viaja a Londres", "Una conspiración que va mucho más allá"),
    ]
    d = ImageDraw.Draw(img)
    y = 430
    alto = 170
    for etq, a, b in filas:
        d.line([(110, y), (W - 110, y)], fill=DORADO + (120,), width=1)
        rombo(d, W / 2, y, 7)
        rotulo(img, (W / 2, y + 34), etq, 20, color=DORADO_CLARO, espaciado=4)
        parrafo(img, xi, y + 66, a, fuente("texto", 34), ancho_max=380, interlinea=1.2)
        parrafo(img, xd, y + 66, b, fuente("texto_bold", 34), ancho_max=400, interlinea=1.2, color=CREMA)
        y += alto
    d.line([(W / 2, 300), (W / 2, 418)], fill=DORADO + (90,), width=1)
    d.line([(110, y), (W - 110, y)], fill=DORADO + (120,), width=1)
    parrafo(img, W / 2, y + 30, "¿Cuál de las dos leerías primero?", fuente("cursiva", 40), color=DORADO_CLARO)
    logo_pie(img, y=1266, ancho=200)
    return img


# ------------------------------------------------ viernes 27: 813 (CONSULTA)
def lupin_813():
    img = lienzo(brillo_verde=(0.5, 0.5), intensidad=0.6, semilla=65)
    marco(img)
    rotulo(img, (W / 2, 118), "El Archivo Lupin  ·  Dossier IV", 22)
    texto_dorado(img, (W / 2, 240), "813", fuente("titulo", 190))
    separador(img, W / 2, 348)
    portada(img, N / "813_portada.jpg", (W / 2, 720), 620)
    parrafo(img, W / 2, 1075, "¿Sabes qué significa?", fuente("cursiva", 50), color=DORADO_CLARO)
    rotulo(img, (W / 2, 1165), "Próximamente", 22, color=CREMA, espaciado=6)
    logo_pie(img, y=1262, ancho=210)
    return img


# ------------------------------------------------ sábado 28: los maestros de Lovecraft (HABITUAL)
def maestros():
    img = lienzo(brillo_verde=(0.5, 0.5), intensidad=0.6, semilla=66)
    marco(img)
    rotulo(img, (W / 2, 118), "Lovecraft, 1927  ·  Una lista", 22)
    texto_dorado(img, (W / 2, 205), "Sus cuatro maestros", fuente("titulo", 86))
    parrafo(img, W / 2, 262, "«El horror sobrenatural en la literatura»", fuente("cursiva", 34))
    separador(img, W / 2, 335)
    portada(img, R / "granpan.jpg", (W / 2 - 215, 640), 470, angulo=4)
    portada(img, R / "sauces.jpg", (W / 2 + 215, 640), 470, angulo=-4)
    nombres = ["Arthur Machen", "Algernon Blackwood", "Lord Dunsany", "M. R. James"]
    d = ImageDraw.Draw(img)
    y = 930
    for i, n in enumerate(nombres):
        cx = W / 2 + (-230 if i % 2 == 0 else 230)
        yy = y + (i // 2) * 70
        rombo(d, cx - 190, yy, 7)
        d.text((cx - 170, yy), n, font=fuente("texto_bold", 40), fill=CREMA, anchor="lm")
    parrafo(img, W / 2, 1090, "Dos ya están en el Gabinete. ¿A quién añadirías tú?", fuente("cursiva", 36), color=DORADO_CLARO)
    logo_pie(img, y=1262, ancho=210)
    return img


if __name__ == "__main__":
    guardar(makt_anuncio(), SALIDA / "2026-11-23_makt.jpg")
    guardar(horla(), SALIDA / "2026-11-24_horla.jpg")
    guardar(peligro_azul(), SALIDA / "2026-11-25_peligro_azul.jpg")
    guardar(makt_comparativa(), SALIDA / "2026-11-26_makt_comparativa.jpg")
    guardar(lupin_813(), SALIDA / "2026-11-27_813.jpg")
    guardar(maestros(), SALIDA / "2026-11-28_maestros.jpg")
