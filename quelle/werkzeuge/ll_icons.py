"""
Menue-Symbole fuer LazyLogistics (32x32), im selben Stil wie die LazyChestShops-Symbole.

Erzeugt Textur, Modell und Item-Definition je Symbol unter der Kennung lazymc:gui/ll_<name>.
Zeichnet mit denselben Hilfen wie lcs_icons.py, damit alle Symbole dieselbe Tiefe haben.

Die Zeichenfunktionen werden auch von gui_boards.py benutzt, um die grossen Bilder auf den
Panels der Hauptmenues zu malen.
"""
import json
import os

from lcs_icons import Canvas, TEX, MODELS, ITEMS


def warehouse(c):
    """Regal mit Kisten."""
    c.rect(4, 6, 27, 27, 'j')
    c.rect(6, 8, 25, 25, 'K')
    c.rect(6, 15, 25, 16, 'i')
    c.rect(6, 24, 25, 25, 'i')
    c.rect(7, 9, 14, 14, 'd')
    c.rect(16, 10, 23, 14, 'e')
    c.rect(7, 18, 13, 23, 'e')
    c.rect(15, 17, 24, 23, 'd')
    c.rect(10, 11, 11, 12, 'Y')
    c.rect(19, 19, 20, 20, 'Y')


def warehouse_add(c):
    warehouse(c)
    c.rect(21, 3, 29, 5, 'N')
    c.rect(24, 0, 26, 8, 'N')


def order(c):
    """Lieferschein auf Klemmbrett."""
    c.rect(7, 5, 24, 28, 'd')
    c.rect(9, 8, 22, 26, 'I')
    c.rect(12, 3, 19, 7, 'i')
    for yy in (11, 15, 19):
        c.rect(11, yy, 20, yy + 1, 'j')
    c.ell(16, 20, 22, 26, 'O')
    c.rect(18, 22, 20, 24, 'h')


def transport(c):
    """Lieferwagen."""
    c.rect(3, 10, 19, 22, 'B')
    c.rect(3, 10, 19, 12, 'I')
    c.rect(19, 14, 27, 22, 'u')
    c.rect(21, 15, 25, 18, 'c')
    c.rect(2, 22, 29, 24, 'j')
    c.ell(6, 21, 12, 27, 'K')
    c.ell(8, 23, 10, 25, 'i')
    c.ell(19, 21, 25, 27, 'K')
    c.ell(21, 23, 23, 25, 'i')


def supply(c):
    """Trichter, der in eine Kiste fuellt."""
    c.poly([(5, 4), (26, 4), (19, 13), (12, 13)], 'i')
    c.rect(5, 4, 26, 6, 'm')
    c.rect(13, 13, 18, 16, 'j')
    c.rect(6, 18, 25, 28, 'd')
    c.rect(6, 17, 25, 19, 'e')
    c.rect(14, 21, 17, 24, 'Y')


def network(c):
    """Verbundene Knoten."""
    c.line([(9, 9), (22, 9)], 'i', 2)
    c.line([(9, 9), (9, 22)], 'i', 2)
    c.line([(9, 22), (22, 22)], 'i', 2)
    c.line([(22, 9), (22, 22)], 'i', 2)
    c.line([(9, 9), (22, 22)], 'j', 1)
    c.ell(4, 4, 13, 13, 'c')
    c.ell(18, 4, 27, 13, 'P')
    c.ell(4, 18, 13, 27, 'N')
    c.ell(18, 18, 27, 27, 'Y')


def compass(c):
    """Kompass."""
    c.ell(4, 4, 27, 27, 'j')
    c.ell(6, 6, 25, 25, 'I')
    c.poly([(16, 7), (19, 16), (16, 15), (13, 16)], 'X')
    c.poly([(16, 24), (13, 16), (16, 17), (19, 16)], 'u')
    c.rect(15, 15, 16, 16, 'K')


def contract(c):
    """Vertrag mit Siegel und Feder."""
    c.rect(6, 4, 23, 27, 'I')
    for yy in (8, 12, 16):
        c.rect(9, yy, 20, yy + 1, 'j')
    c.ell(14, 19, 22, 27, 'X')
    c.ell(16, 21, 20, 25, 'x')
    c.line([(28, 3), (21, 16)], 'W', 2)
    c.line([(28, 3), (25, 4)], 'g', 2)


def route(c):
    """Strecke zwischen zwei Punkten."""
    c.line([(8, 24), (14, 14), (20, 18), (25, 8)], 'Y', 2)
    c.ell(3, 19, 12, 28, 'N')
    c.ell(6, 22, 9, 25, 'K')
    c.poly([(25, 2), (30, 8), (25, 15), (20, 8)], 'X')
    c.ell(23, 6, 27, 10, 'h')


def priority(c):
    """Warndreieck mit Ausrufezeichen."""
    c.poly([(16, 3), (29, 27), (3, 27)], 'O')
    c.poly([(16, 8), (25, 24), (7, 24)], 'Y')
    c.rect(15, 11, 17, 19, 'K')
    c.rect(15, 21, 17, 22, 'K')


def recommend(c):
    """Gluehbirne."""
    c.ell(8, 3, 24, 19, 'Y')
    c.ell(11, 6, 17, 12, 'h')
    c.rect(12, 18, 20, 22, 'i')
    c.rect(12, 23, 20, 24, 'j')
    c.rect(14, 25, 18, 27, 'j')


def deliver(c):
    """Paket mit Pfeil hinein."""
    c.rect(5, 15, 27, 28, 'd')
    c.rect(5, 13, 27, 16, 'e')
    c.rect(14, 13, 18, 28, 'h')
    c.poly([(16, 12), (9, 5), (13, 5), (13, 1), (19, 1), (19, 5), (23, 5)], 'N')


