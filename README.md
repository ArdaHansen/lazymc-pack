# LazyMC Resource-Pack

Aktuelle Version: **LazyMC_Pack_v18.zip** (in der server.properties eingetragen).

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
