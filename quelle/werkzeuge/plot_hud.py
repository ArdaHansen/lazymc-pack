"""Plot-Anzeige ueber der Hotbar: Plakette mit Haus-Symbol (Font lazymc:hud, Textur 2x)."""
from PIL import Image
import json, os
PACK='/home/claude/work/pack/'
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
OUT=hx('#07080B'); CY=hx('#5FD8E6'); CYD=hx('#1E7E8C'); TOP=hx('#4A505B'); BOT=hx('#30343C'); INNER=hx('#1B1E24')
H=28  # Texturhoehe (=14 Pixel im Spiel)
def body(w, left=False, right=False):
    im=Image.new('RGBA',(w,H),(0,0,0,0)); px=im.load()
    for y in range(H):
        t=y/(H-1); fill=tuple(int(TOP[i]*(1-t)+BOT[i]*t) for i in range(3))
        for x in range(w):
            if y<2 or y>=H-2: c=OUT
            elif y<4: c=CY
            elif y>=H-4: c=CYD
            elif y<5: c=INNER
            else: c=fill
            px[x,y]=c+(255,)
    def edge(xs, outer_first=True):
        for i,x in enumerate(xs):
            for y in range(H):
                if i<2: c=OUT
                elif i<4: c=CY if y < H//2 else CYD
                else: c=INNER if 4<=y<H-4 else None
                if c and 2<=y<H-2 or (c and i<2): px[x,y]=c+(255,)
    if left:
        edge([0,1,2,3,4])
        for (x,y) in [(0,0),(1,0),(0,1),(0,H-1),(1,H-1),(0,H-2)]: px[x,y]=(0,0,0,0)
        px[1,1]=OUT+(255,); px[1,H-2]=OUT+(255,)
    if right:
        edge([w-1,w-2,w-3,w-4,w-5])
        for (x,y) in [(w-1,0),(w-2,0),(w-1,1),(w-1,H-1),(w-2,H-1),(w-1,H-2)]: px[x,y]=(0,0,0,0)
        px[w-2,1]=OUT+(255,); px[w-2,H-2]=OUT+(255,)
    return im
def house(im, ox, oy):
    px=im.load()
    # Kachel-Hintergrund (dunkle Mulde)
    for y in range(oy-1, oy+21):
        for x in range(ox-1, ox+21):
            px[x,y]=hx('#1A1D23')+(255,)
    for x in range(ox-1,ox+21): px[x,oy-1]=hx('#101217')+(255,); px[x,oy+20]=hx('#5E6673')+(255,)
    roof=hx('#00E5FF'); roofd=hx('#0094FF'); wall=hx('#E8EEF4'); walld=hx('#B9C3CF'); door=hx('#2B2F37'); win=hx('#7FF3FF'); o=hx('#07080B')
    cx=ox+10
    for r in range(9):   # Dach (Dreieck)
        y=oy+1+r
        for x in range(cx-1-r, cx+1+r):
            edge = x in (cx-1-r, cx+r) or r==8
            px[x,y]=(o if edge else (roof if x<cx else roofd))+(255,)
    for y in range(oy+10, oy+19):   # Wand
        for x in range(ox+3, ox+17):
            edge = x in (ox+3, ox+16) or y==oy+18
            px[x,y]=(o if edge else (wall if x<cx+2 else walld))+(255,)
    for y in range(oy+13, oy+18):   # Tuer
        for x in range(ox+8, ox+12): px[x,y]=door+(255,)
    for y in range(oy+11, oy+14):   # Fenster
        for x in range(ox+13, ox+16): px[x,y]=win+(255,)
    for y in range(oy+2, oy+6):     # Schornstein
        for x in range(ox+14, ox+16): px[x,y]=o+(255,)
d=PACK+'assets/lazymc/textures/font/hud/'; os.makedirs(d,exist_ok=True)
glyphs=[]
left=body(36,left=True); house(left,7,4)
for y in range(6,H-6): left.load()[32,y]=hx('#1B1E24')+(255,); left.load()[33,y]=hx('#5E6673')+(255,)
left.save(d+'left.png'); glyphs.append(('left.png',0xE600))
for i,w in enumerate([1,2,4,8,16,32]):
    body(w*2).save(d+f'mid{w}.png'); glyphs.append((f'mid{w}.png',0xE601+i))
body(8,right=True).save(d+'right.png'); glyphs.append(('right.png',0xE607))
prov=[{"type":"bitmap","file":"lazymc:font/hud/"+f,"ascent":10,"height":14,"chars":[chr(c)]} for f,c in glyphs]
adv={"":-1}
for i in range(8):
    adv[chr(0xE6E0+i)]=-(1<<i); adv[chr(0xE6E8+i)]=(1<<i)
prov.append({"type":"space","advances":adv})
os.makedirs(PACK+'assets/lazymc/font',exist_ok=True)
json.dump({"providers":prov},open(PACK+'assets/lazymc/font/hud.json','w'),indent=2)
# Vorschau
pv=Image.new('RGBA',(36+64+32+8+20,40),(70,90,60,255))
x=10; 
for im in [left, body(64), body(64), body(8,right=True)]:
    pv.alpha_composite(im,(x,6)); x+=im.width
pv.resize((pv.width*5,pv.height*5),Image.NEAREST).save('/home/claude/work/hud_preview.png')
print('ok')
