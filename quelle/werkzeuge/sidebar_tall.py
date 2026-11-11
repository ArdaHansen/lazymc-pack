"""
Hoeherer Sidebar-Rahmen fuer die Unternehmenszeilen.

Der normale Rahmen (sb_frame.png) ist ein festes Bild und deckt genau die zehn Zeilen des
Citybuild-Scoreboards ab. Haengt ein Plugin unten Zeilen an, rutschen die unter dem Rahmen
heraus und stehen frei auf der Welt - es sieht kaputt aus.

Dieses Werkzeug erzeugt daraus einen hoeheren Rahmen: der Kopf und der Fuss bleiben wie sie
sind, dazwischen wird ein gleichfoermiges Band so oft wiederholt, dass der Rahmen die
zusaetzlichen Zeilen mit abdeckt. Dadurch sieht die erweiterte Sidebar aus wie eine einzige,
nur laengere Flaeche.

Font: minecraft:default
  U+E010  normaler Rahmen (vorhanden)
  U+E011  hoher Rahmen    (hier erzeugt)
"""
from PIL import Image
import json
import os

HERE = os.path.dirname(__file__)
PACK = os.path.join(HERE, '..', 'pack')
TEX = os.path.join(PACK, 'assets', 'minecraft', 'textures', 'font')
FONT = os.path.join(PACK, 'assets', 'lazymc', 'font', 'sidebar.json')

SCALE = 2          # Textur liegt in doppelter Groesse vor
BASE_HEIGHT = 104  # Hoehe des normalen Rahmens im Spiel
EXTRA_LINES = 7    # so viele Zeilen haengt LazyChestShops hoechstens an
LINE_HEIGHT = 10.4  # 104 Pixel verteilt auf zehn Zeilen


def uniform_band(im):
    """Findet ein Band gleicher Zeilen in der Mitte, das sich wiederholen laesst."""
    px = im.load()
    w, h = im.size

    def row(y):
        return tuple(px[x, y] for x in range(w))

    best = None
    start = 0
    prev = row(0)
    for y in range(1, h):
        current = row(y)
        if current != prev:
            length = y - start
            # Nur Baender aus der Mitte nehmen; Kopf und Fuss sollen unberuehrt bleiben.
            if length >= 6 and h * 0.3 < start < h * 0.75:
                if best is None or length > best[1] - best[0]:
                    best = (start, y)
            start = y
            prev = current
    if best is None:
        raise SystemExit('Kein wiederholbares Band gefunden - Rahmen von Hand pruefen.')
    return best


def main():
    source = os.path.join(TEX, 'sb_frame.png')
    im = Image.open(source).convert('RGBA')
    w, h = im.size

    start, end = uniform_band(im)
    band = im.crop((0, start, w, end))
    band_height = end - start

    # Wie viele Texturpixel fehlen fuer die Zusatzzeilen?
    needed = int(round(EXTRA_LINES * LINE_HEIGHT * SCALE))
    copies = max(1, int(round(needed / band_height)))
    added = copies * band_height

    out = Image.new('RGBA', (w, h + added), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, 0, w, end)), (0, 0))
    for i in range(copies):
        out.alpha_composite(band, (0, end + i * band_height))
    out.alpha_composite(im.crop((0, end, w, h)), (0, end + added))

    target = os.path.join(TEX, 'sb_frame_tall.png')
    out.save(target)

    game_height = BASE_HEIGHT + added // SCALE
    print(f'Band {start}-{end} ({band_height} px) {copies}x wiederholt')
    print(f'sb_frame_tall.png: {out.size}, Hoehe im Spiel {game_height}')

    # Font-Eintrag ergaenzen
    with open(FONT, encoding='utf-8') as f:
        data = json.load(f)
    data['providers'] = [p for p in data['providers']
                         if p.get('file') != 'minecraft:font/sb_frame_tall.png']
    for provider in data['providers']:
        if provider.get('file') == 'minecraft:font/sb_frame.png':
            data['providers'].append({
                'type': 'bitmap',
                'file': 'minecraft:font/sb_frame_tall.png',
                'ascent': provider['ascent'],
                'height': game_height,
                'chars': [''],
            })
            break
    with open(FONT, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print('sidebar.json ergaenzt: U+E011')


if __name__ == '__main__':
    main()
