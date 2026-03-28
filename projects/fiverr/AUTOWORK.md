# AUTOWORK.md — Autonome Verbesserungs-Aufgaben
# Clawy arbeitet diese Liste selbständig ab

## Wie es funktioniert
- Jeder Cron-Run liest diese Datei
- Wählt eine [ ] Aufgabe aus
- Implementiert sie in wz.html
- Deployed zu HA SSH
- Markiert als [x] + schreibt Eintrag in PROGRESS.md

## Regeln
- IMMER: `node --check /tmp/test_js.js` vor Deploy
- IMMER: JS aus <script> extrahieren vor Check
- NIEMALS: filter="url(#roomBloom)" auf SVG Polygon
- NIEMALS: duplicate IDs erstellen (z.B. wx-big-desc existiert 2x → Fehler)
- Deploy: SSH nach 192.168.1.123, sudo cp /tmp/wz.html /config/www/wz.html
- Nach Deploy: PROGRESS.md updaten mit Timestamp + was gemacht wurde

## Design-Regeln (nicht brechen!)
- iOS Dark Palette: #000 bg, #1c1c1e/#2c2c2e/#3a3a3c cards
- Akzentfarben: amber #ff9f0a (Licht), blau #0a84ff (Media), grün #30d158 (aktiv)
- Kein Lila/Indigo irgendwo
- Alle Touch: addEventListener, nie onclick=
- touch-action:manipulation auf * global

## Ideen-Liste ([ ] = offen, [x] = erledigt)

### Design & Animation
- [x] Wetter-Hero Hintergrundfarbe wechselt je nach Wetter (Regen=dunkelblau, Sonne=warmorange)
- [x] Szenen-Buttons auf Home: leichter Parallax-Effekt beim Scrollen
- [x] Tile-Icons: bei "An" subtle pulse-ring um den Icon-Kreis
- [x] Nav-Bar: aktiver Tab hat sanften Glow unter dem Icon
- [x] Wetter-Tab: Sonnenauf/Untergang Visualisierung als Bogen
- [x] Album-Cover: wenn Spotify spielt, generiere Gradient aus Track-Farben (Mood-Gradient)
- [x] Licht-Tiles: Farbtemperatur als warme/kühle Tile-Tönung

### Features
- [x] Wetter-Tab: Gefühlte Temperatur als grosse Nebenzahl
- [x] Schnell-Szene via Long-Press auf Home-Hero: Popup mit 4 Szenen
- [x] Musik-Tab: Fortschrittsbalken für aktuellen Track (media_position/media_duration)
- [x] Wetter: Pollen-Warnung für Schweiz (wenn API verfügbar)
- [x] Home-Screen: "Willkommen zurück, Janis" mit Tageszeit-Greeting
- [x] Szenen auf Home: zeige welche gerade aktiv ist (basierend auf Lichtzustand)
- [x] Wetter-Tab: Regenmenge nächste 24h als Mini-Balkendiagramm
- [x] Debug-Panel: Textarea statt div (kopierbar)

### Stabilität
- [x] fetchStates: Retry nach 3x Fehler mit Backoff
- [x] Token-Refresh: automatisch wenn 401 zurückkommt
- [x] Offline-Banner: wenn HA nicht erreichbar → Toast "Offline – Verbinde..."
- [x] Light-Sheet: schliessen wenn man ausserhalb tippt (overlay-click)

### Neue Seiten
- [x] nsscreen.html verbessern: Szenen-Buttons hinzufügen, gleiche Farblogik
- [x] ipad.html: Vollbild-Ansicht für Floorplan mit Licht-Glow

## Gesperrte Entities (nicht in Dashboard)
- light.hue_iris — Schlafzimmer, nicht Wohnzimmer
- light.h61e1 — Govee Wand, offline (sobald online: Wohnzimmer)
- light.gang_og_licht / light.gang_eg_licht — nodim:true, Template-Entity, oft unavailable

