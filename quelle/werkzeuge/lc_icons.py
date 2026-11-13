"""
Symbole fuer LazyCore-Menues (Handel und Ranglisten), im selben Stil wie die uebrigen.

Erzeugt Textur, Modell und Item-Definition je Symbol unter der Kennung lazymc:gui/lc_<name>.
Kachel, Farben und Umriss kommen aus lcs_icons, damit alle LazyMC-Symbole gleich aussehen.
"""
import json
import os

import lcs_icons as base
from lcs_icons import Canvas, ITEMS, MODELS, TEX


def sword(c):
    """Diamantschwert - fuer die Kill-Rangliste."""
    c.poly([(20, 5), (26, 5), (26, 11), (14, 23)], 'c')
    c.poly([(22, 7), (24, 7), (24, 10), (16, 18)], 'W')
    c.rect(9, 20, 17, 23, 'i')
    c.rect(6, 23, 14, 26, 'd')
    c.rect(7, 24, 13, 25, 'e')


def clock(c):
    """Uhr - fuer die Spielzeit-Rangliste."""
    c.ell(5, 5, 27, 27, 'I')
    c.ell(7, 7, 25, 25, 'K')
    c.line([(16, 16), (16, 10)], 'c', 2)
    c.line([(16, 16), (21, 19)], 'W', 2)
    c.ell(15, 15, 17, 17, 'Y')


def handshake(c):
    """Zwei Haende - fuer den Handel."""
    c.rect(4, 14, 14, 19, 'I')
    c.rect(18, 14, 28, 19, 'm')
    c.rect(11, 12, 21, 21, 'N')
    c.rect(13, 14, 19, 19, 'n')


def coins_pile(c):
    """Muenzstapel - fuer das Coinangebot."""
    for idx, yy in enumerate((20, 15, 10)):
        c.ell(8 + idx, yy, 24 - idx, yy + 6, 'Y')
        c.ell(10 + idx, yy + 1, 22 - idx, yy + 4, 'h')


ICONS = {
    'sword': (sword, 'red'),
    'clock': (clock, 'blue'),
    'handshake': (handshake, 'green'),
    'coins': (coins_pile, 'gold'),
}


def main():
    for folder in (TEX, MODELS, ITEMS):
        os.makedirs(folder, exist_ok=True)
    for name, (draw, acc) in ICONS.items():
        canvas = Canvas()
        draw(canvas)
        canvas.finish(acc).save(os.path.join(TEX, f'lc_{name}.png'))
        with open(os.path.join(MODELS, f'lc_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"parent": "minecraft:item/generated",
                       "textures": {"layer0": f"lazymc:item/gui/lc_{name}"}}, f)
        with open(os.path.join(ITEMS, f'lc_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"model": {"type": "minecraft:model",
                                 "model": f"lazymc:item/gui/lc_{name}"}}, f)
    print(f'{len(ICONS)} Symbole geschrieben (lazymc:gui/lc_<name>)')


if __name__ == '__main__':
    main()
