# HEARTBEAT.md

## NACHT-ARBEIT AKTIV (25./26. März)
Arbeite selbstständig durch die Aufgaben in NIGHTPLAN_2.md.
Starte mit Task 1 (wz.html Icons), dann 2 (Präsenz-Widget), dann weiter.
Nach jedem Task: Eintrag in PROGRESS.md.

## AUTO-IMPROVE: autoflow-lab Website

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
