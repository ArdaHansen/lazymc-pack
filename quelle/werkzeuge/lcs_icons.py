"""
Menue-Symbole fuer LazyChestShops (32x32), im selben Stil wie die uebrigen LazyMC-Symbole.

Erzeugt Textur, Modell und Item-Definition je Symbol unter der Kennung lazymc:gui/lcs_<name>.
Das Plugin setzt sie ueber setItemModel; ohne Pack bleibt einfach das normale Item sichtbar.
"""
from PIL import Image, ImageDraw
import json
import os

HERE = os.path.dirname(__file__)
PACK = os.path.join(HERE, '..', 'pack', 'assets', 'lazymc')
TEX = os.path.join(PACK, 'textures', 'item', 'gui')
MODELS = os.path.join(PACK, 'models', 'item', 'gui')
ITEMS = os.path.join(PACK, 'items', 'gui')


def hx(h, a=255):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


OUT = hx('#07080B')
ACC = {
    'cyan': ('#5FD8E6', '#1E7E8C'),
    'gold': ('#FFD36B', '#B07A1E'),
    'green': ('#7DFFB3', '#2E9E5E'),
    'red': ('#FF8A95', '#A3303C'),
    'blue': ('#7FB8FF', '#2B5FA8'),
    'purple': ('#C9A2FF', '#6A3FB0'),
    'orange': ('#FFB86B', '#B0601E'),
    'gray': ('#AEB8C6', '#5E6673'),
}
C = dict(
    W=hx('#F4F6F8'), g=hx('#8A94A5'), m=hx('#C3CBD6'), K=hx('#1E2026'),
    Y=hx('#FFC94A'), y=hx('#C7922A'), h=hx('#FFE69A'),
    c=hx('#00E5FF'), b=hx('#0094FF'), B=hx('#4DA3FF'), u=hx('#2B5FA8'),
    N=hx('#5CFF9D'), n=hx('#2E9E5E'), X=hx('#FF5A6A'), x=hx('#B8333F'),
    P=hx('#C08BFF'), q=hx('#7A4FC0'), O=hx('#FF9F43'), o=hx('#C46A1A'),
    d=hx('#8B5E3C'), e=hx('#6E4A2E'), I=hx('#D8DEE6'), i=hx('#9AA4B2'), j=hx('#6B7482'),
)


def tile(acc):
    """Die Kachel: dunkler Verlauf, farbiger Rand, vier Nieten - wie bei allen LazyMC-Symbolen."""
    a1, a2 = hx(ACC[acc][0]), hx(ACC[acc][1])
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    px = im.load()
    top, bot = hx('#454B56'), hx('#262A31')
    for yy in range(32):
        for xx in range(32):
            if (xx in (0, 31) and yy in (0, 1, 30, 31)) or (yy in (0, 31) and xx in (0, 1, 30, 31)):
                continue
            if xx in (0, 31) or yy in (0, 31):
                col = OUT
            elif yy == 1 or xx == 1:
                col = a1
            elif yy == 30 or xx == 30:
                col = a2
            else:
                t = (yy - 2) / 27
                col = tuple(int(top[k] * (1 - t) + bot[k] * t) for k in range(3)) + (255,)
            px[xx, yy] = col
    for (xx, yy) in ((3, 3), (28, 3), (3, 28), (28, 28)):
        px[xx, yy] = hx('#7F8896')
    return im


