"""LazyMC-Symbole im Minecraft-Pixelstil (32x32) mit dem faulen Panda. Gleiche IDs wie vorher (lazymc:gui/<id>)."""
from PIL import Image, ImageDraw, ImageFont
import os, json
PACK = '/home/claude/work/pack/'
def hx(h, a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
C = dict(K=hx('#1E2026'), W=hx('#F4F6F8'), g=hx('#8A94A5'), m=hx('#C3CBD6'), p=hx('#F2A7B8'),
  R=hx('#5A3D24'), r=hx('#3F2A17'), L=hx('#C29A62'), l=hx('#9C7A47'), G=hx('#A8E4F0'), D=hx('#6B4A2A'),
  S=hx('#6BCB4A'), s=hx('#4E9E33'), d=hx('#8B5E3C'), e=hx('#6E4A2E'),
  Y=hx('#FFC94A'), y=hx('#C7922A'), h=hx('#FFE69A'), c=hx('#00E5FF'), b=hx('#0094FF'),
  I=hx('#D8DEE6'), i=hx('#9AA4B2'), j=hx('#6B7482'), X=hx('#FF5A6A'), x=hx('#B8333F'), N=hx('#5CFF9D'), n=hx('#2E9E5E'),
  B=hx('#4DA3FF'), u=hx('#2B5FA8'), P=hx('#C08BFF'), q=hx('#7A4FC0'), O=hx('#FF9F43'), o=hx('#C46A1A'), T=hx('#E04B3A'))
OUT = hx('#07080B')
ACC = {'cyan':('#5FD8E6','#1E7E8C'),'gold':('#FFD36B','#B07A1E'),'green':('#7DFFB3','#2E9E5E'),'red':('#FF8A95','#A3303C'),
       'blue':('#7FB8FF','#2B5FA8'),'purple':('#C9A2FF','#6A3FB0'),'orange':('#FFB86B','#B0601E'),'gray':('#AEB8C6','#5E6673')}

def tile(acc):
    a1, a2 = hx(ACC[acc][0]), hx(ACC[acc][1])
    im = Image.new('RGBA',(32,32),(0,0,0,0)); px = im.load(); top, bot = hx('#454B56'), hx('#262A31')
    for yy in range(32):
        for xx in range(32):
            if (xx in (0,31) and yy in (0,1,30,31)) or (yy in (0,31) and xx in (0,1,30,31)): continue
            if xx in (0,31) or yy in (0,31): col = OUT
            elif yy == 1 or xx == 1: col = a1
            elif yy == 30 or xx == 30: col = a2
            else:
                t = (yy-2)/27; col = tuple(int(top[k]*(1-t)+bot[k]*t) for k in range(3))+(255,)
            px[xx,yy] = col
    for (xx,yy) in ((3,3),(28,3),(3,28),(28,28)): px[xx,yy] = hx('#7F8896')
    return im

class Canvas:
    def __init__(self): self.im = Image.new('RGBA',(32,32),(0,0,0,0)); self.d = ImageDraw.Draw(self.im)
    def art(self, rows, ox, oy):
        px = self.im.load()
        for yy,row in enumerate(rows):
            for xx,ch in enumerate(row):
                if ch in C and 0 <= ox+xx < 32 and 0 <= oy+yy < 32: px[ox+xx, oy+yy] = C[ch]
    def rect(self, x0,y0,x1,y1,col): self.d.rectangle((x0,y0,x1,y1), fill=C.get(col,col))
    def ell(self, x0,y0,x1,y1,col): self.d.ellipse((x0,y0,x1,y1), fill=C.get(col,col))
    def ring(self, x0,y0,x1,y1,col,w=2): self.d.ellipse((x0,y0,x1,y1), outline=C.get(col,col), width=w)
    def line(self, pts, col, w=2): self.d.line(pts, fill=C.get(col,col), width=w)
    def poly(self, pts, col): self.d.polygon(pts, fill=C.get(col,col))
    def finish(self, acc, shade=True):
        src = self.im; px = src.load()
        out = Image.new('RGBA',(32,32),(0,0,0,0)); q = out.load()
        for yy in range(32):
            for xx in range(32):
                a = px[xx,yy]
                if a[3]:
                    col = a
                    if shade:
                        below = yy+1 < 32 and px[xx,yy+1][3]; right = xx+1 < 32 and px[xx+1,yy][3]
                        above = yy > 0 and px[xx,yy-1][3]; left = xx > 0 and px[xx-1,yy][3]
                        if not below or not right: col = tuple(int(v*0.78) for v in a[:3])+(255,)
                        elif not above or not left: col = tuple(min(255,int(v*1.12)) for v in a[:3])+(255,)
                    q[xx,yy] = col
                elif any(0<=xx+dx<32 and 0<=yy+dy<32 and px[xx+dx,yy+dy][3] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
                    q[xx,yy] = OUT
        im = tile(acc); im.alpha_composite(out); return im

# ---------------------------------------------------------------- Sprites
PANDA = [".KKKK........KKKK.","KKKKKK......KKKKKK","KKKKKWWWWWWWWKKKKK","KKKWWWWWWWWWWWWKKK",".WWWWWWWWWWWWWWWW.",
         "WWWWWWWWWWWWWWWWWW","WWKKKKWWWWWWKKKKWW","WKKKKKKWWWWKKKKKKW","WKgggKKWWWWKKgggKW","WWKKKKWWWWWWKKKKWW",
         "WWWWWWWWKKWWWWWWWW","WpWWWWWWmmWWWWWWpW",".WWWWWWWWWWWWWWWW.","..WWWWWWWWWWWWWW.."]
PANDA_S = ["KK........KK","KKKWWWWWWKKK",".WWWWWWWWWW.","WWKKWWWWKKWW","WKggWWWWggKW","WWWWWKKWWWWW","WpWWWmmWWWpW",".WWWWWWWWWW."]
ZZ = ["cccc","..c.",".c..","cccc"]; Zs = ["ccc",".c.","ccc"]
HOUSE = ["........RR........",".......RrrR.......","......RrrrrR......",".....RrrrrrrR.....","....RrrrrrrrrR....",
         "...RRRRRRRRRRRR...","...LLLLLLLLLLLL...","...LGGLLLLLLGGL...","...LGGLLDDLLGGL...","...LLLLLDDLLLLL...",
         "...LLLLLDDLLLLL...",".SSSSSSSSSSSSSSSS.",".dddddddddddddddd."]
HOUSE_S = ["....RR....","...RrrR...","..RrrrrR..",".RRRRRRRR.","..LLLLLL..","..LGLDLL..","..LLLDLL..",".SSSSSSSS."]
GRASS = ["SSSSSSSSSSSSSS","SSsSSSSSsSSSSS","SsSSSsSSSSSsSS","ddsddddsdddddd","dddddedddddded","ddeddddddddedd","ddddddddeddddd","dedddddddddded","dddddeddddddd d".replace(' ','d')]
COIN = [".hYYYY.","hYYYYYy","yyyyyyy"]
KEY = ["..YYYY..........",".YhhhYY.........","YYy..yYYYYYYYYYY","YY....YyyyyyyyyY",".YYyyYY...Yy.Yy.","..YYYY....yy.yy."]
CROWN = ["Y......YY......Y","YY....YhhY....YY","YYY..YYYYYY..YYY","YYYYYYYYYYYYYYYY","YcYYYYYccYYYYYcY","yyyyyyyyyyyyyyyy"]
TNT = ["xxxxxxxxxxxx","XXXXXXXXXXXX","XxXXxXXxXXxX","IIIIIIIIIIII","IKKKIKIKIKKK","IIKIIKKKIIKI","IIKIIKIKIIKI","IIIIIIIIIIII","XxXXxXXxXXxX","XXXXXXXXXXXX","xxxxxxxxxxxx"]
CHEST = ["DDDDDDDDDDDDDD","DLLLLLLLLLLLLD","DLllllllllllLD","DDDDDDiiDDDDDD","DLLLLLiiLLLLLD","DLllllllllllLD","DLllllllllllLD","DDDDDDDDDDDDDD"]
ENDCHEST = ["KKKKKKKKKKKKKK","KjjjjjjjjjjjjK","KjKKKKKKKKKKjK","KKKKKKNNKKKKKK","KjjjjjNNjjjjjK","KjKKKKKKKKKKjK","KjjjjjjjjjjjjK","KKKKKKKKKKKKKK"]
PAPER = [".WWWWWWWWWW.","WWWWWWWWWWmW","WggggggggWWW","WWWWWWWWWWWW","WggggggWWWWW","WWWWWWWWWWWW","WgggggggggWW","WWWWWWWWWWWW","WggggWWWWWWW","WWWWWWWWWWWW",".mmmmmmmmmm."]
TAG = ["....KKKKKKKK","...KIIIIIIIK","..KIIIIIIIIK",".KIIKIIIIIIK","KIIKKIIIIIIK",".KIIKIIIIIIK","..KIIIIIIIIK","...KIIIIIIIK","....KKKKKKKK"]
DOOR = ["llllllll","lLLLLLLl","lLGGGGLl","lLGGGGLl","lLLLLLLl","lLllllLl","lLLLLLLl","lLLLLYLl","lLLLLLLl","lLllllLl","lLLLLLLl","lLLLLLLl","llllllll"]
PERSON = ["..KKKK..",".KmmmmK.",".KmmmmK.",".KmmmmK.","..KKKK..",".cccccc.","cccccccc","cccccccc","cccccccc"]
PERSON = ["..IIII..",".IIIIII.",".IIIIII.","..IIII..","........","..IIII..",".IIIIII.","IIIIIIII","IIIIIIII"]

PERSON_B = ["...IIIIII...","..IIIIIIII..","..IIIIIIII..","..IIIIIIII..","...IIIIII...","............","...IIIIII...",".IIIIIIIIII.","IIIIIIIIIIII","IIIIIIIIIIII","IIIIIIIIIIII"]
TAG_B = [".....KKKKKKKKK","....KIIIIIIIIK","...KIIIIIIIIIK","..KIIIIIIIIIIK",".KIIIKIIIIIIIK","KIIIKKKIIIIIIK",".KIIIKIIIIIIIK","..KIIIIIIIIIIK","...KIIIIIIIIIK","....KIIIIIIIIK",".....KKKKKKKKK"]
def door_b(c, ox, oy):
    c.rect(ox,oy,ox+11,oy+17,'l'); c.rect(ox+1,oy+1,ox+10,oy+16,'L'); c.rect(ox+2,oy+2,ox+9,oy+6,'G')
    c.rect(ox+2,oy+8,ox+9,oy+8,'l'); c.rect(ox+2,oy+12,ox+9,oy+12,'l'); c.rect(ox+8,oy+10,ox+9,oy+10,'Y')

def big_key(c, ox, oy):
    c.ring(ox,oy,ox+9,oy+9,'Y',3); c.rect(ox+9,oy+4,ox+19,oy+6,'Y'); c.rect(ox+15,oy+7,ox+16,oy+9,'Y'); c.rect(ox+18,oy+7,ox+19,oy+10,'Y'); c.rect(ox+2,oy+2,ox+3,oy+3,'h')
def big_chest(c, ox, oy, purple=False):
    a,b,k = ('K','j','N') if purple else ('D','L','I')
    c.rect(ox,oy,ox+17,oy+13,a); c.rect(ox+1,oy+1,ox+16,oy+4,b); c.rect(ox+1,oy+7,ox+16,oy+12,b)
    c.rect(ox,oy+5,ox+17,oy+6,a); c.rect(ox+8,oy+4,ox+9,oy+8,k)
    if not purple: c.rect(ox+1,oy+10,ox+16,oy+12,'l')
def stall(c):
    c.rect(8,15,23,25,'L'); c.rect(8,22,23,25,'l'); c.rect(14,18,17,25,'D')
    for k in range(5): c.rect(6+k*4,9,9+k*4,13,'X' if k%2==0 else 'W')
    c.rect(6,7,25,8,'x')
def badge(cv, kind, col):
    cx, cy = 22, 22
    cv.ell(cx-5,cy-5,cx+5,cy+5,col)
    W='W'
    if kind=='+': cv.rect(cx-3,cy-1,cx+3,cy,W); cv.rect(cx-1,cy-3,cx,cy+3,W)
    if kind=='x': cv.line([(cx-3,cy-3),(cx+2,cy+2)],W,2); cv.line([(cx+2,cy-3),(cx-3,cy+2)],W,2)
    if kind=='v': cv.line([(cx-3,cy),(cx-1,cy+2),(cx+3,cy-3)],W,2)
    if kind=='$': cv.art(["WWWW","W...","WWWW","...W","WWWW"],cx-2,cy-2); cv.rect(cx,cy-4,cx,cy+3,W)
    if kind=='up': cv.poly([(cx-3,cy),(cx,cy-3),(cx+3,cy)],W); cv.rect(cx-1,cy,cx,cy+3,W)
    if kind=='down': cv.poly([(cx-3,cy),(cx,cy+3),(cx+3,cy)],W); cv.rect(cx-1,cy-3,cx,cy,W)
    if kind=='=': cv.rect(cx-3,cy-2,cx+2,cy-1,W); cv.rect(cx-3,cy+1,cx+2,cy+2,W)
def coins(cv, ox=6, oy=16):
    for (dx,dy) in ((0,6),(8,6),(16,6),(4,3),(12,3),(8,0)): cv.art(COIN, ox+dx, oy+dy)
def gear(cv, cx, cy, r, col='I', dark='i'):
    import math
    for a in range(8):
        ang = a*math.pi/4
        x, y = cx+math.cos(ang)*(r+1.5), cy+math.sin(ang)*(r+1.5)
        cv.rect(int(x-1.5),int(y-1.5),int(x+1.5),int(y+1.5),col)
    cv.ell(cx-r,cy-r,cx+r,cy+r,col); cv.ell(cx-r+2,cy-r+2,cx+r,cy+r,dark); cv.ell(cx-r+1,cy-r+1,cx+r-1,cy+r-1,col); cv.ell(cx-2,cy-2,cx+2,cy+2,'K')

ICONS = {}
def icon(name, acc):
    def deco(fn): ICONS[name] = (fn, acc); return fn
    return deco

# ---- Grundstuecke (mit Panda)
@icon('plot','cyan')
def _(c): c.art(HOUSE,7,9)
@icon('plot_free','green')
def _(c): c.art(GRASS,7,10); badge(c,'+','N')
@icon('plot_add','green')
def _(c): c.art(GRASS,7,10); badge(c,'+','N')
@icon('plot_sale','gold')
def _(c): c.art(HOUSE,6,8); badge(c,'$','y')
@icon('plot_rent','blue')
def _(c): c.art(HOUSE,6,8); badge(c,'v','B')
@icon('plot_rented','red')
def _(c): c.art(HOUSE,6,8); badge(c,'x','X')
@icon('plot_list','cyan')
def _(c): c.art(HOUSE_S,4,16); c.art(HOUSE_S,17,16); c.art(HOUSE_S,11,6)
@icon('no_plot','gray')
def _(c): c.ell(8,8,23,23,'i'); c.ell(9,9,22,22,'I'); c.poly([(15,10),(17,15),(15,21),(14,15)],'X'); c.poly([(15,21),(17,15),(14,15)],'j')
@icon('market','gold')
def _(c): stall(c)
@icon('rent','blue')
def _(c): big_key(c,6,10)
@icon('limit','green')
def _(c): c.art(PAPER,10,10); c.rect(12,22,19,23,'N')
@icon('team','red')
def _(c): c.poly([(8,7),(23,7),(23,16),(15,25),(8,16)],'I'); c.poly([(16,7),(23,7),(23,16),(16,24)],'X')
@icon('close','red')
def _(c): c.line([(9,9),(22,22)],'X',4); c.line([(22,9),(9,22)],'X',4)
@icon('back','cyan')
def _(c): c.poly([(7,15),(14,8),(14,12),(24,12),(24,19),(14,19),(14,23)],'c')
@icon('prev','cyan')
def _(c): c.line([(18,8),(11,15),(18,22)],'c',4)
@icon('next','cyan')
def _(c): c.line([(13,8),(20,15),(13,22)],'c',4)
@icon('teleport','purple')
def _(c): c.ell(9,9,22,22,'n'); c.ell(10,10,21,21,'N'); c.ell(12,12,19,19,'n'); c.rect(12,11,13,12,'W')
# ---- Mitglieder
@icon('members','cyan')
def _(c): c.art(PERSON,7,11); c.art([r.replace('I','c') for r in PERSON],16,9)
@icon('member_add','green')
def _(c): c.art(PERSON_B,6,7); badge(c,'+','N')
@icon('member_name','cyan')
def _(c): c.art(PERSON_B,5,6); c.art(TAG,17,18)
@icon('trust','green')
def _(c): c.poly([(8,7),(23,7),(23,16),(15,25),(8,16)],'I'); c.line([(11,15),(14,18),(20,11)],'n',3)
@icon('member','cyan')
def _(c): c.art([r.replace('I','c') for r in PERSON_B],10,9)
@icon('deny','red')
def _(c): c.ring(7,7,24,24,'X',3); c.line([(11,11),(20,20)],'X',3)
@icon('remove','red')
def _(c): c.rect(9,9,22,10,'i'); c.rect(13,7,18,8,'i'); c.poly([(10,12),(21,12),(20,24),(11,24)],'I'); [c.rect(xx,14,xx,22,'j') for xx in (13,15,17,19)]
@icon('members_clear','red')
def _(c): c.art(PERSON,6,9); c.art(PERSON,13,7); badge(c,'x','X')
# ---- Einstellungen (Panda)
@icon('settings','cyan')
def _(c): gear(c,15,15,8)
@icon('admin_manage','red')
def _(c): gear(c,14,14,7); badge(c,'v','X')
@icon('name','cyan')
def _(c): c.art(TAG_B,9,10); c.rect(15,15,20,15,'c')
@icon('name_reset','orange')
def _(c): c.art(TAG_B,6,7); badge(c,'x','X')
@icon('description','cyan')
def _(c): c.art(PAPER,8,10); c.line([(24,6),(17,17)],'W',2); c.rect(23,6,25,7,'c')
@icon('sell','green')
def _(c): coins(c,5,13); badge(c,'up','N')
@icon('sell_stop','orange')
def _(c): coins(c,4,12); badge(c,'x','X')
@icon('rent_stop','orange')
def _(c): c.art(KEY,6,12); badge(c,'x','X')
@icon('offers_remove','orange')
def _(c): coins(c,4,12); badge(c,'x','X')
# ---- Flags
@icon('pvp','red')
def _(c):
    c.line([(8,8),(21,21)],'I',2); c.line([(23,8),(10,21)],'I',2)
    c.rect(18,20,22,21,'D'); c.rect(9,20,13,21,'D'); c.rect(20,22,22,24,'l'); c.rect(9,22,11,24,'l')
@icon('explosion','orange')
def _(c): c.art(TNT,10,10)
@icon('fire','orange')
def _(c): c.poly([(15,6),(21,13),(22,19),(19,24),(12,24),(9,19),(10,14),(12,16),(13,10)],'O'); c.poly([(15,14),(18,18),(17,23),(13,23),(12,19)],'Y')
@icon('visit','cyan')
def _(c): door_b(c,10,7)
@icon('animals','gold')
def _(c): c.ell(11,15,20,23,'W'); [c.ell(xx,yy,xx+3,yy+4,'W') for xx,yy in ((8,11),(11,8),(17,8),(20,11))]
@icon('devices','cyan')
def _(c): c.rect(9,20,22,24,'j'); c.rect(10,21,21,23,'i'); c.line([(15,20),(19,11)],'D',2); c.ell(17,8,21,12,'c')
@icon('redstone','red')
def _(c): c.poly([(17,6),(10,17),(15,17),(13,25),(21,13),(16,13)],'X')
@icon('toggle_on','green')
def _(c): c.ell(6,10,15,20,'N'); c.ell(16,10,25,20,'N'); c.rect(10,10,20,20,'N'); c.ell(16,11,24,19,'W')
@icon('toggle_off','gray')
def _(c): c.ell(6,10,15,20,'j'); c.ell(16,10,25,20,'j'); c.rect(10,10,20,20,'j'); c.ell(7,11,15,19,'I')
@icon('weather_world','cyan')
def _(c): c.ell(7,7,24,24,'B'); c.poly([(10,11),(15,9),(17,13),(13,16),(11,15)],'S'); c.poly([(18,17),(22,15),(23,20),(19,22)],'S'); c.rect(14,19,16,21,'S')
@icon('weather_clear','gold')
def _(c):
    c.ell(11,11,20,20,'Y')
    for (x0,y0,x1,y1) in ((15,5,16,8),(15,23,16,26),(5,15,8,16),(23,15,26,16),(8,8,9,9),(22,8,23,9),(8,22,9,23),(22,22,23,23)): c.rect(x0,y0,x1,y1,'Y')
@icon('weather_rain','blue')
def _(c): c.ell(7,9,15,17,'I'); c.ell(12,6,22,16,'I'); c.ell(17,10,25,18,'I'); c.rect(9,13,23,17,'I'); [c.line([(xx,20),(xx-1,24)],'B',2) for xx in (11,16,21)]
@icon('time','cyan')
def _(c): c.ell(7,7,24,24,'Y'); c.ell(9,9,22,22,'h'); c.rect(15,11,16,16,'K'); c.rect(16,15,19,16,'K')
@icon('biome','green')
def _(c): c.rect(15,17,16,25,'D'); c.ell(9,6,22,19,'S'); c.ell(12,9,19,16,'s'); c.rect(9,24,22,25,'d')
# ---- Allgemein
@icon('empty','gray')
def _(c): [c.rect(xx,9,xx+1,9,'j') for xx in range(9,23,4)]; [c.rect(xx,22,xx+1,22,'j') for xx in range(9,23,4)]; [c.rect(9,yy,9,yy+1,'j') for yy in range(9,23,4)]; [c.rect(22,yy,22,yy+1,'j') for yy in range(9,23,4)]
@icon('confirm','green')
def _(c): c.line([(8,16),(13,21),(23,10)],'N',4)
@icon('cancel','red')
def _(c): c.line([(9,9),(22,22)],'X',4); c.line([(22,9),(9,22)],'X',4)
@icon('summary','cyan')
def _(c): c.art(PAPER,10,10)
@icon('owner','gold')
def _(c): c.art(CROWN,8,10); c.art(CROWN[3:],8,16)
@icon('history','cyan')
def _(c): c.ring(7,7,24,24,'I',2); c.poly([(5,13),(10,13),(7,17)],'I'); c.rect(15,10,16,16,'c'); c.rect(16,15,20,16,'c')
@icon('history_entry','gray')
def _(c): c.art(PAPER,10,10)
@icon('voucher','green')
def _(c): c.art(PAPER,7,8); badge(c,'+','N')
@icon('messages','cyan')
def _(c): c.rect(7,8,24,19,'I'); c.poly([(10,19),(10,24),(15,19)],'I'); [c.rect(xx,13,xx+1,14,'c') for xx in (11,15,19)]
@icon('join','green')
def _(c): door_b(c,7,6); badge(c,'+','N')
@icon('scoreboard','cyan')
def _(c): c.rect(8,7,23,24,'I'); c.rect(8,7,23,10,'c'); [c.rect(10,yy,21,yy,'i') for yy in (13,16,19,22)]
@icon('eye','purple')
def _(c): c.poly([(6,15),(11,10),(20,10),(25,15),(20,20),(11,20)],'W'); c.ell(12,11,19,19,'P'); c.ell(14,13,17,16,'K'); c.rect(17,12,17,12,'W')
@icon('sound','cyan')
def _(c): c.poly([(7,13),(11,13),(16,8),(16,23),(11,18),(7,18)],'I'); c.line([(19,11),(21,15),(19,20)],'c',2); c.line([(22,8),(25,15),(22,23)],'c',2)
@icon('filter','cyan')
def _(c): c.poly([(7,8),(24,8),(18,16),(18,23),(13,25),(13,16)],'i'); c.rect(8,9,23,10,'I')
@icon('sort','cyan')
def _(c): c.rect(7,8,19,10,'I'); c.rect(7,14,16,16,'I'); c.rect(7,20,13,22,'I'); c.rect(21,8,22,20,'c'); c.poly([(18,20),(25,20),(21,25)],'c')
@icon('refresh','green')
def _(c): c.ring(8,8,23,23,'N',3); c.rect(14,6,18,10,(0,0,0,0)); c.rect(13,21,17,25,(0,0,0,0)); c.poly([(18,4),(22,8),(17,11)],'N'); c.poly([(13,27),(9,23),(14,20)],'N')
@icon('reset','red')
def _(c): c.ring(8,8,23,23,'X',3); c.rect(14,6,18,10,(0,0,0,0)); c.rect(13,21,17,25,(0,0,0,0)); c.poly([(18,4),(22,8),(17,11)],'X'); c.poly([(13,27),(9,23),(14,20)],'X')
@icon('info','cyan')
def _(c): c.ell(7,7,24,24,'c'); c.rect(15,10,16,11,'W'); c.rect(15,13,16,21,'W')
@icon('my_listings','gold')
def _(c): c.art(TAG_B,5,6); c.rect(11,11,16,11,'Y'); badge(c,'$','y')
@icon('storage','purple')
def _(c): big_chest(c,7,9,True)
@icon('search_reset','red')
def _(c): c.ring(6,6,18,18,'I',2); c.line([(17,17),(21,21)],'I',3); badge(c,'x','X')
@icon('sell_all','gold')
def _(c): coins(c,5,12)
@icon('payout','gold')
def _(c): coins(c,4,12); badge(c,'up','N')
@icon('hand_add','green')
def _(c): c.art(GRASS,5,8); badge(c,'+','N')
@icon('stats','cyan')
def _(c): c.rect(7,7,8,24,'I'); c.rect(7,23,24,24,'I'); c.rect(11,16,13,22,'I'); c.rect(15,12,17,22,'I'); c.rect(19,9,21,22,'c')
@icon('price_base','gold')
def _(c): c.ell(6,6,19,19,'y'); c.ell(7,7,18,18,'Y'); c.ell(9,9,16,16,'h'); badge(c,'=','B')
@icon('price_min','orange')
def _(c): c.ell(6,6,19,19,'y'); c.ell(7,7,18,18,'Y'); c.ell(9,9,16,16,'h'); badge(c,'down','X')
@icon('price_max','green')
def _(c): c.ell(6,6,19,19,'y'); c.ell(7,7,18,18,'Y'); c.ell(9,9,16,16,'h'); badge(c,'up','N')
@icon('sensitivity','purple')
def _(c): c.line([(6,16),(9,10),(12,16),(15,22),(18,16),(21,10),(24,16)],'P',2)
@icon('recovery','green')
def _(c): c.ring(7,7,24,24,'N',2); c.poly([(5,13),(10,13),(7,17)],'N'); c.rect(15,10,16,16,'W'); c.rect(16,15,20,16,'W')
@icon('expected','gold')
def _(c): c.rect(9,6,22,7,'D'); c.rect(9,24,22,25,'D'); c.poly([(10,8),(21,8),(17,15),(21,23),(10,23),(14,15)],'G'); c.poly([(12,9),(19,9),(15,13)],'Y'); c.poly([(15,18),(19,22),(12,22)],'Y')
@icon('ranks','gold')
def _(c): c.art(CROWN,8,12); c.art(CROWN[3:],8,18); c.poly([(15,4),(17,7),(20,7),(18,9),(15,8),(13,9),(11,7),(14,7)],'h')
@icon('team_ranks','red')
def _(c): c.poly([(8,7),(23,7),(23,16),(15,25),(8,16)],'I'); c.poly([(15,9),(17,13),(21,13),(18,16),(19,20),(15,18),(12,20),(13,16),(10,13),(14,13)],'X')
@icon('gift','green')
def _(c): c.rect(8,14,23,24,'X'); c.rect(7,11,24,14,'X'); c.rect(14,11,17,24,'Y'); c.rect(7,12,24,13,'x'); c.ring(10,5,15,10,'Y',2); c.ring(16,5,21,10,'Y',2)
@icon('palette','purple')
def _(c): c.ell(6,7,25,24,'L'); c.ell(16,16,20,20,(0,0,0,0)); [c.ell(xx,yy,xx+3,yy+3,col) for xx,yy,col in ((9,11,'X'),(14,9,'Y'),(19,11,'N'),(9,16,'B'))]
@icon('classic','green')
def _(c): c.art(GRASS,9,11)

tex = PACK+'assets/lazymc/textures/item/gui/'
os.makedirs(tex, exist_ok=True)
names = list(ICONS)
sheet = Image.new('RGBA',(12*36+4, ((len(names)+11)//12)*36+4),(30,33,30,255))
for k,name in enumerate(names):
    fn, acc = ICONS[name]; cv = Canvas(); fn(cv); im = cv.finish(acc)
    im.save(tex+name+'.png')
    sheet.alpha_composite(im,(4+(k%12)*36, 4+(k//12)*36))
sheet.resize((sheet.width*3, sheet.height*3), Image.NEAREST).save('/home/claude/work/pixel_sheet.png')
print(len(ICONS),'Symbole')
