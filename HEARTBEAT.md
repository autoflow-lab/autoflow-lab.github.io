# HEARTBEAT.md

## AUTO-IMPROVE: autoflow-lab Website + Dashboards

Bei jedem Heartbeat: Prüfe ob ein Auto-Improve Run fällig ist.
Tracking-Datei: /home/node/.openclaw/workspace/projects/fiverr/PROGRESS.md

**Regel**: Wenn der letzte Eintrag in PROGRESS.md älter als 4 Stunden ist → führe einen Improvement-Run durch:
1. Lies /home/node/.openclaw/workspace/projects/fiverr/AUTOWORK.md
2. Wähle eine [ ] Aufgabe aus der Ideen-Liste
3. Implementiere sie in /home/node/.openclaw/workspace/projects/fiverr/demo.html
4. Deploye zu GitHub (Python deploy snippet in AUTOWORK.md)
5. Markiere Aufgabe als [x] in AUTOWORK.md
6. Schreibe Eintrag in PROGRESS.md mit Timestamp

**Wichtig**: NIEMALS filter="url(#roomBloom)" auf SVG Polygon-Elementen.
**Deploy**: demo.html + index.html beide updaten.
**Qualität**: Dark Mode, Mobile, DE+EN Übersetzung immer mitdenken.

Wenn Run durchgeführt: Eintrag in PROGRESS.md schreiben damit nächster Heartbeat es sieht.
Wenn kein Run fällig (< 4h seit letztem): HEARTBEAT_OK antworten.

## HA DASHBOARD NACHT-VERBESSERUNGEN

Wenn es zwischen 23:00 und 08:00 Uhr ist und kein Improvement in den letzten 3h gemacht wurde:
1. Prüfe wz.html auf offene Issues (aus memory/2026-03-22.md oder aktuellen Stand)
2. Mache targeted fixes
3. Node --check vor jedem Deploy
4. Deploye via SSH
5. Commit zu git

### Bekannte Todo-Liste für Nacht:
- [x] Light mode vollständig fixen (updateHeroGradient setzt dark bg unconditional) — 2026-03-23 01:xx
- [x] Musik-Tab: Spotify Source-Auswahl verbessern — 2026-03-24 01:xx
- [ ] Wetter-Tab: UV-Index anzeigen wenn verfügbar
- [ ] nsscreen.html: WebSocket für live updates
- [ ] family.html: Push-Notification bei offenem Garagentor > 10min
- [x] wz.html: Timer-Funktion für Lichter (auto-aus nach X min) — 2026-03-23 01:xx
- [x] wz.html: Bessere Offline-Banner (aktuell nur nach 2 polls) — 2026-03-24 01:xx
