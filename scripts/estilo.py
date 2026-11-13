"""Estilo visual de El Gabinete Negro para Instagram (1080x1350, 4:5).

Paleta: negro #0B0B0B, dorado #C9A24B, verde botella #0F3D2E, crema #EFE6D2.
Tipografías (libres, OFL): UnifrakturMaguntia (títulos góticos),
Cinzel (rótulos en versalitas) y Cormorant Garamond (texto).
"""
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "fuentes"
MARCA = RAIZ / "marca"
RECURSOS = RAIZ / "recursos"

W, H = 1080, 1350
NEGRO = (11, 11, 11)
DORADO = (201, 162, 75)
DORADO_OSC = (140, 108, 48)
DORADO_CLARO = (232, 207, 140)
VERDE = (15, 61, 46)
CREMA = (239, 230, 210)
SEPIA = (112, 84, 52)


def fuente(nombre, tam):
    archivos = {
        "gotica": "unifrakturmaguntia-latin-400-normal.ttf",
        "rotulo": "cinzel-latin-500-normal.ttf",
        "rotulo_bold": "cinzel-latin-700-normal.ttf",
        "texto": "cormorant-garamond-latin-500-normal.ttf",
        "texto_bold": "cormorant-garamond-latin-700-normal.ttf",
        "cursiva": "cormorant-garamond-latin-500-italic.ttf",
    }
    return ImageFont.truetype(str(FUENTES / archivos[nombre]), tam)


# ---------------------------------------------------------------- fondo
def lienzo(brillo_verde=(0.5, 0.42), intensidad=0.55, base=NEGRO, semilla=7):
    """Fondo negro con resplandor verde botella, viñeta y grano de papel."""
    rng = np.random.default_rng(semilla)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = brillo_verde[0] * W, brillo_verde[1] * H
    d = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    glow = np.clip(1 - d / 0.62, 0, 1) ** 1.8 * intensidad
    img = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        img[..., i] = base[i] + (VERDE[i] - base[i]) * glow
    # viñeta
    dv = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    img *= (1 - np.clip(dv - 0.32, 0, 1) * 1.1)[..., None]
    # grano y fibras de papel viejo
    img += rng.normal(0, 4.0, (H, W, 1))
    fibras = rng.normal(0, 1, (H // 6, W // 2)).astype(np.float32)
    fibras = np.array(Image.fromarray(fibras).resize((W, H), Image.BILINEAR))
    img += fibras[..., None] * 2.2
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


def degradado_dorado(ancho, alto):
    """Textura dorada metálica (vertical) para rellenar texto y adornos."""
    y = np.linspace(0, 1, alto)[:, None]
    stops = [(0, DORADO_OSC), (0.35, DORADO_CLARO), (0.55, DORADO), (1, DORADO_OSC)]
    out = np.zeros((alto, 1, 3))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (y >= p0) & (y <= p1)
        t = (y - p0) / (p1 - p0)
        for i in range(3):
            out[..., i] = np.where(m, c0[i] + (c1[i] - c0[i]) * t, out[..., i])
    out = np.repeat(out, ancho, axis=1)
    return Image.fromarray(out.astype(np.uint8)).convert("RGBA")


# ---------------------------------------------------------------- texto
def medir(texto, f):
    l, t, r, b = f.getbbox(texto)
    return r - l, b - t


def texto_dorado(img, xy, texto, f, anchor="mm", sombra=True, espaciado=0):
    """Texto con relleno dorado metálico y sombra suave."""
    mascara = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mascara)
    if espaciado:
        _texto_espaciado(d, xy, texto, f, 255, anchor, espaciado)
    else:
        d.text(xy, texto, font=f, fill=255, anchor=anchor)
    if sombra:
        s = mascara.filter(ImageFilter.GaussianBlur(6))
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
        capa.putalpha(s.point(lambda v: int(v * 0.8)))
        img.alpha_composite(capa, (0, 3))
    bbox = mascara.getbbox()
    if not bbox:
        return
    oro = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g = degradado_dorado(bbox[2] - bbox[0], bbox[3] - bbox[1])
    oro.paste(g, bbox[:2])
    oro.putalpha(mascara)
    img.alpha_composite(oro)


def _texto_espaciado(d, xy, texto, f, fill, anchor, esp):
    total = sum(f.getlength(c) for c in texto) + esp * (len(texto) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for c in texto:
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
        x += f.getlength(c) + esp


def rotulo(img, xy, texto, tam=26, color=DORADO, anchor="mm", espaciado=6, f=None):
    d = ImageDraw.Draw(img)
    _texto_espaciado(d, xy, texto.upper(), f or fuente("rotulo", tam), color, anchor, espaciado)


def parrafo(img, centro_x, y, texto, f, color=CREMA, ancho_max=820, interlinea=1.32, anchor="ma"):
    """Párrafo centrado con ajuste de línea. Devuelve la y final."""
    d = ImageDraw.Draw(img)
    lineas = []
    for bloque in texto.split("\n"):
        palabras, actual = bloque.split(), ""
        for p in palabras:
            prueba = (actual + " " + p).strip()
            if f.getlength(prueba) <= ancho_max:
                actual = prueba
            else:
                lineas.append(actual)
                actual = p
        lineas.append(actual)
    alto = f.size * interlinea
    for i, l in enumerate(lineas):
        d.text((centro_x, y + i * alto), l, font=f, fill=color, anchor=anchor)
    return y + len(lineas) * alto


# ---------------------------------------------------------------- adornos
def marco(img, margen=38):
    """Doble filete dorado con rombos en las esquinas."""
    d = ImageDraw.Draw(img)
    m1, m2 = margen, margen + 11
    d.rectangle([m1, m1, W - m1, H - m1], outline=DORADO + (230,), width=2)
    d.rectangle([m2, m2, W - m2, H - m2], outline=DORADO + (120,), width=1)
    for (x, y) in [(m1, m1), (W - m1, m1), (m1, H - m1), (W - m1, H - m1)]:
        rombo(d, x, y, 11)


def rombo(d, x, y, r, relleno=DORADO):
    d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=relleno + (255,))
    d.polygon([(x, y - r + 4), (x + r - 4, y), (x, y + r - 4), (x - r + 4, y)], fill=NEGRO + (255,))
    d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=relleno + (255,))


