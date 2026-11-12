"""
Hintergrundtafeln fuer die grossen LazyMC-Menues (Marktplatz-Stil).

Die Tafel wird als Schrift-Glyphe in den Inventar-Titel geschrieben (Font lazymc:gui) und liegt
damit ueber der normalen Truhen-Textur. Die Knoepfe darunter sind unsichtbare Items
(lazymc:filler) - sie tragen nur Name und Beschreibung. So entstehen grosse, bemalte Flaechen,
die trotzdem anklickbar sind.

Aufbau des Titels (siehe Theme.java in den Plugins):

    <white><!shadow><font:lazymc:gui> [-8] [Tafel links] [-1] [Tafel rechts] [-1] [-168] </font>
    + Plakette von LazyCore + Untertitel

Jede Tafel ist doppelt aufgeloest (2 Texturpixel = 1 Menuepixel) und in zwei Haelften geteilt,
damit keine Glyphe groesser als 256 Pixel wird. ascent 13 setzt die Oberkante genau an den
oberen Rand des Menues.

WICHTIG: Die Felder (LAYOUTS) muessen zu den Menues in LazyChestShops (MainMenu) und
LazyLogistics (LogisticsMenu) passen. Wer hier etwas verschiebt, muss es dort auch tun.
"""
import json
import os

from PIL import Image, ImageDraw

import lcs_icons
import ll_icons
from lcs_icons import Canvas, hx

HERE = os.path.dirname(__file__)
PACK = os.path.join(HERE, '..', 'pack', 'assets', 'lazymc')
FONT_TEX = os.path.join(PACK, 'textures', 'font', 'gui')
FONT_FILE = os.path.join(PACK, 'font', 'gui.json')

S = 2          # Texturpixel je Menuepixel
W = 176        # Breite eines Truhenmenues in Menuepixeln

# ------------------------------------------------------------------ Farben

OUTLINE = hx('#07080B')
EDGE_A = hx('#00E5FF')
EDGE_B = hx('#0094FF')
BOARD_TOP = hx('#3B414C')
BOARD_BOT = hx('#272B33')
STRIP_TOP = hx('#4A5260')
STRIP_BOT = hx('#353B46')
INSET = hx('#1A1D23')
INSET_DARK = hx('#111318')
INSET_LIGHT = hx('#3A404B')
SOCKET = hx('#14161B')
SOCKET_HI = hx('#4A515D')
SOCKET_LO = hx('#0B0C0F')

ACCENT = {
    #          hell         mitte        dunkel
    'cyan':   ('#7FF0FA', '#14B9D3', '#0A5E72'),
    'green':  ('#8DFFBE', '#2FC57A', '#16663F'),
    'gold':   ('#FFE38A', '#EFAE24', '#87590C'),
    'orange': ('#FFC38A', '#EE8424', '#86420C'),
    'purple': ('#D9B4FF', '#9A5CEF', '#4E2690'),
    'blue':   ('#9CC8FF', '#3D7FE0', '#1B3F85'),
    'teal':   ('#8AF5DC', '#1EC7A3', '#0B6654'),
    'red':    ('#FFA3AE', '#E24A5C', '#7C1A27'),
    'steel':  ('#C9D1DC', '#7D8796', '#3E4552'),
}

# ------------------------------------------------------------------ Pixelschrift 5x7

