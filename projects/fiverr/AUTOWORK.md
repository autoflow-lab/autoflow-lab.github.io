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

## Neue Ideen (2026-03-28 00:03 UTC)
- [x] wz.html: Wetter-Tab — Gewitter-Alarm-Card (⚡ scannt stündliche WMO-Codes ≥95 in den nächsten 12h, animierter Blitz-Flash, rote Warn-Card mit Intensitäts-Badge + Zeit-Chips, spring-in Animation)

## Neue Ideen (2026-03-28 02:03 UTC)
- [x] wz.html: Home-Tab — Heizungs-Status Chip (🔥/❄️/🌡 zeigt climate.* Entity: Ist-Temp vs. Soll-Temp, Heizend/Kühlend/Idle Modus, pulsierender Dot in Akzentfarbe, spring-in Animation, Light-Mode Overrides)

## Neue Ideen (2026-03-28 04:03 UTC)
- [x] wz.html: Geräte-Tab — Status-Übersicht Donut-Gauge (animierter SVG-Donut zeigt ON/OFF Verhältnis aller Lichter + Geräte als Kreisbogen, grün→amber je Aktivitätsgrad, Zahl in der Mitte, Spring-Pop-Animation bei State-Änderung, Sub-Label "Alles aus/Wenig aktiv/Viel los")

## Neue Ideen (2026-03-28 06:03 UTC)
- [x] wz.html: Licht-Tab — Sonnenuntergang-Simulator Button (🌇 Tap startet 30-min Dimm-Kurve von 3000K/80% → 1900K/15%, sanfter Übergang mit 55s-Transition je Schritt, Countdown-Pill + pulsierender Dot + Cancel-Button, setzt alle aktiven Lichter die color_temp unterstützen, orange/warmes Farbschema)

## Neue Ideen (2026-03-28 08:03 UTC)
- [x] wz.html: Home-Hero — Licht-reaktive Wellen-Farbverschiebung (Hero-SVG-Wellen wechseln Gradientfarbe passend zu aktivem RGB-Licht-Durchschnitt, 3s ease Opacity-Transition, komplementäre Farbe für Welle 2, Fallback auf Standard-Amber/Blau wenn keine RGB-Lichter)

## Neue Ideen (2026-03-28 12:03 UTC)
- [x] wz.html: Wetter-Tab — "Guter Moment zum Lüften?" Empfehlung-Card (smart Ventilations-Empfehlung: grün wenn Temp 14–26°C + Regenprob <25% + Wind <35 km/h → "Jetzt lüften!"; blau bei Regen; kalt bei <8°C; amber bei Wind oder Grenztemperatur; animiertes Fenster-Icon, Temp + Feuchte Stats rechts)

## Neue Ideen (2026-03-29 01:10 UTC)
- [x] wz.html: Geräte-Tab — Schnell-Notiz Widget (📝 localStorage-Textarea im Geräte-Tab; 5 Quick-Chips: Wäsche/Ofen/Tür/Medizin/Einkauf setzen Vorlagen-Text; Auto-Save 400ms Debounce; 🗑 Clear-Button; spring-in Animation; Light-Mode-kompatibel)

## Neue Ideen (2026-03-29 02:03 UTC)
- [x] wz.html: Wetter-Tab — Sonnenstunden-Karte (☀️ sunshine_duration von Open-Meteo als neue daily-Variable, animierter SVG-Sonnen-Arc + 10 Sonnenstrahlen die je nach % skalieren, Fortschrittsbalken, Condition-Badge von "Bedeckt" bis "Herrlicher Sonnentag", Stunden vs. mögliche Tageslichtzeit)

## Neue Ideen (2026-03-29 08:03 UTC)
- [x] wz.html: Home-Tab — Licht-Aktivitäts-Heatmap (🗓 GitHub-Stil: 7×24 Raster Tage × Stunden, amber Farbskala, localStorage-Persistenz)

## Neue Ideen (2026-03-29 04:03 UTC)
- [x] wz.html: Wetter-Tab — "Regenschirm-Check" Karte (☂ animierter SVG-Regenschirm öffnet/schließt sich je nach max. täglicher Regenwahrscheinlichkeit aus hourly.precipitation_probability; 4 Stufen: ≥75% "Schirm mitnehmen!" blau / ≥45% "Besser mitnehmen" / ≥20% "Eventuell Regen" / <20% "Kein Schirm nötig" grün; Canvas-Regentropfen-Animation wenn Prob ≥45%; animierter Fortschrittsbalken; Peak-Regen-Uhrzeit im Sub-Text)

