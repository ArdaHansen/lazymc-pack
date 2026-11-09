"""Fix Logo-Panda (ascent <= height) + Info-Platte im Pausenmenue unter 'Verbindung trennen'."""
from PIL import Image, ImageDraw
import json, re
PACK='/home/claude/work/pack/assets/minecraft/'
def hx(h,a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
def shift(n):
    s=''; base=0xE4E0 if n<0 else 0xE4E8; v=abs(n)
    for bit in range(7,-1,-1):
        if v & (1<<bit): s+=chr(base+bit)
    return s
f=PACK+'font/default.json'; d=json.load(open(f))
# ---- 1) Panda: Zeichen-Hoehe muss >= ascent sein -> Textur nach unten transparent verlaengern
p=Image.open(PACK+'textures/font/lazymc_panda.png').convert('RGBA')
bb=p.getbbox(); p=p.crop((0,0,p.width,bb[3]))            # 3 Texturpixel je Panda-Pixel, 2 Texturpixel = 1 GUI-Pixel
H_GUI=38; canvas=Image.new('RGBA',(p.width,H_GUI*2),(0,0,0,0)); canvas.alpha_composite(p,(0,0))
canvas.save(PACK+'textures/font/lazymc_panda.png')
d['providers']=[x for x in d['providers'] if x.get('chars') not in ([''],[''],[''])]
d['providers'].append({"type":"bitmap","file":"minecraft:font/lazymc_panda.png","ascent":H_GUI,"height":H_GUI,"chars":[""]})
PW=p.width//2
title=""+shift(-48)+""+shift(48-PW)

# ---- 2) Info-Platte (2x Aufloesung, in zwei Haelften wegen der 256-Pixel-Grenze)
src=open('/tmp/claude-0/scratch/headers.py').read()
F=eval(src[src.index('F={')+2:src.index("\ndef hx")])
F.update({'.':["..","..","..","..","#."],',':["..","..","..",".#","#."],'!':["#","#","#",".","#"],':':[".","#",".","#","."]})
def text(d, x, y, s, col, shadow=hx('#05060A')):
    for ch in s.upper():
        g=F.get(ch, F[' '])
        for oy,c in ((1,shadow),(0,col)):
            for yy,row in enumerate(g):
                for xx,v in enumerate(row):
                    if v=='#': d.rectangle((x+(xx+ (1 if oy else 0))*2, y+(yy+oy)*2, x+(xx+(1 if oy else 0))*2+1, y+(yy+oy)*2+1), fill=c)
        x+=(len(g[0])+1)*2
    return x
def width(s): return sum((len(F.get(ch,F[' '])[0])+1)*2 for ch in s.upper())-2
L1="DISCORD.LAZYMC.DE"; L2="SCHÖN, DASS DU HIER BIST!"
ICON=26
W=max(width(L1)+ICON+8, width(L2))+28; W+=W%4; H=52
im=Image.new('RGBA',(W,H),(0,0,0,0)); px=im.load()
top,bot=hx('#454B56'),hx('#2A2E36')
for y in range(H):
    t=y/(H-1); fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))+(255,)
    for x in range(W):
        if x<2 or y<2 or x>=W-2 or y>=H-2: c=hx('#07080B')
        elif x<4 or y<4: c=hx('#5FD8E6')
        elif x>=W-4 or y>=H-4: c=hx('#1E7E8C')
        elif y<6: c=hx('#1B1E24')
        else: c=fill
        px[x,y]=c
for (x,y) in [(0,0),(1,0),(0,1),(W-1,0),(W-2,0),(W-1,1),(0,H-1),(1,H-1),(0,H-2),(W-1,H-1),(W-2,H-1),(W-1,H-2)]: px[x,y]=(0,0,0,0)
for (x,y) in [(8,8),(W-10,8),(8,H-10),(W-10,H-10)]:
    for dx in range(2):
        for dy in range(2): px[x+dx,y+dy]=hx('#7F8896')
dr=ImageDraw.Draw(im)
# Zeile 1: blaues Chat-Symbol + Adresse (mittig)
w1=ICON+8+width(L1); x=(W-w1)//2; y=10
B=hx('#5B7CFF'); Bd=hx('#3A55C8')
dr.rectangle((x,y,x+ICON-1,y+13), fill=B); dr.rectangle((x+2,y-2,x+ICON-3,y+15), fill=B)
dr.polygon([(x+6,y+15),(x+6,y+21),(x+12,y+15)], fill=B); dr.rectangle((x+2,y+14,x+ICON-3,y+15), fill=Bd)
for k in range(3): dr.rectangle((x+5+k*6,y+5,x+8+k*6,y+8), fill=hx('#FFFFFF'))
text(dr, x+ICON+8, y+2, L1, hx('#00E5FF'))
# Zeile 2
text(dr, (W-width(L2))//2, 34, L2, hx('#E6EBF0'))
half=W//2
im.crop((0,0,half,H)).save(PACK+'textures/font/lazymc_info_l.png'); im.crop((half,0,W,H)).save(PACK+'textures/font/lazymc_info_r.png')
# Platte beginnt 3 Pixel unter dem Knopf: Oberkante = Textoberkante + 17  ->  ascent = 7 - 17
for name,ch in (('l',''),('r','')):
    d['providers'].append({"type":"bitmap","file":f"minecraft:font/lazymc_info_{name}.png","ascent":-10,"height":H//2,"chars":[ch]})
json.dump(d,open(f,'w'),indent=2)
PWG=W//2
def cw(c):
    return {' ':3,'i':1,'!':1,'.':1,',':1,':':1,'l':2,'I':3,'t':3,'f':4,'k':4}.get(c,5)+1
def label(txt):
    wt=sum(cw(c) for c in txt)
    start=wt//2-PWG//2
    return txt+shift(start-wt)+""+shift(wt-(start+PWG))
json.dump({"menu.game":title,"menu.disconnect":label("Verbindung trennen")}, open(PACK+'lang/de_de.json','w'))
json.dump({"menu.game":title,"menu.disconnect":label("Disconnect")}, open(PACK+'lang/en_us.json','w'))
im.resize((W*3,H*3),Image.NEAREST).save('/home/claude/work/info_plate.png')
# Pruefung: jede Bitmap-Angabe ascent <= height, Breite <= 256
for x in d['providers']:
    if x.get('type')=='bitmap':
        t=Image.open(PACK+'textures/'+x['file'].split(':')[1]); assert x['ascent']<=x['height'],x; assert t.width<=256 and t.height<=256,(x['file'],t.size)
print('ok', 'Platte', (W//2,H//2), 'GUI-Pixel')