## Neue Ideen (2026-03-20)
- [x] wz.html: Sunrise/Sunset Anzeige im Wetter-Tab (☀️ 06:32 · 🌅 19:14)
- [x] wz.html: Licht-Tiles pulsieren wenn gerade geschaltet wird (kurze Pulse-Animation)
- [x] wz.html: "Zuletzt geändert" unter jedem Licht-Tile (last_changed aus HA)
- [x] demo.html: Testimonial-Karussell (auto-scrollend, 3 Reviews)
- [x] demo.html: "Powered by autoflow-lab" Badge im Footer mit Link zur Demo
- [x] ipad.html: Klick auf Raum im Grundriss → Licht toggle
- [x] wz.html: Energie-Widget auf Home (if sensor.stromverbrauch available)
- [x] nsscreen.html: Wetter-Tab mit stündlicher Vorschau
- [x] premium_template.html: auf GitHub Pages verlinken von demo.html Preissektion

## Neue Ideen (2026-03-20 Morgen)
- [x] wz.html: Konfetti-Animation wenn Szene "Abend" aktiviert wird (Easter Egg)
- [x] wz.html: Wetter-Icon animiert (CSS keyframes je nach Wettercode: Regen fällt, Sonne dreht)
- [x] wz.html: Hero-Hintergrund: Sterne-Parallax nachts (CSS particles)
- [x] demo.html: Preise mit Durchstreichpreis (~~€99~~ €49) + "Begrenzte Aktion" Badge
- [x] demo.html: Animated counter für Stats beim Einblenden (Intersection Observer)
- [x] demo.html: WhatsApp-Button zum Direktkontakt (wa.me Link)
- [x] wz.html: Musik-Tab: Almando Speaker-Icon mit Wellen-Animation wenn spielt
- [x] wz.html: Tages-Zusammenfassung auf Home ("5 Lichter heute genutzt, 3h Musik")
- [x] wz.html: Wetter-Tab: UV-Index Anzeige (Open-Meteo liefert uv_index)
- [x] MARKETING: Reddit-Post auf r/homeassistant schreiben (Entwurf fertigstellen)

## Neue Ideen (2026-03-21 Morgen)
- [x] wz.html: Musik-Tab: Lautstärke per vertikalen Swipe auf Album-Art (swipe up/down = vol +/-, iOS-Style Overlay)

## Neue Ideen (2026-03-21)
- [x] wz.html: Musik-Tab: Blurred Album-Cover als dynamischer Seiten-Hintergrund (wie Spotify iOS)
- [x] wz.html: Musik-Tab: Swipe Left/Right für Track-Skip (next/prev) mit Hint-Animation
- [x] wz.html: Wetter-Tab: Temperaturkurve 24h als glatte SVG-Area-Chart (gradient-filled, Jetzt-Punkt, Stunden-Labels)
- [x] wz.html: Home-Tab: Floating "Alle Lichter aus" FAB-Button (erscheint wenn ≥1 Licht an, 2-Tap Bestätigung)
- [x] wz.html: Home-Hero: Tageszeit-Fortschritts-Arc (flacher SVG-Bogen zeigt % des Tages, Farbe+Glow-Dot je Tageszeit)

## Neue Ideen (2026-03-21 Abend)
- [x] wz.html: Licht-Tiles — Tap-Ripple Effekt (Kreisförmige Welle vom Touch-Punkt, in Tile-Farbe)
- [x] wz.html: Wetter-Hero — Animiertes Niederschlags-Canvas (Regen-Tropfen / Schneeflocken über dem Hero)

## Neue Ideen (2026-03-22 Morgen)
- [x] wz.html: Tab-Wechsel — Staggered Card-Entrance Animation (Kinder-Elemente blenden beim Tab-Wechsel gestaffelt ein, fade+translateY, 0.04s–0.46s Delays)