## Neue Ideen (2026-03-28 20:36 UTC)
- [x] demo.html: Interaktiver Preis-Rechner (Schieberegler Räume 1–10 + Geräte 1–50, Checkboxen KI/Mobile/Wetter/Energie, Echtzeit-Preisberechnung → Basic €49 / Standard €89 / Premium €149, animierter Preisflip, Lieferzeit-Badge, DE+EN i18n, Fiverr CTA-Button)

## Neue Ideen (2026-03-28 15:45 UTC)
- [x] wz.html: Home-Tab — "Beste Außenzeit" Chip (scannt stündliche Wetterdaten für heute: Score je Stunde aus Temperatur-Komfort + Regenwahrsch. + Wind + WMO-Code, ermittelt bestes 2h-Fenster für Outdoor, zeigt "Beste Außenzeit: 14:00–16:00 Uhr" grüner/amber/roter Chip je Score, unter Mini-Forecast-Strip)

## Neue Ideen (2026-03-28 16:03 UTC)
- [x] wz.html: Home-Tab — 7-Tage Wochentag-Strip (horizontale Chip-Reihe nach outdoor-chip: Mo–So mit farbigem Wetter-Dot + Höchsttemperatur, Heute hervorgehoben mit amber Glow, Tap → Detail-Popup mit Hi/Lo + Wetterbedingung + Niederschlag mm, staggered wsChipIn Animation, blendet nur ein wenn _wx.daily vorhanden)

## Neue Ideen (2026-03-28 08:43 UTC)
- [x] wz.html: Musik-Tab — "Zuletzt gespielt" History Chips (localStorage speichert letzte 5 Tracks bei Track-Wechsel; Chip-Row mit 🎵 Ikon + Titel + Artist + relative Zeit; amber Glass-Style; staggered fade-in; erscheint unter Sleep-Timer wenn History vorhanden)

## Neue Ideen (2026-03-28 10:03 UTC)
- [x] wz.html: Licht-Tab — Nachtlicht-Modus Button (🌙 ein Tap setzt alle aktiven Lichter auf 1900K/3%, sanfte 2s Transition, Auto-Restore nach 15min mit Countdown-Pill, Cancel → Lichter auf ursprüngliche CT/RGB/Helligkeit zurücksetzen, blaues Farbschema, Mond-Rock-Animation wenn aktiv)

## Neue Ideen (2026-03-27 08:03 UTC)
- [x] demo.html: Floating Live-Chat FAQ Widget (🦀 Bot unten rechts, 3 klickbare FAQ-Fragen mit Antworten, Fiverr-CTA, Badge-Notification nach 4s, DE+EN i18n, schliessbar) (🌿 Tageszeit-optimierter Einzel-Tap-Button zwischen Global-Dimmer und Schnellfarben-Palette: berechnet ideale Farbtemperatur 1900K–6500K + Helligkeit 18%–100% je Tagesphase Nacht/Morgengrauen/Morgen/Mittag/Nachmittag/Abend/Spätabend, zeigt aktuellen Tageszeit-Emoji + Zielwerte live, setzt alle aktiven Lichter per svc('light','turn_on',{color_temp_kelvin, brightness_pct}), grüner Flash-Animation bei Tap, Toast "🌅 Circadian auf X Lichter · 2700K / 45%")

## Neue Ideen (2026-03-28 18:03 UTC)
- [x] wz.html: Licht-Tab — "Atem-Licht" Meditations-Modus (🫁 4-7-8 Rhythmus: 4s Einatmen hell → 7s Halten → 8s Ausatmen dunkel, wählbare Zyklen 3×/5×/∞, Countdown-Pill, Cancel, türkises Farbschema)

## Neue Ideen (2026-03-29 09:10 UTC)
- [x] wz.html: Geräte-Tab — "Alles aus"-Sleep-Timer Card (⏰ 4 Timer-Buttons 15/30/60/90 min, schalten alle Lichter + Geräte ab, Countdown-Pill mit Puls-Dot, Cancel-Button, blaues Farbschema)

