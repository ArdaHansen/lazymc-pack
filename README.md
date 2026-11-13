# LazyMC Resource-Pack

Aktuelle Version: **LazyMC_Pack_v35.zip** (in der server.properties eingetragen).

Inhalt: Cyan-Menü-Design, LazyMC-Logo (Pausenmenü, Hauptmenü, Tablist), Scoreboard-Rahmen mit Icons
und Rang-Abzeichen für alle 17 Ränge.
Ab v10: alle Menüs (Inventar, Truhen, Ofen, Amboss, Braustand ...) und das HUD (Hotbar, XP-Leiste, Herzen) im LazyMC-v2-Design mit Farbverläufen.

## Ordner `quelle`
- `quelle/pack` – entpackter Inhalt des Packs (zum Bearbeiten)
- `quelle/werkzeuge/badges.py` – erzeugt die Rang-Abzeichen neu (Farben aus `lazyranks-ranks.yml`)
- `quelle/werkzeuge/icons12.py` – die 12×12-Pixel-Symbole der Ränge

Abzeichen neu erzeugen: `lazyranks-ranks.yml` aus dem lazycore-Repository nach `quelle/werkzeuge/` kopieren,
dann im Ordner `quelle/werkzeuge` `python3 badges.py` ausführen (benötigt Pillow und PyYAML).
Danach den Inhalt von `quelle/pack` als neue ZIP-Datei packen und SHA1 in der server.properties anpassen.

- `quelle/werkzeuge/gui_recolor.py` – färbt die Original-GUIs von Minecraft in das LazyMC-Design um (Farbverläufe oben im Skript änderbar)
- `quelle/werkzeuge/gui_tech.py` – Tech-Stil der Menüs (v11): dunkles Metall, Neon-Kanten, Nieten, helle Titelplaketten
- `quelle/werkzeuge/gui_graphite.py` – aktueller Menü-Stil (v12): Graphit-Metall, scharfe Kanten, Cyan nur als Akzent

- `quelle/werkzeuge/ll_icons.py` – Menü-Symbole für LazyLogistics (`lazymc:gui/ll_<name>`), gleicher Stil wie `lcs_icons.py`
- `quelle/werkzeuge/gui_boards.py` – Hintergrundtafeln im Marktplatz-Stil (Font `lazymc:gui`):
  `wirtschaft` (/unternehmen), `logistik` (/logistik), `frame1..6` und `plain1..6` für alle übrigen Menüs.
  Die Panel-Felder müssen zu den Menüs in LazyChestShops und LazyLogistics passen – Layout steht oben im Skript.

### v28
- Marktplatz-Look für `/unternehmen` und `/logistik`: farbige Panels mit Bildern, Beschriftung und Regalbrett
- Tafeln für alle übrigen Menüs (Rahmen + vertiefte Plätze)
- 23 neue Logistik-Symbole
- Server: `resource-pack=` auf `LazyMC_Pack_v28.zip` umstellen, SHA1 `693ed3d13cb02fe7b8fa0e447d0a29922589c9bd`

### v29
- Tafel `unternehmen` für das Unternehmens-Dashboard (Kasse, Team, Shops, Anteile, Zahlen, Upgrades, Gewinn, Logistik)
- Server: `resource-pack=` auf `LazyMC_Pack_v29.zip` umstellen, SHA1 `230bf919fcfa3a44a6d5bd8049220cc8440625a2`

### v30
- Alle Menü-Tafeln im LAZYMC-V2-Look: Navy, Cyan-Neonkante, Panels als dunkles Glas mit Neonrand, Beschriftung in weißer Steinschrift mit Schein
- Neuer Inventarteil `bottom1`..`bottom6` (U+E050..U+E05B): die Plugin-Menüs sind jetzt bis unten im selben Look, Vanilla-Truhen bleiben unverändert
- Kleines LAZYMC-Logo auf der Wirtschaftszentrale (`/unternehmen`)
- Server: `resource-pack=` auf `LazyMC_Pack_v30.zip` umstellen, SHA1 `dbcb612f6f479786b603380899fa696547bf877f`
- Benötigt LazyChestShops 1.2.0 und LazyLogistics 1.1.0 (sonst fehlt der Inventarteil, sonst alles kompatibel)

### v31
- Kleine Pixel-Figuren als Deko (Grasblock, Spitzhacke, Truhe, Münzen, Edelstein, Fackel): auf der Inventar-Leiste, in der Titelleiste, in freien Feldern der Hauptmenüs und in den oberen Ecken der Rahmen-Menüs
- Rahmen-Menüs mit Neonleisten und Nieten rundum
- Keine Plugin-Änderung nötig (gleiche Zeichen wie v30)
- Server: `resource-pack=` auf `LazyMC_Pack_v31.zip` umstellen, SHA1 `dc9c53046af3d686d4bad63251b384af92d6d1a9`

### v32
- Panel-Beschriftungen in derselben Schrift wie die Titel-Plaketten, mit feinem Rand und Schatten statt der groben Steinschrift; Umlaut-Punkte über dem Buchstaben
- Keine Plugin-Änderung nötig
- Server: `resource-pack=` auf `LazyMC_Pack_v32.zip` umstellen, SHA1 `bf8324861580276ce0f4c61ac331045b2e14cc2d`
