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

import gui_deko
import lc_icons
import lcm_icons
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

OUTLINE = hx('#02060F')
EDGE_A = hx('#3FF2FF')     # Neonkante oben
EDGE_B = hx('#1E8CFF')     # Neonkante unten
BOARD_TOP = hx('#13285A')
BOARD_BOT = hx('#0A1638')
STRIP_TOP = hx('#1C3D7E')
STRIP_BOT = hx('#0F2452')
INSET = hx('#081430')
INSET_DARK = hx('#040A1C')
INSET_LIGHT = hx('#1F4A8C')
SOCKET = hx('#0B1A3E')
SOCKET_HI = hx('#2D5BA8')
SOCKET_LO = hx('#030814')
STONE_HI = hx('#FFFFFF')   # Steinschrift wie im LAZYMC-V2-Logo
STONE_LO = hx('#C9D5EA')
STONE_CRACK = hx('#93A3C4')
TEXT_RIM = hx('#050C22')
LOGO = os.path.join(HERE, '..', 'logo', 'lazymc_v2.png')

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
    'pink':   ('#FFB3E3', '#E05BB8', '#7A2460'),
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


# Schrift der Plaketten (5 x 5, wie "WIRTSCHAFT" oben) - wird aus den Plaketten-Kacheln gelesen,
# damit Titel und Panel-Beschriftungen genau gleich aussehen.
HEADER_DIR = os.path.join(HERE, '..', 'pack', 'assets', 'minecraft', 'textures', 'font', 'header')
_HEADER_NAMES = {'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '&': 'and', '-': 'minus', '+': 'plus'}
_PLATE = {}


def plate_glyph(ch):
    """5 Zeilen Bitmuster eines Zeichens aus der Plakettenschrift."""
    if ch in _PLATE:
        return _PLATE[ch]
    if ch == ' ':
        rows = ['...'] * 5
    elif ch == '!':
        rows = ['#', '#', '#', '.', '#']
    elif ch in 'ÄÖÜ':
        # Punkte eine Reihe ueber dem Buchstaben, darunter der normale Buchstabe
        base = plate_glyph({'Ä': 'A', 'Ö': 'O', 'Ü': 'U'}[ch])
        rows = ['.#.#.'] + base
    else:
        name = _HEADER_NAMES.get(ch, 'n' + ch if ch.isdigit() else ch.lower())
        im = Image.open(os.path.join(HEADER_DIR, f'c_{name}.png')).convert('RGBA')
        px = im.load()
        white = [(x, y) for y in range(im.size[1]) for x in range(im.size[0])
                 if px[x, y][3] and sum(px[x, y][:3]) > 600]
        x0 = min(p[0] for p in white)
        x1 = max(p[0] for p in white)
        y1 = max(p[1] for p in white)
        top = 8   # Oberkante der Grossbuchstaben in den Kacheln
        rows = []
        for uy in range(5):
            yy = top + uy * 3
            rows.append(''.join('#' if yy <= y1 and px[x0 + ux * 3, yy][3]
                                and sum(px[x0 + ux * 3, yy][:3]) > 600 else '.'
                                for ux in range((x1 - x0) // 3 + 1)))
    _PLATE[ch] = rows
    return rows


TEXT_H = 5   # Hoehe der Beschriftung in Menuepixeln


def text_width(text):
    return sum(len(plate_glyph(ch)[0]) + 1 for ch in text) - 1


def draw_text(img, x, y, text, color, outline, glow=None):
    """
    Beschriftung in der Plakettenschrift: weisse Buchstaben (unterste Reihe leicht blaugrau),
    ein feiner Rand von einem Texturpixel und ein Schatten darunter in der Panelfarbe.
    """
    px = img.load()
    fill = {}
    cx = x
    for ch in text:
        glyph = plate_glyph(ch)
        lift = len(glyph) - 5          # Umlaute ragen eine Reihe nach oben
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == '#':
                    for dx in range(S):
                        for dy in range(S):
                            fill[((cx + gx) * S + dx, (y + gy - lift) * S + dy)] = gy - lift
        cx += len(glyph[0]) + 1
    solid = set(fill)
    rim = set()
    for (tx, ty) in solid:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                rim.add((tx + dx, ty + dy))
    rim -= solid
    shadow = {(tx, ty + 1) for (tx, ty) in rim} - rim - solid
    shade = mix(outline, glow, 0.45) if glow is not None else outline
    w, h = img.size

    def dot(p, col):
        if 0 <= p[0] < w and 0 <= p[1] < h:
            px[p] = col

    for p in shadow:
        dot(p, shade)
    for p in rim:
        dot(p, outline)
    for p, row in fill.items():
        dot(p, STONE_LO if (color == STONE_HI and row == 4) else color)


def blend(px, size, x, y, col, t):
    """Mischt einen Menuepixel mit einer Farbe (fuer Glow)."""
    for dx in range(S):
        for dy in range(S):
            tx, ty = x * S + dx, y * S + dy
            if 0 <= tx < size[0] and 0 <= ty < size[1]:
                cur = px[tx, ty]
                if cur[3]:
                    px[tx, ty] = mix(cur, col, t)


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

def neon_frame(img, height, top=True, bottom=True, ca=None, cb=None):
    """Dunkler Umriss, Neonkante (Cyan nach Blau) und ein schwacher Schein nach innen."""
    px = img.load()
    rect(img, 0, 0, 0, height - 1, OUTLINE)
    rect(img, W - 1, 0, W - 1, height - 1, OUTLINE)
    if top:
        rect(img, 0, 0, W - 1, 0, OUTLINE)
    if bottom:
        rect(img, 0, height - 1, W - 1, height - 1, OUTLINE)
    for y in range(1 if top else 0, height - 1 if bottom else height):
        t = y / max(1, height - 1)
        edge = mix(ca or EDGE_A, cb or EDGE_B, t)
        for x in (1, W - 2):
            put(px, img.size, x, y, edge)
        for x in (2, W - 3):
            blend(px, img.size, x, y, edge, 0.35)
    if top:
        rect(img, 1, 1, W - 2, 1, EDGE_A)
        for x in range(2, W - 2):
            blend(px, img.size, x, 2, EDGE_A, 0.30)
    if bottom:
        rect(img, 1, height - 2, W - 2, height - 2, EDGE_B)
        for x in range(2, W - 2):
            blend(px, img.size, x, height - 3, EDGE_B, 0.30)
    corners = []
    if top:
        corners += [(0, 0), (W - 1, 0)]
    if bottom:
        corners += [(0, height - 1), (W - 1, height - 1)]
    for (cx, cy) in corners:
        put(px, img.size, cx, cy, (0, 0, 0, 0))


def rivet(img, x, y):
    """Kleine Neon-Raute als Niete."""
    px = img.load()
    put(px, img.size, x, y, EDGE_A)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        blend(px, img.size, x + dx, y + dy, EDGE_A, 0.45)


def board(rows, strip=True):
    """Die Grundtafel: Navy mit Neonkante, Titelleiste und dunkler Innenbereich."""
    height = 17 + rows * 18 + 1
    img = Image.new('RGBA', (W * S, height * S), (0, 0, 0, 0))
    gradient(img, 0, 0, W - 1, height - 1, BOARD_TOP, BOARD_BOT)
    # Unten offen - der Inventarteil schliesst nahtlos an.
    neon_frame(img, height, top=True, bottom=False, cb=mix(EDGE_A, EDGE_B, 0.5))
    if strip:
        gradient(img, 3, 3, W - 4, 15, STRIP_TOP, STRIP_BOT)
        rect(img, 3, 16, W - 4, 16, EDGE_B)
        px = img.load()
        for x in range(3, W - 3):
            blend(px, img.size, x, 15, EDGE_B, 0.35)
        rect(img, 3, 3, W - 4, 3, mix(STRIP_TOP, EDGE_A, 0.35))
        for (nx, ny) in ((6, 9), (W - 7, 9)):
            rivet(img, nx, ny)
        # rechts in der Titelleiste: Spitzhacke und Edelstein wie im Logo
        deko(img, 'pickaxe', W - 30, 5)
        deko(img, 'gem', W - 20, 5)
    # Innenbereich der Felder
    rect(img, 6, 17, W - 7, 17 + rows * 18, INSET_DARK)
    rect(img, 7, 17, W - 8, 16 + rows * 18, INSET)
    rect(img, 6, 17 + rows * 18, W - 7, 17 + rows * 18, INSET_LIGHT)
    rect(img, W - 7, 17, W - 7, 17 + rows * 18, INSET_LIGHT)
    return img


BOTTOM_H = 95   # Inventarteil: von 18*Reihen+18 bis zum Ende des Menues


def bottom():
    """Der Inventarteil unter jeder Tafel - Steinplatte fuer 'Inventar', 27 + 9 Plaetze."""
    img = Image.new('RGBA', (W * S, BOTTOM_H * S), (0, 0, 0, 0))
    gradient(img, 0, 0, W - 1, BOTTOM_H - 1, BOARD_BOT, hx('#07102A'))
    neon_frame(img, BOTTOM_H, top=False, bottom=True, ca=mix(EDGE_A, EDGE_B, 0.5))
    # helle Steinplatte hinter der Beschriftung 'Inventar' (dunkle Vanilla-Schrift bleibt lesbar)
    gradient(img, 6, 1, W - 7, 10, hx('#E6EDF8'), hx('#B7C5DE'))
    rect(img, 6, 1, W - 7, 1, hx('#FFFFFF'))
    rect(img, 6, 10, W - 7, 10, hx('#8D9EBE'))
    rect(img, 6, 11, W - 7, 11, EDGE_B)
    px = img.load()
    # kleine Figuren auf der Steinplatte, rechts neben 'Inventar'
    for idx, name in enumerate(('grass', 'pickaxe', 'chest', 'coins', 'gem', 'torch')):
        deko(img, name, 64 + idx * 16, 2)
    rivet(img, W - 12, 6)
    for (y0, count) in ((12, 3), (70, 1)):
        rect(img, 6, y0 - 1, W - 7, y0 + 18 * count, INSET_DARK)
        rect(img, 6, y0 + 18 * count, W - 7, y0 + 18 * count, INSET_LIGHT)
        for r in range(count):
            for c in range(9):
                x0, y = 7 + 18 * c, y0 + 18 * r
                rect(img, x0, y, x0 + 17, y + 17, SOCKET_LO)
                rect(img, x0 + 1, y + 1, x0 + 17, y + 17, SOCKET_HI)
                rect(img, x0 + 1, y + 1, x0 + 16, y + 16, SOCKET)
    return img


def deko(img, name, x, y, scale=1):
    """Setzt eine kleine Figur (8 x 8 Menuepixel, bei scale=2 ein ganzes Feld)."""
    fig = gui_deko.figure(name)
    if scale != 1:
        fig = fig.resize((16 * scale, 16 * scale), Image.NEAREST)
    img.alpha_composite(fig, (x * S, y * S))


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


def logo(width):
    """Das LAZYMC-V2-Logo, auf 'width' Menuepixel verkleinert (in doppelter Aufloesung)."""
    src = Image.open(LOGO).convert('RGBA')
    w = width * S
    h = round(src.size[1] * w / src.size[0])
    small = src.resize((w, h), Image.LANCZOS)
    # weiche Kanten haerter machen, damit es zum Pixel-Look passt
    q = small.load()
    for yy in range(h):
        for xx in range(w):
            r, g, b, a = q[xx, yy]
            q[xx, yy] = (r, g, b, 0 if a < 90 else 255)
    return small


def panel(img, area, accent, label, pictures, hero=False):
    """
    Ein Panel ueber mehreren Feldern - dunkles Glas mit Neonrand in der Panelfarbe.

    area     (c0, r0, c1, r1)
    pictures Liste von Zeichenfunktionen, die auf einem Regalbrett stehen
    """
    light, mid, dark = (hx(c) for c in ACCENT[accent])
    x0, y0, x1, y1 = cell_box(*area)
    x0, y0, x1, y1 = x0 + 1, y0 + 1, x1 - 1, y1 - 1
    px = img.load()
    rect(img, x0, y0, x1, y1, OUTLINE)
    fill_top = mix(BOARD_TOP, mid, 0.34)
    fill_bot = mix(INSET, dark, 0.50)
    gradient(img, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill_top, fill_bot)
    # Neonrand
    rect(img, x0 + 1, y0 + 1, x1 - 1, y0 + 1, light)
    rect(img, x0 + 1, y0 + 1, x0 + 1, y1 - 1, mix(light, mid, 0.4))
    rect(img, x1 - 1, y0 + 1, x1 - 1, y1 - 1, mid)
    rect(img, x0 + 1, y1 - 1, x1 - 1, y1 - 1, mix(mid, dark, 0.4))
    for xx in range(x0 + 2, x1 - 1):
        blend(px, img.size, xx, y0 + 2, light, 0.30)
        blend(px, img.size, xx, y1 - 2, mid, 0.20)
    for yy in range(y0 + 2, y1 - 1):
        blend(px, img.size, x0 + 2, yy, light, 0.25)
        blend(px, img.size, x1 - 2, yy, mid, 0.25)
    for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        put(px, img.size, cx, cy, INSET)
    # feines Punktraster wie ein Display
    for yy in range(y0 + 4, y1 - 3):
        for xx in range(x0 + 4, x1 - 3):
            if (xx + yy) % 6 == 0 and (xx - yy) % 6 == 0:
                blend(px, img.size, xx, yy, mid, 0.40)

    height = y1 - y0 + 1
    width = x1 - x0 + 1
    single_row = height < 24

    if single_row:
        if pictures:
            pic = art(pictures[0], 1)
            img.alpha_composite(pic, ((x0 + 1) * S, (y0 + 0) * S))
            free = x1 - 2 - (x0 + 19)
            tx = x0 + 19 + max(0, (free - text_width(label)) // 2)
        else:
            tx = x0 + (width - text_width(label)) // 2
        draw_text(img, tx, y0 + (height - TEXT_H) // 2, label, STONE_HI, TEXT_RIM, mid)
        return

    tx = x0 + (width - text_width(label)) // 2
    draw_text(img, tx, y0 + 4, label, STONE_HI, TEXT_RIM, mid)

    # Regalbrett als Neonlinie
    shelf_y = y1 - 4
    rect(img, x0 + 3, shelf_y, x1 - 3, shelf_y + 1, mix(dark, OUTLINE, 0.4))
    rect(img, x0 + 3, shelf_y, x1 - 3, shelf_y, light)

    if not pictures:
        return
    if hero:
        # Kleines LAZYMC-Logo unter der Beschriftung, darunter das Unternehmen
        mark = logo(width - 10)
        mh = mark.size[1] // S
        img.alpha_composite(mark, ((x0 + 5) * S, (y0 + 14) * S))
        size = 32
        pic = art(pictures[0], 2)
        img.alpha_composite(pic, ((x0 + (width - size) // 2) * S, (shelf_y - size) * S))
        for idx, extra in enumerate(pictures[1:3]):
            small = art(extra, 1)
            ex = x0 + 4 if idx == 0 else x1 - 4 - 16
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
K = lcm_icons
C = lc_icons

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
    ], sockets=[(0, 5), (1, 5), (2, 5), (4, 5), (6, 5), (7, 5), (8, 5)],
        deko=[(3, 5, 'torch'), (5, 5, 'torch')]),

    # Unternehmens-Dashboard - LazyChestShops CompanyMenu
    'unternehmen': dict(rows=6, panels=[
        ((0, 0, 3, 1), 'gold', 'KASSE', [L.treasury, L.dividend], False),
        ((4, 0, 6, 1), 'orange', 'TEAM', [L.members, L.invite], False),
        ((7, 0, 8, 1), 'green', 'SHOPS', [L.shops], False),
        ((0, 2, 2, 3), 'purple', 'ANTEILE', [L.shares], False),
        ((3, 2, 5, 3), 'blue', 'ZAHLEN', [L.stats], False),
        ((6, 2, 8, 3), 'teal', 'UPGRADES', [L.upgrade], False),
        ((0, 4, 3, 4), 'green', 'GEWINN', [L.dividend], False),
        ((4, 4, 8, 4), 'cyan', 'LOGISTIK', [G.transport], False),
    ], sockets=[(0, 5), (1, 5), (2, 5), (4, 5), (6, 5), (8, 5)],
        deko=[(3, 5, 'coins'), (5, 5, 'gem'), (7, 5, 'torch')]),

    # Kleiderkammer (/kosmetik) - LazyCosmetics MainMenu
    # Jede Abteilung bekommt ihre eigene Farbe, damit man schon an der Tafel sieht,
    # wo man ist - dieselbe Farbe fuehrt im Abteilungsmenue weiter.
    'kosmetik': dict(rows=6, panels=[
        ((0, 0, 2, 1), 'gold', 'TITEL', [K.titel], False),
        ((3, 0, 5, 1), 'pink', 'NAMEN', [K.namensfarben], False),
        ((6, 0, 8, 1), 'purple', 'EFFEKTE', [K.effekte], False),
        ((0, 2, 3, 3), 'teal', 'SPUREN', [K.spuren], False),
        ((4, 2, 8, 3), 'green', 'HAUSTIERE', [K.haustiere], False),
        ((0, 4, 4, 4), 'blue', 'ANSICHT', [K.eye, K.eye_off], False),
        ((5, 4, 8, 4), 'red', 'ABLEGEN', [], False),
    ], sockets=[(0, 5), (2, 5), (4, 5), (6, 5), (8, 5)],
        deko=[(1, 5, 'gem'), (3, 5, 'torch'), (5, 5, 'torch'), (7, 5, 'gem')]),

    # Handelsfenster (/trade) - LazyCore TradeMenu
    # Links die eigene Seite, rechts die des Partners, dazwischen eine Mittellinie.
    # Die Felder muessen zu TradeMenu.MINE und TradeMenu.THEIRS passen.
    'handel': dict(rows=6, panels=[
        ((0, 0, 3, 0), 'cyan', 'DU', [C.handshake], False),
        ((5, 0, 8, 0), 'orange', 'PARTNER', [C.coins_pile], False),
    ], sockets=[(c, r) for r in (1, 2, 3) for c in (1, 2, 3, 5, 6, 7)]
        + [(1, 4), (3, 4), (5, 4), (7, 4), (4, 5)],
        deko=[(4, 1, 'coins'), (4, 3, 'gem')]),

    # Ranglisten (/topspieler) - LazyCore LeaderboardMenu
    'topspieler': dict(rows=6, panels=[
        ((0, 0, 3, 2), 'gold', 'UNTERNEHMEN', [L.company], False),
        ((5, 0, 8, 2), 'green', 'BARGELD', [L.treasury], False),
        ((0, 3, 3, 4), 'red', 'KILLS', [C.sword], False),
        ((5, 3, 8, 4), 'blue', 'STUNDEN', [C.clock], False),
    ], sockets=[(0, 5), (2, 5), (4, 5), (6, 5), (8, 5)]),

    # Belohnungen (/belohnungen) - LazyCore RewardsMenu
    # Oben die Woche, darunter links die Stufen und rechts die Spielzeit. Die Felder
    # muessen zu RewardsMenu.DAYS, .LEVELS und .HOURS passen.
    'belohnungen': dict(rows=6, panels=[
        ((0, 0, 8, 0), 'red', 'TÄGLICH', [C.gift], False),
        ((0, 2, 3, 2), 'blue', 'STUFEN', [C.stairs], False),
        ((5, 2, 8, 2), 'gold', 'STUNDEN', [C.clock], False),
    ], sockets=[(c, 1) for c in range(1, 8)]
        + [(c, r) for r in (3, 4) for c in (1, 2, 3, 5, 6, 7)]
        + [(4, 5), (8, 5)],
        deko=[(4, 2, 'torch')]),

    # Logistikzentrale (/logistik) - LazyLogistics LogisticsMenu
    'logistik': dict(rows=6, panels=[
        ((0, 0, 3, 1), 'cyan', 'LAGER', [G.warehouse, G.crate], False),
        ((4, 0, 8, 1), 'orange', 'AUFTRÄGE', [G.order, G.market, G.escrow], False),
        ((0, 2, 3, 3), 'green', 'TRANSPORTE', [G.transport, G.route], False),
        ((4, 2, 8, 3), 'teal', 'VERSORGUNG', [G.supply, L.shops, G.automation], False),
        ((0, 4, 2, 4), 'purple', 'NETZWERK', [], False),
        ((3, 4, 5, 4), 'blue', 'STATISTIK', [], False),
        ((6, 4, 8, 4), 'gold', 'UPGRADES', [], False),
    ], sockets=[(0, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (8, 5)],
        deko=[(1, 5, 'chest'), (7, 5, 'grass')]),
}

GLYPHS = {}   # Name -> (Zeichen links, Zeichen rechts, Hoehe)


def build_layout(name, spec):
    img = board(spec['rows'])
    for area, accent, label, pictures, hero in spec['panels']:
        panel(img, area, accent, label, pictures, hero)
    for (c, r) in spec['sockets']:
        socket(img, c, r)
    for (c, r, name) in spec.get('deko', []):
        x0, y0, _, _ = cell_box(c, r, c, r)
        deko(img, name, x0 + 5, y0 + 5)
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
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 9, INSET_DARK)
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 8, EDGE_B)
        x0, y0, x1, y1 = cell_box(0, rows - 1, 8, rows - 1)
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 9, INSET_DARK)
        rect(img, x0 + 3, y0 + 8, x1 - 3, y0 + 8, EDGE_B)
        # seitliche Leisten und Nieten auf den Feldgrenzen - liegen nie unter einem Knopf
        top = cell_box(0, 0, 0, 0)[1] + 8
        bottom_line = cell_box(0, rows - 1, 0, rows - 1)[1] + 8
        for xs in (cell_box(0, 0, 0, 0)[0] + 8, cell_box(8, 0, 8, 0)[0] + 9):
            rect(img, xs, top, xs, bottom_line, EDGE_B)
        for c in range(1, 9):
            bx = 7 + 18 * c
            rivet(img, bx, top)
            rivet(img, bx, bottom_line)
        # oben in den Ecken je eine kleine Figur (dort liegt nie ein Knopf)
        for (c, name) in ((0, 'gem'), (8, 'pickaxe')):
            cx0, cy0, _, _ = cell_box(c, 0, c, 0)
            deko(img, name, cx0 + 1, cy0 + 1, scale=2)
        for r in range(1, rows):
            by = 17 + 18 * r
            rivet(img, cell_box(0, 0, 0, 0)[0] + 8, by)
            rivet(img, cell_box(8, 0, 8, 0)[0] + 9, by)
    return img


def save_glyph(img, key, first_codepoint, providers, ascent=13):
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
                          "ascent": ascent, "height": height, "chars": [ch]})
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
    # Feste Zeichen je Tafel - neue Tafeln hinten anhaengen, nie umnummerieren.
    fixed = {'wirtschaft': 0xE000, 'logistik': 0xE002, 'unternehmen': 0xE004,
             'kosmetik': 0xE006, 'handel': 0xE008, 'topspieler': 0xE00A,
             'belohnungen': 0xE00C}
    for name, spec in LAYOUTS.items():
        img = build_layout(name, spec)
        save_glyph(img, name, fixed[name], providers)
        previews[name] = img
    code = 0xE010
    for rows in range(1, 7):
        save_glyph(build_generic(rows, True), f'frame{rows}', code, providers)
        code += 2
    code = 0xE030
    for rows in range(1, 7):
        save_glyph(build_generic(rows, False), f'plain{rows}', code, providers)
        code += 2
    # Inventarteil je Reihenzahl: beginnt 18*Reihen+18 Pixel unter dem Tafelanfang
    code = 0xE050
    low = bottom()
    for rows in range(1, 7):
        save_glyph(low, f'bottom{rows}', code, providers, ascent=13 - (18 * rows + 18))
        code += 2
    previews['bottom'] = low
    os.makedirs(os.path.dirname(FONT_FILE), exist_ok=True)
    with open(FONT_FILE, 'w', encoding='utf-8') as f:
        json.dump({"providers": providers}, f, indent=2, ensure_ascii=True)
    for key, (l, r, h) in GLYPHS.items():
        print(f'{key:12s} U+{ord(l):04X} U+{ord(r):04X}  Hoehe {h}')
    return previews


if __name__ == '__main__':
    main()