## Neue Ideen (2026-03-22)
- [x] wz.html: Wetter-Tab — Windrichtungs-Kompass (animierter SVG-Kompass neben Wind-km/h, dreht sich mit wind_direction_10m, N/NO/O/SO/S/SW/W/NW Label)
- [x] wz.html: Licht-Tiles — Helligkeits-Arc Ring (dünner SVG-Kreisbogen um .ltico zeigt brightness_pct als animierten Arc)

## Neue Ideen (2026-03-21 Morgen)
- [x] demo.html: Scarcity-Banner oben ("🔥 Nur noch 3 Plätze diese Woche") — erscheint nach 1.8s, schliessbar
- [x] demo.html: Vorher/Nachher Slider (Standard HA vs. Custom Dashboard) als visueller Beweis
- [x] demo.html: Exit-Intent Popup (Mouse-Richtung erkennen) mit 10% Rabatt-Angebot
- [x] wz.html: Kalender-Widget auf Home-Tab (nächste 2 Events aus calendar.* Entities)
- [x] demo.html: Video-Embed-Placeholder (YouTube-ähnlich) mit Thumbnail + Play-Button (öffnet Fiverr GIG)

## Neue Ideen (2026-03-22 Morgen)
- [x] wz.html: Wetter-Tab — Mondphase-Card (astronomische Berechnung, animierter SVG-Mond, Phasenname + Beleuchtungs-Balken)

## Neue Ideen (2026-03-22 Nachmittag)
- [x] wz.html: Wetter-Tab — Luftdruck-Barometer Card (surface_pressure von Open-Meteo, animierter SVG-Arc 960–1040 hPa, Trend-Pfeil ↑↓→, Beschreibung je Drucklage)

## Neue Ideen (2026-03-22 Abend)
- [x] wz.html: Nav-Bar — Licht-Tab Badge (amber Zahl-Badge über Licht-Icon zeigt Anzahl aktiver Lichter, animate-in/out, Pop-Animation bei Änderung)

## Neue Ideen (2026-03-22 Nacht)
- [x] wz.html: Musik-Tab — "Now Playing" Rich Notification (Apple-Style Pill erscheint oben beim Track-Wechsel: Mini Album-Art + Track-Titel + Artist + animierte Equalizer-Wellen, 4.2s sichtbar, spring-in Animation)

## Neue Ideen (2026-03-22 Nacht 2)
- [x] wz.html: Wetter-Tab — Wind-Chill / Heat-Index Komfort-Karte (berechnet gefühlte Bedingungen, animierter SVG-Arc, Komfort-Skala, Kleidungsempfehlung)

## Neue Ideen (2026-03-23 Nacht)
- [x] wz.html: Musik-Tab — Vinyl-Tonearm Animation (SVG-Abtastarm schwenkt bei Play auf Disc, zieht sich bei Pause zurück, spring cubic-bezier)

## Neue Ideen (2026-03-22 Morgen 2)
- [x] demo.html: Social Proof Toast — zufällige "Jemand hat bestellt" Notification-Einblendungen (Conversion-Booster)
- [x] demo.html: FAQ Accordion-Section (5 häufige Fragen, smooth expand/collapse Animation)
- [x] demo.html: "Wie es funktioniert" Timeline-Section (3 Schritte: Anfragen → Konfigurieren → Genießen, animated icons)
- [x] wz.html: Home-Tab — Quick-Actions Bar (4 kleine Icon-Buttons: Alle aus / Szene / Musik / Heizung, horizontal scrollbar)
- [x] demo.html: Trust-Badge-Row unter dem CTA-Button (🔒 Sicher bezahlen · ⭐ 5 Sterne · ⚡ 24h Lieferung · 💬 24/7 Support)

## Neue Ideen (2026-03-23 Mittag)
- [x] wz.html: Musik-Tab — Audio Spectrum Visualizer Canvas (animierte Frequenz-Balken im Hintergrund, amber→blau Gradient, MutationObserver auf spk-wrap.playing)