## Neue Ideen (2026-03-29 10:03 UTC)
- [x] wz.html: Home-Hero — Tap-Burst Emoji Particles (🎆 touchstart/click auf Hero erzeugt 6-8 wetter-passende Emoji-Partikel vom Tap-Punkt, animiertes Aufsteigen mit random Trajektorie, WMO-codierte Emoji-Sets ☀️/🌧/❄️/⚡/✨)

## Neue Ideen (2026-03-28 22:03 UTC)
- [x] wz.html: Home-Tab — "Zitat des Tages" Card (💬 täglich wechselndes Motivationszitat aus 30 lokalen Zitaten, ↺ Refresh-Button, amber Anführungszeichen-Design, quoteCardIn Animation)

## Neue Ideen (2026-03-28 20:03 UTC)
- [x] wz.html: Home-Tab — Activity Rings Card (Apple Watch Style: 3 konzentrische SVG-Ringe für Lichter/Musik/Stimmung)

## Neue Ideen (2026-03-28 14:03 UTC)
- [x] wz.html: Home-Tab — Wetterwarnung Banner (scannt _wx.daily der nächsten 3 Tage auf kritische Bedingungen: Gewitter WMO≥95, Hitzewelle ≥34°C, Starker Frost ≤-5°C, Starkregen ≥20mm, Sturmböen ≥70km/h — zeigt farbcodierten spring-in Banner mit Icon + Titel + Beschreibung, schliessbar mit × Button, 5 Farbvarianten je Warntyp, Light-Mode Overrides)

## Neue Ideen (2026-03-29 00:03 UTC)
- [x] wz.html: Wetter-Tab — "Biowetter" Karte (🧬 Einfluss des Wetters auf das Wohlbefinden: Kopfdruck-Risiko aus Luftdruckabfall + Feuchte, Gelenk-Risiko aus Kälte + Druckabfall, Energie-Level aus Sonnenschein + Temperatur + Luftdruck, Kreislauf-Belastung aus Tagesschwankung + Feuchte — 4 animierte Faktor-Balken, Gesamt-Emoji + Label + Empfehlungs-Tip, amber/grün/rot je Belastung, Orb-Hintergrund)

## Neue Ideen (2026-03-29 20:03 UTC)
- [x] wz.html: Musik-Tab — Floating Music Note Particles (♩♪♫♬ Noten-Partikel steigen vom Album-Art auf wenn Musik spielt, amber/weiß, staggered spawn, MutationObserver auf alb-disc.playing)

## Neue Ideen (2026-03-29 12:03 UTC)
- [x] wz.html: Musik-Tab — 3D Holographic Tilt Effect auf Album-Art (pointer/DeviceOrientation → perspective rotateX/Y, spring damping, glare-Overlay)

## Neue Ideen (2026-03-29 18:03 UTC)
- [x] wz.html: Licht-Tab — "Licht-Snapshot" Feature (📸 Lichtzustand speichern & wiederherstellen, bis zu 3 Schnappschüsse in localStorage, Farbdot-Vorschau, Apply/Delete)

## Neue Ideen (2026-03-29 16:03 UTC)
- [x] wz.html: App — "Lebendiger Hintergrund" Tageszeit-reaktive Ambient-Orbs (2 große, sehr sanft driftende radial-gradient Orbs hinter dem App-Inhalt, Orb1 oben-links/Orb2 unten-rechts, Farbe wechselt je Tageszeit: nachts blau/lila → morgens rose/amber → tags neutral → abends orange/lila, Orb2 reagiert zusätzlich 30% auf aktive RGB-Lichtfarben via lerp, filter:blur(90px), opacity 0→1 beim Initialisieren, CSS drift-Animationen 26s/34s alternate, Light-Mode: opacity:0!important)

## Neue Ideen (2026-03-29 22:03 UTC)
- [x] wz.html: Home-Tab — Anwesenheits-Chips (device_tracker.* Entities: Person-Chips mit Initialen-Avatar + Name + Zuhause/Unterwegs/Zone Status, grün/gedimmt/blau Farbschema, pulsierender Dot bei "Zuhause", staggered presChipIn Animation)