def pickup(c):
    """Paket mit Pfeil heraus."""
    c.rect(5, 15, 27, 28, 'd')
    c.rect(5, 13, 27, 16, 'e')
    c.rect(14, 13, 18, 28, 'h')
    c.poly([(16, 1), (23, 8), (19, 8), (19, 12), (13, 12), (13, 8), (9, 8)], 'B')


def escrow(c):
    """Schloss vor einer Muenze."""
    c.ell(14, 4, 28, 18, 'Y')
    c.ell(17, 7, 25, 15, 'h')
    c.ring(5, 7, 15, 19, 'i', 2)
    c.rect(3, 14, 17, 27, 'm')
    c.rect(9, 18, 11, 23, 'K')


def crate(c):
    """Versiegelte Frachtkiste."""
    c.rect(4, 8, 27, 27, 'd')
    c.rect(4, 8, 27, 10, 'e')
    c.line([(5, 11), (26, 26)], 'e', 2)
    c.line([(26, 11), (5, 26)], 'e', 2)
    c.rect(13, 14, 18, 21, 'X')
    c.rect(14, 15, 17, 16, 'h')


def market(c):
    """Auftragsmarkt: Tafel mit Zetteln."""
    c.rect(3, 5, 28, 25, 'd')
    c.rect(5, 7, 26, 23, 'e')
    c.rect(7, 9, 13, 15, 'I')
    c.rect(16, 9, 23, 16, 'h')
    c.rect(9, 17, 16, 22, 'N')
    c.rect(19, 18, 24, 22, 'c')
    c.rect(6, 25, 8, 29, 'e')
    c.rect(23, 25, 25, 29, 'e')


def capacity(c):
    """Fuellstandsanzeige."""
    c.rect(5, 5, 26, 27, 'j')
    c.rect(7, 7, 24, 25, 'K')
    c.rect(9, 17, 22, 23, 'N')
    c.rect(9, 12, 22, 15, 'Y')
    c.rect(9, 9, 22, 10, 'X')


def plot_link(c):
    """Zwei Grundstuecke mit Pfeil."""
    c.rect(2, 14, 12, 26, 'n')
    c.poly([(1, 15), (7, 8), (13, 15)], 'x')
    c.rect(20, 14, 30, 26, 'n')
    c.poly([(19, 15), (25, 8), (31, 15)], 'u')
    c.poly([(13, 18), (18, 18), (18, 15), (21, 20), (18, 25), (18, 22), (13, 22)], 'Y')


def automation(c):
    """Zahnrad mit Pfeil im Kreis."""
    c.ring(5, 5, 26, 26, 'c', 3)
    c.poly([(23, 2), (29, 9), (21, 10)], 'c')
    c.ell(11, 11, 20, 20, 'i')
    c.ell(14, 14, 17, 17, 'K')


def location(c):
    """Kartennadel."""
    c.ell(8, 3, 24, 19, 'X')
    c.poly([(9, 14), (23, 14), (16, 28)], 'X')
    c.ell(12, 7, 20, 15, 'W')


def log(c):
    """Protokoll mit Uhr."""
    c.rect(4, 4, 21, 27, 'I')
    for yy in (8, 12, 16, 20):
        c.rect(7, yy, 18, yy + 1, 'j')
    c.ell(16, 16, 29, 29, 'B')
    c.ell(18, 18, 27, 27, 'I')
    c.rect(22, 19, 23, 23, 'K')
    c.rect(22, 22, 25, 23, 'K')


def failed(c):
    """Kiste mit rotem Kreuz."""
    c.rect(5, 12, 27, 27, 'd')
    c.rect(5, 10, 27, 13, 'e')
    c.line([(9, 2), (23, 16)], 'X', 3)
    c.line([(23, 2), (9, 16)], 'X', 3)


def done(c):
    """Kiste mit Haken."""
    c.rect(5, 12, 27, 27, 'd')
    c.rect(5, 10, 27, 13, 'e')
    c.line([(8, 7), (13, 13), (25, 1)], 'N', 3)


ICONS = {
    'warehouse': (warehouse, 'cyan'),
    'warehouse_add': (warehouse_add, 'green'),
    'order': (order, 'orange'),
    'transport': (transport, 'green'),
    'supply': (supply, 'cyan'),
    'network': (network, 'purple'),
    'compass': (compass, 'purple'),
    'contract': (contract, 'gold'),
    'route': (route, 'blue'),
    'priority': (priority, 'orange'),
    'recommend': (recommend, 'gold'),
    'deliver': (deliver, 'green'),
    'pickup': (pickup, 'blue'),
    'escrow': (escrow, 'gold'),
    'crate': (crate, 'red'),
    'market': (market, 'orange'),
    'capacity': (capacity, 'blue'),
    'plot_link': (plot_link, 'green'),
    'automation': (automation, 'cyan'),
    'location': (location, 'red'),
    'log': (log, 'blue'),
    'failed': (failed, 'red'),
    'done': (done, 'green'),
}


def main():
    for folder in (TEX, MODELS, ITEMS):
        os.makedirs(folder, exist_ok=True)
    for name, (draw, acc) in ICONS.items():
        canvas = Canvas()
        draw(canvas)
        canvas.finish(acc).save(os.path.join(TEX, f'll_{name}.png'))
        with open(os.path.join(MODELS, f'll_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"parent": "minecraft:item/generated",
                       "textures": {"layer0": f"lazymc:item/gui/ll_{name}"}}, f)
        with open(os.path.join(ITEMS, f'll_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"model": {"type": "minecraft:model",
                                 "model": f"lazymc:item/gui/ll_{name}"}}, f)
    print(f'{len(ICONS)} Symbole geschrieben (lazymc:gui/ll_<name>)')


if __name__ == '__main__':
    main()
