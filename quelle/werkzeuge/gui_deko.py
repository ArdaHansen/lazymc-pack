"""
Kleine Pixel-Figuren als Deko fuer die Menue-Tafeln (Pack v31).

Jede Figur ist 16 x 16 Texturpixel (= 8 x 8 Menuepixel bei doppelter Aufloesung).
Zeichen: '.' frei, sonst Farbe aus PAL.
"""
from PIL import Image

PAL = {
    'k': '#050C22',   # Umriss
    'g': '#5BD63A', 'G': '#3A9E24', 'h': '#9BF26A',          # Gras
    'd': '#8A5A34', 'D': '#5E3B20', 'e': '#A8754A',          # Erde / Holz
    'c': '#5FF3FF', 'C': '#1EA6E8', 'w': '#D9FBFF', 'B': '#0E5FA8',  # Diamant / Neon
    'y': '#FFD447', 'Y': '#E39A16', 'l': '#FFF2A8',          # Gold
    'o': '#FF9F1C', 'r': '#FF5A2C',                          # Flamme
    's': '#C9D5EA', 'S': '#8D9EBE',                          # Stein
    'b': '#7A4A26', 'n': '#4A2C16',                          # Truhe
}

FIGURES = {
    'grass': [
        "................",
        ".kkkkkkkkkkkkkk.",
        ".khgghgghgghggk.",
        ".kgGggGgggGgGgk.",
        ".kgGgGGggGGgGGk.",
        ".kdGdGdGdGdGddk.",
        ".kddeddddeddddk.",
        ".kdDddddDdddedk.",
        ".kddddeddddDddk.",
        ".keddDdddeddddk.",
        ".kdddddDdddddDk.",
        ".kDddeddddeDddk.",
        ".kddddddDdddddk.",
        ".kDDDDDDDDDDDDk.",
        ".kkkkkkkkkkkkkk.",
        "................",
    ],
    'pickaxe': [
        "................",
        "...kkkkkkkkk....",
        "..kwcccccccCk...",
        ".kwcCkkkkkcCCk..",
        ".kcCk...kekCCk..",
        ".kCk...kekk.kCk.",
        "..k...kek....kk.",
        "......kek.......",
        ".....kek........",
        "....kek.........",
        "...kek..........",
        "..kek...........",
        ".kek............",
        ".kk.............",
        "................",
        "................",
    ],
    'chest': [
        "................",
        "................",
        "..kkkkkkkkkkkk..",
        ".kbbbbbbbbbbbbk.",
        ".kebbbbbbbbbbnk.",
        ".knnnnnyynnnnnk.",
        ".kkkkkyllykkkkk.",
        ".kbbbbbyYbbbbbk.",
        ".kebbbbbbbbbbnk.",
        ".kbbbbbbbbbbbnk.",
        ".kbbbbbbbbbbbnk.",
        ".knnnnnnnnnnnnk.",
        ".kkkkkkkkkkkkkk.",
        "................",
        "................",
        "................",
    ],
    'coins': [
        "................",
        "......kkkk......",
        ".....kllyyk.....",
        ".....kYYYYk.....",
        "....kkkkkkkk....",
        "...kllyyyyyyk...",
        "...kYYYYYYYYk...",
        "...kkkkkkkkkk...",
        ".kkkkkkkkkkkkkk.",
        "kllyyyyykllyyyyk",
        "kYYYYYYYkYYYYYYk",
        "kllyyyyykllyyyyk",
        "kYYYYYYYkYYYYYYk",
        "kkkkkkkkkkkkkkkk",
        "................",
        "................",
    ],
    'gem': [
        "................",
        "................",
        "....kkkkkkkk....",
        "...kwwcccccCk...",
        "..kwccwccccCCk..",
        ".kkkkkkkkkkkkkk.",
        ".kwcccccccccCBk.",
        "..kcccccccccBk..",
        "...kcccccccBk...",
        "....kcccccBk....",
        ".....kcccBk.....",
        "......kcBk......",
        ".......kk.......",
        "................",
        "................",
        "................",
    ],
    'torch': [
        "......kkk.......",
        ".....kork.......",
        "....kroook......",
        "....kroylok.....",
        "....kolyyok.....",
        ".....kyyok......",
        "......kek.......",
        "......kek.......",
        "......kek.......",
        "......kdk.......",
        "......kek.......",
        "......kek.......",
        "......kdk.......",
        "......kek.......",
        "......kkk.......",
        "................",
    ],
}


def hx(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def figure(name):
    rows = FIGURES[name]
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        assert len(row) == 16, (name, y, len(row))
        for x, ch in enumerate(row):
            if ch != '.':
                px[x, y] = hx(PAL[ch])
    return img
