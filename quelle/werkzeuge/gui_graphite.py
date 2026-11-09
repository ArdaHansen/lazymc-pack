"""LazyMC v2 'Graphit'-GUIs: neutrales dunkles Metall, scharfe 1px-Kanten, Cyan nur als Akzent.
Layout bleibt exakt wie bei Minecraft (umgefärbt aus den Originaltexturen)."""
from PIL import Image
import os, glob, shutil, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'vanilla/assets/minecraft/textures/gui'
DST = sys.argv[2] if len(sys.argv) > 2 else '../pack/assets/minecraft/textures/gui'
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

OUTLINE = hx('#07080B')   # äußerer Umriss
SHADOW  = hx('#101217')   # Schattenkanten
DARK    = hx('#1B1E24')
SLOT    = hx('#16191F')   # Slot-Innenfläche
PANEL   = hx('#2B2F37')   # Fläche (Graphit)
PANEL_L = hx('#30353E')   # obere Hälfte minimal heller
EDGE    = hx('#4A515D')   # Lichtkante innen (neutral)
ACCENT  = hx('#00E5FF')   # Serverfarbe - nur Außenrand
ACCENT2 = hx('#0094FF')
PLATE   = hx('#C9D1DC')   # Titelplakette (Silber)
PLATE_D = hx('#AEB8C6')

def label_bands(rel, H):
    n = rel.replace('\\','/')
    if 'beacon' in n or 'sprites/' in n or 'recipe_book' in n: return []
    bands = [(4, 14)]
    if 'generic_54' in n: bands.append((127, 137))
    elif 'hopper' in n: bands.append((37, 47))
    elif H >= 166 and 'creative_inventory' not in n: bands.append((70, 80))
    return bands

def graphite(im, rel):
    im = im.convert('RGBA'); src = im.copy().load(); px = im.load(); W, H = im.size
    x0,y0,x1,y1 = im.getbbox() or (0,0,W,H)
    bands = label_bands(rel, y1)
    def transparent_near(x, y, d):
        for j in range(-d, d+1):
            for i in range(-d, d+1):
                xx, yy = x+i, y+j
                if xx < 0 or yy < 0 or xx >= W or yy >= H or src[xx,yy][3] == 0:
                    return True
        return False
    for y in range(H):
        for x in range(W):
            r,g,b,a = src[x,y]
            if a == 0 or max(r,g,b)-min(r,g,b) > 12:
                continue
            v = (r+g+b)/3
            if v < 25:   c = OUTLINE
            elif v < 70: c = SHADOW
            elif v < 110:c = DARK
            elif v < 150:c = SLOT
            elif v < 215:
                c = PANEL_L if (y-y0) < (y1-y0)//2 else PANEL
                band = next((bb for bb in bands if bb[0] <= y-y0 <= bb[1]), None)
                if band:
                    yy = y-y0
                    if yy == band[1]: c = ACCENT          # scharfe Cyan-Linie unter der Plakette
                    elif yy == band[0]: c = hx('#E6ECF3')  # Lichtkante oben
                    else: c = PLATE if yy < (band[0]+band[1])//2 + 1 else PLATE_D
            else:
                # Lichtkanten: am Außenrand Cyan-Akzent, innen (Slots) neutral
                if transparent_near(x, y, 3):
                    c = ACCENT if (x-x0) + (y-y0) < (x1-x0) else ACCENT2
                else:
                    c = EDGE
            px[x,y] = c + (a,)
    # Nieten (neutral, scharf)
    for cx, cy in [(x0+5,y0+5),(x1-7,y0+5),(x0+5,y1-7),(x1-7,y1-7)]:
        ok = 0 <= cx < W-1 and 0 <= cy < H-1
        if ok:
            for i in range(2):
                for j in range(2):
                    r,g,b,a = src[cx+i,cy+j]
                    if a == 0 or max(r,g,b)-min(r,g,b) > 12 or not (150 <= (r+g+b)/3 < 215): ok = False
        if ok:
            px[cx,cy] = hx('#8A94A5')+(255,); px[cx+1,cy] = hx('#5B6372')+(255,)
            px[cx,cy+1] = hx('#5B6372')+(255,); px[cx+1,cy+1] = hx('#1B1E24')+(255,)
    return im

def hotbar(src_dir, dst_dir):
    im = Image.open(os.path.join(src_dir,'sprites/hud/hotbar.png')).convert('RGBA'); px = im.load(); W,H = im.size
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            if a < 255: px[x,y] = hx('#0E1014') + (min(190,a),); continue
            v = (r+g+b)/3
            px[x,y] = (OUTLINE if v < 20 else DARK if v < 110 else EDGE) + (255,)
    im.save(os.path.join(dst_dir,'sprites/hud/hotbar.png'))
    im = Image.open(os.path.join(src_dir,'sprites/hud/hotbar_selection.png')).convert('RGBA'); px = im.load(); W,H = im.size
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            if a < 255: px[x,y] = ACCENT + (40,); continue
            v = (r+g+b)/3
            px[x,y] = (OUTLINE if v < 20 else ACCENT2 if v < 140 else ACCENT if v < 200 else hx('#C8FAFF')) + (255,)
    im.save(os.path.join(dst_dir,'sprites/hud/hotbar_selection.png'))

count = 0
def out(rel):
    p = os.path.join(DST, rel); os.makedirs(os.path.dirname(p), exist_ok=True); return p
targets = []
for pattern in ['container/**/*.png','sprites/container/**/*.png','recipe_book.png','sprites/recipe_book/**/*.png',
                'sprites/hud/effect_background*.png','sprites/hud/experience_bar_background.png']:
    targets += glob.glob(os.path.join(SRC, pattern), recursive=True)
for src in sorted(set(targets)):
    rel = os.path.relpath(src, SRC)
    graphite(Image.open(src), rel).save(out(rel)); count += 1
    if os.path.exists(src + '.mcmeta'): shutil.copy(src + '.mcmeta', out(rel) + '.mcmeta')
hotbar(SRC, DST)
print(count, 'GUI-Texturen im Graphit-Stil')
