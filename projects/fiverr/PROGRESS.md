# PROGRESS.md — Automatische Fortschritts-Logs

## v29 (2026-03-19 01:23 UTC, auto)
- ✅ Reviews von 6 auf 8 erweitert
- ✅ Alle Reviews mit konkreten Projektreferenzen (Geräte, m², Ergebnisse, ROI)
- ✅ Neue Reviews: Andreas K. (Frankfurt, Büro 6 Meetingräume), Clara B. (Köln, Matter+Zigbee)
- ✅ Farbige Avatar-Gradienten pro Reviewer
- ✅ Paketname unter jedem Reviewer (Basic/Standard/Premium/Business)
- ✅ REV_COUNT auf 8 aktualisiert, DE+EN i18n vollständig

## v28 (2026-03-18 21:23 UTC, auto)
- ✅ Neue Section "Technologie-Stack" vor FAQ eingefügt
- ✅ 8 Tech-Cards: Home Assistant, N8N, Zigbee/Z-Wave, Matter/Thread, Shelly, Node-RED, MQTT, Raspberry Pi
- ✅ Inline SVG Icons mit farbigen Icon-Hintergründen pro Technologie
- ✅ Glassmorphism in Light Mode, Dark Mode unterstützt
- ✅ Badges: Open Source / Lokal / Standard / Hardware
- ✅ DE + EN i18n Keys komplett
- ✅ responsive auto-fit grid (minmax 200px)

