# LazyMC Resource-Pack

Aktuelle Version: **LazyMC_Pack_v9.zip** (in der server.properties eingetragen).

Inhalt: Cyan-Menü-Design, LazyMC-Logo (Pausenmenü, Hauptmenü, Tablist), Scoreboard-Rahmen mit Icons
und Rang-Abzeichen für alle 17 Ränge.

## Ordner `quelle`
- `quelle/pack` – entpackter Inhalt des Packs (zum Bearbeiten)
- `quelle/werkzeuge/badges.py` – erzeugt die Rang-Abzeichen neu (Farben aus `lazyranks-ranks.yml`)
- `quelle/werkzeuge/icons12.py` – die 12×12-Pixel-Symbole der Ränge

Abzeichen neu erzeugen: `lazyranks-ranks.yml` aus dem lazycore-Repository nach `quelle/werkzeuge/` kopieren,
dann im Ordner `quelle/werkzeuge` `python3 badges.py` ausführen (benötigt Pillow und PyYAML).
Danach den Inhalt von `quelle/pack` als neue ZIP-Datei packen und SHA1 in der server.properties anpassen.
