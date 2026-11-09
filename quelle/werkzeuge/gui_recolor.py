"""LazyMC v2 GUI-Design: farbt die originalen Minecraft-GUIs in Farbverläufe um (Layout bleibt exakt gleich)."""
from PIL import Image
import os, glob, shutil, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'vanilla/assets/minecraft/textures/gui'
DST = sys.argv[2] if len(sys.argv) > 2 else '../pack/assets/minecraft/textures/gui'

def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): t=max(0,min(1,t)); return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def mul(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)

# Farbverläufe je GUI-Familie (oben-links -> unten-rechts)
THEMES = {
 'default':   ('#78B4FF', '#8C7BFF'),   # Blau -> Violett
 'inventory': ('#6FE3FF', '#5E8BFF'),   # Cyan -> Blau
 'furnace':   ('#7AA6FF', '#B07BFF'),   # Blau -> Lila
 'anvil':     ('#5FE0D0', '#5C8CFF'),   # Türkis -> Blau
 'enchant':   ('#B07BFF', '#FF7BD8'),   # Violett -> Pink
 'brewing':   ('#9A7BFF', '#5FB4FF'),   # Lila -> Blau
 'beacon':    ('#6FF0E0', '#4FA0FF'),   # Türkis -> Blau
 'villager':  ('#7FD0FF', '#6F7BFF'),
 'hud':       ('#3A6BFF', '#7A4CFF'),
}
def theme_for(path):
    n = path.replace('\\','/').lower()
    for key, names in [('inventory',['container/inventory','crafting_table','creative_inventory','recipe_book','crafter']),
                       ('furnace',['furnace','smoker','blast_furnace']),
                       ('anvil',['anvil','smithing','grindstone','stonecutter','cartography','loom']),
                       ('enchant',['enchanting']), ('brewing',['brewing']), ('beacon',['beacon']),
                       ('villager',['villager','horse','hopper','dispenser','shulker'])]:
        if any(x in n for x in names):
            return THEMES[key]
    if '/hud/' in n:
        return THEMES['hud']
    return THEMES['default']

def recolor(im, theme):
    im = im.convert('RGBA'); px = im.load(); W, H = im.size
    bbox = im.getbbox() or (0,0,W,H)
    x0,y0,x1,y1 = bbox; bw=max(1,x1-x0); bh=max(1,y1-y0)
    top, bot = hx(theme[0]), hx(theme[1])
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0:
                continue
            if max(r,g,b) - min(r,g,b) > 12:      # farbige Pixel (Flammen, Pfeile, Symbole) bleiben
                continue
            v = (r+g+b)/3
            t = ((x-x0)/bw*0.35 + (y-y0)/bh*0.65)
            panel = mix(top, bot, t)
            if v < 25:   c = hx('#0A1030')                          # Umriss
            elif v < 70: c = mix(hx('#0A1030'), mul(panel,0.45), (v-25)/45)   # Schatten
            elif v < 110:c = mix(mul(panel,0.45), hx('#1C2A66'), (v-70)/40)   # Slot-Rand
            elif v < 150:c = mix(hx('#1C2A66'), hx('#243A82'), (v-110)/40)    # Slot-Innen
            elif v < 215:c = mix(mix(hx('#243A82'), panel, 0.6), panel, (v-150)/65)  # Fläche
            else:        c = mix(panel, hx('#E4F8FF'), (v-215)/40)              # Licht/Kante
            px[x,y] = c + (a,)
    return im

def hearts(im):
    im = im.convert('RGBA'); px = im.load(); W,H = im.size
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            if r > 120 and r > g + 40:                     # rote Herzpixel -> Rot/Pink-Verlauf mit Glanz
                lum = r/255
                c = mix(hx('#FF2D55'), hx('#FF7AB6'), y/max(1,H-1))
                c = mul(c, 0.55 + 0.5*lum)
                px[x,y] = c + (a,)
            elif max(r,g,b)-min(r,g,b) <= 12:              # Umriss -> dunkles Navy
                v=(r+g+b)/3
                px[x,y] = mix(hx('#0A1030'), hx('#3A4FA0'), v/255) + (a,)
    return im

def xp_progress(im):
    im = im.convert('RGBA'); px = im.load(); W,H = im.size
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            lum = (r+g+b)/3/255
            c = mix(mix(hx('#00E5FF'), hx('#B66DFF'), x/max(1,W-1)), (255,255,255), max(0,lum-0.55))
            px[x,y] = mul(c, 0.6+0.6*lum) + (a,)
    return im

count = 0
def out_path(rel): 
    p = os.path.join(DST, rel); os.makedirs(os.path.dirname(p), exist_ok=True); return p

targets = []
for pattern in ['container/**/*.png', 'sprites/container/**/*.png', 'recipe_book.png', 'sprites/recipe_book/**/*.png',
                'sprites/hud/hotbar*.png', 'sprites/hud/experience_bar_background.png', 'sprites/hud/effect_background*.png',
                'sprites/hud/jump_bar_background.png', 'sprites/hud/heart/*.png', 'sprites/hud/experience_bar_progress.png']:
    targets += glob.glob(os.path.join(SRC, pattern), recursive=True)
for src in sorted(set(targets)):
    rel = os.path.relpath(src, SRC)
    im = Image.open(src)
    if 'heart/' in rel.replace('\\','/'):
        res = hearts(im)
    elif rel.endswith('experience_bar_progress.png'):
        res = xp_progress(im)
    else:
        res = recolor(im, theme_for(rel))
    res.save(out_path(rel)); count += 1
    meta = src + '.mcmeta'
    if os.path.exists(meta):
        shutil.copy(meta, out_path(rel) + '.mcmeta')
print(count, 'Texturen umgefärbt')