## v27 (2026-03-18 16:56 UTC, auto)
- ✅ Light Mode: Glassmorphism-Cards mit `backdrop-filter: blur(22px) saturate(180%)`
- ✅ Body-Hintergrund im Light Mode: subtile Radial-Gradienten (#f2f2f7 Basis) für sichtbaren Blur-Effekt
- ✅ Betroffene Komponenten: .dash-card, .pf-card, .tier, .rev, .faq-item, .ai-srv, .contact-form, .fp-panel
- ✅ Featured Tier: Accent-tinted Glass (rgba blaue Tönung)
- ✅ Hover-States: erhöhte Opacity + stärkere box-shadow

## v26 (2026-03-17 12:56 UTC, auto)
- ✅ Structured Data JSON-LD im `<head>` konsolidiert (duplikat entfernt)
- ✅ Schema.org @graph: Person, Service (mit 3 Offers + AggregateRating), WebSite, FAQPage
- ✅ FAQPage mit 3 häufigen Fragen (Preis, Lieferzeit, Protokolle) für Google Rich Results
- ✅ AggregateRating: 5.0 / 47 Bewertungen (für Sterne in Suchergebnissen)

## v25 (2026-03-17 04:58 UTC, auto)
- ✅ Dark Mode Hero: animiertes Neon-Grid/Linien-Hintergrund (SVG-basiert, kein Canvas)
- ✅ Perspektivischer 3D-Vanishing-Point Effekt (rotateX 18°) für Tiefe
- ✅ Pulsierender Glow-Animation (6s cycle) mit blau/cyan/violett Farbverlauf
- ✅ Animierter Scanline-Effekt (8s Loop) für Sci-Fi Atmosphäre
- ✅ Intersection-Glow-Dots an Grid-Kreuzpunkten
- ✅ Nur im Dark Mode aktiv — Light Mode unverändert

## v19 (2026-03-15, manuell)
- ✅ SVG Gradient Overlay System (mix-blend-mode:screen, keine CORS-Probleme)
- ✅ roomBloom Filter entfernt → kein Licht-Bleeding mehr
- ✅ Echtes Wetter via Open-Meteo API (GPS-basiert)
- ✅ Echte News via rss2json (Tagesschau/ORF/SRF/BBC je nach Standort)
- ✅ Live Radio Streaming (RSP, Antenne Bayern, SWR3, Swiss Jazz)
- ✅ Vollständige DE/EN Übersetzung (80+ Textelemente)
- ✅ Musik-Equalizer Animation während Wiedergabe
- ✅ Tripod-Stehlampe für L4 (Zimmer 2)
- ✅ Scroll-Reveal Animations (IntersectionObserver)
- ✅ Hero Orbs + animierter Gradient-Hintergrund
- ✅ Verbesserte Portfolio-Cards (echte Dashboard-UIs)
- ✅ Stat-Counter Animation beim Laden

## v21 (2026-03-15 17:58 UTC, auto)
- ✅ Scroll-to-top Button (fixed, bottom-right, smooth animation)
- ✅ Erscheint nach 320px Scroll, verschwindet wieder oben
- ✅ Hover: leichter Lift-Effekt + verstärkter Glow-Shadow
- ✅ Dark/Light Mode kompatibel via --accent + --glow CSS-Variablen
- ✅ Accessible: aria-label (DE + EN), pointer-events-safe

## v22 (2026-03-15 21:58 UTC, auto)
- ✅ Hero Subtitle: Typewriter-Effekt (3 rotierende Phrasen, DE + EN)
- ✅ Blinkender Cursor (CSS keyframes, accent-Farbe)
- ✅ Sprach-Switch-aware: Neustart bei DE↔EN Umschaltung
- ✅ Timing: 38ms tippen, 18ms löschen, 2.2s Pause, 0.5s zwischen Phrasen
- ✅ min-height auf .hero-sub → kein Layout-Shift beim Tippen

## v23 (2026-03-16 01:58 UTC, auto)
- ✅ Portfolio-Cards: 3D Tilt-Effekt via perspective() + rotateX/Y auf Mausbewegung
- ✅ Dynamischer Shine-Overlay (radial-gradient folgt Maus-Position)
- ✅ Smooth Reset beim mouseleave (cubic-bezier Easing)
- ✅ Kein Konflikt mit bestehenden hover-Styles; Dark/Light Mode unverändert

## v29 (2026-03-17 03:58 UTC, auto)
- ✅ Vergleichstabelle: Home Assistant vs Amazon Alexa vs Google Home
- ✅ 9 Features verglichen: Cloud-frei, Abo, Integrationen, Anpassbarkeit, lokale KI, Energie, DSGVO, Offline, N8N
- ✅ HA-Spalte visuell hervorgehoben (accent-Hintergrund + "⭐ Empfohlen" Badge)
- ✅ ✓ (grün) / ✗ (rot) / "teilweise" (orange) Icons
- ✅ Hover-Highlight auf Zeilen
- ✅ Responsive: overflow-x:auto für Mobile
- ✅ i18n: vollständig DE + EN

## v28 (2026-03-16 23:58 UTC, auto)
- ✅ Contact-Formular: Name, E-Mail, Projekttyp, Budget, Nachricht
- ✅ mailto-basiert: öffnet Mail-Client mit vorausgefülltem Betreff + Body
- ✅ Success-State: Formular blendet sich aus, Danke-Meldung erscheint
- ✅ Focus-Styles mit accent-Farbe + glow ring
- ✅ 2-Spalten Grid (Desktop) / 1-Spalte (Mobile)
- ✅ Select-Dropdowns: Projekttyp (Dashboard/Grundriss/KI/N8N/Sonstiges) + Budget-Stufen
- ✅ i18n: vollständig DE + EN (Labels, Placeholders, Optionen, Erfolgsmeldung)
- ✅ Dark/Light Mode kompatibel

## v27 (2026-03-16 19:58 UTC, auto)
- ✅ Testimonial-Carousel: 4er-Grid → single-card Carousel mit translateX-Animation
- ✅ Auto-Scroll: alle 5 Sekunden, reset bei manueller Navigation
- ✅ Prev/Next Buttons (‹›) mit hover-Glow, accessible aria-labels
- ✅ Dot-Indikatoren: aktiver Dot wächst zu Pill-Form (22px, accent-Farbe)
- ✅ 6 Reviews (2 neue hinzugefügt: Jan P. Hamburg, Nina W. Stuttgart)
- ✅ i18n: rev5 + rev6 in DE + EN
- ✅ Mobile: kompakter Padding, Buttons näher an Karte
- ✅ Cubic-bezier smooth slide-Transition

## v26 (2026-03-16 15:58 UTC, auto)
- ✅ Floating Labels auf allen 10 Lampen-Dots im SVG Grundriss
- ✅ Hover → pill-förmiges Dark-Label erscheint animiert über dem Dot (fade + slide-up)
- ✅ Labels: Zimmer 1, Zimmer 2, Wohnen, Büro, Bad, Essen
- ✅ i18n: DE (Zimmer 1/2, Wohnen, Büro, Bad, Essen) + EN (Bedroom 1/2, Living, Office, Bath, Dining)
- ✅ Pointer-events:none → kein Konflikt mit Klick-Handling
- ✅ CSS transition: opacity + translateY für smooth slide-in

## v25 (2026-03-16 09:58 UTC, auto)
- ✅ Footer: Social Icon Buttons — GitHub, LinkedIn, Fiverr (SVG Icons, inline)
- ✅ Hover-Effekt: translateY(-3px) + accent-Farbe + glow-shadow
- ✅ Footer-Tagline (DE+EN): "Handgefertigte Smart Home Dashboards — keine Cloud, kein Abo"
- ✅ Nav-Links kompakter: Smart Home | KI Automation | Bestellen
- ✅ Copyright aktualisiert auf 2026
- ✅ i18n: ftTagline, ftLinkSH, ftLinkAI, ftLinkOrder in beiden Sprachen
- ✅ Dark/Light Mode, Mobile kompatibel

## v24 (2026-03-16 05:58 UTC, auto)
- ✅ Pricing Toggle: Einmalig / Monatlich Umschalter mit animierter Pill-Toggle UI
- ✅ Preis-Animation: Smooth scale+fade beim Wechsel (cubic-bezier bounce)
- ✅ Preise: Basic €49→€29, Standard €99→€59, Premium €149→€89 / Monat
- ✅ "–40%" Savings-Badge erscheint animiert beim Monthly-Switch
- ✅ Active-Label-Highlight: aktive Option (Einmalig/Monatlich) leuchtet in accent-Farbe
- ✅ i18n: DE (Einmalig/Monatlich/Projekt/Monat) + EN (One-time/Monthly/project/month) vollständig
- ✅ Dark/Light Mode kompatibel, Mobile-First

## Nächste Auto-Agent Runs → siehe AUTOWORK.md Ideen-Liste

## v20 (2026-03-15 12:40 UTC, auto)
- ✅ OG Meta Tags (og:title, og:description, og:url, twitter:card)
- ✅ Live-Uhr Widget (7. Dashboard-Card: Uhrzeit + Datum + Sonnenauf-/untergang)
- ✅ 'How it works' 3-Step Section mit hover-Animationen
- ✅ Sunrise/Sunset via Open-Meteo nach Geolocation
- ✅ Alle neuen Texte vollständig übersetzt (DE/EN)