FONT = {
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': ["###", " # ", " # ", " # ", " # ", " # ", "###"],
    'J': ["  ###", "    #", "    #", "    #", "#   #", "#   #", " ### "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    'Ä': ["#   #", " ### ", "#   #", "#   #", "#####", "#   #", "#   #"],
    'Ö': ["#   #", " ### ", "#   #", "#   #", "#   #", "#   #", " ### "],
    'Ü': ["#   #", "     ", "#   #", "#   #", "#   #", "#   #", " ### "],
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': [" # ", "## ", " # ", " # ", " # ", " # ", "###"],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    '4': ["#   #", "#   #", "#   #", "#####", "    #", "    #", "    #"],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    '-': ["    ", "    ", "    ", "####", "    ", "    ", "    "],
    '&': [" ##  ", "#  # ", " ##  ", " # # ", "#  # ", "#  # ", " ## #"],
    '!': ["#", "#", "#", "#", "#", " ", "#"],
    ' ': ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
}


def text_width(text):
    return sum(len(FONT[ch][0]) + 1 for ch in text) - 1


def draw_text(img, x, y, text, color, outline):
    """Schreibt Text in Menuepixeln mit 1 Pixel Umriss und Schatten nach unten."""
    px = img.load()
    cells = set()
    cx = x
    for ch in text:
        glyph = FONT[ch]
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == '#':
                    cells.add((cx + gx, y + gy))
        cx += len(glyph[0]) + 1
    ring = set()
    for (gx, gy) in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1, 2):
                ring.add((gx + dx, gy + dy))
    for (gx, gy) in ring - cells:
        put(px, img.size, gx, gy, outline)
    for (gx, gy) in cells:
        put(px, img.size, gx, gy, color)


def put(px, size, x, y, col):
    """Setzt einen Menuepixel (= S x S Texturpixel)."""
    for dx in range(S):
        for dy in range(S):
            tx, ty = x * S + dx, y * S + dy
            if 0 <= tx < size[0] and 0 <= ty < size[1]:
                px[tx, ty] = col


def rect(img, x0, y0, x1, y1, col):
    ImageDraw.Draw(img).rectangle((x0 * S, y0 * S, (x1 + 1) * S - 1, (y1 + 1) * S - 1), fill=col)


def mix(a, b, t):
    return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3)) + (255,)


def gradient(img, x0, y0, x1, y1, top, bottom):
    d = ImageDraw.Draw(img)
    h = max(1, (y1 - y0 + 1) * S - 1)
    for ty in range(y0 * S, (y1 + 1) * S):
        t = (ty - y0 * S) / h
        d.line((x0 * S, ty, (x1 + 1) * S - 1, ty), fill=mix(top, bottom, t))


# ------------------------------------------------------------------ Bausteine

def board(rows, strip=True):
    """Die Grundtafel: Umriss, Cyan-Kante, Graphit, Titelleiste und dunkler Innenbereich."""
    height = 17 + rows * 18 + 1
    img = Image.new('RGBA', (W * S, height * S), (0, 0, 0, 0))
    px = img.load()
    gradient(img, 0, 0, W - 1, height - 1, BOARD_TOP, BOARD_BOT)
    # Umriss mit abgerundeten Ecken
    rect(img, 0, 0, W - 1, 0, OUTLINE)
    rect(img, 0, height - 1, W - 1, height - 1, OUTLINE)
    rect(img, 0, 0, 0, height - 1, OUTLINE)
    rect(img, W - 1, 0, W - 1, height - 1, OUTLINE)
    for (cx, cy) in ((0, 0), (W - 1, 0), (0, height - 1), (W - 1, height - 1)):
        put(px, img.size, cx, cy, (0, 0, 0, 0))
    for y in range(1, height - 1):
        t = y / max(1, height - 2)
        put(px, img.size, 1, y, mix(EDGE_A, EDGE_B, t))
        put(px, img.size, W - 2, y, mix(EDGE_A, EDGE_B, t))
    for x in range(1, W - 1):
        put(px, img.size, x, 1, EDGE_A)
    # Titelleiste
    if strip:
        gradient(img, 2, 2, W - 3, 15, STRIP_TOP, STRIP_BOT)
        rect(img, 2, 16, W - 3, 16, OUTLINE)
        rect(img, 2, 2, W - 3, 2, hx('#5E6878'))
        for (nx, ny) in ((4, 4), (W - 5, 4), (4, 13), (W - 5, 13)):
            put(px, img.size, nx, ny, hx('#8A94A5'))
            put(px, img.size, nx + 1, ny + 1, hx('#22262D'))
    # Innenbereich der Felder
    rect(img, 6, 16, W - 7, 17 + rows * 18, INSET_DARK)
    rect(img, 7, 17, W - 8, 16 + rows * 18, INSET)
    rect(img, 6, 17 + rows * 18, W - 7, 17 + rows * 18, INSET_LIGHT)
    rect(img, W - 7, 16, W - 7, 17 + rows * 18, INSET_LIGHT)
    return img