def separador(img, cx, y, ancho=320):
    d = ImageDraw.Draw(img)
    d.line([(cx - ancho / 2, y), (cx - 18, y)], fill=DORADO + (200,), width=1)
    d.line([(cx + 18, y), (cx + ancho / 2, y)], fill=DORADO + (200,), width=1)
    rombo(d, cx, y, 9)
    for s in (-1, 1):
        d.ellipse([cx + s * ancho / 2 - 3, y - 3, cx + s * ancho / 2 + 3, y + 3], fill=DORADO + (220,))


def logo_pie(img, y=1262, ancho=300):
    logo = Image.open(MARCA / "logo.png").convert("RGBA")
    logo = logo.resize((ancho, int(logo.height * ancho / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, ((W - ancho) // 2, y - logo.height // 2))


def monograma(tam):
    m = Image.open(MARCA / "monograma.png").convert("RGBA")
    return m.resize((tam, tam), Image.LANCZOS)


def portada(img, ruta, centro, alto, angulo=0, borde=True):
    """Coloca una portada 2:3 con sombra y filete dorado fino."""
    p = Image.open(ruta).convert("RGBA")
    ancho = int(p.width * alto / p.height)
    p = p.resize((ancho, alto), Image.LANCZOS)
    if borde:
        d = ImageDraw.Draw(p)
        d.rectangle([0, 0, ancho - 1, alto - 1], outline=DORADO + (200,), width=2)
    pad = 60
    cap = Image.new("RGBA", (ancho + 2 * pad, alto + 2 * pad), (0, 0, 0, 0))
    sombra = Image.new("RGBA", (ancho, alto), (0, 0, 0, 210))
    cap.alpha_composite(sombra, (pad + 8, pad + 16))
    cap = cap.filter(ImageFilter.GaussianBlur(18))
    cap.alpha_composite(p, (pad, pad))
    if angulo:
        cap = cap.rotate(angulo, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(cap, (int(centro[0] - cap.width / 2), int(centro[1] - cap.height / 2)))
    return ancho, alto


def sepia_grabado(ruta, caja, tam, oscuro=(28, 20, 12), claro=(233, 220, 190)):
    """Convierte una imagen en un duotono sepia con trama de grabado."""
    im = Image.open(ruta).convert("L").crop(caja)
    im = ImageOps.fit(im, tam, Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=1)
    a = (np.asarray(im).astype(np.float32) / 255) ** 0.8
    # trama de líneas horizontales finas, más marcadas en las sombras
    lineas = (np.sin(np.arange(tam[1]) * np.pi / 2.2)[:, None] * 0.5 + 0.5)
    a = np.clip(a - (1 - a) * lineas * 0.22, 0, 1)
    out = np.zeros((tam[1], tam[0], 3), np.float32)
    for i in range(3):
        out[..., i] = oscuro[i] + (claro[i] - oscuro[i]) * a
    return Image.fromarray(out.astype(np.uint8)).convert("RGBA")


def arco_gotico(d, x, y, ancho, alto, color, grosor=3):
    """Puerta de arco apuntado: x,y = esquina inferior izquierda."""
    r = ancho
    recto = alto - ancho * 0.87
    pts_izq, pts_der = [], []
    import math
    for i in range(41):
        t = math.radians(60 * i / 40)
        # arco izquierdo: centro en el lado derecho
        pts_izq.append((x + ancho - r * math.cos(t), y - recto - r * math.sin(t)))
        pts_der.append((x + r * math.cos(t), y - recto - r * math.sin(t)))
    contorno = [(x, y), (x, y - recto)] + pts_izq[1:] + list(reversed(pts_der))[:-1] + [(x + ancho, y - recto), (x + ancho, y)]
    d.line(contorno, fill=color, width=grosor, joint="curve")
    return contorno


def guardar(img, ruta):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(ruta, "JPEG", quality=93, optimize=True, progressive=True)
    print("guardado", ruta.relative_to(RAIZ))
