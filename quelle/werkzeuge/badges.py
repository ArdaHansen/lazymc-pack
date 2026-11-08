from PIL import Image
import json, os, yaml
P='../pack/'
G={
'A':[".###.","#...#","#####","#...#","#...#"],'B':["####.","#...#","####.","#...#","####."],
'C':[".####","#....","#....","#....",".####"],'D':["####.","#...#","#...#","#...#","####."],
'E':["#####","#....","####.","#....","#####"],'G':[".####","#....","#..##","#...#",".####"],
'I':["###",".#.",".#.",".#.","###"],'L':["#....","#....","#....","#....","#####"],
'M':["#...#","##.##","#.#.#","#...#","#...#"],'N':["#...#","##..#","#.#.#","#..##","#...#"],
'O':[".###.","#...#","#...#","#...#",".###."],'P':["####.","#...#","####.","#....","#...."],
'R':["####.","#...#","####.","#..#.","#...#"],'S':[".####","#....",".###.","....#","####."],
'T':["#####","..#..","..#..","..#..","..#.."],'U':["#...#","#...#","#...#","#...#",".###."],
'W':["#...#","#...#","#.#.#","##.##","#...#"],'-':["...","...","###","...","..."],
'+':["...",".#.","###",".#.","..."],
}
ICONS={
'person':["..##..","..##..",".####.","######",".####.","......"],
'star':  ["..##..","######",".####.",".####.","##..##","......"],
'moon':  ["..###.",".##...","##....","##....",".##...","..###."],
'gem':   [".####.","######","######",".####.","..##..","......"],
'bolt':  ["...##.","..##..",".####.","..##..",".##...","##...."],
'play':  ["#.....","###...","#####.","###...","#.....","......"],
'shield':["######","######","######",".####.","..##..","......"],
'hammer':["#####.","#####.","..#...","..#...","..#...","......"],
'sword': ["....##","...##.","#.##..",".##...","##.#..","#....."],
'crown': [".#..#.","#.##.#","######","######","######","......"],
}
ICONS.update({
'question':[".####.","##..##","...##.","..##..","......","..##.."],
'shovel':  [".....#","....#.","...#..","####..","###...","##...."],
'bubble':  ["######","#.##.#","######","######",".#....","#....."],
'shieldplus':["######","##..##","#....#","##..##",".####.","..##.."],
'pickaxe': [".####.","#.##.#","..##..","..##..","..##..","..##.."],
'swords':  ["#....#",".#..#.","..##..","..##..",".#..#.","#....#"],
'gear':    ["..##..","######",".#..#.",".#..#.","######","..##.."],
'case':    ["..##..","######","#....#","######","#....#","######"],
})
ICON_OF={'spieler':'person','premium':'star','dream':'moon','prime':'gem','ultimate':'bolt','creator':'play',
 'tsup':'question','tbuilder':'shovel','sup':'bubble','builder':'hammer','supplus':'shieldplus','builderplus':'pickaxe',
 'mod':'sword','modplus':'swords','admin':'gear','manager':'case','owner':'crown'}
def hexc(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mul(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def mix(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
GOLD_T=(255,221,94); GOLD_B=(214,150,40)
ns={}; exec(open('icons12.py').read(),ns); I12=ns['I']; PAL12=ns['PAL']
ranks=yaml.safe_load(open('lazyranks-ranks.yml',encoding='utf-8'))['ranks']
NAMED={'gray':'#AAAAAA','white':'#FFFFFF'}
providers=[]; mapping={}; preview=[]
for i,(rid,r) in enumerate(ranks.items()):
    text=r['name'].upper()
    col=hexc(NAMED.get(r['color'],r['color']))
    lum=0.299*col[0]+0.587*col[1]+0.114*col[2]
    if lum>130: col=mul(col,130/lum)   # helle Farben abdunkeln -> weisse Schrift lesbar
    S=2; H=16
    tw=sum(len(G[ch][0])*S for ch in text)+(len(text)-1)*S
    W=17+tw+5
    im=Image.new('RGBA',(W,H),(0,0,0,0)); px=im.load()
    dark=mul(col,0.35)
    raw=hexc(NAMED.get(r['color'],r['color']))
    BT=mix(raw,(255,255,255),0.35); BB=mul(raw,0.75)
    for y in range(H):
        for x in range(W):
            if (x in (0,W-1)) and (y in (0,H-1)): continue
            if x==0 or y==0 or x==W-1 or y==H-1: px[x,y]=dark+(255,)
            elif x==1 or y==1 or x==W-2 or y==H-2 or x==14: px[x,y]=mix(BT,BB,y/(H-1))+(255,)
            elif x<14: px[x,y]=mul(col,0.55-0.15*(y/H))+(255,)
            else:
                c=mix(mul(col,1.18),mul(col,0.72),(y-2)/(H-5))
                if y==2: c=mix(c,(255,255,255),0.35)
                px[x,y]=c+(255,)
    ic=I12.get(rid)
    for yy,row in enumerate(ic):
        for xx,ch in enumerate(row):
            if PAL12[ch]:
                px[2+xx,2+yy]=PAL12[ch]+(255,)
    def draw(ox,oy,color):
        x=17+ox
        for ch in text:
            g=G[ch]
            for yy,row in enumerate(g):
                for xx,c in enumerate(row):
                    if c=='#':
                        for dy in range(S):
                            for dx in range(S):
                                X=x+xx*S+dx; Y=3+oy+yy*S+dy
                                if 2<=X<W-2 and 2<=Y<H-2: px[X,Y]=color+(255,)
            x+=len(g[0])*S+S
    draw(1,1,mul(col,0.3)); draw(0,0,(255,255,255))
    fn=f'rank_{rid}.png'
    im.save(P+'assets/minecraft/textures/font/'+fn)
    ch=chr(0xE200+i); mapping[rid]=ch
    providers.append({"type":"bitmap","file":"minecraft:font/"+fn,"ascent":7,"height":8,"chars":[ch]})
    preview.append(im)
json.dump({"providers":providers},open(P+'assets/lazymc/font/ranks.json','w'),indent=2)
json.dump(mapping,open('badge_map.json','w'))
m=json.load(open(P+'pack.mcmeta')); m['pack']['description']="§bLazyMC §7- Citybuild Design v11"; json.dump(m,open(P+'pack.mcmeta','w'),indent=2)
rows=[preview[i:i+2] for i in range(0,len(preview),2)]
Wc=max(p.width for p in preview)*3
pv=Image.new('RGBA',(Wc*2+30,len(rows)*54+10),(45,45,45,255))
for r,pair in enumerate(rows):
    for c,p in enumerate(pair):
        pv.alpha_composite(p.resize((p.width*3,p.height*3),Image.NEAREST),(10+c*(Wc+10),10+r*54))
pv.save('badges_preview.png')
print(len(providers))