def cell_box(c0, r0, c1, r1):
    """Menuepixel-Rechteck eines Feldbereichs (Spalten c0..c1, Zeilen r0..r1)."""
    return 7 + 18 * c0, 17 + 18 * r0, 7 + 18 * (c1 + 1) - 1, 17 + 18 * (r1 + 1) - 1


def socket(img, c, r):
    """Vertiefter Platz fuer einen normalen Knopf."""
    x0, y0, x1, y1 = cell_box(c, r, c, r)
    rect(img, x0, y0, x1, y1, SOCKET_LO)
    rect(img, x0 + 1, y0 + 1, x1, y1, SOCKET_HI)
    rect(img, x0 + 1, y0 + 1, x1 - 1, y1 - 1, SOCKET)


def art(draw_fn, scale):
    """Zeichnung aus den Symbol-Skripten - ohne Kachel, mit Umriss - in Texturpixeln."""
    canvas = Canvas()
    draw_fn(canvas)
    src = canvas.im.load()
    out = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    q = out.load()
    for yy in range(32):
        for xx in range(32):
            a = src[xx, yy]
            if a[3]:
                below = yy + 1 < 32 and src[xx, yy + 1][3]
                right = xx + 1 < 32 and src[xx + 1, yy][3]
                above = yy > 0 and src[xx, yy - 1][3]
                left = xx > 0 and src[xx - 1, yy][3]
                col = a
                if not below or not right:
                    col = tuple(int(v * 0.78) for v in a[:3]) + (255,)
                elif not above or not left:
                    col = tuple(min(255, int(v * 1.12)) for v in a[:3]) + (255,)
                q[xx, yy] = col
            elif any(0 <= xx + dx < 32 and 0 <= yy + dy < 32 and src[xx + dx, yy + dy][3]
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                q[xx, yy] = lcs_icons.OUT
    if scale != 1:
        out = out.resize((32 * scale, 32 * scale), Image.NEAREST)
    return out


def panel(img, area, accent, label, pictures, hero=False):
    """
    Ein farbiges Panel ueber mehreren Feldern - wie die Kacheln im Marktplatz.

    area     (c0, r0, c1, r1)
    pictures Liste von Zeichenfunktionen, die auf einem Regalbrett stehen
    """
    light, mid, dark = (hx(c) for c in ACCENT[accent])
    x0, y0, x1, y1 = cell_box(*area)
    x0, y0, x1, y1 = x0 + 1, y0 + 1, x1 - 1, y1 - 1
    px = img.load()
    # Umriss mit runden Ecken
    rect(img, x0, y0, x1, y1, OUTLINE)
    gradient(img, x0 + 1, y0 + 1, x1 - 1, y1 - 1, mix(light, mid, 0.35), mix(mid, dark, 0.55))
    for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        put(px, img.size, cx, cy, INSET)
    # Glanzkante oben, Schatten unten
    rect(img, x0 + 1, y0 + 1, x1 - 1, y0 + 1, mix(light, (255, 255, 255, 255), 0.35))
    rect(img, x0 + 1, y0 + 1, x0 + 1, y1 - 1, mix(light, mid, 0.2))
    rect(img, x0 + 1, y1 - 1, x1 - 1, y1 - 1, dark)
    rect(img, x1 - 1, y0 + 1, x1 - 1, y1 - 1, mix(mid, dark, 0.7))
    # feines Rautenmuster als Struktur
    for yy in range(y0 + 3, y1 - 2):
        for xx in range(x0 + 3, x1 - 2):
            if (xx + yy) % 6 == 0 and (xx - yy) % 6 == 0:
                put(px, img.size, xx, yy, mix(light, mid, 0.5))

    height = y1 - y0 + 1
    width = x1 - x0 + 1
    single_row = height < 24

    if single_row:
        # Leiste: Bild links, Text daneben
        if pictures:
            pic = art(pictures[0], 1)
            img.alpha_composite(pic, ((x0 + 1) * S, (y0 + 0) * S))
        tx = x0 + 19 if pictures else x0 + (width - text_width(label)) // 2
        if pictures and tx + text_width(label) > x1 - 2:
            tx = x1 - 2 - text_width(label)
        if pictures:
            tx = max(tx, x0 + 19)
            free = x1 - 2 - (x0 + 19)
            tx = x0 + 19 + max(0, (free - text_width(label)) // 2)
        draw_text(img, tx, y0 + (height - 7) // 2, label, hx('#FFFFFF'), dark)
        return

    # Beschriftung oben mittig
    tx = x0 + (width - text_width(label)) // 2
    draw_text(img, tx, y0 + 3, label, hx('#FFFFFF'), dark)

    # Regalbrett
    shelf_y = y1 - 4
    rect(img, x0 + 3, shelf_y, x1 - 3, shelf_y + 1, mix(dark, OUTLINE, 0.4))
    rect(img, x0 + 3, shelf_y, x1 - 3, shelf_y, mix(light, mid, 0.3))

    if not pictures:
        return
    if hero:
        pic = art(pictures[0], 3)            # 96 Texturpixel = 48 Menuepixel
        size = 48
        px_x = x0 + (width - size) // 2
        img.alpha_composite(pic, (px_x * S, (shelf_y - size) * S))
        # kleine Begleiter links und rechts
        for idx, extra in enumerate(pictures[1:3]):
            small = art(extra, 1)
            ex = x0 + 3 if idx == 0 else x1 - 3 - 16
            img.alpha_composite(small, (ex * S, (shelf_y - 16) * S))
        return
    count = len(pictures)
    gap = 3
    total = count * 16 + (count - 1) * gap
    start = x0 + (width - total) // 2
    for idx, fn in enumerate(pictures):
        pic = art(fn, 1)
        img.alpha_composite(pic, ((start + idx * (16 + gap)) * S, (shelf_y - 16) * S))


# ------------------------------------------------------------------ Die Tafeln

L = lcs_icons
G = ll_icons

LAYOUTS = {
    # Wirtschaftszentrale (/unternehmen) - LazyChestShops MainMenu
    'wirtschaft': dict(rows=6, panels=[
        ((0, 0, 3, 3), 'cyan', 'UNTERNEHMEN', [L.company, L.treasury, L.members], True),
        ((4, 0, 6, 1), 'green', 'SHOPS', [L.shops, L.claim], False),
        ((7, 0, 8, 1), 'gold', 'TOP', [L.ranking], False),
        ((4, 2, 5, 3), 'orange', 'MARKT', [L.market], False),
        ((6, 2, 8, 3), 'purple', 'ANTEILE', [L.shares, L.dividend], False),
        ((0, 4, 3, 4), 'blue', 'LOGISTIK', [G.transport], False),
        ((4, 4, 8, 4), 'teal', 'SHOPFINDER', [L.price], False),
    ], sockets=[(0, 5), (1, 5), (2, 5), (4, 5), (6, 5), (7, 5), (8, 5)]),

    # Logistikzentrale (/logistik) - LazyLogistics LogisticsMenu
    'logistik': dict(rows=6, panels=[
        ((0, 0, 3, 1), 'cyan', 'LAGER', [G.warehouse, G.crate], False),
        ((4, 0, 8, 1), 'orange', 'AUFTRÄGE', [G.order, G.market, G.escrow], False),
        ((0, 2, 3, 3), 'green', 'TRANSPORTE', [G.transport, G.route], False),
        ((4, 2, 8, 3), 'teal', 'VERSORGUNG', [G.supply, L.shops, G.automation], False),
        ((0, 4, 2, 4), 'purple', 'NETZWERK', [], False),
        ((3, 4, 5, 4), 'blue', 'STATISTIK', [], False),
        ((6, 4, 8, 4), 'gold', 'UPGRADES', [], False),
    ], sockets=[(0, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (8, 5)]),
}

GLYPHS = {}   # Name -> (Zeichen links, Zeichen rechts, Hoehe)


def build_layout(name, spec):
    img = board(spec['rows'])
    for area, accent, label, pictures, hero in spec['panels']:
        panel(img, area, accent, label, pictures, hero)
    for (c, r) in spec['sockets']:
        socket(img, c, r)
    return img


def build_generic(rows, framed):
    """Tafel fuer alle uebrigen Menues: Rahmenfelder als Teil der Tafel, innen vertiefte Plaetze."""
    img = board(rows)
    for r in range(rows):
        for c in range(9):
            border = framed and rows > 2 and (r in (0, rows - 1) or c in (0, 8))
            if not border:
                socket(img, c, r)
    if framed and rows > 2:
        # Zierleiste im Rahmen, damit er nicht leer wirkt
        x0, y0, x1, y1 = cell_box(0, 0, 8, 0)
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 9, hx('#2E333C'))
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 8, hx('#444B57'))
        x0, y0, x1, y1 = cell_box(0, rows - 1, 8, rows - 1)
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 9, hx('#2E333C'))
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 8, hx('#444B57'))
    return img


