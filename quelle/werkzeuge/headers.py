"""Erzeugt die Titel-Plaketten (Pixelschrift-Kacheln) fuer eigene Menues + GuiTitle.java."""
from PIL import Image
import json, os
PACK='/home/claude/work/pack/'
F={
'A':[".###.","#...#","#####","#...#","#...#"],'B':["####.","#...#","####.","#...#","####."],'C':[".####","#....","#....","#....",".####"],
'D':["####.","#...#","#...#","#...#","####."],'E':["#####","#....","####.","#....","#####"],'F':["#####","#....","####.","#....","#...."],
'G':[".####","#....","#..##","#...#",".####"],'H':["#...#","#...#","#####","#...#","#...#"],'I':["###",".#.",".#.",".#.","###"],
'J':["..###","...#.","...#.","#..#.",".##.."],'K':["#...#","#..#.","###..","#..#.","#...#"],'L':["#....","#....","#....","#....","#####"],
'M':["#...#","##.##","#.#.#","#...#","#...#"],'N':["#...#","##..#","#.#.#","#..##","#...#"],'O':[".###.","#...#","#...#","#...#",".###."],
'P':["####.","#...#","####.","#....","#...."],'Q':[".###.","#...#","#.#.#","#..#.",".##.#"],'R':["####.","#...#","####.","#..#.","#...#"],
'S':[".####","#....",".###.","....#","####."],'T':["#####","..#..","..#..","..#..","..#.."],'U':["#...#","#...#","#...#","#...#",".###."],
'V':["#...#","#...#","#...#",".#.#.","..#.."],'W':["#...#","#...#","#.#.#","##.##","#...#"],'X':["#...#",".#.#.","..#..",".#.#.","#...#"],
'Y':["#...#",".#.#.","..#..","..#..","..#.."],'Z':["#####","...#.","..#..",".#...","#####"],
'Ä':["#...#",".###.","#...#","#####","#...#"],'Ö':["#...#",".###.","#...#","#...#",".###."],'Ü':["#...#","....." ,"#...#","#...#",".###."],
'0':[".###.","#..##","#.#.#","##..#",".###."],'1':[".#.","##.",".#.",".#.","###"],'2':["####.","....#",".###.","#....","#####"],
'3':["####.","....#",".###.","....#","####."],'4':["#..#.","#..#.","#####","...#.","...#."],'5':["#####","#....","####.","....#","####."],
'6':[".###.","#....","####.","#...#",".###."],'7':["#####","...#.","..#..",".#...",".#..."],'8':[".###.","#...#",".###.","#...#",".###."],
'9':[".###.","#...#",".####","....#",".###."],'-':["...","...","###","...","..."],'+':["...",".#.","###",".#.","..."],
'&':[".##..","#..#.",".##.#","#..#.",".##.#"],' ':["..","..","..","..",".."],
}
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
OUT=hx('#07080B'); BORDER=hx('#00E5FF'); BORDER_D=hx('#0094FF'); PLATE=hx('#2B2F37'); PLATE_L=hx('#353A44'); INNER=hx('#14171C')
SCALE=3; TH=52; PH=32  # Texturhoehe, Plakettenhoehe (Textur = 2x Anzeige)
def tile(width, letter=None, kind='mid'):
    im=Image.new('RGBA',(width,TH),(0,0,0,0)); px=im.load()
    for y in range(PH):
        for x in range(width):
            if y in (0,PH-1): c=OUT
            elif y==1: c=BORDER
            elif y==PH-2: c=BORDER_D
            elif y==2 or y==PH-3: c=INNER
            else: c=PLATE_L if y < PH//2 else PLATE
            px[x,y]=c+(255,)
    if kind=='left':
        for y in range(PH):
            px[0,y]=OUT+(255,)
            if 0<y<PH-1: px[1,y]=(BORDER if y<PH//2 else BORDER_D)+(255,)
            if 1<y<PH-2: px[2,y]=INNER+(255,)
        px[0,0]=(0,0,0,0); px[0,PH-1]=(0,0,0,0)
    if kind=='right':
        w=width
        for y in range(PH):
            px[w-1,y]=OUT+(255,)
            if 0<y<PH-1: px[w-2,y]=(BORDER if y<PH//2 else BORDER_D)+(255,)
            if 1<y<PH-2: px[w-3,y]=INNER+(255,)
        px[w-1,0]=(0,0,0,0); px[w-1,PH-1]=(0,0,0,0)
    if letter:
        g=F[letter]; top=(PH-5*SCALE)//2
        for oy,col in ((2,hx('#05060A')),(0,hx('#F2F6FA'))):
            for yy,row in enumerate(g):
                for xx,ch in enumerate(row):
                    if ch=='#':
                        for dy in range(SCALE):
                            for dx in range(SCALE):
                                X=2+xx*SCALE+dx+(oy//2); Y=top+yy*SCALE+dy+oy//2
                                if Y<PH-3: px[X,Y]=col+(255,)
    return im
os.makedirs(PACK+'assets/minecraft/textures/font/header',exist_ok=True)
providers=[]; java=[]; cp=0xE400
def add(name, im, ch):
    fn=f'font/header/{name}.png'; im.save(PACK+'assets/minecraft/textures/'+fn)
    providers.append({"type":"bitmap","file":"minecraft:"+fn,"ascent":25,"height":26,"chars":[ch]})
left=tile(6,kind='left'); right=tile(6,kind='right')
add('cap_left',left,chr(cp)); java.append(('LEFT',cp,3)); cp+=1
add('cap_right',right,chr(cp)); java.append(('RIGHT',cp,3)); cp+=1
letters={}
for ch,g in F.items():
    w=len(g[0])*SCALE+SCALE+1
    if w%2: w+=1
    name='sp' if ch==' ' else {'Ä':'ae','Ö':'oe','Ü':'ue','-':'minus','+':'plus','&':'and'}.get(ch, ch.lower() if ch.isalpha() else 'n'+ch)
    add('c_'+name, tile(w, None if ch==' ' else ch), chr(cp)); letters[ch]=(cp,w//2); cp+=1
# Abstands-Zeichen im Standard-Font
space={"":-1}
shifts=[1,2,4,8,16,32,64,128]
for i,s in enumerate(shifts):
    space[chr(0xE4E0+i)]=-s; space[chr(0xE4E8+i)]=s
providers.append({"type":"space","advances":space})
f=PACK+'assets/minecraft/font/default.json'; d=json.load(open(f))
d['providers']=[p for p in d['providers'] if not ('header/' in p.get('file','') or ('advances' in p and '' in p['advances']))]
d['providers']+=providers
json.dump(d,open(f,'w'),indent=2)
# Java-Klasse
entries=",\n".join(f"            Map.entry('{('\\\\'+'u%04X'%ord(c)) if False else c}', new int[]{{0x{v[0]:04X}, {v[1]}}})" for c,v in letters.items())
src=f'''package de.lazymc.core;

import java.util.Locale;
import java.util.Map;

/**
 * Titel-Plakette ueber eigenen Menues (wie "AUKTIONSHAUS" oben am Menue). Die Kacheln liegen im
 * Resource-Pack (Font minecraft:default, Zeichen ab U+E400). Diese Klasse wurde zusammen mit den
 * Texturen erzeugt - Breiten muessen zum Pack passen.
 */
public final class GuiTitle {{

    private static final int LEFT = 0x{java[0][1]:04X};
    private static final int RIGHT = 0x{java[1][1]:04X};
    private static final int CAP_WIDTH = 3;
    private static final char GAP = '\\uE4F0';
    private static final Map<Character, int[]> CHARS = Map.ofEntries(
{entries}
    );

    private GuiTitle() {{
    }}

    /** Verschiebung in Pixeln (negativ = links) aus den Abstands-Zeichen zusammensetzen. */
    private static String shift(int pixels) {{
        StringBuilder sb = new StringBuilder();
        int base = pixels < 0 ? 0xE4E0 : 0xE4E8;
        int value = Math.abs(pixels);
        for (int bit = 7; bit >= 0; bit--) {{
            if ((value & (1 << bit)) != 0) {{
                sb.append((char) (base + bit));
            }}
        }}
        return sb.toString();
    }}

    /** MiniMessage-Titel mit Plakette, zentriert ueber einem 176 Pixel breiten Menue. */
    public static String header(String text) {{
        String upper = text.toUpperCase(Locale.GERMAN).replace("ß", "SS");
        StringBuilder glyphs = new StringBuilder();
        int width = CAP_WIDTH;
        glyphs.append((char) LEFT).append(GAP);
        for (char c : upper.toCharArray()) {{
            int[] info = CHARS.get(c);
            if (info == null) {{
                continue;
            }}
            glyphs.append((char) info[0]).append(GAP);
            width += info[1];
        }}
        glyphs.append((char) RIGHT).append(GAP);
        width += CAP_WIDTH;
        int offset = 80 - width / 2;
        return "<white><!shadow>" + shift(offset) + glyphs + "</white>";
    }}
}}
'''
open('/home/claude/lazycore/GuiTitle.java','w',encoding='utf-8').write(src)
# Vorschau
def render(text):
    parts=[left]; 
    for c in text.upper():
        if c in letters: parts.append(Image.open(PACK+'assets/minecraft/textures/font/header/c_'+('sp' if c==' ' else {'Ä':'ae','Ö':'oe','Ü':'ue','-':'minus','+':'plus','&':'and'}.get(c, c.lower() if c.isalpha() else 'n'+c))+'.png'))
    parts.append(right)
    W=sum(p.width for p in parts); im=Image.new('RGBA',(W,PH)); x=0
    for p in parts: im.alpha_composite(p.crop((0,0,p.width,PH)),(x,0)); x+=p.width
    return im
pv=Image.new('RGBA',(700,200),(60,64,70,255)); y=10
for t in ['Auktionshaus','Kauf bestätigen','Ränge','Namensfarben']:
    im=render(t); pv.alpha_composite(im.resize((im.width*1,im.height*1)),(10,y)); y+=44
pv.save('/home/claude/work/headers_preview.png'); print(len(letters),'Zeichen')