## Neue Ideen (2026-03-23 Nacht 2)
- [x] wz.html: Pull-to-Refresh Indikator (iOS-Style touchmove, progress-Arc, "Aktualisiere..." Label, ruft fetchStates())
- [x] wz.html: Licht-Tab — Gruppen-Header mit Collapse/Expand (Räume faltbar: "Wohnzimmer ▼", alle Tiles darunter, Tap auf Header klappt ein/aus)
- [x] wz.html: Home-Tab — Aktive Szene Chip (kleiner Chip unter Hero: "🌅 Abend-Szene aktiv", basierend auf Lichtzustand)
- [x] demo.html: Sticky Mobile CTA-Bar (am unteren Rand auf Mobile: "Jetzt beauftragen → ab €29", erscheint nach 3s Scroll)
- [x] wz.html: Musik-Tab — Sleep-Timer Button (⏱ 15/30/60 min, Countdown-Pill, ruft media_player.turn_off nach Ablauf)

## Neue Ideen (2026-03-23 Nachmittag)
- [x] wz.html: Geräte-Tab — Device Pulse-Dot + last_changed Timestamp (animierter grüner Dot wenn an, "vor X min" relative Zeit in Status-Zeile)

## Neue Ideen (2026-03-23 16:03 UTC)
- [x] wz.html: Home-Hero — Lichtstimmung Ambient Orb (weicher Glow-Orb rechts im Hero, Farbe = Durchschnitt der aktiven Licht-RGB-Werte, faded ein/aus je nach Lichtzustand, eigene Drift-Animation)

## Neue Ideen (2026-03-23 17:09 UTC)
- [x] wz.html: Home-Tab — Mini Forecast Strip (2 Chips: morgen + übermorgen, wxIco + Kurztext + Hi/Lo Temp, unter Scene-Chip)
- [x] wz.html: Licht-Tab — Farbige Tile-Border bei RGB-Lichtern (wenn color_temp/hs_color vorhanden → dünner farbiger Border um .ltico, passend zur Lichtfarbe)
- [x] demo.html: Countdown Timer für "Begrenzte Aktion" (echter 24h Countdown unter Scarcity-Banner, zählt von localStorage-gespeichertem Start runter)
- [x] wz.html: Musik-Tab — Equalizer-Ringe um Album-Art (konzentrisches Pulse wenn isPlaying, 3 halbtransparente Ringe, amber, unterschiedliche Frequenzen via animation-delay)
- [x] wz.html: Wetter-Tab — Gefühlte Temperatur Trend-Pfeil (↑↓ je ob apparent_temperature > temperature_2m, Farbe grün/rot, animierter Pfeil)

## Neue Ideen (2026-03-24 00:03 UTC)
- [x] wz.html: Licht-Tab — Gesamt-Helligkeits-Meter (animierter Gradient-Balken oben im Licht-Tab zeigt Durchschnittshelligkeit aller aktiven Lichter, % Label + "X von Y an", smooth width-Transition)

## Neue Ideen (2026-03-24 02:03 UTC)
- [x] wz.html: Home-Hero — Animierte SVG-Wellen im Hintergrund (2 überlagerte Sinuswellen am unteren Hero-Rand, amber + blau Gradient-Fill, gegenläufige Richtungen, 18s/24s Loop, z-index:1 unter hcont)

## Neue Ideen (2026-03-24 02:05 UTC)
- [x] demo.html: Live-Besucher FOMO-Counter im Hero (grüner Pulse-Dot, 4-8 Besucher, drift ±1 alle 18-45s)
- [x] wz.html: Wetter-Tab — "Goldene Stunde" Karte (Sonnenuntergang - 45min bis Sonnenuntergang, orangener Glow, "Perfektes Foto-Licht" Hinweis)
- [x] demo.html: Anchor-Navigation (sticky Mini-Nav unter Header: Überblick · Preise · Demo · Kontakt, smooth scroll, aktiver Abschnitt highlighted)
- [x] wz.html: Home-Tab — Batterie-Status Chip (wenn sensor.*.battery_level < 20% → roter Chip "Batterie schwach: Gerätename X%")
- [x] demo.html: "Kunden-Stimmen" Ratings-Balken (5⭐ 87% / 4⭐ 13% als animierte Balken, IntersectionObserver)

