"""Escape-Menue im LazyMC-Pixelstil (2x Aufloesung): Knoepfe, Regler, Textfelder, Checkboxen, Scrollbar + Panda auf dem Logo."""
from PIL import Image, ImageDraw
import json, os
PACK='/home/claude/work/pack/assets/minecraft/'
W_DIR=PACK+'textures/gui/sprites/widget/'
def hx(h,a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
OUT=hx('#07080B')
def grad(w,h,top,bot):
    im=Image.new('RGBA',(w,h)); px=im.load(); t1,t2=hx(top),hx(bot)
    for y in range(h):
        t=y/max(1,h-1); c=tuple(int(t1[i]*(1-t)+t2[i]*t) for i in range(3))+(255,)
        for x in range(w): px[x,y]=c
    return im
def frame(w,h,top,bot,edge_top,edge_bot,hl,sh,rivets='#7F8896',accent=None):
    """w,h in Texturpixeln (2x). Rahmen 2px, abgeschnittene Ecken."""
    im=grad(w,h,top,bot); px=im.load()
    for y in range(h):
        for x in range(w):
            if x<2 or y<2 or x>=w-2 or y>=h-2: px[x,y]=OUT
            elif y<4: px[x,y]=hx(edge_top)
            elif y>=h-4: px[x,y]=hx(edge_bot)
            elif x<4: px[x,y]=hx(edge_top) if y<h//2 else hx(edge_bot)
            elif x>=w-4: px[x,y]=hx(edge_top) if y<h//2 else hx(edge_bot)
            elif y<6: px[x,y]=hx(hl)
            elif y>=h-6: px[x,y]=hx(sh)
    for (x,y) in [(0,0),(1,0),(0,1),(w-1,0),(w-2,0),(w-1,1),(0,h-1),(1,h-1),(0,h-2),(w-1,h-1),(w-2,h-1),(w-1,h-2)]: px[x,y]=(0,0,0,0)
    for (x,y) in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]: px[x,y]=OUT
    if accent:
        for x in range(8,w-8):
            for y in (h-6,h-5): px[x,y]=hx(accent)
    if rivets:
        for (x,y) in [(7,7),(w-9,7),(7,h-9),(w-9,h-9)]:
            for dx in range(2):
                for dy in range(2): px[x+dx,y+dy]=hx(rivets) if (dx,dy)!=(1,1) else hx('#1B1E24')
    return im
def save(name, im, scaling=None):
    im.save(W_DIR+name+'.png')
    meta=W_DIR+name+'.png.mcmeta'
    if scaling: json.dump({"gui":{"scaling":scaling}}, open(meta,'w'))
    elif os.path.exists(meta): os.remove(meta)
NS=lambda w,h,b: {"type":"nine_slice","width":w,"height":h,"border":b}
# Knoepfe 200x20 -> 400x40
save('button', frame(400,40,'#4A505B','#2C3038','#5E6673','#1B1E24','#59606C','#24272E',accent='#1E7E8C'), NS(200,20,4))
save('button_highlighted', frame(400,40,'#566070','#353B46','#5FD8E6','#1E7E8C','#6A7484','#2A2F38',rivets='#5FD8E6',accent='#00E5FF'), NS(200,20,4))
save('button_disabled', frame(400,40,'#2E3238','#24272C','#3A3F47','#16181C','#33373E','#1E2024',rivets='#3A3F47'), NS(200,20,4))
# Textfeld / Regler-Schiene: dunkle Mulde
def inset(w,h,edge,glow=None):
    im=Image.new('RGBA',(w,h),hx('#14171C')); px=im.load()
    for y in range(h):
        for x in range(w):
            if x<2 or y<2 or x>=w-2 or y>=h-2: px[x,y]=hx(edge)
            elif y<4: px[x,y]=hx('#0C0E12')
            elif glow and y>=h-4: px[x,y]=hx(glow)
    return im
save('text_field', inset(400,40,'#4A515D'), NS(200,20,4))
save('text_field_highlighted', inset(400,40,'#00E5FF','#0E3E46'), NS(200,20,4))
def track(hl):
    im=inset(400,40,'#5FD8E6' if hl else '#4A515D'); d=ImageDraw.Draw(im)
    d.rectangle((12,18,387,21), fill=hx('#2B2F37')); d.rectangle((12,18,387,18), fill=hx('#0C0E12'))
    return im
