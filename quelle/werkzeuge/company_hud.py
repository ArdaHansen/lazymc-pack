"""
Unternehmens-Anzeige (LazyChestShops).

Erzeugt ein Panel aus gestapelten Zeilen, das wie die Citybuild-Sidebar aussieht - nur am
linken Bildschirmrand. Jede Zeile ist eine eigene Boss-Leiste; die Zeilenbilder sind genau so
hoch wie der Abstand zweier Boss-Leisten, damit sie nahtlos aneinanderstossen und das Ganze
als EIN Panel wirkt.

Font: lazymc:chud
  U+E700  Kopfzeile   (runde obere Ecken, Akzentstreifen)
  U+E701  Mittelzeile
  U+E702  Fusszeile   (runde untere Ecken)
  U+E703  Trennzeile  (duenne Linie, fuer Abschnitte)

Texturen liegen in 2-facher Groesse vor, damit sie auf hohen Aufloesungen sauber bleiben.
"""
from PIL import Image
import json
import os

PACK = os.path.join(os.path.dirname(__file__), '..', 'pack')
FONT_DIR = os.path.join(PACK, 'assets', 'lazymc', 'font')
TEX_DIR = os.path.join(PACK, 'assets', 'lazymc', 'textures', 'font', 'chud')


def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


OUT = hx('#07080B')     # Aussenlinie
CY = hx('#5FD8E6')      # Akzent hell
CYD = hx('#1E7E8C')     # Akzent dunkel
BG_TOP = hx('#161A21')  # Hintergrund oben
BG_BOT = hx('#10131A')  # Hintergrund unten
LINE = hx('#262B34')    # Trennlinie

SCALE = 2
W = 128            # Breite im Spiel
ROW = 19           # Zeilenhoehe im Spiel = Abstand zweier Boss-Leisten
TW, TH = W * SCALE, ROW * SCALE


def base(round_top=False, round_bottom=False):
    """Eine Zeile: dunkler Hintergrund, links ein Akzentstreifen, aussen eine Linie."""
    im = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
    px = im.load()
    # Flacher Hintergrund, kein Verlauf: die Zeilen stossen nahtlos aneinander. Ein Verlauf
    # je Zeile wuerde bei jedem Zeilenwechsel von vorn beginnen und das Panel streifig machen.
    for y in range(TH):
        for x in range(TW):
            if x < 2 * SCALE:
                # Aussenlinie und Akzentstreifen am linken Rand
                px[x, y] = OUT + (255,) if x < SCALE else CY + (255,)
            elif x >= TW - SCALE:
                px[x, y] = OUT + (255,)
            else:
                px[x, y] = BG_TOP + (236,)

    # Obere und untere Abschlusslinie nur an den Enden des Panels
    if round_top:
        for x in range(TW):
            for y in range(SCALE):
                px[x, y] = OUT + (255,)
        # Kraeftiger Akzentstreifen unter der Oberkante - das Panel bekommt damit einen Kopf,
        # so wie die Citybuild-Sidebar.
        for x in range(2 * SCALE, TW - SCALE):
            for y in range(SCALE, 3 * SCALE):
                px[x, y] = CY + (255,)
            for y in range(3 * SCALE, 4 * SCALE):
                px[x, y] = CYD + (255,)
        # Ecken abrunden
        for x in range(SCALE):
            for y in range(SCALE):
                px[x, y] = (0, 0, 0, 0)
        for x in range(TW - SCALE, TW):
            for y in range(SCALE):
                px[x, y] = (0, 0, 0, 0)
    if round_bottom:
        for x in range(TW):
            for y in range(TH - SCALE, TH):
                px[x, y] = OUT + (255,)
        for x in range(SCALE):
            for y in range(TH - SCALE, TH):
                px[x, y] = (0, 0, 0, 0)
        for x in range(TW - SCALE, TW):
            for y in range(TH - SCALE, TH):
                px[x, y] = (0, 0, 0, 0)
    return im


def divider():
    """Mittelzeile mit duenner Trennlinie oben - trennt Abschnitte im Panel."""
    im = base()
    px = im.load()
    for x in range(3 * SCALE, TW - 2 * SCALE):
        for y in range(SCALE):
            px[x, y] = LINE + (255,)
    return im


def main():
    os.makedirs(TEX_DIR, exist_ok=True)
    base(round_top=True).save(os.path.join(TEX_DIR, 'top.png'))
    base().save(os.path.join(TEX_DIR, 'mid.png'))
    base(round_bottom=True).save(os.path.join(TEX_DIR, 'bottom.png'))
    divider().save(os.path.join(TEX_DIR, 'divider.png'))

    providers = []
    for char, name in (('', 'top'), ('', 'mid'),
                       ('', 'bottom'), ('', 'divider')):
        providers.append({
            "type": "bitmap",
            "file": f"lazymc:font/chud/{name}.png",
            # ascent so gewaehlt, dass die Zeile hinter dem Text sitzt und die Zeilen
            # buendig aneinanderstossen
            "ascent": 14,
            "height": ROW,
            "chars": [char],
        })
    # Dieselben Verschiebungen wie im hud-Font, damit sich Text im Panel ausrichten laesst.
    advances = {}
    for i in range(8):
        advances[chr(0xE7E0 + i)] = -(1 << i)
        advances[chr(0xE7E8 + i)] = (1 << i)
    advances[chr(0xE7F0)] = -1
    providers.append({"type": "space", "advances": advances})

    os.makedirs(FONT_DIR, exist_ok=True)
    with open(os.path.join(FONT_DIR, 'chud.json'), 'w', encoding='utf-8') as f:
        json.dump({"providers": providers}, f, indent=2)
    print('chud: 4 Zeilenbilder und Font geschrieben')


if __name__ == '__main__':
    main()