class Canvas:
    def __init__(self):
        self.im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def rect(self, x0, y0, x1, y1, col):
        self.d.rectangle((x0, y0, x1, y1), fill=C.get(col, col))

    def ell(self, x0, y0, x1, y1, col):
        self.d.ellipse((x0, y0, x1, y1), fill=C.get(col, col))

    def ring(self, x0, y0, x1, y1, col, w=2):
        self.d.ellipse((x0, y0, x1, y1), outline=C.get(col, col), width=w)

    def line(self, pts, col, w=2):
        self.d.line(pts, fill=C.get(col, col), width=w)

    def poly(self, pts, col):
        self.d.polygon(pts, fill=C.get(col, col))

    def pie(self, x0, y0, x1, y1, a0, a1, col):
        self.d.pieslice((x0, y0, x1, y1), a0, a1, fill=C.get(col, col))

    def finish(self, acc):
        """Umrandet die Zeichnung und setzt sie auf die Kachel - gibt allen Symbolen dieselbe Tiefe."""
        px = self.im.load()
        out = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        q = out.load()
        for yy in range(32):
            for xx in range(32):
                a = px[xx, yy]
                if a[3]:
                    below = yy + 1 < 32 and px[xx, yy + 1][3]
                    right = xx + 1 < 32 and px[xx + 1, yy][3]
                    above = yy > 0 and px[xx, yy - 1][3]
                    left = xx > 0 and px[xx - 1, yy][3]
                    col = a
                    if not below or not right:
                        col = tuple(int(v * 0.78) for v in a[:3]) + (255,)
                    elif not above or not left:
                        col = tuple(min(255, int(v * 1.12)) for v in a[:3]) + (255,)
                    q[xx, yy] = col
                elif any(0 <= xx + dx < 32 and 0 <= yy + dy < 32 and px[xx + dx, yy + dy][3]
                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    q[xx, yy] = OUT
        base = tile(acc)
        base.alpha_composite(out)
        return base


# ------------------------------------------------------------------ Die Symbole

def company(c):
    """Buerohaus mit Fenstern."""
    c.rect(9, 9, 22, 25, 'i')
    c.rect(11, 8, 20, 9, 'I')
    for yy in (12, 16, 20):
        for xx in (11, 15, 19):
            c.rect(xx, yy, xx + 2, yy + 2, 'c')
    c.rect(14, 22, 17, 25, 'u')


def company_new(c):
    company(c)
    c.rect(22, 18, 28, 20, 'N')
    c.rect(24, 16, 26, 22, 'N')


def shops(c):
    """Truhe."""
    c.rect(6, 13, 25, 25, 'd')
    c.rect(6, 10, 25, 14, 'e')
    c.rect(14, 15, 17, 20, 'Y')
    c.rect(15, 17, 16, 19, 'K')


def shop_pending(c):
    shops(c)
    c.rect(20, 5, 27, 12, 'O')
    c.rect(22, 7, 25, 8, 'K')
    c.rect(24, 8, 25, 10, 'K')
    c.rect(23, 10, 25, 11, 'K')


def market(c):
    """Zwei Haende, die etwas uebergeben."""
    c.rect(5, 15, 14, 19, 'I')
    c.rect(18, 15, 27, 19, 'I')
    c.rect(12, 12, 20, 22, 'N')
    c.rect(14, 14, 18, 20, 'n')


def shares(c):
    """Tortendiagramm."""
    c.ell(7, 7, 25, 25, 'j')
    c.pie(7, 7, 25, 25, 270, 90, 'P')
    c.pie(7, 7, 25, 25, 90, 200, 'B')
    c.ring(7, 7, 25, 25, 'K', 1)


def treasury(c):
    """Muenzstapel."""
    for idx, yy in enumerate((20, 16, 12)):
        c.ell(8 + idx, yy, 24 - idx, yy + 6, 'Y')
        c.ell(10 + idx, yy + 1, 22 - idx, yy + 4, 'h')


def members(c):
    """Zwei Personen."""
    c.ell(6, 8, 14, 16, 'I')
    c.rect(5, 17, 15, 24, 'B')
    c.ell(17, 10, 25, 18, 'm')
    c.rect(16, 19, 26, 25, 'u')


def invite(c):
    """Briefumschlag."""
    c.rect(5, 10, 27, 23, 'I')
    c.poly([(5, 10), (16, 19), (27, 10)], 'i')
    c.line([(5, 23), (14, 17)], 'j', 1)
    c.line([(27, 23), (18, 17)], 'j', 1)


def upgrade(c):
    """Pfeil nach oben auf Sockel."""
    c.poly([(16, 5), (26, 16), (20, 16), (20, 23), (12, 23), (12, 16), (6, 16)], 'N')
    c.rect(9, 25, 23, 27, 'n')


def profile(c):
    """Ausweis."""
    c.rect(4, 8, 28, 24, 'I')
    c.rect(4, 8, 28, 11, 'B')
    c.ell(7, 13, 14, 20, 'j')
    for yy in (14, 17, 20):
        c.rect(16, yy, 25, yy + 1, 'j')


def rating(c):
    """Stern."""
    c.poly([(16, 4), (20, 13), (29, 14), (22, 20), (24, 29), (16, 24), (8, 29), (10, 20), (3, 14), (12, 13)], 'Y')


def dividend(c):
    """Muenze, die sich aufteilt."""
    c.ell(11, 4, 21, 14, 'Y')
    c.line([(16, 14), (8, 22)], 'h', 2)
    c.line([(16, 14), (24, 22)], 'h', 2)
    c.ell(4, 21, 12, 29, 'Y')
    c.ell(20, 21, 28, 29, 'Y')


def price(c):
    """Lupe ueber einem Preisschild."""
    c.poly([(4, 16), (14, 6), (24, 16), (14, 26)], 'O')
    c.ell(8, 11, 14, 17, 'K')
    c.ring(15, 6, 29, 20, 'I', 3)
    c.line([(26, 18), (30, 24)], 'I', 3)


def claim(c):
    """Paket mit Schleife."""
    c.rect(5, 12, 27, 26, 'd')
    c.rect(5, 9, 27, 13, 'e')
    c.rect(14, 9, 18, 26, 'N')
    c.rect(5, 16, 27, 18, 'N')


def link(c):
    """Kettenglieder."""
    c.ring(4, 11, 17, 22, 'c', 3)
    c.ring(15, 11, 28, 22, 'b', 3)


def stats(c):
    """Balkendiagramm."""
    c.rect(5, 25, 27, 27, 'j')
    c.rect(7, 17, 11, 25, 'B')
    c.rect(14, 11, 18, 25, 'N')
    c.rect(21, 6, 25, 25, 'Y')


def ranking(c):
    """Siegertreppchen."""
    c.rect(4, 18, 11, 27, 'j')
    c.rect(12, 11, 20, 27, 'Y')
    c.rect(21, 21, 28, 27, 'o')
    c.poly([(16, 4), (18, 8), (22, 8), (19, 11), (20, 15), (16, 12), (12, 15), (13, 11), (10, 8), (14, 8)], 'h')


def hud(c):
    """Bildschirm mit Zeilen."""
    c.rect(4, 7, 28, 23, 'j')
    c.rect(6, 9, 26, 21, 'K')
    c.rect(8, 11, 20, 12, 'c')
    for yy in (14, 17):
        c.rect(8, yy, 23, yy + 1, 'i')
    c.rect(13, 24, 19, 27, 'j')


def journal(c):
    """Buch mit Lesezeichen."""
    c.rect(6, 5, 25, 27, 'I')
    c.rect(6, 5, 10, 27, 'u')
    for yy in (10, 14, 18, 22):
        c.rect(12, yy, 22, yy + 1, 'j')
    c.poly([(19, 5), (24, 5), (24, 15), (21, 12), (19, 15)], 'X')


ICONS = {
    'company': (company, 'gold'),
    'company_new': (company_new, 'green'),
    'shops': (shops, 'green'),
    'shop_pending': (shop_pending, 'orange'),
    'market': (market, 'orange'),
    'shares': (shares, 'purple'),
    'treasury': (treasury, 'gold'),
    'members': (members, 'orange'),
    'invite': (invite, 'orange'),
    'upgrade': (upgrade, 'cyan'),
    'profile': (profile, 'blue'),
    'rating': (rating, 'gold'),
    'dividend': (dividend, 'green'),
    'price': (price, 'cyan'),
    'claim': (claim, 'green'),
    'link': (link, 'cyan'),
    'stats': (stats, 'blue'),
    'ranking': (ranking, 'gold'),
    'hud': (hud, 'cyan'),
    'journal': (journal, 'red'),
}


def main():
    for folder in (TEX, MODELS, ITEMS):
        os.makedirs(folder, exist_ok=True)
    for name, (draw, acc) in ICONS.items():
        canvas = Canvas()
        draw(canvas)
        canvas.finish(acc).save(os.path.join(TEX, f'lcs_{name}.png'))

        with open(os.path.join(MODELS, f'lcs_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"parent": "minecraft:item/generated",
                       "textures": {"layer0": f"lazymc:item/gui/lcs_{name}"}}, f)
        with open(os.path.join(ITEMS, f'lcs_{name}.json'), 'w', encoding='utf-8') as f:
            json.dump({"model": {"type": "minecraft:model",
                                 "model": f"lazymc:item/gui/lcs_{name}"}}, f)
    print(f'{len(ICONS)} Symbole geschrieben (lazymc:gui/lcs_<name>)')


if __name__ == '__main__':
    main()
