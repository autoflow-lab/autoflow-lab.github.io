# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Home Assistant
- URL: http://192.168.1.123:8123
- HA Version: 2025.10.3 (Update auf 2026.x verfügbar)
- Token: in /home/node/.openclaw/workspace/config/.env gespeichert
- SSH: hassio@192.168.1.123:22 (kein Passwort gespeichert → kein Zugriff)

### Wichtige Entitäten
- Shelly Büro: switch.shelly1_98cdac0ca9b2 (Wandlampe/Decke)
- Hue Büro: light.hue_play_l (Play Bar) — Raum: Wohnzimmer (falsch zugewiesen!)
- light.buro: EXISTIERT NICHT MEHR (war früher Gruppe, jetzt gelöscht)
- Automation: automation.buro_shelly_hue_synchronisieren (Shelly ↔ Hue sync)
- Dashboards: clawy-dashboard, wohnzimmer-ipad, googel-nest, test-bild

### Fix 2026-03-15
- light.buro (nicht existent) in allen 8 Dashboard-Stellen durch switch.shelly1_98cdac0ca9b2 ersetzt
- Shelly State-Icon zum Büro-View (picture-elements) hinzugefügt
