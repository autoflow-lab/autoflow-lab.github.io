# Reddit Posts v2 — Mit Demo-Link Hook (2026-03-20)
# Diese Posts sind copy-paste ready für Janis

## 🔥 POST 1: r/homeassistant (bester ROI)
**Title:** I built an iOS-style HA dashboard that runs as a single HTML file — here's the live demo

**Body:**
Hey r/homeassistant!

For the past few months I've been building a custom Home Assistant dashboard that looks like a native iOS app — dark mode, smooth animations, live weather, radio streaming, interactive floor plan.

**Live demo here:** https://autoflow-lab.github.io/demo.html
(no HA needed to try it — it works with demo data)

Tech details if you're curious:
- Single HTML file, no frameworks, no build step
- Connects via HA WebSocket + OAuth PKCE  
- Open-Meteo for real weather
- Works on any phone, tablet, or wall panel

I've been deploying it on a Sonoff NS Panel Pro and an iPad as permanent wall dashboards.

**If you want the template** (pre-configured, just add your entities): https://autoflow-lab.github.io/premium_template.html

Happy to answer questions or share specific code snippets!

---
**[Für Janis: Posten wenn du 5 Min hast — kein Account nötig, kannst auch Reddit-App nutzen]**

---

## 🔥 POST 2: r/homeassistant — Showcase (alternativ)
**Title:** 6 months of Home Assistant dashboard work — from chaos to iOS-style dark UI [OC]

**Body:**
Started with the default Lovelace dashboard, ended up building my own iOS-style dark dashboard from scratch.

Features:
- 🌤 Live weather with animated icons
- 💡 Light control with color picker & dimmer
- 🎵 Music player (Almando + Spotify + Radio)
- 🏠 Interactive floor plan — tap a room to toggle lights
- 🎬 Scene buttons (Abend / Film / Hell)
- ⚡ Offline detection + auto-retry

It's a single HTML file. Demo: https://autoflow-lab.github.io/demo.html

If you want the source/template: https://autoflow-lab.github.io/premium_template.html ($29, includes setup guide)

---

## 🔥 POST 3: r/selfhosted
**Title:** Single-file Home Assistant dashboard with no frameworks — live demo

**Body:**
Built a HA dashboard as a pure HTML/CSS/JS file. No React, no Vue, no build step. Just one file you drop in `/config/www/`.

Features: WebSocket connection, OAuth PKCE auth, live weather (Open-Meteo), Spotify + radio, light dimming with color picker, scene buttons, interactive SVG floor plan, standby screen.

Demo: https://autoflow-lab.github.io/demo.html
Template: https://autoflow-lab.github.io/premium_template.html

The full file is ~160KB including everything. Happy to discuss the architecture.

---

## 💬 KOMMENTAR-VORLAGE (wenn jemand fragt "how did you make this?")
```
I built it as a pure HTML/CSS/JS file — no frameworks at all. 
Connects to HA via WebSocket API with OAuth PKCE auth.
The whole thing is one file you drop in /config/www/.
Template here if you want a starting point: https://autoflow-lab.github.io/premium_template.html
```

---
## 📋 POSTING CHECKLIST für Janis:
1. [ ] Reddit-Account öffnen (oder erstellen)
2. [ ] Zu r/homeassistant gehen
3. [ ] "Create Post" → Text → Post 1 einfügen
4. [ ] Screenshot von demo.html als Bild anhängen (macht +50% mehr Upvotes)
5. [ ] Posten!

**Screenshot machen:** autoflow-lab.github.io/demo.html auf dem Handy öffnen → Screenshot → an Reddit-Post anhängen
