"""Einfaerbbarer Rahmen fuer die Titel-Plaketten: weisse Rahmen-Kacheln, die im Spiel in der Systemfarbe getoent werden."""
from PIL import Image
import json
PACK='/home/claude/work/pack/assets/minecraft/'
TH=52; PH=32
W=(255,255,255,255); D=(150,150,150,255)   # oben volle Farbe, unten abgedunkelt
def mid(w):
    im=Image.new('RGBA',(w,TH),(0,0,0,0)); px=im.load()
    for x in range(w): px[x,1]=W; px[x,PH-2]=D
    return im
def cap(left):
    im=Image.new('RGBA',(6,TH),(0,0,0,0)); px=im.load()
    for x in range(6): px[x,1]=W; px[x,PH-2]=D
    xx = 1 if left else 4
    for y in range(1,PH-1): px[xx,y]=W if y<PH//2 else D
    edge = 0 if left else 5
    px[edge,1]=(0,0,0,0); px[edge,PH-2]=(0,0,0,0)
    # die aeusserste Spalte muss sichtbar bleiben, damit die Zeichenbreite stimmt
    for y in range(2,PH-2): px[edge,y]=(7,8,11,255)
    return im
f=PACK+'font/default.json'; d=json.load(open(f))
d['providers']=[p for p in d['providers'] if 'header/tint_' not in p.get('file','')]
def add(name, im, cp):
    im.save(PACK+'textures/font/header/tint_'+name+'.png')
    d['providers'].append({"type":"bitmap","file":"minecraft:font/header/tint_"+name+".png","ascent":25,"height":26,"chars":[chr(cp)]})
add('l',cap(True),0xE440); add('r',cap(False),0xE441)
for i,w in enumerate([1,2,4,8,16,32,64]):
    add('m%d'%w, mid(w*2), 0xE442+i)
json.dump(d,open(f,'w'),indent=2)
for p in d['providers']:
    if p.get('type')=='bitmap': assert p['ascent']<=p['height']
print('ok')
