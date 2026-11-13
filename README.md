# El Gabinete Negro · Imágenes para Instagram

Imágenes 1080×1350 (4:5) para @elgabinetenegro, con enlaces directos (raw) para programarlas en Buffer.

## Estructura
- `publicaciones/<fecha>_semana/` — imágenes finales de cada semana (JPG).
- `scripts/estilo.py` — guía de estilo en código: paleta, marco dorado, tipografías, portadas sobre lienzo 4:5.
- `scripts/semana_AAAA_MM_DD.py` — composición de las publicaciones de cada semana.
- `marca/` — logotipo y monograma dorado (transparentes).
- `recursos/` — portadas e ilustraciones de elgabinetenegro.com.
- `fuentes/` — Playfair Display, Cinzel y Cormorant Garamond (Google Fonts, licencia SIL OFL).

## Paleta
| Negro | Dorado | Verde botella | Crema |
|---|---|---|---|
| `#0B0B0B` | `#C9A24B` | `#0F3D2E` | `#EFE6D2` |

## Regenerar
```bash
pip install pillow numpy
cd scripts && python semana_2026_11_16.py
```