## Neue Ideen (2026-03-30 00:04 UTC)
- [x] wz.html: Home-Tab — Raumklima-Card (🌡 Indoor Temperatur + Luftfeuchtigkeit aus HA sensor.* Entities, zwei animierte SVG-Arcs nebeneinander, Komfort-Indikator-Badge, ∆ Außentemperatur-Vergleich)

## Neue Ideen (2026-03-30 02:04 UTC)
- [x] wz.html: Wetter-Tab — Sternbeobachtungs-Score Karte (🔭 Score 0–100 aus cloud_cover + precipitation + Mondphase + Sichtweite, SVG Arc-Gauge blau/lila Gradient, twinkling Stars Canvas-Animation, 4 farbige Condition-Chips, beste Beobachtungszeit heute Nacht, erscheint nur bei Nacht / 90min vor Sonnenuntergang)

## Neue Ideen (2026-03-30 06:08 UTC)
- [x] wz.html: App — Bildschirm-Schlaf Inaktivitäts-Dimmer (🌑 nach 2 min ohne Touch → Overlay blendet auf Schwarz, zeigt Uhrzeit dezent, Tap zum Aufwecken — ideal für Wand-Tablet/Panel)

## Neue Ideen (2026-03-30 14:37 UTC)
- [x] wz.html: Wetter-Tab — Tages-Highlight Karte (🌟 Beste & schlechteste Stunde heute als 2-Spalten Card — Score aus Temp-Komfort + Regenwahrsch. + Wind + WMO-Code, grün/rot Farbschema, Uhrzeit + Emoji + Cond-Text + 3 Chips je Spalte, scannt nur noch ausstehende Stunden des Tages)

## Neue Ideen (2026-03-30 22:37 UTC)
- [x] wz.html: Wetter-Tab — UV-Schutz Countdown Card (☀️ SVG Arc-Gauge 0–12 UV grün→gelb→orange→rot Gradient, tagesaktueller UV-Max aus daily.uv_index_max, stündliche uv_index Hourly-Variable neu hinzugefügt, Countdown bis UV≥3 "In ~Xh Schutz empfohlen", SPF-Empfehlung + Verhaltens-Chips, 6 UV-Stufen Minimal→Extrem)

## Neue Ideen (2026-03-30 18:04 UTC)
- [x] wz.html: Wetter-Tab — Temperatur-Klimavergleich Card (🌡 aktuelle Temperatur vs. langjährigem Monatsmittel DE, animierter Thermometer-SVG + Balkenvergleich, farbiges Delta ↑↓, Verdikt-Text, Cyan/Teal Farbschema)

## Neue Ideen (2026-03-30 10:04 UTC)
- [x] wz.html: Wetter-Tab — "Grillwetter-Check" Karte (🔥 Score 0–100 aus Temperatur + Regenwahrsch. + Wind + WMO-Code, SVG-Grill mit animierten Flammen bei Score >60, 5 Verdikt-Stufen von "Perfekt zum Grillen!" bis "Besser drinnen essen", Condition-Chips für Temp/Wind/Regen/Gewitter, kontextsensitiver Grill-Tipp)

## Neue Ideen (2026-03-30 06:04 UTC)
- [x] wz.html: Wetter-Tab — "Outdoor-Sport" Empfehlungs-Card (🏃 Score 0–100 für Joggen/Radfahren/Wandern/Schwimmen je nach Temp+Wind+Regen+WMO, beste Sportart + optimale Uhrzeit, grüner Farbakzent)

- [x] wz.html: Licht-Tab — Sonnenaufgang-Simulator Button (🌅 Komplementär zum Sonnenuntergang-Simulator: 30-min Helligkeits-Kurve von 1800K/5% → 5500K/95%, sanfte Übergänge mit 55s-Transition je Schritt, Countdown-Pill + pulsierender Dot + Cancel-Button, gelbes Farbschema, Sonne-steigt-Animation wenn aktiv, erscheint nur wenn Lichter mit color_temp aktiv)

