"""Hintergrund der Coinflip-Animation: ersetzt im 3-reihigen Kistenmenue das Slot-Raster durch eine
schlichte Rolle (7 Plaetze) mit goldenem Zeiger. Zwei Haelften als Schrift-Zeichen U+E450/U+E451."""
from PIL import Image, ImageDraw
import json, os, random
PACK = '/home/claude/work/pack/assets/minecraft/'
S = 2                                   # Textur-Pixel pro Menue-Pixel
W, H = 176, 71                          # oberer Teil eines 3-reihigen Kistenmenues
GOLD, GOLD_D, GOLD_L, GOLD_OUT = (255, 212, 71, 255), (201, 154, 30, 255), (255, 236, 150, 255), (58, 44, 5, 255)

base = Image.open(PACK + 'textures/gui/container/generic_54.png').convert('RGBA').crop((0, 0, W, H))
im = base.resize((W * S, H * S), Image.NEAREST)
px = im.load()
d = ImageDraw.Draw(im)
rnd = random.Random(7)

# Slot-Raster uebermalen: ruhige Flaeche wie der Rand der Platte
for y in range(17 * S, H * S):
    t = (y - 17 * S) / (H * S - 17 * S)
    for x in range(7 * S, 169 * S):
        n = rnd.choice((-1, 0, 0, 1))
        px[x, y] = (int(0x45 - 4 * t) + n, int(0x4B - 5 * t) + n, int(0x56 - 6 * t) + n, 255)

def rect(x0, y0, x1, y1, c):            # Menue-Koordinaten, x1/y1 exklusiv
    d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=c)

# Rolle: vertiefte Leiste hinter den Plaetzen 10-16 (Items bei x 26..150, y 36..52)
X0, X1, Y0, Y1 = 22, 154, 32, 56
d.rounded_rectangle([X0 * S, Y0 * S, X1 * S - 1, Y1 * S - 1], radius=5, fill=(7, 8, 11, 255))
d.rounded_rectangle([X0 * S + 2, Y0 * S + 2, X1 * S - 3, Y1 * S - 3], radius=3, fill=(24, 27, 33, 255))
for y in range(Y0 * S + 2, Y1 * S - 2):                      # zu den Enden hin dunkler
    for x in range(X0 * S + 2, X1 * S - 2):
        if px[x, y][:3] != (24, 27, 33):
            continue
        edge = min(x - X0 * S, X1 * S - 1 - x) / (30.0 * S)
        k = 0.55 + 0.45 * min(1.0, edge)
        top = 0.8 if y < Y0 * S + 5 else 1.0                 # Schatten oben
        px[x, y] = (int(24 * k * top), int(27 * k * top), int(33 * k * top), 255)
d.line([X0 * S + 5, Y1 * S, X1 * S - 6, Y1 * S], fill=(94, 102, 115, 255))   # Lichtkante unten

# Mitte: der Platz unter dem Zeiger
CX = 88
d.rectangle([(CX - 10) * S, Y0 * S + 2, (CX + 10) * S - 1, Y1 * S - 3], fill=(46, 39, 16, 255))
for x in ((CX - 10) * S, (CX + 10) * S - 2):
    d.rectangle([x, Y0 * S + 2, x + 1, Y1 * S - 3], fill=GOLD)
    d.rectangle([x, Y1 * S - 9, x + 1, Y1 * S - 3], fill=GOLD_D)

def pointer(tip_y, direction):          # direction 1 = zeigt nach unten, -1 = nach oben
    rows = 12
    for i in range(rows):
        half = i + 1                    # Spitze (an der Rolle) schmal, Basis breit
        y = tip_y * S - direction * (i + 1) + (0 if direction == 1 else -1)
        for x in range(CX * S - half, CX * S + half):
            c = GOLD
            if x < CX * S - half + 2 or x >= CX * S + half - 2 or i >= rows - 2:
                c = GOLD_OUT
            elif x < CX * S - half + 4:
                c = GOLD_L
            elif x >= CX * S + half - 5:
                c = GOLD_D
            px[x, y] = c
pointer(31, 1)
pointer(57, -1)

os.makedirs(PACK + 'textures/font/coinflip', exist_ok=True)
halves = [im.crop((0, 0, 88 * S, H * S)), im.crop((88 * S, 0, W * S, H * S))]
f = PACK + 'font/default.json'
data = json.load(open(f))
data['providers'] = [p for p in data['providers'] if 'font/coinflip/' not in p.get('file', '')]
for name, half, cp in (('reel_l', halves[0], 0xE450), ('reel_r', halves[1], 0xE451)):
    assert half.size[0] <= 256 and half.size[1] <= 256
    # aeusserste Spalte muss deckend sein, sonst stimmt die Zeichenbreite nicht
    assert any(half.getpixel((half.size[0] - 1, y))[3] > 0 for y in range(half.size[1]))
    half.save(PACK + 'textures/font/coinflip/' + name + '.png')
    data['providers'].append({"type": "bitmap", "file": "minecraft:font/coinflip/" + name + ".png",
                              "ascent": 13, "height": H, "chars": [chr(cp)]})
for p in data['providers']:
    if p.get('type') == 'bitmap':
        assert p['ascent'] <= p['height'], p
json.dump(data, open(f, 'w'), indent=2)
im.save('/tmp/claude-0/scratch/coinflip/reel_full.png')
print('ok', im.size)
