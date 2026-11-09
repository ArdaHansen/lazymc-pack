"""LazyMC v2 'Tech'-GUIs: dunkler Metallrahmen, Neon-Kanten in Serverfarben, Nieten und helle Titelplaketten.
Layout bleibt exakt wie bei Minecraft (umgefärbt aus den Originaltexturen)."""
from PIL import Image
import os, glob, shutil, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'vanilla/assets/minecraft/textures/gui'
DST = sys.argv[2] if len(sys.argv) > 2 else '../pack/assets/minecraft/textures/gui'

def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): t=max(0.0,min(1.0,t)); return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def mul(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)

# Neon-Akzent je Menü-Art (Kante oben-links -> unten-rechts)
ACCENTS = {
 'default':  ('#00E5FF', '#348BFF'),
 'inventory':('#00E5FF', '#35D9D0'),
 'furnace':  ('#348BFF', '#B66DFF'),
 'anvil':    ('#35D9D0', '#348BFF'),
 'enchant':  ('#B66DFF', '#FF77E9'),
 'brewing':  ('#B66DFF', '#348BFF'),
 'beacon':   ('#35D9D0', '#00E5FF'),
}
def accent_for(n):
    n=n.lower()
    for key,names in [('inventory',['container/inventory','crafting_table','creative_inventory','recipe_book','crafter']),
                      ('furnace',['furnace','smoker']),('anvil',['anvil','smithing','grindstone','stonecutter','cartography','loom']),
                      ('enchant',['enchanting']),('brewing',['brewing']),('beacon',['beacon'])]:
        if any(x in n for x in names): return ACCENTS[key]
    return ACCENTS['default']

PANEL_TOP, PANEL_BOT = hx('#16234F'), hx('#0B1230')
PLATE_TOP, PLATE_BOT = hx('#D9F8FF'), hx('#8FD8FF')

def label_bands(rel, H):
    """Zeilen, in denen Minecraft dunkelgraue Beschriftungen zeichnet -> helle Plaketten."""
    n = rel.replace('\\','/')
    if 'beacon' in n or 'sprites/' in n or 'recipe_book' in n: return []
    bands = [(4, 15)]
    if 'generic_54' in n: bands.append((127, 138))
    elif 'hopper' in n: bands.append((37, 48))
    elif H >= 166 and 'creative_inventory' not in n: bands.append((70, 81))
    return bands

def tech(im, rel):
    im = im.convert('RGBA'); px = im.load(); W, H = im.size
    x0,y0,x1,y1 = im.getbbox() or (0,0,W,H); bw=max(1,x1-x0); bh=max(1,y1-y0)
    acc = accent_for(rel); a1, a2 = hx(acc[0]), hx(acc[1])
    bands = label_bands(rel, y1)
    src = im.copy().load()
    def gray(x,y):
        r,g,b,a = src[x,y]
        return a > 0 and max(r,g,b)-min(r,g,b) <= 12, (r+g+b)/3, a
    for y in range(H):
        for x in range(W):
            isg, v, a = gray(x,y)
            if a == 0 or not isg: continue
            t = (x-x0)/bw*0.4 + (y-y0)/bh*0.6
            accent = mix(a1, a2, t)
            if v < 25:                      # äußerer Umriss
                c = hx('#03061A')
            elif v < 70:                    # Schatten (unten/rechts, Slot oben/links)
                c = hx('#060B22')
            elif v < 110:                   # dunkle Kanten
                c = hx('#0E1738')
            elif v < 150:                   # Slot-Innenfläche
                c = mix(hx('#0A1129'), hx('#111C42'), (y-y0)/bh)
            elif v < 215:                   # Fläche: dunkles Metall mit feinem Raster
                c = mix(PANEL_TOP, PANEL_BOT, (y-y0)/bh)
                if (x - x0) % 8 == 0 or (y - y0) % 8 == 0:
                    c = mul(c, 1.18)
                in_band = any(b0 <= y-y0 <= b1 for b0,b1 in bands)
                if in_band:                 # helle Titelplakette (dunkle Schrift bleibt lesbar)
                    b0,b1 = next(bb for bb in bands if bb[0] <= y-y0 <= bb[1])
                    edge = (y-y0) in (b0, b1)
                    c = accent if edge else mix(PLATE_TOP, PLATE_BOT, ((y-y0)-b0)/max(1,b1-b0))
            else:                           # Lichtkanten -> Neon
                c = mix(accent, hx('#FFFFFF'), (v-230)/60)
            px[x,y] = c + (a,)
    # Nieten in den Ecken der Fläche
    for cx, cy in [(x0+5,y0+5),(x1-7,y0+5),(x0+5,y1-7),(x1-7,y1-7)]:
        if 0 <= cx < W-2 and 0 <= cy < H-2 and all(gray(cx+i,cy+j)[0] and 150 <= gray(cx+i,cy+j)[1] < 215 for i in range(2) for j in range(2)):
            px[cx,cy] = hx('#9FB4E8')+(255,); px[cx+1,cy] = hx('#5E74B8')+(255,)
            px[cx,cy+1] = hx('#5E74B8')+(255,); px[cx+1,cy+1] = hx('#2A3768')+(255,)
    return im

count = 0
def out(rel):
    p = os.path.join(DST, rel); os.makedirs(os.path.dirname(p), exist_ok=True); return p
targets = []
for pattern in ['container/**/*.png', 'sprites/container/**/*.png', 'recipe_book.png', 'sprites/recipe_book/**/*.png',
                'sprites/hud/effect_background*.png']:
    targets += glob.glob(os.path.join(SRC, pattern), recursive=True)
for src in sorted(set(targets)):
    rel = os.path.relpath(src, SRC)
    tech(Image.open(src), rel).save(out(rel)); count += 1
    if os.path.exists(src + '.mcmeta'): shutil.copy(src + '.mcmeta', out(rel) + '.mcmeta')
print(count, 'GUI-Texturen im Tech-Stil')