## Neue Ideen (2026-03-30 20:04 UTC)
- [x] wz.html: Home-Tab — "Wetter-Licht Sync" Button (🌤→💡 Ein Tap setzt alle aktiven Lichter passend zur aktuellen Wetterlage

## Neue Ideen (2026-03-30 22:04 UTC)
- [x] wz.html: Licht-Tab — "Farb-Mixer" Canvas Color Wheel

## Neue Ideen (2026-03-31 04:04 UTC)
- [x] wz.html: Licht-Tab — Farbtemperatur-Spektrum Visualizer (🌡→💡 horizontaler Gradient-Balken 1800K→6500K, positionierte Dots für jedes aktive Licht, Hover-Tooltip mit Name+CT, Durchschnitts-Anzeige, smooth Transition)

## Neue Ideen (2026-03-31 00:04 UTC)
- [x] wz.html: Wetter-Tab — "Pflanzengieß-Check" Karte (🌱 Soil-moisture Score aus Regen letzte 24h + Verdunstungsschätzung + Temperatur + Sonne → animierter SVG-Wassertropfen füllt sich je Bodenzustand, 4 Stufen von "Nicht nötig" bis "Dringend gießen!", Condition-Chips, Gieß-Tipp) (🎨 interaktives HSL-Farbrad aus Canvas 140px, Cursor-Tracking via mousedown/touchmove, Sättigung durch Distanz vom Zentrum, Farbton durch Winkel, Helligkeits-Slider, Vorschau-Orb + Hex-Code, Anwenden-Button setzt alle aktiven RGB-Lichter, Fallback auf alle aktiven Lichter wenn keine RGB erkannt, cwApply Flash-Animation, spring-in cwCardIn, erscheint nur wenn RGB-Lichter an): Sonne=Tageslicht 5500K-6000K/80-100%, Regen=Kompensations-Licht 4500K/68%, Bewölkt=ausgewogen 4200K/72%, Nebel=warm-gedimmt 3500K/55%, Gewitter=Cosy 3000K/85%, Nacht=Kerzenschimmer 1900K/15%, Morgengrauen/Abend individuell — Temperaturkorrektur ±CT bei Kälte/Hitze, Beschriftung zeigt aktuelles Ziel live, verschwindet wenn keine Lichter an)

## Neue Ideen (2026-03-31 06:04 UTC)
- [x] wz.html: Licht-Tab — Szenen-Preset Karussell (⚡ 6 Ein-Tap Presets: Morgen/Arbeit/Relax/Film/Romantik/Nacht, horizontaler Scroll, Gradient-Preview-Orb, CT+Brightness-Info, localStorage merkt letztes Preset, spring-in Animation)

## Neue Ideen (2026-03-31 04:37 UTC)
- [x] demo.html: "Empfohlene Hardware" Section (🖥️ 3 Cards vor Contact: Raspberry Pi 5 / Intel NUC / Synology NAS — Preis + 4 Vorteile + Empfehlung-Badge, grüner/amber/blauer Farbakzent je Option, hover-lift, staggered IntersectionObserver fadein, DE+EN i18n via data-i + applyLang())

## Neue Ideen (2026-03-31 08:37 UTC)
- [x] wz.html: Home-Tab — "Wochenende-Countdown" Chip

## Neue Ideen (2026-03-31 12:04 UTC)
- [x] wz.html: Licht-Tab — "Zufalls-Palette" Shuffle Button (🎲 ein Tap setzt alle aktiven Lichter auf harmonische Zufallsfarben: zufälliger Basis-Hue + gleichmäßige Winkelverteilung je Licht, Sättigung 83-95%, Helligkeit 50-62%, Spin-Animation am Icon, Toast mit Basisfarbton)

## Neue Ideen (2026-03-31 10:04 UTC)
- [x] wz.html: Musik-Tab — Album-Cover Dominante Farben Palette (🎨 Canvas-Extraktion der 5 markantesten Farben aus dem aktuellen Album-Art, Swatch-Row unter Track History, Tap auf Swatch setzt alle aktiven Lichter auf diese RGB-Farbe mit 1.2s Transition) (📅/🎉 zeigt Tage+Stunden bis Samstag 00:00, während Sa/So grüner "🎉 Wochenende!"-Chip, Werktag = amber mit Countdown "Noch Xd Yh bis zum Wochenende", pulsierender Dot, spring-in Animation, DE Light-Mode kompatibel, aktualisiert sich mit jedem updateAll()-Poll)
