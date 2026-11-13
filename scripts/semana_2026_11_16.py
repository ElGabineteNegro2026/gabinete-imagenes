"""Imágenes de Instagram para la semana del 16 al 22 de noviembre de 2026."""
from PIL import Image, ImageDraw, ImageFilter

from estilo import *  # noqa: F401,F403

SALIDA = RAIZ / "publicaciones" / "2026-11-16_semana"
R = RECURSOS


# ------------------------------------------------ 1) lunes 16: carrusel
def carrusel_portada():
    img = lienzo(brillo_verde=(0.5, 0.62), intensidad=0.6)
    marco(img)
    rotulo(img, (W / 2, 150), "El catálogo del Gabinete", 26)
    texto_dorado(img, (W / 2, 262), "Cuatro salas,", fuente("titulo", 112))
    texto_dorado(img, (W / 2, 382), "una pregunta", fuente("titulo", 112))
    separador(img, W / 2, 470)

    # cuatro puertas de arco apuntado
    d = ImageDraw.Draw(img)
    nombres = [("Cámara", "Sellada"), ("Límite", "Abisal"), ("Archivo", "Arcano"), ("Archivo", "Lupin")]
    ancho, alto, hueco = 170, 360, 46
    x0 = (W - (4 * ancho + 3 * hueco)) / 2
    base = 960
    for i, (a, b) in enumerate(nombres):
        x = x0 + i * (ancho + hueco)
        # interior oscuro de la puerta con resplandor verde
        interior = Image.new("L", (W, H), 0)
        arco_gotico(ImageDraw.Draw(interior), x, base, ancho, alto, 255, grosor=1)
        ImageDraw.Draw(interior).polygon(arco_gotico(ImageDraw.Draw(Image.new("L", (1, 1))), x, base, ancho, alto, 0), fill=255)
        verde = Image.new("RGBA", (W, H), VERDE + (0,))
        verde.putalpha(interior.point(lambda v: int(v * 0.55)))
        img.alpha_composite(verde)
        arco_gotico(d, x, base, ancho, alto, DORADO + (255,), grosor=3)
        arco_gotico(d, x + 12, base, ancho - 24, alto - 22, DORADO + (110,), grosor=1)
        # cerradura
        cx = x + ancho / 2
        d.ellipse([cx - 9, base - 150, cx + 9, base - 132], fill=DORADO + (255,))
        d.polygon([(cx - 6, base - 136), (cx + 6, base - 136), (cx + 10, base - 104), (cx - 10, base - 104)], fill=DORADO + (255,))
        rotulo(img, (cx, base - alto - 40), ["I", "II", "III", "IV"][i], 24)
        rotulo(img, (cx, base + 44), a, 22, color=CREMA, espaciado=3)
        rotulo(img, (cx, base + 76), b, 22, color=CREMA, espaciado=3)
    d.line([(90, base), (W - 90, base)], fill=DORADO + (160,), width=1)

    parrafo(img, W / 2, 1100, "¿Qué puerta abrirías esta noche?", fuente("cursiva", 40))
    rotulo(img, (W / 2, 1170), "Desliza  ›", 20, color=DORADO, espaciado=5)
    logo_pie(img, y=1250, ancho=250)
    return img


SALAS = [
    dict(num="Sala I", nombre="Cámara Sellada", para="para los enigmas",
         texto="Misterios clásicos, presencias inquietantes y secretos al otro lado de una puerta.",
         portadas=["carmilla.jpg", "bierce.jpg", "otravuelta.jpg"], verde=(0.5, 0.5)),
    dict(num="Sala II", nombre="Límite Abisal", para="para lo inexplicable",
         texto="Horror cósmico y ficción extraña, ahí donde la razón empieza a resquebrajarse.",
         portadas=["innsmouth.jpg", "montanas.jpg", "reyamarillo.jpg"], verde=(0.5, 0.55)),
    dict(num="Sala III", nombre="Archivo Arcano", para="para las piezas de colección",
         texto="Ediciones en tapa dura, con ilustraciones, pensadas para quedarse en la estantería.",
         portadas=["casas.png", "dracula.jpg", "objetos.jpg"], verde=(0.5, 0.5)),
    dict(num="Sala IV", nombre="Archivo Lupin", para="para el ingenio",
         texto="Las aventuras del caballero ladrón: elegancia, burla y un golpe siempre por delante.",
         portadas=["lupin2.jpg", "lupin1.jpg", "lupin3.jpg"], verde=(0.5, 0.5)),
]