save('slider', track(False), NS(200,20,4)); save('slider_highlighted', track(True), NS(200,20,4))
def handle(hl):
    im=frame(16,40,'#6A7484' if hl else '#5A616E','#3A404B','#5FD8E6' if hl else '#7F8896','#1E7E8C' if hl else '#2B2F37','#7C8696','#30343C',rivets=None)
    d=ImageDraw.Draw(im); d.rectangle((6,10,9,29), fill=hx('#00E5FF' if hl else '#5FD8E6')); d.rectangle((6,10,9,10), fill=hx('#C8FAFF'))
    return im
save('slider_handle', handle(False), NS(8,20,3)); save('slider_handle_highlighted', handle(True), NS(8,20,3))
# Checkbox 20x20 -> 40x40 (kein Nine-Slice)
def checkbox(sel, hl):
    im=frame(40,40,'#3A404B','#24272E','#5FD8E6' if hl else '#5E6673','#1E7E8C' if hl else '#1B1E24','#454B56','#1E2127',rivets=None)
    d=ImageDraw.Draw(im); d.rectangle((8,8,31,31), fill=hx('#14171C'))
    if sel:
        d.line([(12,20),(18,26),(28,13)], fill=hx('#00E5FF'), width=4)
        d.line([(12,19),(18,25),(28,12)], fill=hx('#C8FAFF'), width=1)
    return im
for sel in (False,True):
    for hl in (False,True):
        save('checkbox'+('_selected' if sel else '')+('_highlighted' if hl else ''), checkbox(sel,hl))
# Scrollbar 6x32 -> 12x64
sc=frame(12,64,'#6A7484','#3A404B','#5FD8E6','#1E7E8C','#7C8696','#30343C',rivets=None); save('scroller', sc, NS(6,32,1))
save('scroller_background', inset(12,64,'#2B2F37'), NS(6,32,1))

# ---------------------------------------------------------------- Panda auf dem Logo
P={'K':hx('#1E2026'),'W':hx('#F4F6F8'),'g':hx('#8A94A5'),'m':hx('#C3CBD6'),'p':hx('#F2A7B8'),'c':hx('#00E5FF')}
LYING=[".......................ccc",
       "..................cccc..c..",
       "...................c..ccc..",
       "KK........KK......c........",
       "KKKWWWWWWKKK......cccc.....",
       ".WWWWWWWWWWWKKKKWWWWWWWKK.",
       "WWKKWWWWKKWKKKKWWWWWWWWWKK",
       "WKggWWWWggKWKKWWWWWWWWWWWK",
       "WWWWWKKWWWWWWWWWWWWWWWWWWK",
       "WpWWWmmWWWpWWWWWWWWWWWWWKK",
       ".WWWWWWWWWWKKKWWWWWWWKKKK.",
       "..WWWWWWWW.KKKK....KKKKK..",
       "...........KKK.......KK...",
       "............K..............."[:27]]
w=len(LYING[0]); h=len(LYING)
g=Image.new('RGBA',(w+2,h+2),(0,0,0,0)); px=g.load()
for y,row in enumerate(LYING):
    for x,ch in enumerate(row):
        if ch in P: px[x+1,y+1]=P[ch]
# Umriss + Schattierung
o=Image.new('RGBA',g.size,(0,0,0,0)); q=o.load(); W2,H2=g.size
for y in range(H2):
    for x in range(W2):
        a=px[x,y]
        if a[3]:
            below = y+1<H2 and px[x,y+1][3]; right = x+1<W2 and px[x+1,y][3]
            q[x,y] = tuple(int(v*0.8) for v in a[:3])+(255,) if (not below or not right) and a!=P['c'] else a
        elif any(0<=x+dx<W2 and 0<=y+dy<H2 and px[x+dx,y+dy][3] and px[x+dx,y+dy]!=P['c'] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
            q[x,y]=hx('#07080B')
panda=o.resize((o.width*3,o.height*3),Image.NEAREST)
panda.save(PACK+'textures/font/lazymc_panda.png')
f=PACK+'font/default.json'; d=json.load(open(f))
d['providers']=[p for p in d['providers'] if p.get('chars')!=['']]
d['providers'].append({"type":"bitmap","file":"minecraft:font/lazymc_panda.png","ascent":38,"height":o.height*3//2,"chars":[""]})
json.dump(d,open(f,'w'),indent=2)
PW=round(o.width*1.5)
def shift(n):
    s=''; base=0xE4E0 if n<0 else 0xE4E8; v=abs(n)
    for bit in range(7,-1,-1):
        if v & (1<<bit): s+=chr(base+bit)
    return s
title=""+shift(-48)+""+shift(48-PW)
for lang in ('de_de','en_us'):
    json.dump({"menu.game":title}, open(PACK+'lang/'+lang+'.json','w'))
print('Panda', o.size, 'Titel', [hex(ord(ch)) for ch in title])