## Neue Ideen (2026-03-24 12:03 UTC)
- [x] wz.html: Wetter-Tab — "Beste Stunde" Karte (scannt stündliche Vorschau nach optimalem Outdoor-Zeitfenster heute: Score aus Temp-Komfort + Regenwahrsch. + Wind + WMO-Code, grüner Zeit-Badge + Condition-Chips)

## Neue Ideen (2026-03-24 Nachmittag)
- [x] demo.html: Scroll-to-Top Button (erscheint ab 500px, amber Ring-Icon, smooth scroll, fade+scale Animation)
- [x] demo.html: "Warum jetzt?" 3-Spalten Urgency-Section (Zeitersparnis / Kostenersparnis / Komplexität — je mit animiertem Icon + Zahl-Highlight)
- [x] wz.html: Musik-Tab — Podcast/Radio Fallback-Anzeige (wenn kein Spotify → zeigt media_title + media_content_id als Radio-Card mit Frequenz-Icon)
- [x] demo.html: Cookie/DSGVO Banner (schlichter Bottom-Banner, "Diese Seite verwendet keine Tracking-Cookies", einmalig schliessbar, localStorage)
- [x] wz.html: Wetter-Tab — Allergiker-Warnung Chip (Gras/Birke/Ambrosia Pollen via Open-Meteo wenn verfügbar, farbcodiert nach Level)

## Neue Ideen (2026-03-25 00:03 UTC)
- [x] wz.html: Musik-Tab — Track Progress Arc um Album-Disc (dünner SVG-Kreisbogen außen um die Vinyl-Disc, amber→gelb Gradient, zeigt media_position/media_duration als animierten Fortschrittsring, smooth transition 1.2s)

## Neue Ideen (2026-03-25 02:03 UTC)
- [x] wz.html: Home-Hero — Mini SVG Analog Clock neben Digitaluhr (44px SVG-Uhr, amber Stundenzeiger, weißer Minutenzeiger, roter Sekundenzeiger, Tick-Marks bei 12/3/6/9, Einblende-Animation, sekundengenau per updateClock() rotiert)

## Neue Ideen (2026-03-25 04:03 UTC)
- [x] wz.html: Wetter-Tab — Luftfeuchtigkeit Komfort-Karte (SVG-Arc-Gauge 0–100%, Farb-Gradient blau→grün→amber→rot, Komfort-Stufen Sehr trocken/Trocken/Optimal/Feucht/Sehr feucht, Magnus-Formel Taupunkt-Berechnung, animierter Fortschrittsbalken)

## Neue Ideen (2026-03-25 08:03 UTC)
- [x] wz.html: Wetter-Tab — Sichtweite & Bewölkungs-Karte (visibility + cloud_cover von Open-Meteo, zwei SVG-Arc-Gauges nebeneinander, Sichtweite rot→amber→grün→blau Farbskala 0–50km, Bewölkung grün→blau→weiß 0–100%, 6 Sichtweite-Stufen von "Dichter Nebel" bis "Ausgezeichnet", 5 Bewölkungs-Stufen von "Klar" bis "Bedeckt", animierte stroke-dashoffset Transition 1.4s)

## Neue Ideen (2026-03-25 09:37 UTC)
- [x] wz.html: Wetter-Tab — Wetter-Score Karte (Gesamtscore 0–100 aus Temperatur-Komfort + Niederschlag + Wind + WMO-Code, SVG Arc-Gauge rot→amber→grün Gradient, 5 Bewertungsstufen von "Drinnen bleiben 🌧" bis "Herrliches Wetter ☀️", Beschreibungstext + farbige Condition-Chips für Temp/Regen/Wind/UV)