def save_glyph(img, key, first_codepoint, providers):
    os.makedirs(FONT_TEX, exist_ok=True)
    half = img.size[0] // 2
    height = img.size[1] // S
    chars = []
    for idx, (a, b) in enumerate(((0, half), (half, img.size[0]))):
        part = img.crop((a, 0, b, img.size[1]))
        file = f'{key}_{"l" if idx == 0 else "r"}.png'
        part.save(os.path.join(FONT_TEX, file))
        ch = chr(first_codepoint + idx)
        chars.append(ch)
        providers.append({"type": "bitmap", "file": f"lazymc:font/gui/{file}",
                          "ascent": 13, "height": height, "chars": [ch]})
    GLYPHS[key] = (chars[0], chars[1], height)


def main():
    providers = []
    # Abstaende: U+F801.. nach links (1, 2, 4 ... 128), U+F811.. nach rechts
    advances = {}
    for bit in range(8):
        advances[chr(0xF801 + bit)] = -(1 << bit)
        advances[chr(0xF811 + bit)] = (1 << bit)
    providers.append({"type": "space", "advances": advances})

    code = 0xE000
    previews = {}
    for name, spec in LAYOUTS.items():
        img = build_layout(name, spec)
        save_glyph(img, name, code, providers)
        previews[name] = img
        code += 2
    code = 0xE010
    for rows in range(1, 7):
        save_glyph(build_generic(rows, True), f'frame{rows}', code, providers)
        code += 2
    code = 0xE030
    for rows in range(1, 7):
        save_glyph(build_generic(rows, False), f'plain{rows}', code, providers)
        code += 2
    os.makedirs(os.path.dirname(FONT_FILE), exist_ok=True)
    with open(FONT_FILE, 'w', encoding='utf-8') as f:
        json.dump({"providers": providers}, f, indent=2, ensure_ascii=True)
    for key, (l, r, h) in GLYPHS.items():
        print(f'{key:12s} U+{ord(l):04X} U+{ord(r):04X}  Hoehe {h}')
    return previews


if __name__ == '__main__':
    main()
