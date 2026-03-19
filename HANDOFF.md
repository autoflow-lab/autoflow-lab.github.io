# 🦀 Clawy Handoff — Stand 17. März 2026

## 🌐 Portfolio-Webseite (autoflow-lab.github.io)
**Live:** https://autoflow-lab.github.io/  
**Lokale Datei:** `/workspace/projects/fiverr/demo.html` (v29d, 230KB)  
**GitHub Token:** `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`  
**Deploy:** Python mit requests + base64, PUT to `https://api.github.com/repos/autoflow-lab/autoflow-lab.github.io/contents/demo.html`

### Was noch fehlt auf der Webseite:
1. **Floor-Plan Lichter** — Glow-Kreise stimmen noch nicht 100% mit Wänden überein (schwieriges Problem, v28 deployed aber nicht bestätigt gut)
2. **Fiverr Link** — `openFiverr()` zeigt auf `https://www.fiverr.com/autoflow-lab` — Gig muss noch live sein
3. **Slider auf Mobile** — `touch-action:pan-x` sollte funktionieren (v29d), bitte nochmal testen
4. **SEO** — Open Graph image fehlt noch für Social Sharing

---

## 💼 Fiverr Gig
**Inhalt:** `/workspace/projects/fiverr/FIVERR_GIG.md`
- Basic: €49 | Standard: €149 | Premium: €349
- Manuell erstellen auf fiverr.com → "Create New Gig"
- Titel: "I will build your premium smart home dashboard in Home Assistant"
- Screenshots vom Portfolio machen für Gig-Bilder

---

## 🏠 Home Assistant (192.168.1.123:8123)
**Token:** in `/workspace/config/.env`  
**Version:** 2025.10.3 (Update verfügbar!)

### Wohnzimmer iPad Dashboard
**URL:** http://192.168.1.123:8123/wohnzimmer-ipad  
**Status:** Custom JS Card deployed (custom:wz-dashboard)  
**JS hosted:** https://autoflow-lab.github.io/wz-dashboard.js  
**⚠️ Security TODO:** JS lokal auf HA hosten → `/config/www/wz-dashboard.js`  
**Fix:** Auf dem Pi einloggen (Terminal/SSH mit richtigem Key) und:
```bash
wget -O /config/www/wz-dashboard.js https://autoflow-lab.github.io/wz-dashboard.js
```
Dann in HA unter Einstellungen → Dashboard → Ressourcen:
- `/hacsfiles/...` Einträge behalten
- `https://autoflow-lab.github.io/wz-dashboard.js` → ersetzen durch `/local/wz-dashboard.js`

### Almando Radio schaltet sich aus — URSACHE GEFUNDEN
**Pattern aus Logbook:** `playing → buffering → idle → off` (Stream-Timeout nach ~5-15 Min)  
**Fix benötigt:** Automation erstellen:
```yaml
alias: "Almando Radio Watchdog"
trigger:
  - platform: state
    entity_id: media_player.wohnzimmer_alm
    to: "idle"
    for: "00:00:30"
condition:
  - condition: state
    entity_id: input_boolean.radio_watchdog_active  # helper erstellen
    state: "on"
action:
  - service: media_player.play_media
    data:
      entity_id: media_player.wohnzimmer_alm
      media_content_id: "{{ states('input_text.last_radio_url') }}"
      media_content_type: audio/mp4
```
→ `input_boolean.radio_watchdog_active` + `input_text.last_radio_url` als Helper erstellen  
→ Beim Radio-Start: Watchdog aktivieren + URL speichern

### Büro Dashboard
**URL:** http://192.168.1.123:8123/clawy-dashboard → Tab "Buero"  
**Fix:** `light.buro` → `switch.shelly1_98cdac0ca9b2` in 8 Stellen ersetzt ✅  
**Hue Play L:** `light.hue_play_l` — Raum falsch (Wohnzimmer statt Büro), ggf. korrigieren

---

## 📁 Wichtige Dateien lokal
```
/workspace/
  config/.env          → HA Token, URLs, Passwörter
  MEMORY.md            → Langzeit-Erinnerungen
  memory/2026-03-15.md → Session-Log
  TOOLS.md             → HA-Entities, Zugangsdaten
  projects/fiverr/
    demo.html          → Portfolio-Seite (aktuell v29d)
    demo_v28.html      → Backup v28
    FIVERR_GIG.md      → Gig-Texte
    wz-dashboard.js    → Custom HA Card
```

---

## 🚀 Nächste Schritte (Priorität)
1. **Fiverr Gig erstellen** → fiverr.com → create gig → copy from FIVERR_GIG.md
2. **HA Update** → 2025.10.3 → 2026.x (lange überfällig)
3. **Almando Watchdog** Automation in HA
4. **wz-dashboard.js lokal** hosten (SSH auf Pi oder HA Terminal Addon)
5. **Floor-Plan Polygone** nochmal kalibrieren wenn wieder genug Tokens

---

## 💡 Prompts für Perplexity/andere KI

### Floor-Plan Fix:
> "Ich habe eine SVG Overlay auf einem isometrischen Grundriss (1376x768px). 
> Die Räume sind als Polygone definiert. Ich brauche radiale Gradients (mix-blend-mode:screen) 
> die genau innerhalb der Polygon-Grenzen bleiben. 
> Polygon bed1: 688,148 992,193 992,328 688,283
> Wie berechne ich den korrekten Mittelpunkt und Radius?"

### Almando Watchdog:
> "In Home Assistant möchte ich eine Automation die: 
> wenn media_player.wohnzimmer_alm in den Zustand 'idle' wechselt (nach 30 Sek), 
> den letzten Radio-Stream neu startet. 
> Die URL soll in input_text.last_radio_url gespeichert sein."

### HA Dashboard Security:
> "Wie kann ich eine JS-Datei in Home Assistant's /config/www/ Ordner 
> hochladen ohne SSH-Zugang? HA 2025.10.3 auf Raspberry Pi."