def carrusel_sala(i, sala):
    img = lienzo(brillo_verde=sala["verde"], intensidad=0.62, semilla=10 + i)
    marco(img)
    rotulo(img, (W / 2, 128), sala["num"], 26)
    texto_dorado(img, (W / 2, 222), sala["nombre"], fuente("titulo", 104))
    parrafo(img, W / 2, 292, sala["para"], fuente("cursiva", 44), color=CREMA)
    separador(img, W / 2, 380)
    izq, centro, der = sala["portadas"]
    portada(img, R / izq, (W / 2 - 250, 720), 470, angulo=6)
    portada(img, R / der, (W / 2 + 250, 720), 470, angulo=-6)
    portada(img, R / centro, (W / 2, 705), 560)
    parrafo(img, W / 2, 1060, sala["texto"], fuente("texto", 36), ancho_max=760)
    logo_pie(img, y=1252, ancho=240)
    rotulo(img, (W - 92, 1252), f"{i + 2} / 5", 18, color=DORADO, anchor="rm", espaciado=3)
    return img


# ------------------------------------------------ 2) martes 17: Bierce
def bierce():
    img = lienzo(brillo_verde=(0.5, 0.45), intensidad=0.7, semilla=21)
    marco(img)
    rotulo(img, (W / 2, 122), "Colección Cámara Sellada", 24)
    portada(img, R / "bierce.jpg", (W / 2, 610), 860)
    texto_dorado(img, (W / 2, 1110), "Ambrose Bierce", fuente("titulo", 76))
    parrafo(img, W / 2, 1160, "Doce historias de lo inexplicable", fuente("cursiva", 36))
    logo_pie(img, y=1262, ancho=220)
    return img


# ------------------------------------------------ 3) jueves 19: Lupin 1905
def lupin():
    img = lienzo(brillo_verde=(0.5, 0.4), intensidad=1.0, semilla=33)
    marco(img)
    rotulo(img, (W / 2, 122), "Archivo Lupin  ·  Curiosidad", 24)
    texto_dorado(img, (W / 2, 238), "1905", fuente("titulo", 150))

    # camafeo oval con la ilustración en sepia de grabado
    ow, oh = 470, 600
    cx, cy = W / 2, 640
    ilus = sepia_grabado(R / "lupin1.jpg", (130, 290, 451, 700), (ow, oh))
    mascara = Image.new("L", (ow, oh), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, ow - 1, oh - 1], fill=255)
    ilus.putalpha(mascara.filter(ImageFilter.GaussianBlur(1)))
    sombra = Image.new("RGBA", (ow + 80, oh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse([40, 52, ow + 40, oh + 52], fill=(0, 0, 0, 200))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(20)), (int(cx - ow / 2 - 40), int(cy - oh / 2 - 40)))
    img.alpha_composite(ilus, (int(cx - ow / 2), int(cy - oh / 2)))
    d = ImageDraw.Draw(img)
    for k, (g, a) in enumerate([(4, 255), (1, 150)]):
        e = 10 + k * 14
        d.ellipse([cx - ow / 2 - e, cy - oh / 2 - e, cx + ow / 2 + e, cy + oh / 2 + e], outline=DORADO + (a,), width=g)
    for ang_x, ang_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        rombo(d, cx + ang_x * (ow / 2 + 17), cy + ang_y * (oh / 2 + 17), 12)

    parrafo(img, W / 2, 990, "Arsène Lupin aparece por primera vez en julio de 1905, en las páginas de la revista «Je sais tout», de la mano de Maurice Leblanc.",
            fuente("texto", 35), ancho_max=800)
    parrafo(img, W / 2, 1140, "Elegante, burlón y siempre un paso por delante.", fuente("cursiva", 36), color=DORADO_CLARO)
    logo_pie(img, y=1262, ancho=220)
    return img


# ------------------------------------------------ 4) viernes 20: lecturas
def icono_audio(img, cx, cy, r=92):
    """Medallón con micrófono de época y ondas de sonido."""
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=VERDE + (255,), outline=DORADO + (255,), width=3)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], outline=DORADO + (120,), width=1)
    # micrófono
    d.rounded_rectangle([cx - 20, cy - 52, cx + 20, cy + 10], radius=20, outline=DORADO + (255,), width=4)
    for k in range(4):
        d.line([(cx - 12, cy - 36 + k * 12), (cx + 12, cy - 36 + k * 12)], fill=DORADO + (200,), width=2)
    d.arc([cx - 34, cy - 30, cx + 34, cy + 28], 20, 160, fill=DORADO + (255,), width=4)
    d.line([(cx, cy + 28), (cx, cy + 48)], fill=DORADO + (255,), width=4)
    d.line([(cx - 22, cy + 50), (cx + 22, cy + 50)], fill=DORADO + (255,), width=4)
    for s in (-1, 1):
        for k, rr in enumerate((52, 68)):
            caja = [cx - rr, cy - 22 - rr, cx + rr, cy - 22 + rr]
            ini, fin = (-35, 35) if s == 1 else (145, 215)
            d.arc(caja, ini, fin, fill=DORADO + (220 - k * 70,), width=3)