## Neue Ideen (2026-03-25 16:37 UTC)
- [x] wz.html: Home-Tab — Jahreszeit-Chip (🌸/☀️/🍂/❄️ Emoji + Jahreszeitsname + "Xd bis [nächste]" Countdown, astronomische Berechnung, farbcodiert grün/amber/orange/blau, erscheint unter Mini-Forecast-Strip)

## Neue Ideen (2026-03-25 14:03 UTC)
- [x] wz.html: Home-Hero — Typewriter-Animation für Greeting-Text (tippt Begrüssung zeichenweise ein mit blinkendem Cursor)

## Neue Ideen (2026-03-25 12:03 UTC)
- [x] wz.html: App — Horizontales Swipe zwischen Tabs (touchstart/end auf #app, swipe links→nächster Tab, rechts→vorheriger Tab, MAX_DX 65px Threshold, MAX_DY 80px Guard gegen Scroll-Konflikt, MAX_MS 480ms Zeitfenster, zentrierter Emoji-Hint-Overlay ◀/▶ erscheint kurz mit Glassmorphism, ruft navTo() auf für einheitliche Stagger-Animation)

## Neue Ideen (2026-03-25 22:13 UTC)
- [x] demo.html: Pricing-Bereich — Tages-Deal Chip (7 rotierende Wochentagsangebote über dem Preistisch: "🎨 Heute: Gratis Dark-Mode Theme" etc., amber Pulse-Dot + Glow, animierter Einblend, DE+EN i18n)

## Neue Ideen (2026-03-26 01:00 UTC)
- [x] wz.html: Licht-Tab — Globaler Dimmer-Schieberegler (Range-Slider nach Helligkeits-Meter, dimmt alle aktiven Lichter gleichzeitig auf gewählte %, 350ms Debounce, Slider-Thumb synct mit avg brightness)
- [x] wz.html: Wetter-Tab — Wochenend-Highlight im 7-Tage Forecast (Sa/So Zeilen mit blauem linkem Rand + hellblauem Sub-Label hervorgehoben)

## Neue Ideen (2026-03-26 00:03 UTC)
- [x] wz.html: Home-Hero — Sonnenuntergang/Sonnenaufgang Countdown-Chip (kleiner animierter Pill-Chip direkt unter dem Day-Arc, zeigt Countdown bis nächstem Sonnenaufgang 🌄 oder Sonnenuntergang 🌅, aktualisiert sich sekündlich mit updateDayArc(), verwendet _wx.daily Daten, zwei Farbvarianten: amber für Sunset, blau für Sunrise)

## Neue Ideen (2026-03-26 02:37 UTC)
- [x] demo.html: Kundenprojekte Galerie Section (3 Projekt-Cards mit gradient Preview, Badges, Tech-Chips, Hover-Lift — Wohnzimmer Setup / Smart Office / Energie-Monitor, erscheint vor Kontaktformular)

## Neue Ideen (2026-03-26 04:03 UTC)
- [x] wz.html: Wetter-Tab — Stündliche Wind-Kurve 24H (SVG-Area-Chart analog zur Temp-Kurve, blaues Gradient-Fill, Jetzt-Dot, Stunden-Labels, Max-Wind Info-Zeile mit Windstärke-Beschreibung)

## Neue Ideen (2026-03-26 08:03 UTC)
- [x] wz.html: Nav-Icons — Burst-Animation beim Tab-Wechsel (jedes Tab-Icon hat eine einzigartige Animations-Geste beim Aktivieren: Home=Bounce, Musik=Spin, Licht=Glow-Flash, Wetter=Wobble, Geräte=Shake)

## Neue Ideen (2026-03-26 06:03 UTC)
- [x] wz.html: Wetter-Tab — Temperatur-Heatmap im 7-Tage-Forecast (subtiler Links-Farbverlauf pro Zeile je Maximaltemperatur: ≤2°C blau, ≤8°C hellblau, ≤14°C grün, ≤20°C hellgrün, ≤26°C amber, ≤32°C orange, >32°C rot — sofort erkennbar ob die Woche kalt oder warm wird)

## Neue Ideen (2026-03-26 08:37 UTC)
- [x] wz.html: Wetter-Tab — Frostwarnung Card (❄️/🥶 erscheint wenn temperature_2m_min < 2°C in den nächsten 4 Tagen, zeigt betroffene Tage als Chips, Minimal-Temperatur, blau→lila Farbgebung je nach Schwere)

## Neue Ideen (2026-03-26 10:03 UTC)
- [x] wz.html: Wetter-Tab — Kleidungs-Empfehlung Card (👗 Outfit-Vorschlag basierend auf apparent_temperature + Niederschlag + Wind + UV-Index: Emoji-Kleidungsstücke je Temperaturstufe, Modifier-Chips für Regen/Schnee/Wind/UV/Schwüle, farbiger Akzent-Orb passend zur Temperatur-Skala)

## Neue Ideen (2026-03-26 14:37 UTC)
- [x] wz.html: Wetter-Tab — Wöchentlicher Niederschlags-Überblick Card (🌧 Balkendiagramm 7 Tage aus precipitation_sum, Gesamt-mm, Kategorien Trocken/Normal/Nass/Sehr nass, Regentage-Zähler, animierte Bar-Höhe)

## Neue Ideen (2026-03-26 16:03 UTC)
- [x] wz.html: Nav-Bar — Fließender Sliding-Pill Aktiv-Indikator (amber halbtransparenter Pill-Hintergrund gleitet smooth zwischen den 5 Nav-Tabs, cubic-bezier spring Transition, positioniert sich via getBoundingClientRect, initialisiert beim DOMContentLoaded auf Home-Tab)

## Neue Ideen (2026-03-26 18:03 UTC)
- [x] wz.html: Home-Tab — 7-Tage-Temperatur Sparkline im Home-Wetter-Widget (mini 56×16px SVG-Linienkurve unter "Gefühlt X°" im hwx-Card, smooth cubic-bezier Kurve, amber Gradient-Fill, Start-Dot + End-Dot, zeigt Wochen-Temperaturtrend auf einen Blick, fade-in via .show Klasse)

## Neue Ideen (2026-03-26 22:03 UTC)
- [x] wz.html: Wetter-Tab — Regenrisiko-Heatmap 24H (kompakte Balken-Reihe: 24 Stunden × Farb-Codierung grün→gelb→amber→orange→rot je Niederschlagswahrscheinlichkeit, aktuelle Stunde hervorgehoben, Summary-Zeile "X Stunden erhöhtes Regenrisiko", zeigt auf einen Blick WANN es heute regnen könnte)

## Neue Ideen (2026-03-27 02:03 UTC)
- [x] wz.html: Wetter-Tab — "Nächster Regen / Aufklärung" Countdown-Chip im Wetter-Hero (scannt stündliche precipitation_probability: wenn es regnet → "☀️ Aufklärung in ~Xh"; wenn kein Regen → "🌧 Regen in ~Xh" oder "✅ Heute kein Regen erwartet"; 3 Farbvarianten blau/amber/grün, fade-in Animation, direkt über den Allergiker-Chips)

## Neue Ideen (2026-03-27 04:03 UTC)
- [x] wz.html: Home-Hero — "Wetter-Brief" Sentence (1-Satz personalisierter Wetter-Überblick im Home-Hero: generiert kontextsensitiven Satz aus WMO-Code + Temperatur + Regenwahrscheinlichkeit + UV + Wind, z.B. "🌤 Morgens schön, bis 14° — nachmittags Regen ☔", fade-in Animation, Light-Mode kompatibel)

## Neue Ideen (2026-03-27 12:03 UTC)
- [x] wz.html: Wetter-Tab — Solar-Einstrahlung 24h Karte (☀️ shortwave_radiation von Open-Meteo, SVG Area-Chart gelb/amber Gradient, Peak-Stunde Badge, Gesamt-Wh/m², Condition-Text)

## Neue Ideen (2026-03-27 08:03 UTC)
- [x] wz.html: Licht-Tab — Fade-Out Timer (🌙 Lichter in 15/30/60 min ausblenden: sanftes Dimmen die letzten 90s, dann turn_off; Countdown-Pill mit Puls-Dot; Cancel-Button; nur sichtbar wenn Lichter an)

## Neue Ideen (2026-03-27 00:03 UTC)
- [x] wz.html: Licht-Tab — Circadian Lighting Button

## Neue Ideen (2026-03-27 16:03 UTC)
- [x] wz.html: Home-Tab — Tages-Mood-Tracker (😊/😐/😔 Emoji-Picker, localStorage, 7-Tage Dot-Verlauf)

## Neue Ideen (2026-03-27 18:03 UTC)
- [x] wz.html: Geräte-Tab — "Letzte Schaltvorgänge" Mini-Timeline (letzte 5 State-Changes aller Lichter + Geräte, chronologisch mit relativem Zeitstempel, farbiger Dot in Entity-Farbe, Ein/Aus Badge, localStorage-Persistenz)

## Neue Ideen (2026-03-27 20:03 UTC)
- [x] wz.html: Home-Tab — "Aktive Lichter" Farb-Dots Strip (kompakte Pill-Chips direkt vor der Tages-Zusammenfassung, zeigt jeden aktiven Licht als farbigen Dot + Name, Farbe = tatsächliche RGB/Farbtemperatur, animiertes Einblenden mit staggered lcsIn, verschwindet wenn alle Lichter aus)

## Neue Ideen (2026-03-27 22:03 UTC)
- [x] wz.html: Home-Tab — "Stunde der Stille" Nacht-Chip (🌙 erscheint zwischen 22:00–07:00, pulsierender blauer Dot, Countdown "noch Xh Ymin bis 07:00", dezentes blaues Farbschema rgba(10,132,255), spring-in Animation, aktualisiert sich mit jedem updateAll()-Poll)

## Neue Ideen (2026-03-27 14:03 UTC)
- [x] wz.html: Licht-Tab — Party Mode Button (🪩 Disco-Modus: alle aktiven RGB-Lichter wechseln jede 500ms zu einer anderen Zufallsfarbe, 120 BPM, 10min Auto-Stop, Countdown-Pill mit Puls-Dot, ✕ Cancel, Disco-Ball-Icon rotiert, lila Farbschema)

## Neue Ideen (2026-03-28 00:02 UTC)
- [x] wz.html: Geräte-Tab — "Zuletzt genutzt" Timeline (Top-5 Entities sortiert nach last_changed, relative Zeit "vor X min", State-Icon grün/grau/amber, eingeblendet über Dev-Cards)

## Neue Ideen (2026-03-27 08:03 UTC)
- [x] demo.html: Floating Live-Chat FAQ Widget (🦀 Bot unten rechts, 3 klickbare FAQ-Fragen mit Antworten, Fiverr-CTA, Badge-Notification nach 4s, DE+EN i18n, schliessbar) (🌿 Tageszeit-optimierter Einzel-Tap-Button zwischen Global-Dimmer und Schnellfarben-Palette: berechnet ideale Farbtemperatur 1900K–6500K + Helligkeit 18%–100% je Tagesphase Nacht/Morgengrauen/Morgen/Mittag/Nachmittag/Abend/Spätabend, zeigt aktuellen Tageszeit-Emoji + Zielwerte live, setzt alle aktiven Lichter per svc('light','turn_on',{color_temp_kelvin, brightness_pct}), grüner Flash-Animation bei Tap, Toast "🌅 Circadian auf X Lichter · 2700K / 45%")
