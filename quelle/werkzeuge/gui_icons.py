"""Hochaufloesende Menue-Symbole (64x64) fuer LazyPlots: Graphit-Kachel, Cyan-Kante, weisse Symbole mit Glow.
Gezeichnet in 256x256 und weich verkleinert."""
from PIL import Image, ImageDraw, ImageFilter
import os, json, math
PACK = '/home/claude/work/pack/'
S = 256
def hx(h, a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
W = hx('#F4F8FC'); CY = hx('#00E5FF'); GR = hx('#5CFF9D'); RD = hx('#FF5A6A'); GD = hx('#FFC94A'); OR = hx('#FF9F43'); PU=hx('#C08BFF'); BL=hx('#4DA3FF')
DK = hx('#1A1D23')

def tile(accent):
    im = Image.new('RGBA', (S, S), (0,0,0,0))
    # Schatten
    sh = Image.new('RGBA', (S, S), (0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((14,20,242,248), 52, fill=(0,0,0,150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    # Verlauf
    grad = Image.new('RGBA', (S, S)); g = grad.load()
    top, bot = hx('#3E4450'), hx('#1F232A')
    for y in range(S):
        t = y/(S-1); c = tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))+(255,)
        for x in range(S): g[x,y] = c
    mask = Image.new('L', (S,S), 0); ImageDraw.Draw(mask).rounded_rectangle((12,12,244,244), 50, fill=255)
    im.paste(grad, (0,0), mask)
    d = ImageDraw.Draw(im)
    # Kante: oben Akzent, unten dunkler
    edge = Image.new('RGBA', (S,S), (0,0,0,0)); e = ImageDraw.Draw(edge)
    e.rounded_rectangle((12,12,244,244), 50, outline=accent[:3]+(230,), width=7)
    fade = Image.new('L', (S,S)); f = fade.load()
    for y in range(S):
        v = int(255 - 170*(y/S))
        for x in range(S): f[x,y] = v
    edge.putalpha(Image.composite(edge.getchannel('A'), Image.new('L',(S,S),0), fade).point(lambda a: a))
    im.alpha_composite(edge)
    # Glanz oben
    gl = Image.new('RGBA', (S,S), (0,0,0,0)); ImageDraw.Draw(gl).rounded_rectangle((26,22,230,110), 40, fill=(255,255,255,18))
    im.alpha_composite(gl)
    return im

def finish(glyph, accent, glow=True):
    im = tile(accent)
    if glow:
        a = glyph.getchannel('A').filter(ImageFilter.GaussianBlur(10))
        g = Image.new('RGBA', (S,S), accent[:3]+(0,)); g.putalpha(a.point(lambda v: int(v*0.75)))
        im.alpha_composite(g)
    # leichter Schatten unter dem Symbol
    s = Image.new('RGBA', (S,S), (0,0,0,0)); s.putalpha(glyph.getchannel('A').point(lambda v: int(v*0.55)))
    im.alpha_composite(s, (0,5))
    im.alpha_composite(glyph)
    return im.resize((64,64), Image.LANCZOS)

def G(): 
    g = Image.new('RGBA', (S,S), (0,0,0,0)); return g, ImageDraw.Draw(g)
def ln(d, pts, w, c): d.line(pts, fill=c, width=w, joint='curve'); [d.ellipse((x-w/2+1,y-w/2+1,x+w/2-1,y+w/2-1), fill=c) for x,y in (pts[0], pts[-1])]

# ---------------------------------------------------------------- Symbole
def house(d, c=W, acc=CY, door=True):
    d.polygon([(128,52),(206,118),(186,118),(186,198),(70,198),(70,118),(50,118)], fill=c)
    d.polygon([(128,52),(214,124),(196,138),(128,80),(60,138),(42,124)], fill=acc)
    if door: d.rounded_rectangle((112,148,144,198), 8, fill=DK)
def badge(d, cx, cy, r, fill, kind):
    d.ellipse((cx-r-6,cy-r-6,cx+r+6,cy+r+6), fill=DK); d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=fill)
    w = max(8, r//3)
    if kind=='+': ln(d,[(cx-r*0.5,cy),(cx+r*0.5,cy)],w,W); ln(d,[(cx,cy-r*0.5),(cx,cy+r*0.5)],w,W)
    if kind=='x': ln(d,[(cx-r*0.4,cy-r*0.4),(cx+r*0.4,cy+r*0.4)],w,W); ln(d,[(cx+r*0.4,cy-r*0.4),(cx-r*0.4,cy+r*0.4)],w,W)
    if kind=='v': ln(d,[(cx-r*0.45,cy),(cx-r*0.1,cy+r*0.35),(cx+r*0.5,cy-r*0.35)],w,W)
    if kind=='$': ln(d,[(cx+r*0.35,cy-r*0.35),(cx-r*0.3,cy-r*0.35),(cx-r*0.35,cy),(cx+r*0.35,cy),(cx+r*0.3,cy+r*0.35),(cx-r*0.35,cy+r*0.35)],w-2,W); ln(d,[(cx,cy-r*0.6),(cx,cy+r*0.6)],w-3,W)
def person(d, cx, cy, s, c):
    d.ellipse((cx-24*s,cy-60*s,cx+24*s,cy-12*s), fill=c)
    d.pieslice((cx-46*s,cy-4*s,cx+46*s,cy+88*s), 180, 360, fill=c)
def coin(d, cx, cy, r, c=GD):
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=hx('#C7922A')); d.ellipse((cx-r+8,cy-r+8,cx+r-8,cy+r-8), fill=c)
    d.ellipse((cx-r+22,cy-r+22,cx+r-22,cy+r-22), outline=hx('#C7922A'), width=6)
def key(d, c):
    d.ellipse((52,64,124,136), outline=c, width=20)
    ln(d,[(116,124),(200,190)],20,c); ln(d,[(166,164),(186,144)],18,c); ln(d,[(184,178),(202,160)],18,c)
def gear(d, c, cx=128, cy=128, r=70):
    for i in range(8):
        a = i*math.pi/4
        x, y = cx+math.cos(a)*r, cy+math.sin(a)*r
        pts = [(cx+math.cos(a+da)*rr, cy+math.sin(a+da)*rr) for da,rr in ((-0.2,r-6),(-0.14,r+16),(0.14,r+16),(0.2,r-6))]
        d.polygon(pts, fill=c)
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=c); d.ellipse((cx-26,cy-26,cx+26,cy+26), fill=DK)
def clock(d, c, acc):
    d.ellipse((50,50,206,206), fill=c); d.ellipse((66,66,190,190), fill=DK)
    ln(d,[(128,128),(128,82)],14,c); ln(d,[(128,128),(162,146)],12,acc); d.ellipse((118,118,138,138), fill=acc)
def arrow(d, c, left=True):
    if left: d.polygon([(64,128),(128,64),(128,104),(196,104),(196,152),(128,152),(128,192)], fill=c)
    else: d.polygon([(192,128),(128,64),(128,104),(60,104),(60,152),(128,152),(128,192)], fill=c)
def tag(d, c, acc):
    d.polygon([(60,80),(140,58),(206,124),(130,200),(64,134)], fill=c); d.ellipse((90,88,114,112), fill=DK)
    ln(d,[(120,150),(160,110)],10,acc)
def lines(d, c, acc):
    d.rounded_rectangle((60,48,196,208), 18, fill=c)
    for i,y in enumerate((84,112,140,168)):
        d.rounded_rectangle((82,y,174 if i<3 else 140,y+12), 6, fill=acc if i==0 else hx('#9AA4B2'))
def shield(d, c):
    d.polygon([(128,44),(200,72),(196,140),(128,212),(60,140),(56,72)], fill=c)
def ban(d, c):
    d.ellipse((56,56,200,200), outline=c, width=22); ln(d,[(88,88),(168,168)],22,c)
def trash(d, c):
    d.rounded_rectangle((62,66,194,86), 8, fill=c); d.rounded_rectangle((104,48,152,72), 8, fill=c)
    d.polygon([(76,94),(180,94),(170,206),(86,206)], fill=c)
    for x in (108,128,148): ln(d,[(x,116),(x,184)],8,DK)
def swords(d, c, acc):
    ln(d,[(66,66),(170,170)],18,c); ln(d,[(190,66),(86,170)],18,c)
    ln(d,[(150,186),(186,150)],14,acc); ln(d,[(70,150),(106,186)],14,acc)
    ln(d,[(176,176),(196,196)],16,acc); ln(d,[(80,176),(60,196)],16,acc)
def bomb(d, c, acc):
    d.ellipse((58,82,178,202), fill=c); d.ellipse((80,104,110,134), fill=hx('#FFFFFF',120))
    ln(d,[(152,92),(176,64),(196,60)],12,hx('#9AA4B2')); d.polygon([(196,40),(206,58),(226,60),(210,72),(214,92),(196,80),(178,92),(182,72),(166,60),(186,58)], fill=acc)
def flame(d, c, acc):
    d.polygon([(128,40),(172,96),(190,140),(178,186),(128,214),(78,186),(66,140),(92,104),(104,134),(116,86)], fill=c)
    d.polygon([(128,110),(152,150),(150,182),(128,198),(106,182),(104,150)], fill=acc)
def door(d, c, acc):
    d.rounded_rectangle((70,40,186,212), 14, fill=c); d.rounded_rectangle((86,58,170,212), 8, fill=DK)
    d.ellipse((142,124,160,142), fill=acc)
def paw(d, c):
    d.ellipse((82,118,174,196), fill=c)
    for (x,y) in ((66,92),(102,62),(150,62),(186,92)): d.ellipse((x-18,y-22,x+18,y+22), fill=c)
def lever(d, c, acc):
    d.rounded_rectangle((60,150,196,198), 14, fill=c); ln(d,[(128,160),(170,72)],18,hx('#9AA4B2')); d.ellipse((152,48,196,92), fill=acc)
def bolt(d, c):
    d.polygon([(142,36),(70,144),(120,144),(104,220),(186,104),(134,104)], fill=c)
def sun(d, c):
    d.ellipse((88,88,168,168), fill=c)
    for i in range(8):
        a=i*math.pi/4; ln(d,[(128+math.cos(a)*62,128+math.sin(a)*62),(128+math.cos(a)*90,128+math.sin(a)*90)],14,c)
def cloud(d, c):
    for b in ((54,102,130,178),(96,70,180,154),(140,100,206,166)): d.ellipse(b, fill=c)
    d.rounded_rectangle((60,130,200,180), 25, fill=c)
def rain(d, c, acc):
    cloud(d, c)
    for x in (90,128,166): ln(d,[(x,196),(x-10,222)],12,acc)
def globe(d, c, acc):
    d.ellipse((52,52,204,204), fill=acc); d.ellipse((52,52,204,204), outline=c, width=12)
    d.ellipse((96,52,160,204), outline=c, width=10); ln(d,[(56,128),(200,128)],10,c); ln(d,[(70,88),(186,88)],8,c); ln(d,[(70,168),(186,168)],8,c)
def leaf(d, c, acc):
    ax, ay, bx, by = 62, 194, 194, 62
    pts_a, pts_b = [], []
    for i in range(41):
        t = i/40; x = ax+(bx-ax)*t; y = ay+(by-ay)*t; w = math.sin(math.pi*t)**0.8*58
        pts_a.append((x+w*0.7071, y+w*0.7071)); pts_b.append((x-w*0.7071, y-w*0.7071))
    d.polygon(pts_a+pts_b[::-1], fill=c)
    ln(d,[(56,200),(176,80)],10,acc)
    for t in (0.35,0.55,0.75):
        x = ax+(bx-ax)*t; y = ay+(by-ay)*t
        ln(d,[(x,y),(x+22,y+4)],7,acc); ln(d,[(x,y),(x-4,y-22)],7,acc)
def portal(d, c, acc):
    d.ellipse((60,40,196,216), outline=c, width=16); d.ellipse((86,70,170,186), fill=acc)
    d.polygon([(128,92),(160,132),(140,132),(140,162),(116,162),(116,132),(96,132)], fill=W)
def stack(d, c, acc):
    for i,y in enumerate((150,112,74)):
        col = c if i<2 else acc
        d.polygon([(128,y-30),(200,y),(128,y+30),(56,y)], fill=col)
        if i<2: d.polygon([(128,y-30+10),(200,y+10),(128,y+40),(56,y+10)], outline=DK, width=0)
def crown(d, c, acc):
    d.polygon([(52,180),(60,82),(100,124),(128,64),(156,124),(196,82),(204,180)], fill=c)
    d.rounded_rectangle((52,180,204,204), 8, fill=c)
    for x in (100,128,156): d.ellipse((x-9,148,x+9,166), fill=acc)
def book(d, c, acc):
    d.arc((48,48,208,208), 60, 390, fill=c, width=22)
    d.polygon([(62,96),(98,128),(44,140)], fill=c)
    ln(d,[(128,88),(128,132),(160,152)],16,acc)
def doc(d, c, acc):
    d.polygon([(70,44),(160,44),(194,78),(194,212),(70,212)], fill=c); d.polygon([(160,44),(194,78),(160,78)], fill=hx('#9AA4B2'))
    for y in (102,130,158): d.rounded_rectangle((92,y,172,y+12), 6, fill=acc if y==102 else hx('#9AA4B2'))
def gauge(d, c, acc):
    d.arc((44,60,212,228), 180, 360, fill=hx('#5E6673'), width=26); d.arc((44,60,212,228), 180, 300, fill=acc, width=26)
    ln(d,[(128,144),(176,100)],14,c); d.ellipse((112,128,144,160), fill=c)
def market(d, c, acc):
    d.rounded_rectangle((60,112,196,208), 12, fill=c)
    for i in range(5):
        x=52+i*30; d.pieslice((x,70,x+30,128), 0, 180, fill=acc if i%2==0 else W); d.rectangle((x,70,x+30,100), fill=acc if i%2==0 else W)
    d.rounded_rectangle((104,146,152,208), 8, fill=DK)
def chev(d, c, left):
    pts = [(150,64),(86,128),(150,192)] if left else [(106,64),(170,128),(106,192)]
    ln(d, pts, 30, c)
def pill(d, on):
    d.rounded_rectangle((44,92,212,164), 36, fill=GR if on else hx('#5E6673'))
    x = 176 if on else 80
    d.ellipse((x-30,98,x+30,158), fill=W)
def compass(d, c, acc):
    d.ellipse((52,52,204,204), outline=c, width=14)
    d.polygon([(128,70),(146,128),(128,186),(110,128)], fill=c); d.polygon([(128,70),(146,128),(110,128)], fill=acc)
def empty(d, c):
    d.rounded_rectangle((60,60,196,196), 26, outline=c, width=14); ln(d,[(90,166),(166,90)],14,c)
def cross(d, c): ln(d,[(76,76),(180,180)],30,c); ln(d,[(180,76),(76,180)],30,c)
def check(d, c): ln(d,[(66,134),(110,178),(194,84)],30,c)

ICONS = {}
def icon(name, accent):
    def deco(fn):
        ICONS[name] = (fn, accent); return fn
    return deco

@icon('plot', CY)
def _(d): house(d)
@icon('plot_free', GR)
def _(d): house(d, acc=GR); badge(d,184,184,34,GR,'+')
@icon('plot_add', GR)
def _(d): house(d, acc=GR); badge(d,184,184,34,GR,'+')
@icon('plot_sale', GD)
def _(d): house(d, acc=GD); badge(d,184,184,34,hx('#E0A92E'),'$')
@icon('plot_rent', BL)
def _(d): house(d, acc=BL); badge(d,184,184,34,BL,'v')
@icon('plot_rented', RD)
def _(d): house(d, acc=RD); badge(d,184,184,34,RD,'x')
@icon('plot_list', CY)
def _(d): stack(d, W, CY)
@icon('no_plot', hx('#9AA4B2'))
def _(d): compass(d, W, CY)
@icon('market', GD)
def _(d): market(d, W, GD)
@icon('rent', BL)
def _(d): key(d, W)
@icon('limit', GR)
def _(d): gauge(d, W, GR)
@icon('team', RD)
def _(d): shield(d, W); d.polygon([(128,70),(176,90),(172,138),(128,184)], fill=RD)
@icon('close', RD)
def _(d): cross(d, W)
@icon('back', CY)
def _(d): arrow(d, W, True)
@icon('prev', CY)
def _(d): chev(d, W, True)
@icon('next', CY)
def _(d): chev(d, W, False)
@icon('teleport', PU)
def _(d): portal(d, W, PU)
@icon('members', CY)
def _(d): person(d,96,118,0.85,hx('#9AA4B2')); person(d,150,128,1.0,W)
@icon('member_add', GR)
def _(d): person(d,112,126,1.0,W); badge(d,184,184,34,GR,'+')
@icon('member_name', CY)
def _(d): person(d,112,126,1.0,W); d.rounded_rectangle((150,160,218,206), 10, fill=CY); ln(d,[(166,183),(204,183)],8,DK)
@icon('trust', GR)
def _(d): shield(d, W); ln(d,[(96,128),(120,154),(164,100)],20,GR)
@icon('member', CY)
def _(d): person(d,128,126,1.1,W)
@icon('deny', RD)
def _(d): ban(d, RD)
@icon('remove', RD)
def _(d): trash(d, W)
@icon('settings', CY)
def _(d): gear(d, W)
@icon('name', CY)
def _(d): tag(d, W, CY)
@icon('description', CY)
def _(d): lines(d, W, CY)
@icon('sell', GR)
def _(d): coin(d,128,128,78)
@icon('sell_stop', OR)
def _(d): coin(d,118,118,70); badge(d,184,184,34,RD,'x')
@icon('rent_stop', OR)
def _(d): key(d, W); badge(d,184,184,34,RD,'x')
@icon('pvp', RD)
def _(d): swords(d, W, RD)
@icon('explosion', OR)
def _(d): bomb(d, hx('#2F343D'), OR); d.ellipse((58,82,178,202), outline=W, width=10)
@icon('fire', OR)
def _(d): flame(d, OR, GD)
@icon('visit', CY)
def _(d): door(d, W, CY)
@icon('animals', GD)
def _(d): paw(d, W)
@icon('devices', CY)
def _(d): lever(d, W, CY)
@icon('redstone', RD)
def _(d): bolt(d, RD)
@icon('toggle_on', GR)
def _(d): pill(d, True)
@icon('toggle_off', hx('#5E6673'))
def _(d): pill(d, False)
@icon('weather_world', CY)
def _(d): globe(d, W, hx('#2B6CB0'))
@icon('weather_clear', GD)
def _(d): sun(d, GD)
@icon('weather_rain', BL)
def _(d): rain(d, W, BL)
@icon('time', CY)
def _(d): clock(d, W, CY)
@icon('biome', GR)
def _(d): leaf(d, GR, hx('#1B6B3E'))
@icon('empty', hx('#5E6673'))
def _(d): empty(d, hx('#9AA4B2'))
@icon('confirm', GR)
def _(d): check(d, W)
@icon('cancel', RD)
def _(d): cross(d, W)
@icon('summary', CY)
def _(d): doc(d, W, CY)
@icon('owner', GD)
def _(d): crown(d, GD, W)
@icon('history', CY)
def _(d): book(d, W, CY)
@icon('history_entry', hx('#9AA4B2'))
def _(d): doc(d, W, hx('#9AA4B2'))
@icon('offers_remove', OR)
def _(d): coin(d,118,118,70); badge(d,184,184,34,RD,'x')
@icon('members_clear', RD)
def _(d): person(d,112,126,1.0,W); badge(d,184,184,34,RD,'x')
@icon('name_reset', OR)
def _(d): tag(d, W, CY); badge(d,184,184,34,RD,'x')
@icon('admin_manage', RD)
def _(d): gear(d, W); badge(d,184,184,34,RD,'v')
@icon('voucher', GR)
def _(d): doc(d, W, GR); badge(d,184,184,34,GR,'+')

tex = PACK+'assets/lazymc/textures/item/gui/'; mod = PACK+'assets/lazymc/models/item/gui/'; itm = PACK+'assets/lazymc/items/gui/'
for p in (tex, mod, itm): os.makedirs(p, exist_ok=True)
sheet = Image.new('RGBA', (8*72+8, ((len(ICONS)+7)//8)*72+8), (40,44,40,255))
for i,(name,(fn,acc)) in enumerate(ICONS.items()):
    g, d = G(); fn(d); im = finish(g, acc)
    im.save(tex+name+'.png')
    json.dump({"parent":"minecraft:item/generated","textures":{"layer0":"lazymc:item/gui/"+name}}, open(mod+name+'.json','w'))
    json.dump({"model":{"type":"minecraft:model","model":"lazymc:item/gui/"+name}}, open(itm+name+'.json','w'))
    sheet.alpha_composite(im, (8+(i%8)*72, 8+(i//8)*72))
sheet.resize((sheet.width*2, sheet.height*2), Image.NEAREST).save('/home/claude/work/icons_sheet.png')
open('/home/claude/work/icon_names.txt','w').write('\n'.join(ICONS))
print(len(ICONS), 'Symbole')
