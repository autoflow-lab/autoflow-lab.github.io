# HEARTBEAT.md

## AUTO-IMPROVE: wz.html Dashboard (Haupt-Aufgabe)

Bei jedem Heartbeat: Prüfe ob ein Auto-Improve Run fällig ist.
Tracking-Datei: /home/node/.openclaw/workspace/projects/fiverr/PROGRESS.md

**Regel**: Wenn der letzte Eintrag in PROGRESS.md älter als 4 Stunden ist → führe einen Improvement-Run durch:
1. Lies /home/node/.openclaw/workspace/projects/fiverr/AUTOWORK.md
2. Wähle eine [ ] Aufgabe aus der Ideen-Liste (bevorzuge Design & Animation)
3. Implementiere sie in /home/node/.openclaw/workspace/projects/fiverr/wz.html
4. JS Check: extrahiere <script>, speichere /tmp/test_js.js, node --check
5. Deploy via SSH: 192.168.1.123, hassio, pw in secure/ha_creds.txt (SSH_PW)
   `sudo cp /tmp/wz.html /config/www/wz.html`
6. Markiere Aufgabe als [x] in AUTOWORK.md
7. Schreibe Eintrag in PROGRESS.md mit UTC Timestamp

**Design-Regeln**: iOS Dark Palette, amber/blau/grün, KEIN Lila.
**Niemals**: duplicate HTML IDs, filter=url(#roomBloom) auf Polygons.
**Qualität**: Mobile-first, touch-action:manipulation, addEventListener statt onclick.

Wenn Run durchgeführt: Eintrag in PROGRESS.md schreiben damit nächster Heartbeat es sieht.
Wenn kein Run fällig (< 4h seit letztem): HEARTBEAT_OK antworten.
