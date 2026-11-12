"""
Menue-Symbole fuer LazyCosmetics (32x32), im selben Stil wie die uebrigen LazyMC-Symbole.

Erzeugt Textur, Modell und Item-Definition je Symbol unter der Kennung lazymc:gui/lcm_<name>.
Das Plugin setzt sie ueber setItemModel; ohne Pack bleibt einfach das normale Item sichtbar.

Kachel, Farben und der Umriss kommen aus lcs_icons - damit die Symbole beider Plugins
nebeneinander gleich aussehen und eine Stilaenderung nur an einer Stelle gemacht werden muss.
"""
import json
import os

import lcs_icons as base
from lcs_icons import Canvas, ITEMS, MODELS, TEX, hx

# Die Abteilung Namensfarben hat ein Pink, das es in der gemeinsamen Liste noch nicht gab.
base.ACC.setdefault('pink', ('#FFA8DC', '#A83C7E'))

C = base.C
C.setdefault('R', hx('#FF9ED8'))
C.setdefault('r', hx('#C4559B'))
C.setdefault('t', hx('#35D9D0'))
C.setdefault('T', hx('#8CF2EC'))


# ------------------------------------------------------------------ Die Symbole

def titel(c):
    """Namensschild mit Schriftzeile."""
    c.rect(4, 10, 27, 22, 'I')
    c.rect(6, 12, 25, 20, 'K')
    c.rect(8, 14, 23, 15, 'Y')
    c.rect(8, 17, 18, 18, 'i')
    c.rect(3, 14, 5, 18, 'y')


def haustiere(c):
    """Pfote."""
    c.ell(11, 14, 21, 24, 'N')
    for xx in (7, 12, 17, 22):
        c.ell(xx, 8, xx + 5, 13, 'n')


def effekte(c):
    """Funkelnder Stern."""
    c.poly([(16, 3), (19, 13), (29, 16), (19, 19), (16, 29), (13, 19), (3, 16), (13, 13)], 'P')
    c.ell(13, 13, 19, 19, 'W')
    c.rect(24, 5, 25, 10, 'q')
    c.rect(22, 7, 27, 8, 'q')


def spuren(c):
    """Fussspuren, die nach hinten kleiner werden."""
    c.ell(6, 20, 12, 27, 'T')
    c.ell(13, 14, 18, 20, 't')
    c.ell(19, 9, 23, 14, 't')
    c.ell(24, 5, 27, 9, 't')


def namensfarben(c):
    """Farbtropfen mit Pinselstrich."""
    c.poly([(16, 4), (24, 18), (16, 26), (8, 18)], 'R')
    c.poly([(16, 10), (20, 18), (16, 23), (12, 18)], 'W')
    c.rect(5, 27, 27, 29, 'r')


def wardrobe(c):
    """Kleiderbuegel."""
    c.ring(13, 5, 19, 11, 'I', 2)
    c.line([(16, 11), (16, 15)], 'i', 2)
    c.poly([(16, 14), (28, 22), (4, 22)], 'c')
    c.poly([(16, 17), (24, 21), (8, 21)], 'u')


def eye(c):
    """Offenes Auge - eigene Partikel sichtbar."""
    c.ell(3, 10, 29, 22, 'I')
    c.ell(11, 11, 21, 21, 'N')
    c.ell(14, 14, 18, 18, 'K')
    c.ell(14, 12, 16, 14, 'W')


def eye_off(c):
    """Durchgestrichenes Auge - Partikel versteckt."""
    c.ell(3, 10, 29, 22, 'i')
    c.ell(11, 11, 21, 21, 'j')
    c.ell(14, 14, 18, 18, 'K')
    c.line([(5, 26), (27, 6)], 'X', 3)


ICONS = {
    'titel': (titel, 'gold'),
    'haustiere': (haustiere, 'green'),
    'effekte': (effekte, 'purple'),
    'spuren': (spuren, 'cyan'),
    'namensfarben': (namensfarben, 'pink'),
    'wardrobe': (wardrobe, 'pink'),
    'eye': (eye, 'green'),
    'eye_off': (eye_off, 'gray'),
}


def main():
    for folder in (TEX, MODELS, ITEMS):
        os.makedirs(folder, exist_ok=True)
    for name, (draw, acc) in ICONS.items():
        canvas = Canvas()
        draw(canvas)
        canvas.finish(acc).save(os.path.join(TEX, f'lcm_{name}.png'))

        with open(os.path.join(MODELS, f'lcm_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"parent": "minecraft:item/generated",
                       "textures": {"layer0": f"lazymc:item/gui/lcm_{name}"}}, f)
        with open(os.path.join(ITEMS, f'lcm_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"model": {"type": "minecraft:model",
                                 "model": f"lazymc:item/gui/lcm_{name}"}}, f)
    print(f'{len(ICONS)} Symbole geschrieben (lazymc:gui/lcm_<name>)')


if __name__ == '__main__':
    main()