def lecturas():
    img = lienzo(brillo_verde=(0.3, 0.5), intensidad=0.45, semilla=44)
    marco(img)
    rotulo(img, (W / 2, 122), "Para este fin de semana", 24)
    texto_dorado(img, (W / 2, 212), "Tres lecturas", fuente("titulo", 100))
    separador(img, W / 2, 290)

    bloques = [
        ("Para conservar", "Archivo Arcano", "En tapa dura y con ilustraciones.", "dracula.jpg"),
        ("Para escuchar", "Audiolibros", "La oscuridad, en voz alta.", None),
        ("Si la razón se resquebraja", "Límite Abisal", "Horror cósmico y ficción extraña.", "montanas.jpg"),
    ]
    d = ImageDraw.Draw(img)
    y0, alto_b = 322, 248
    for i, (etq, nombre, desc, tapa) in enumerate(bloques):
        y = y0 + i * (alto_b + 18)
        panel = Image.new("RGBA", (W - 180, alto_b), VERDE + (70,))
        img.alpha_composite(panel, (90, y))
        d.rectangle([90, y, W - 90, y + alto_b], outline=DORADO + (150,), width=1)
        cx_img, cy_img = 230, y + alto_b / 2
        if tapa:
            portada(img, R / tapa, (cx_img, cy_img), alto_b - 40)
        else:
            icono_audio(img, cx_img, cy_img)
        rotulo(img, (360, y + 58), f"{['I', 'II', 'III'][i]}  ·  {etq}", 20, anchor="lm", espaciado=4)
        texto_dorado(img, (356, y + 126), nombre, fuente("titulo", 70), anchor="lm")
        ImageDraw.Draw(img).text((360, y + 192), desc, font=fuente("cursiva", 36), fill=CREMA, anchor="lm")

    texto_dorado(img, (W / 2, 1172), "¿Cuál te llevas?", fuente("titulo", 66))
    logo_pie(img, y=1268, ancho=200)
    return img


# ------------------------------------------------ 5) domingo 22: Drácula
def dracula():
    img = lienzo(brillo_verde=(0.5, 0.5), intensidad=0.5, semilla=55)
    # grabado del huésped de Drácula como textura de fondo, muy tenue
    fondo = sepia_grabado(R / "drac_huesped.png", (0, 0, 1024, 1536), (W, H), oscuro=(0, 0, 0), claro=(150, 120, 80))
    fondo.putalpha(34)
    img.alpha_composite(fondo)
    marco(img)
    rotulo(img, (W / 2, 120), "Archivos Prohibidos  ·  Episodio V", 24)
    texto_dorado(img, (W / 2, 210), "El expediente Drácula", fuente("titulo", 86))
    separador(img, W / 2, 282)
    portada(img, R / "dracula.jpg", (W / 2 - 70, 712), 760)
    m = monograma(220)
    img.alpha_composite(m, (W // 2 + 150, 930))
    rotulo(img, (W / 2, 1150), "Novedad  ·  Archivo Arcano  ·  Tapa dura", 22, color=CREMA, espaciado=4)
    parrafo(img, W / 2, 1180, "Episodio ya disponible. Enlace en la bio.", fuente("cursiva", 34), color=DORADO_CLARO)
    logo_pie(img, y=1266, ancho=200)
    return img


if __name__ == "__main__":
    guardar(carrusel_portada(), SALIDA / "2026-11-16_salas_1.jpg")
    for i, s in enumerate(SALAS):
        guardar(carrusel_sala(i, s), SALIDA / f"2026-11-16_salas_{i + 2}.jpg")
    guardar(bierce(), SALIDA / "2026-11-17_bierce.jpg")
    guardar(lupin(), SALIDA / "2026-11-19_lupin.jpg")
    guardar(lecturas(), SALIDA / "2026-11-20_lecturas.jpg")
    guardar(dracula(), SALIDA / "2026-11-22_dracula.jpg")
