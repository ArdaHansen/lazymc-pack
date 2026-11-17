# LazyMC Resource-Pack

Aktuelle Version: **LazyMC_Pack_v41.zip** – SHA1 `dd5c351b22a76edd7b71939fc3f80f48e59c26e6`

Im Hauptordner liegen nur die aktuelle und die vorige Version: die vorige, damit ein Server, der noch nicht
umgestellt ist, sein Pack weiter laden kann. Ältere Versionen liegen in `archiv/`. Was sich wann geändert
hat, steht in [CHANGELOG.md](CHANGELOG.md).

## Aufbau

```
LazyMC_Pack_v<N>.zip     das Pack, wie es der Server ausliefert (Link in der server.properties)
archiv/                  ältere Versionen
quelle/pack/             entpackter Inhalt – hier wird bearbeitet
quelle/werkzeuge/        Skripte, die Teile des Packs erzeugen
quelle/logo/             LazyMC-Logo als Vorlage
```

## Neue Version bauen

1. Im Ordner `quelle/werkzeuge` das passende Skript ausführen (siehe unten), oder direkt in `quelle/pack` ändern.
2. Den **Inhalt** von `quelle/pack` als `LazyMC_Pack_v<N>.zip` in den Hauptordner packen
   (`pack.mcmeta` muss oben in der Zip liegen):
   `cd quelle/pack && zip -qr ../../LazyMC_Pack_v<N>.zip . -x ".*"`
3. `sha1sum LazyMC_Pack_v<N>.zip` und Link + SHA1 in der `server.properties` eintragen.
4. Die vorvorige Version nach `archiv/` verschieben und in CHANGELOG.md einen Eintrag ergänzen.

## Werkzeuge

| Skript | Erzeugt |
|---|---|
| `gui_boards.py` | Hintergrundtafeln der Plugin-Menüs (Font `lazymc:gui`) – siehe unten |
| `lc_icons.py` | Menü-Symbole von LazyCore (`lazymc:gui/lc_<name>`) |
| `lcm_icons.py` | Menü-Symbole von LazyCosmetics (`lazymc:gui/lcm_<name>`) |
| `lcs_icons.py` | Menü-Symbole von LazyChestShops (`lazymc:gui/lcs_<name>`) |
| `ll_icons.py` | Menü-Symbole von LazyLogistics (`lazymc:gui/ll_<name>`) |
| `gui_icons.py`, `pixel_icons.py` | allgemeine Menü-Symbole |
| `badges.py`, `icons12.py` | Rang-Abzeichen (Farben aus `lazyranks-ranks.yml` aus dem lazycore-Repo) |
| `headers.py`, `header_tint.py`, `info_platte.py` | Titel-Plaketten über den Menüs |
| `sidebar_tall.py` | Scoreboard-Rahmen |
| `plot_hud.py`, `company_hud.py` | Anzeigen oben am Bildschirm |
| `coinflip_reel.py` | Walze des Münzwurfs |
| `pause_menu.py` | Pausenmenü |
| `gui_recolor.py`, `gui_tech.py`, `gui_graphite.py`, `gui_premium.py`, `gui_deko.py` | Vanilla-Menüs (Truhe, Ofen, Inventar …) im LazyMC-Design |

Alle Skripte brauchen Python 3 mit Pillow; `badges.py` zusätzlich PyYAML.

## Tafeln (`gui_boards.py`)

Eine Tafel ist ein Bild, das als Schriftzeichen in den Titel eines Menüs geschrieben wird. Die Zeichen
sind fest vergeben – **neue Tafeln hinten anhängen, nie umnummerieren**, sonst zeigen ältere Plugins
die falsche Tafel.

| Zeichen | Tafel | Menü |
|---|---|---|
| U+E000 | `wirtschaft` | /unternehmen (LazyChestShops) |
| U+E002 | `logistik` | /logistik |
| U+E004 | `unternehmen` | Unternehmens-Dashboard |
| U+E006 | `kosmetik` | /kosmetik |
| U+E008 | `handel` | /trade |
| U+E00A | `topspieler` | /topspieler |
| U+E00C | `belohnungen` | /belohnungen → Tag |
| U+E00E | `belohnungen_wahl` | /belohnungen |
| U+E010–E01B | `frame1`–`frame6` | alle übrigen Menüs, blau |
| U+E030–E03B | `plain1`–`plain6` | ohne Rahmen |
| U+E050–E05B | `bottom1`–`bottom6` | Inventarteil unter jeder Tafel |
| U+E060 + 0x10·i | `frame<n>_<farbe>` | Rahmen in grün, gold, rot, lila, rosa, türkis, orange, stahl |

Die Felder einer Tafel müssen zu den Plätzen im Menü passen. Wer eine Tafel ändert, prüft die
zugehörige Klasse im Plugin (die Zahlen stehen dort jeweils mit Verweis auf dieses Skript).
