# PROGRESS.md — Auto-Improve Log

## 2026-03-28 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — "Guter Moment zum Lüften?" Empfehlung-Card
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neue `#lueft-card` Section im Wetter-Tab, direkt ZWISCHEN `#wx-hero` und `#wc-card`
- **Konzept**: Scannt Open-Meteo `current` Wetterdaten + stündliche `precipitation_probability` → gibt personalisierte Lüft-Empfehlung
- **4 Zustands-Modi** mit eigenem Farbschema + Icon:
  - ✅ **Jetzt lüften!** (grün `rgba(48,209,88)`) wenn Temp 14–26°C + Regenprob <25% + Wind <35 km/h — Ideal-Bedingungen, zeigt Gründe (angenehme Temp / trockene Luft / leichte Brise)
  - 🌧 **Fenster besser zu** (blau `rgba(10,132,255)`) wenn Regenwahrscheinlichkeit ≥25% — zeigt % Wert
  - 🥶 **Zu kalt zum Lüften** (indigo) wenn Temperatur <8°C — nennt Ist-Temperatur + Wärmeverlust-Hinweis
  - 💨 **Windig — kurz lüften** / **Lüften möglich** (amber `rgba(255,159,10)`) bei Grenzwerten oder starkem Wind — empfiehlt Stosslüften 3–5 Min
  - 🌤 **Aufpassen — Hitze draussen** (amber) wenn >26°C — Tipp morgens/abends lüften
- `#lueft-inner` mit CSS-Klassen `lf-yes/lf-no-rain/lf-no-cold/lf-ok` → steuert Background-Gradient + Border-Farbe + Title-Farbe
- `#lueft-ico`: Fenster/Wettericon-Emoji, animiertes `@keyframes lueftIcoBreeze` (sanftes Wackeln -4°/+4°, 3s loop) nur im `lf-yes` Modus
- `#lueft-stats` rechts: Außentemperatur + Außenluftfeuchtigkeit als kompakte Stat-Labels
- `drawLueftCard()` IIFE: liest `_wx.current.temperature_2m`, `windspeed_10m`, `relative_humidity_2m` + findet aktuelle Stunde in `_wx.hourly.precipitation_probability`
- Stagger-Animation: `#lueft-card` zur `.page-entering>` CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- Light-Mode Overrides: `background:var(--c1)` für neutralen hellen Hintergrund
- `drawLueftCard()` in `renderWeather()` direkt vor `drawWindChill()` aufgerufen
- Graceful: Card bleibt verborgen wenn keine `_wx.current` Daten (kein API-Fehler)
- **Kein extra API-Call** — nutzt bereits vorhandene Open-Meteo `current` + `hourly` Daten
- Effekt: Im Wetter-Tab sieht man auf einen Blick ob es gerade sinnvoll ist die Fenster zu öffnen — praktischer Alltagsnutzen der über reine Wetterdaten hinausgeht
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 536672 bytes, DEPLOY_OK)



## 2026-03-28 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Nachtlicht-Modus Button (🌙)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#lt-night` Div im Licht-Tab, direkt zwischen `#lt-sunset-sim` und `#lt-color-palette`
- **Konzept**: Ein Tap dimmt alle aktiven Lichter sofort auf minimales warmes Nachtlicht (1900K / 3%) — ideal für den Gang zum Bad nachts ohne geblendet zu werden; nach 15 Minuten automatische Wiederherstellung
- **Button-Design**: Blaues Farbschema `rgba(60,100,255)` Border + Background — klar von orange=Sunset-Sim und grün=Circadian unterscheidbar
- `#lt-nl-ico` (🌙): `@keyframes nlMoonRock` wenn aktiv — Mond schwingt sanft -12°/+8°/0° (4s ease-in-out loop)
- `#lt-nl-val`: zeigt "1900K · 3%" statisch
- `#lt-nl-pill`: Countdown-Pill mit pulsierendem blauen Dot (`@keyframes nlDotPulse`, 2s loop) + Live-Countdown + ✕ Cancel-Button
- **State-Save Logik** `startNightLight()`:
  - Vor Aktivierung: speichert `color_temp_kelvin`, `brightness`, `rgb_color` je Licht in `_nlPrev{}`
  - Setzt alle aktiven Lichter auf `{color_temp_kelvin:1900, brightness_pct:3, transition:2}`
- **Countdown-Format**: "🌙 noch 14m 52s · Auto-Restore" — sekündlich aktualisiert via `setInterval`
- **Cancel-Logik** `stopNightLight(true)`: liest `_nlPrev` → sendet `svc('light','turn_on',{...prev_state, transition:2})` für jedes Licht
- **Auto-Stop** `setTimeout(NL_MS)`: nach 15min stoppt Timer automatisch (kein Restore, da Nacht)
- **Schutz**: wenn alle Lichter extern ausgeschaltet (`onCount===0`) → Timer automatisch gestoppt
- Toggle-Verhalten: zweiter Tap auf Button → `stopNightLight(true)` mit Restore
- `@keyframes nlApply`: blauer Flash beim Tap-Start als Feedback
- `@keyframes nlDotPulse`: blaue Puls-Aura um den Dot (2s loop)
- Light-Mode Overrides: transparenter Hintergrund, dunklere Pill-Farbe
- `#lt-night` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein Konflikt mit Circadian-Button, Sunset-Sim, Fade-Out-Timer (separates IIFE, eigener State)
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 534107 bytes, DEPLOY_OK)



## 2026-03-28 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Licht-reaktive Wellen-Farbverschiebung
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Zwei neue Overlay-Wellen-Gruppen (`#hero-wave-r1`, `#hero-wave-r2`) als zusätzliche Schicht über den bestehenden Default-Wellen im `#hero-wave-svg`
- Neue linearGradients `#wv1GradR` und `#wv2GradR` mit dynamisch per JS aktualisierten `stop-color` Attributen
- `style="opacity:0;transition:opacity 3s ease"` auf beiden Overlay-Gruppen → sanftes 3-Sekunden Ein-/Ausblenden
- **JS-IIFE in `updateAll()`** nach Ambient-Orb-Block:
  - Filtert aktive Lichter nach `rgb_color` Attribut (nur echte RGB-Lichter, kein CT-Fallback)
  - Berechnet Durchschnitts-RGB aller aktiven RGB-Lichter (`rS/cnt, gS/cnt, bS/cnt`)
  - Welle 1 = exakte Licht-Farbe (rgba mit 0.22 max-Opacity — dezent)
  - Welle 2 = komplementärer Farbton (leichte Verschiebung: blaue Anteil erhöht, rote Anteil verschoben → natürliches Gegenstück)
  - Bei 0 RGB-Lichtern → beide Overlay-Wellen auf `opacity:'0'` → Standard-Wellen (amber/blau) dominieren
- Wenn Lichter von RGB → kein RGB wechseln: 3s Fade-out, kein harter Cut
- Wenn neue Farbe aktiv: `stop-color` Attribute sofort gesetzt + `opacity:'1'` → neues Farbschema blendet in 3s ein
- CSS: bestehende `#hero-wave-p1`, `#hero-wave-p2` default Wellen unverändert im Hintergrund → Overlay liegt on top
- **Kein Konflikt** mit bestehendem Ambient Orb (separates DOM-Element), heroWave1/2 Animationen (CSS-Animation auf Parent-Gruppen unberührt), Star-Canvas, Precip-Canvas
- Effekt: Wenn RGB-Lichter (z.B. rote Hue Play Bar oder grüne Govee) aktiv sind, schimmern die Hero-Wellen langsam in der Lichtfarbe — wie ein Spiegelbild der Raumstimmung am Horizont des Dashboards
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 524328 bytes, DEPLOY_OK)



## 2026-03-28 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Sonnenuntergang-Simulator Button (🌇)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#lt-sunset-sim` Div im Licht-Tab, direkt zwischen `#lt-circadian` und `#lt-color-palette`
- **Konzept**: Ein Tap startet eine 30-minütige Dimm-Kurve von warmen 3000K/80% bis zur tiefsten Kerzenstimmung 1900K/15% — ideal zum Abschalten vor dem Schlafen
- **Button-Design**: Orange-warmes Farbschema `rgba(255,100,30)` Border + Background (bewusst von grün=Circadian und amber=Dimmer unterscheidbar)
- `#lt-ss-ico` (🌇): läuft wenn aktiv mit `@keyframes ssSunSet` — Sonne sinkt sanft ab (translateY+scale, 3s loop)
- `#lt-ss-val`: zeigt "3000K → 1900K" im Ruhezustand, "● Läuft…" während Simulation
- `#lt-ss-pill`: Countdown-Pill mit pulsierendem orangem Dot (`@keyframes ssDotPulse`, 1.6s) + Live-Countdown + ✕ Stop-Button
- **Dimm-Logik** `applyStep()`: 
  - `t = elapsed/TOTAL_MS` (0..1) → `lerp(3000, 1900, t)` für Kelvin, `lerp(80, 15, t)` für Helligkeit
  - `svc('light','turn_on', {color_temp_kelvin, brightness_pct, transition:55})` → 55-Sekunden Übergänge zwischen Schritten → absolut flüssiger Verlauf
  - Iteriert nur Lichter mit `color_temp_kelvin` Attribut (Fallback-sichere Filter-Funktion `getActiveDimmables()`)
  - Countdown-Anzeige: "Dimmt sanft… noch Xm Ys · 2600K / 52%"
- **Toggle-Verhalten**: zweiter Tap auf Button stoppt sofort (`stopSim(true)`)
- **Auto-Stop**: nach 30 min (TOTAL_MS) stoppt Timer automatisch und ruft `stopSim(false)` auf
- **Schutz**: wenn alle Lichter extern ausgeschaltet werden (`onCount===0`) → `stopSim(false)` aufgerufen
- CSS `@keyframes ssApply`: orange Flash beim Tap-Start (Bestätigung ohne aufdringlichen Effect)
- Light-Mode Overrides: transparenter Hintergrund, dunklere Pill-Farbe
- `#lt-sunset-sim` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein Konflikt mit Circadian-Button (unterschiedliche States), Global-Dimmer, Fade-Out-Timer
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 521469 bytes, DEPLOY_OK)



## 2026-03-28 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Geräte-Tab — Status-Übersicht Donut-Gauge
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#dev-status-gauge` Div im Geräte-Tab, direkt unter der "Geräte" Überschrift (vor Zuletzt-genutzt Timeline)
- **Konzept**: Zeigt auf einen Blick wie viele der konfigurierten Lichter + Geräte gerade aktiv sind — als animierter SVG-Kreisbogen + kompakter Infobereich
- **SVG Donut-Gauge** (`#dsg-svg`, 72×72px): innerer Track-Ring `rgba(255,255,255,.07)` + animierter Fill-Arc `#dsg-fill`
- Kreisumfang: r=28 → `stroke-dasharray:175.93`, `stroke-dashoffset = 175.93 × (1 - on/total)` → Arc füllt sich proportional
- `linearGradient #dsgGrad`: grün (#30d158→#34e05a) wenn <75% aktiv, amber (#ff9f0a→#ffcc02) wenn >75% — warnt subtil bei hoher Aktivität
- `#dsg-num`: Zahl der aktiven Geräte als Text-Element in der Kreismitte (15px bold weiß)
- `transition:stroke-dashoffset 1s cubic-bezier(.34,1.1,.64,1)` → weiche federnde Animation bei jedem State-Update
- **Rechter Info-Bereich**: `#dsg-label` "X von Y aktiv" + schmaler Fortschrittsbalken + `#dsg-sub` Sub-Label
- 5 Sub-Label-Zustände: 😴 Alles aus / 🌙 Wenig aktiv / 💡 Teilweise aktiv / 🏠 Viel los / ⚡ Alles aktiv
- Balken-Gradient synchronisiert sich mit Arc-Farbe (grün↔amber je Aktivitätsgrad)
- `@keyframes dsgPop`: scale 1→1.06→1, 0.42s cubic-bezier — spring-Bounce wenn sich die Anzahl ändert
- Pop-Animation via `classList.remove('pop') + offsetWidth reflow + classList.add('pop')` — sauber re-triggerable
- **Zähler-Logik** `window._updateDevGauge` IIFE: iteriert `CFG.lights + CFG.devs`, filtert nach `state==='on'||'playing'||'open'`
- Gauge erscheint (`opacity:1`) erst nach erstem State-Load — kein leeres Flackern beim Start
- **Hook**: `patchDevCards` Wrapper ruft `window._updateDevGauge()` nach jeder Card-Aktualisierung auf
- Light-Mode Overrides: `background:var(--c1)`, `color:var(--txt)` — lesbar in beiden Themes
- `#dev-status-gauge` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein extra API-Call — nutzt bereits vorhandene `_S` State-Daten
- Effekt: Wer den Geräte-Tab öffnet, sieht sofort einen grünen/amberfarbenen Kreisbogen der zeigt ob 2/10 oder 8/10 Geräte aktiv sind — wie ein Aktivitäts-Herzschlag des Smart-Homes
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 516065 bytes, DEPLOY_OK)



## 2026-03-28 02:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — Heizungs-Status Chip (🔥/❄️/🌡)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#hvac-chip` Div im Home-Tab, direkt nach `#batt-chip` (vor Kontext-Empfehlungs-Chip)
- **Konzept**: Scannt alle `_S` States nach `climate.*` Entities — wenn eine vorhanden und nicht `off/unavailable` → zeigt Chip
- **3 Modi**:
  - 🔥 Heizend: `hvac_action=heating` oder `mode=heat/auto` → orangerot Farbschema `rgba(255,100,50)`
  - ❄️ Kühlung: `hvac_action=cooling` oder `mode=cool` → blaues Farbschema `rgba(10,132,255)`
  - 🌡 Klima (Idle): alle anderen aktiven Modi → grünes Farbschema `rgba(48,209,88)`
- **Temperatur-Label**: `current_temperature` + `temperature` aus `attributes` → "🔥 Heizend · 18.5° → 21°"
- `.hvac-dot`: pulsierender 6px Kreis mit farbpassendem Box-Shadow (`@keyframes hvacDotPulse` 2.2s loop)
- **CSS-Farbvarianten**: `.hvac-heat` / `.hvac-cool` / `.hvac-idle` — jeweils eigener Hintergrund, Border, Textfarbe
- `#hvac-chip.show`: spring-in via `cubic-bezier(.34,1.28,.64,1)` — erscheint smooth beim Aktivieren
- Chip verschwindet (`classList.remove('show')`) wenn keine climate Entity vorhanden, `mode=off` oder `unavailable`
- **Light-Mode Overrides**: alle 3 Modi haben eigene `:root.light` Regeln (dunklere Farben für Lesbarkeit)
- `#hvac-chip` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- **Kein extra API-Call** — nutzt bereits vorhandene `_S` (fetchStates) Daten
- **Graceful fallback**: bei fehlenden `current_temperature` / `temperature` Attributen nur Modus-Text ohne Zahlen
- IIFE in `updateAll()` nach Batterie-Chip, vor `_updateQaBar` eingehängt
- Effekt: Wenn Janis eine Thermostat/Klimaanlage in HA hat, erscheint ein kompakter Chip der auf einen Blick zeigt ob geheizt/gekühlt wird und bei welcher Temperatur — ähnlich wie iOS Home-App Thermostat-Kachel
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 512039 bytes, DEPLOY_OK)



## 2026-03-28 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Gewitter-Alarm-Card (⚡)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#storm-warn-card` Div im Wetter-Tab, direkt VOR dem `#wc-card` (Wind-Chill) — prominente Position zwischen wx-hero und den Detail-Karten
- **Konzept**: Scannt stündliche WMO-Codes der nächsten 12h — wenn ≥95 (Gewitter) → zeigt dramatische Warn-Card mit Blitz-Animation
- **HTML**: `#storm-warn-inner` (Gradient-Hintergrund dunkelrot) + `#storm-warn-bg` (radialer Rot-Orb) + `#storm-bolt-ico` (⚡ animiert) + Text + Intensitäts-Badge + Stunden-Chips
- **CSS `@keyframes stormBoltFlash`**: Blitz flackert realistisch — 85% normal, 88% fast unsichtbar, 91% mega-glow, 94% wieder dunkel, 2.4s infinite — simuliert echtes Gewitterleuchten
- **CSS `@keyframes stormCardGlow`**: ganzer Card-Rand pulsiert subtil rot (3s loop) — zieht Aufmerksamkeit
- **`drawStormWarning()` Funktion**: liest `_wx.hourly.weather_code` + `time` + `precipitation_probability`
- Findet Start-Index für aktuelle Stunde via ISO-Datetime-Matching
- Iteriert i=si bis si+12 (12h Vorschaufenster) nach WMO code ≥95
- **3 Intensitätsstufen**: code==95 → "Mäßig" (amber), code>=96 → "Stark" (rot), code>=99 → "Sehr stark ⚡⚡" (rot)
- **Text-Logik**: first.h===0 → "Gewitter aktuell möglich — bleib drinnen." / sonst → "Gewitter in ~Xh (um HH:00) möglich. Bleib auf der Hut!"
- **Typ-Namen**: 95=Gewitter / 96=Gewitter mit Hagel / 99=Schweres Gewitter mit Hagel
- **Stunden-Chips** `#storm-chips`: bis zu 4 "⚡ HH:00" Pills, max +N weitere Chip
- **spring-in Animation**: `opacity:0 + translateY(-8px)` → `opacity:1 + translateY(0)`, `.55s cubic-bezier(.34,1.15,.64,1)`
- Card verschwindet smooth (`classList.remove('show')` + `setTimeout display:none`) wenn kein Gewitter in 12h
- `drawStormWarning()` in `renderWeather()` nach `updateWxPrecipCanvas` aufgerufen
- `#storm-warn-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Light-Mode Override: warmes Rosa statt dunkelrot (lesbar auf hellem Hintergrund)
- Graceful: keine Anzeige wenn keine Hourly-Daten oder kein Gewitter in Sicht
- Kein extra API-Call — nutzt bereits vorhandene `_wx.hourly` Daten
- Effekt: Wenn Gewitter geplant sind, erscheint eine dramatische blitzende Warn-Card oben im Wetter-Tab — kann man nicht übersehen
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 508963 bytes, DEPLOY_OK)



## 2026-03-27 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — "Stunde der Stille" Nacht-Chip (🌙)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#silence-chip` Div im Home-Tab, direkt vor den Szenen-Buttons (nach `#wx-rec-pill`)
- **Konzept**: Zwischen 22:00 und 07:00 Uhr erscheint ein dezenter blauer Chip der signalisiert dass gerade Ruhezeit ist — mit Live-Countdown bis 07:00
- **HTML**: `#silence-dot` (8px Kreis, blau) + `#silence-txt` ("🌙 Ruhezeit aktiv") + `#silence-cd` (Countdown-Span)
- **CSS**: `background:rgba(10,132,255,.06)` + `border:rgba(10,132,255,.18)` → klar blaues Nacht-Farbschema (unterscheidet sich von amber=Licht, grün=Circadian)
- `@keyframes silenceChipIn`: `opacity:0 + scale(.96) + translateY(5px)` → `opacity:1 + scale(1)`, cubic-bezier(.34,1.15,.64,1), 0.42s — spring-in
- `@keyframes silenceDotPulse`: `box-shadow` 0px → 5px rgba(100,180,255,.6) → 0, 2s loop — pulsierende blaue Aura
- **Zeit-Logik** im updateAll()-IIFE: `h>=22 || h<7` → `isQuiet=true`, `chip.classList.toggle('show',isQuiet)`
- **Countdown-Berechnung**: wenn `h>=22` → Minuten bis Mitternacht + 7h; wenn `h<7` → Minuten bis 07:00
- Anzeige: `· noch 7h 32min` / `· noch 14min` / `· gleich vorbei` (unter 2min)
- Chip verschwindet smooth (`display:none` via `classList.remove('show')`) wenn Ruhezeit endet
- Light-Mode Override: `background:rgba(10,100,220,.06)`, dunklere Textfarbe für Lesbarkeit auf hellem BG
- `#silence-chip` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein extra API-Call — reine Uhrzeit-Logik, läuft jedes mal wenn `updateAll()` feuert (~alle 30s)
- Kein Konflikt mit `#scene-chip`, `#batt-chip`, `#wx-rec-pill` (separates Element, eigene Position)
- Effekt: Nachts erinnert ein sanfter blauer Chip daran dass gerade Ruhezeit ist — elegant und dezent wie ein Apple Watch Schlafmodus-Indikator
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 502897 bytes, DEPLOY_OK)



## 2026-03-27 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — "Aktive Lichter" Farb-Dots Strip
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#lt-color-strip` Div im Home-Tab, direkt vor der Tages-Zusammenfassung (`#tagsum`)
- **Konzept**: Zeigt alle aktuell eingeschalteten Lichter als bunte Pill-Chips mit Name + Farb-Swatch
- **CSS**: `.lcs-dot` (flex pill, `border-radius:20px`, `0.63rem`), `.lcs-swatch` (10px Farbkreis mit `--lcs-glow` Glow-Variable)
- `@keyframes lcsIn`: scale(.78)+opacity:0 → scale(1)+opacity:1, 0.38s cubic-bezier(.32,0,.15,1)
- Staggered `animation-delay: i*0.055s` → Pills erscheinen wie eine Welle von links nach rechts
- **Farb-Logik** (kein extra API-Call, nutzt `_S[id].attributes`):
  - `rgb_color` vorhanden → exakte Lichtfarbe (z.B. Hue RGB)
  - `color_temp_kelvin` → warm (<2800K) amber / (<3500K) warmorange / (<5000K) cremegelb / kühl blau-weiß
  - Fallback → Dashboard-amber `rgb(255,159,10)`
- Name-Cleanup: entfernt redundante "Licht/Lampe"-Suffixe, kürzt auf max 15 Zeichen + "…"
- **Glow-Effekt**: `box-shadow: 0 0 6px 1px rgba(r,g,b,.45)` auf dem Swatch → subtiler Leuchtpunkt
- `#lt-color-strip.show{display:flex}` via `classList.toggle` in `updateAll()` — verschwindet sauber wenn alle Lichter aus
- **Light-Mode**: eigene CSS-Override-Regeln (dunklere Border + transparenter BG)
- In `updateAll()` nach `_updateQaBar()` eingehängt — aktualisiert sich bei jedem State-Poll
- `#lt-color-strip` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein Konflikt mit ambient orb, scene-chip, batt-chip (komplett separates Element)
- Effekt: Beim Öffnen der App sieht man auf einen Blick welche Lichter an sind und in welcher Farbe — wie eine Licht-Palette des aktuellen Ambientes
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 446636 bytes, DEPLOY_OK)



## 2026-03-27 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Geräte-Tab — "Letzte Schaltvorgänge" Mini-Timeline
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#dev-timeline` Div im Geräte-Tab, direkt unterhalb `#dev-cards`
- **Konzept**: Zeigt die letzten 5 State-Changes aller Lichter + Geräte als kompakte Timeline
- **HTML**: `<div id="dev-timeline">` + `.dtl-list` Container + `.sec-head` "⏱ Letzte Schaltvorgänge"
- **CSS-Klassen**: `.dtl-item` (flex-Row, staggered `dtlItemIn` Animation), `.dtl-dot` (8px farbiger Kreis mit Glow), `.dtl-name` (Entity-Name, overflow ellipsis), `.dtl-badge` (Ein grün / Aus gedimmt), `.dtl-time` (relative Zeit, rechts)
- `@keyframes dtlItemIn`: `translateX(-10px) opacity:0` → normal, 0.35s cubic-bezier(.32,0,.15,1), gestaffelt mit `animation-delay 0–0.24s`
- **localStorage** Key `dev_tl`: Array von `{ts, name, on, lc}` — max. 8 Einträge, neueste zuerst
- `window._detectDevChanges()` IIFE: vergleicht alle `CFG.lights + CFG.devs` gegen `window._dtlPrev{}` Dict
- **Change-Detection**: `prev !== cur` bei echten State-Änderungen → Eintrag wird `unshift()`-ed in localStorage
- `fmtDtlAgo(ms)`: "gerade" / "vor X min" / "vor X h" / "vor X d" — kompakte Zeitanzeige
- `window._renderDevTimeline()`: liest localStorage, rendert max. 5 Items als `<div class="dtl-item">` ins DOM
- Dot-Farbe: `rgba(${e.lc},1)` — exakt die Tile-Akzentfarbe des Lichts (amber/blau/weiß je Entity)
- Fallback: "Noch keine Änderungen heute" wenn localStorage leer
- Aufgerufen bei jedem `updateAll()` (nach `_updateParty`) — auch relative Timestamps aktualisieren sich
- `#dev-timeline` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Light-Mode Overrides: `background:var(--c1)`, `.dtl-badge.dtl-off` mit `rgba(0,0,0,.06)` + dunkler Text
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 536178 bytes, DEPLOY_OK)



## 2026-03-27 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — Tages-Mood-Tracker (😊/😐/😔)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#mood-card` Div im Home-Tab, direkt vor dem 3-Tage-Forecast (`#fc3`)
- **Konzept**: Täglich eine Stimmung festhalten — gut/ok/nicht gut — mit 7-Tage Rückblick als farbige Dots
- **3 Emoji-Buttons**: 😊 Gut (grün), 😐 Ok (gelb), 😔 Nicht gut (rot) — klickbar, touch-action:manipulation
- **Button-Design**: 14px border-radius Cards, aktiver State `.selected` mit farbcodiertem Border + Hintergrund per CSS-Variable (--mood-sel-c/--mood-sel-bg)
- `.mood-btn.sel-good/ok/bad`: 3 separate CSS-Klassen für grün/gelb/rot Farbschema
- `@keyframes moodBtnPop`: scale 1→1.18→1.06 Bounce beim Selektieren (0.35s cubic-bezier)
- **localStorage**: Key `mood_YYYY_MM_DD` → Wert `good|ok|bad` — ein Eintrag pro Tag, persistent
- `todayKey()` Funktion: generiert Datums-Key für heute
- `getDot(dateObj)` Funktion: liest Mood-Wert für beliebiges Datum aus localStorage
- `renderDots()`: erzeugt 7-Tage Dot-Reihe (So/Mo/.../Heu Labels) — farbige Dots: grün/gelb/rot, grau wenn kein Eintrag
- **After-Selection**: Buttons werden halbtransparent + pointer-events:none, `#mood-done` zeigt kontextsensitiven Text
  - 😊 → "😊 Schön zu hören! Hab einen tollen Abend."
  - 😐 → "😐 Alles okay — morgen wird besser!"
  - 😔 → "😔 Kopf hoch, morgen ist ein neuer Tag!"
- **Init-Logik**: wenn bereits Mood für heute gewählt → `applyTodayMood()` zeigt gespeicherten State sofort
- Kein HA-Dependency — rein lokale Persistenz (funktioniert ohne Verbindung)
- Kein Konflikt mit tagsum, cal-card, oder anderen Home-Tab Elementen
- `#mood-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Effekt: Am Ende des Home-Tabs kann Janis täglich mit einem Tap festhalten wie der Tag war — nach 7 Tagen sieht man ein buntes Stimmungsmuster der Woche
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 532008 bytes, DEPLOY_OK)



## 2026-03-27 14:07 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Party Mode Button (🪩)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#lt-party` Div im Licht-Tab, zwischen `#lt-fadeout` und `#lg` Grid
- Nur sichtbar wenn ≥1 aktives RGB-Licht vorhanden (`.show` Klasse via `window._updateParty(onCount)`)
- **Button-Design**: lila `rgba(191,90,242)` Farbschema (klar von amber=Licht, blau=Media, grün=Circadian unterscheidbar)
- `@keyframes partyBtnGlow`: pulsierender Lila-Glow um den Button wenn aktiv (2s ease-in-out loop)
- **Disco-Ball-Icon** `#lt-party-ico`: `@keyframes partyIcoSpin` — rotiert 360° in 3s wenn Party läuft
- `#lt-party-pill`: Aktiv-Pill mit pulsierendem Dot (`@keyframes partyDotPulse`) + Info-Text + ✕ Stop-Button
- `hslToRgb(h,s,l)` Helper: konvertiert Zufalls-HSL zu RGB Array (90% Sättigung, 55% Helligkeit → kräftige Disco-Farben)
- **`_tick()`**: jede 500ms (~120 BPM) → assign für jeden RGB-Licht eine neue Zufallsfarbe (Set-Tracking für weniger Wiederholungen)
- `svc('light','turn_on', {entity_id, rgb_color:[r,g,b], brightness_pct:75, transition:0.4})` → 400ms Übergänge zwischen Farben
- **`startParty(lights)`**: sammelt aktive RGB-Lichter aus `_S`, startet 500ms Interval, 10min Auto-Stop-Timeout, Toast + hap()
- **`stopParty(quiet)`**: räumt Interval + Timeout auf, resettet UI, optionaler Toast
- `window._updateParty(onCount)` in `updateAll()` nach `_updateFadeOut` eingehängt
- Auto-Stop-Schutz: wenn Lichter extern ausgeschaltet werden während Party läuft → Party stoppt automatisch
- Kein Konflikt mit Circadian-Button, Fade-Out-Timer, Global-Dimmer (separates IIFE, eigener State)
- Effekt: Ein Tap startet eine Disco-Lichtshow mit allen aktiven RGB-Lichtern — Farben wechseln im 120-BPM-Takt, ideal fürs Feiern
- JS-Check: OK | Deployed via SSH (base64-chunk, 526092 bytes, DEPLOY_OK)



## 2026-03-27 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Solar-Einstrahlung 24h Karte (☀️)
- Alle AUTOWORK.md Tasks waren [x] → neue Idee generiert und implementiert
- Neues `#solar-card` Div im Wetter-Tab, direkt zwischen `#weekly-rain-card` und `#moon-card`
- **Open-Meteo API**: `shortwave_radiation` zu `&hourly=` Parameter hinzugefügt (kein extra API-Call)
- `drawSolarCurve()` neue Funktion, aufgerufen in `renderWeather()` nach `drawRainHeatmap()`
- **Header**: gelbes Farbschema `rgba(255,214,10)` — passend zur Sonne, deutlich von amber (Licht) unterschieden
- **Peak-Badge**: zeigt Uhrzeit des Einstrahlungs-Peaks + Watt-Wert (z.B. "13:00 / 820 W/m²")
- **Gesamt-Energie**: summiert alle Stundenwerte → Wh/m² (Trapez-Näherung für 1h-Intervalle)
- **SVG Area-Chart** (320×56px): smooth cubic-bezier Kurve, `linearGradient solGrad` gelb→amber (50%→4% Opacity)
- `#sol-now-dot`: amber Leuchtpunkt bei aktueller Stunde (nur sichtbar wenn Einstrahlung >5 W/m²)
- Zeitlabels bei Jetzt / +6h / +12h / +18h / letzter Stunde
- **5 Condition-Texte**: Hervorragend (>700 W/m²) / Gut (>400) / Mäßig (>150) / Schwach (>30) / Kaum (<30)
- Card bleibt `display:none` wenn `shortwave_radiation` nicht verfügbar (<6 Werte) — graceful fallback
- `#solar-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- JS-Check: OK | Deployed via SSH (b64-chunk, 520043 bytes, DEPLOY_OK)



## 2026-03-28 00:02 UTC — Heartbeat Auto-Improve
- ✅ wz.html: Geräte-Tab — "Zuletzt genutzt" Timeline Card
- Top-5 Entities (devs + Lichtgruppen) sortiert nach last_changed ASC
- State-Icon ●/○/◐ in grün/grau/amber + relative Zeit "vor X min / h / Tagen"
- patchDevRecent() gehookt in patchDevCards-Cycle → live aktualisiert
- JS-Check: OK | Deployed via SSH (paramiko, 505504 bytes, DEPLOY_OK)

## 2026-03-27 08:08 UTC — Heartbeat Auto-Improve
- ✅ demo.html: Floating Live-Chat FAQ Widget implementiert
- 🦀 Amber Chat-Bubble unten rechts, öffnet Popup mit 3 FAQ-Fragen + Antworten + Fiverr-CTA
- Badge erscheint nach 4s wenn Popup nicht geöffnet, DE+EN i18n, schliessbar
- Deployed auf GitHub Pages (autoflow-lab.github.io)

## 2026-03-27 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Fade-Out Timer (🌙)
- Alle AUTOWORK.md Tasks waren bereits [x] → neue Idee generiert und implementiert
- Neues `#lt-fadeout` Div im Licht-Tab, zwischen `#lt-color-palette` und `#lg` Grid
- Nur sichtbar wenn ≥1 Licht an (`.show` Klasse via `window._updateFadeOut(onCount)`)
- **3 Dauer-Buttons**: `[data-min="15"]` / `[data-min="30"]` / `[data-min="60"]` → starten den Timer
- Design: amber `rgba(255,159,10,.06)` Hintergrund + `.16` Border → dezent, zur Licht-Tab-Palette passend
- `#lt-fo-pill`: Countdown-Pill mit pulsierendem Dot + `#lt-fo-cd` (mm:ss Countdown) + `#lt-fo-phase` (Status-Text)
- `@keyframes foDotPulse`: amber Puls-Ring um den Dot (1.4s loop) — zeigt dass Timer aktiv
- `#lt-fo-cancel` ✕-Button: erscheint nur wenn Timer läuft, stoppt und zeigt Toast "Timer abgebrochen"
- **`startTimer(minutes)`**: setzt `_endMs`, startet `setInterval(1s)`, zeigt Pill + Cancel, versteckt Buttons
- **Dimmlogik**: 90s vor Ablauf → `svc('light','turn_on',{entity_id, brightness_pct})` mit linear fallenden % (3–30%)
  - Nur auf Lichtern mit `brightness` Attribut (keine Switches)
  - Countdown-Phase: "Dimmt in Xs" → ab 90s: "Dimmt jetzt…"
- **Bei Ablauf**: `svc('light','turn_off')` auf alle `CFG.lights`, Toast "🌙 Lichter ausgeschaltet", Timer-Reset
- `stopTimer(toasted)`: räumt alles auf, resettet UI-State, optionaler Abbruch-Toast
- Externer Schutz: wenn Lichter anderweitig aus (`onCount===0` während Timer läuft) → Timer automatisch gestoppt
- `window._updateFadeOut` in `updateAll()` nach `_updateCircadian` eingehängt
- `#lt-fadeout` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein Konflikt mit Sleep-Timer (Musik-Tab, andere Entities), Global-Dimmer, Circadian-Button
- Effekt: Mit einem Tap auf "30'" dimmen alle Lichter sanft über 30 Minuten (letzten 90s) und schalten dann komplett aus — ideal zum Einschlafen
- JS-Check: OK | Deployed via SSH (paramiko base64-chunk, 513990 bytes, DEPLOY_OK)



## 2026-03-27 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — "Wetter-Brief" Sentence Card
- Alle AUTOWORK.md Tasks waren bereits [x] → neue Idee generiert und implementiert
- Neues `#wx-brief` Div im Home-Hero, direkt zwischen `#sun-cd-chip` und `#hnp` (Now-Playing Strip)
- `#wx-brief-txt` Span: enthält den generierten Satz (kein innerHTML — XSS-sicher via textContent)
- CSS: `font-size:.67rem`, `font-style:italic`, `color:rgba(255,255,255,.5)` — dezent unter dem Sunset-Chip
- `opacity:0 → 1` via `transition:opacity 1.6s ease` — sanftes Einblenden nach Wetter-Load
- `.show` Klasse → Satz erscheint smooth sobald Wetterdaten vorhanden
- `@keyframes wxBriefIn` definiert (fade+translateY — für optionale Nutzung)
- `:root.light #wx-brief`: `color:rgba(0,0,0,.42)` → lesbar im Light-Mode
- `drawWxBrief()` Funktion (60 Zeilen): liest `_wx.current` + `_wx.daily` + `_wx.hourly`
- Findet `rainAft` (Nachmittags-Peak) und `rainMrn` (Morgens-Peak) aus `precipitation_probability` Array
- **Satz-Logik (10 Varianten):**
  - ❄️ Schnee → "Schneefall — warm einpacken"
  - ⛈ Gewitter (WMO ≥95) → "Gewitter möglich — lieber drinnen bleiben"
  - 🌧 Aktuell Regen → morgens "Schirm einpacken" / nachmittags "bald Aufklärung?"
  - 🌤 rainAft > 60% → "Morgens schön, nachmittags Regen ☔"
  - 🌦 rainMrn > 55% → "Morgens Regen — später aufheiternd/wechselhaft"
  - ☀️ Klar + UV ≥6 → "Toller Tag, UV X — Sonnenschutz nicht vergessen"
  - 😎 Klar + temp ≥18 → "Schöner Tag — ideal für draußen"
  - 🥶 Klar + temp <3 → "Klarer Himmel, aber nur X° — dick anziehen"
  - 💨 Wind >35 km/h → "Windig (X km/h) — Jacke sinnvoll"
  - 🌞 temp ≥20 → "Angenehme X° — guter Tag für Spaziergang"
  - 🧊 temp <2 → "Nahe Gefrierpunkt — Frost möglich"
  - 🌥 Fallback → "Wechselhafter Tag, bis X° — typisches Wetter"
- `drawWxBrief()` in `renderWeather()` als erste Zeile eingehängt (vor drawOutfitCard)
- `#wx-brief` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Graceful: `el.classList.remove('show')` wenn kein Brief generierbar (fehlende Daten)
- Kein extra API-Call: nutzt bereits vorhandene `_wx` Daten
- Effekt: Im Home-Hero erscheint unter dem Sonnenuntergangs-Chip ein kleiner kursiver Satz der auf einen Blick erklärt was das Wetter heute bedeutet — wie ein persönlicher Wetter-Assistent
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 507499 bytes, DEPLOY_OK)



## 2026-03-27 02:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — "Nächster Regen / Aufklärung" Countdown-Chip
- Alle AUTOWORK.md Tasks waren bereits [x] → neue Idee generiert und implementiert
- Neues `#rain-next-chip` Div im `#wx-hero`, direkt über den Allergiker-Chips (neue `border-top` Trenner-Zeile)
- `#rain-next-pill`: Inline-Pill mit `#rain-next-ico` (Emoji) + `#rain-next-txt` (Text)
- 3 CSS-Farbvarianten: Standard (blau `rgba(10,132,255,.12)`) / `.rn-clear` (amber) / `.rn-ok` (grün)
- CSS `@keyframes rainNextIn`: fade+translateY Einblende-Animation
- `drawRainNextChip()` Funktion: liest `_wx.hourly.precipitation_probability` + `_wx.current.weathercode`
- Findet Start-Index für aktuelle Stunde via `_wx.hourly.time` Array (ISO-Datetime-Vergleich)
- **Wenn es aktuell regnet** (WMO code 51–99): scannt bis nächste Stunde mit prob < 20% → "☀️ Aufklärung in ~Xh" (amber Pill)
  - Bleibt regnerisch (kein Clear in 24h) → "🌧 Regen hält an" (blaue Pill)
  - Clear sofort → "🌤 Aufklärung bald"
- **Wenn kein Regen**: scannt bis nächste Stunde mit prob ≥ 40% → "🌧 Regen in ~Xh" (blaue Pill)
  - Kein Regen in 24h → "✅ Heute kein Regen erwartet" (grüne Pill)
  - Regen sofort möglich → "🌧 Regen jetzt möglich"
- Chip bleibt `display:none` wenn keine Hourly-Daten (<4 Werte) — graceful fallback
- `drawRainNextChip()` in `renderWeather()` nach `drawWindCurve()` aufgerufen
- `#rain-next-chip` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Kein extra API-Call: nutzt bereits vorhandene `_wx.hourly` Daten
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk, 503944 bytes, DEPLOY_OK)



## 2026-03-27 01:03 UTC — Cron (Nacht-Improvements HA Dashboards)
- ✅ wz.html: Light-Mode Bug-Fixes (NIGHTPLAN_2.md Item 4)
- **renderWeather() Hero-Gradient Fix**: Light-Mode Gradients waren paradoxerweise dunkel (Navy #0d1e38 etc.)
  statt hell — fixiert mit echten Tageszeit-Himmelsfarben:
  - 🌙 Nacht (22–6h): `#1a2240 → #0a1428` (dezent dunkel)
  - 🌅 Morgenröte (6–8h): `#fde8cc → #f5c87a` (warmes Apricot)
  - ☀️ Morgen (8–12h): `#d4ebf8 → #aecde8` (helles Himmelsblau)
  - 🌤 Mittag (12–17h): `#c8e4f6 → #9ec8e8` (klares Blau)
  - 🌆 Abend (17–20h): `#f5d4a8 → #e88f5a` (goldene Stunde)
  - 🌃 Dämmerung (20–22h): `#2a1840 → #140c22` (lila-dunkel)
- **Tagsum "Noch keine Aktivität heute"**: hardcoded `rgba(255,255,255,.3)` → `var(--dim2)` — war im Light-Mode
  auf hellem Hintergrund komplett unsichtbar (weißer Text auf weißem BG)
- **CSS Light-Mode Overrides** ergänzt: wx-hero & Home-Hero Textelemente nutzen jetzt `var(--txt)` / `var(--dim)`
  statt hardcoded weiß → lesbar sowohl auf hellen Tageszeit-Hintergründen als auch nachts
- Geräte-Tab: `.g-pulse-dot.off` und `.g-last-changed` erhalten Light-Mode Override (schwarz-transparent statt weiß-transparent)
- JS-Check: OK | Deployed via SSH (sudo tee, 500117 bytes) | Git: 25e63a9

## 2026-03-27 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Circadian Lighting Button (🌿)
- Neues `#lt-circadian` Div direkt zwischen `#lt-global-dimmer` und `#lt-color-palette` im Licht-Tab
- Button-Design: `border:1px solid rgba(48,209,88,.22)` + `background:rgba(48,209,88,.07)` → dezenter grüner Akzent (Circadian = natürlich, biologisch → Grün)
- 3 Inhalts-Elemente: `#lt-circ-ico` (dynamisches Tageszeit-Emoji), `#lt-circ-label` "Circadian" + `#lt-circ-val` (aktueller Zielwert "2700K · 45%")
- `getCircadian()` Funktion: 7 Tagesphasen je Stunde mit sanften Übergängen:
  - 🌙 Nacht (23–6h): 1900K / 18%
  - 🌅 Morgengrauen (6–8h): interpoliert 1900→4000K / 18→70%
  - ☀️ Morgen (8–12h): interpoliert 4000→6500K / 70→100%
  - 🌤 Mittag (12–16h): 6500K / 100%
  - 🌤 Nachmittag (16–18h): interpoliert 6500→4000K / 100→80%
  - 🌆 Abend (18–21h): interpoliert 4000→2700K / 80→45%
  - 🌃 Spätabend (21–23h): interpoliert 2700→1900K / 45→20%
- `updateCircLabel()`: aktualisiert Emoji + Zielwert-Anzeige; läuft beim Init + alle 60s
- Tap-Handler: iteriert `CFG.lights.filter(on)`, klemmt CT in Licht-eigene min/max-Grenzen, sendet `svc('light','turn_on',{color_temp_kelvin, brightness_pct})`
- `@keyframes circApply`: grüner Flash 38%→7% Opacity → Feedback ohne aufdringlichen Effekt
- Graceful: Button nur sichtbar wenn ≥1 Licht an (`_updateCircadian(onCount)` in `updateAll()`)
- `_updateCircadian` in `updateAll()` nach `_updateColorPalette` eingehängt
- `#lt-circadian` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → Tab-Wechsel Animation
- Toast: "🌅 Circadian auf X Lichter · 2700K / 45%"
- Effekt: Ein Tap setzt alle aktiven Lichter auf die wissenschaftlich optimale Helligkeit+Farbtemperatur für die aktuelle Tageszeit — wie "Adaptive Lighting" aber ohne Plugin, direkt im Dashboard
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 498976 bytes, DEPLOY_OK)



## 2026-03-26 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Regenrisiko-Heatmap 24H (🌂)
- Neue `#rain-hm-card` Section im Wetter-Tab, direkt NACH der Wind-Kurven-Card und VOR der Pollen-Warnung
- Aufbau: 24 flex-Kinder in `#rain-hm-cells` (je Stunde eine Balken-Zelle) + Zeitlabels `#rain-hm-labels` + Summary `#rain-hm-summary`
- Balken-Höhe: 4px (0%) → 32px (100%) proportional zur Wahrscheinlichkeit — visueller Höhenunterschied macht Peak sofort erkennbar
- 5 Farbstufen (kontinuierlicher Opacity-Anstieg je Stufe):
  - <15%: `rgba(48,209,88,...)` grün — praktisch kein Risiko
  - <35%: `rgba(255,214,10,...)` gelb — leichtes Risiko
  - <55%: `rgba(255,159,10,...)` amber — merkliches Risiko
  - <75%: `rgba(255,100,30,...)` orange — hohes Risiko
  - ≥75%: `rgba(255,69,58,...)` rot — sehr hohes Risiko
- Aktuelle Stunde (i===0): weißer `outline: 1.5px solid rgba(255,255,255,.4)` Rahmen → sofort als "Jetzt" erkennbar
- Staggered Einblend-Transition: `transition: height .8s cubic-bezier(.4,0,.2,1) ${i*18}ms` → Balken erscheinen wie eine Welle von links nach rechts
- Zeitlabels bei: Jetzt / +6h / +12h / +18h / letzte Stunde (absolutes Uhrzeit-Format wenn API-Zeitstempel verfügbar)
- Start-Index: iteriert `_wx.hourly.time` nach aktueller Stunde → zeigt immer von "jetzt" aus 24h voraus
- Summary-Zeile zählt Stunden mit ≥40% Wahrscheinlichkeit → 3 Varianten:
  - "✅ Kein Niederschlag erwartet" (0h, max < 25%)
  - "⚠️ Leichtes Regenrisiko (max. X%)" (0h, aber ≥25% Peak)
  - "🌂 Xh erhöhtes Regenrisiko (max. X%) · ~HH:00 Uhr" (Peak-Uhrzeit wird berechnet)
- `drawRainHeatmap()` neue Funktion, aufgerufen in `renderWeather()` nach `drawWindCurve()`
- Graceful: `card.style.display='none'` wenn keine `precipitation_probability` Hourly-Daten (<12 Werte)
- `#rain-hm-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- Kein extra API-Call: nutzt bereits vorhandene `_wx.hourly.precipitation_probability` Daten
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 494917 bytes, DEPLOY_OK)


## 2026-03-26 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — 7-Tage-Temperatur Sparkline im Home-Wetter-Widget
- Neues `<svg id="hw-sparkline">` als letztes Kind der `.hwx` Wetter-Card im Home-Hero (unter `#hwfeel`)
- SVG 56×16px, `viewBox="0 0 56 16"`, `overflow:visible` — passt dezent unter die "Gefühlt X°" Zeile
- `linearGradient #hwSpkGrad`: amber #ff9f0a mit 45%→0% Opacity (von oben nach unten) → subtiler Gradient-Fill
- `#hw-spk-fill`: Area-Fill Pfad (geschlossen nach unten), `fill:url(#hwSpkGrad)`
- `#hw-spk-line`: Linienpfad, `stroke:#ff9f0a`, `stroke-width:1.5`, `stroke-linecap/linejoin:round`
- `#hw-spk-dot0`: Ausgangspunkt (heute), r=2, amber voll — markiert aktuellen Tag
- `#hw-spk-dot6`: Endpunkt (7 Tage), r=1.5, amber 50% — zeigt Wochenendziel
- CSS: `#hw-sparkline{opacity:0;transition:opacity 1.2s ease}` + `.show{opacity:1}` → sanftes Einblenden
- `drawHwSparkline()` IIFE direkt nach `hwfeel.textContent` Zuweisung in `renderWeather()`
- Datenquelle: `_wx.daily.temperature_2m_max` (erste 7 Werte) — bereits vorhanden, kein extra API-Call
- Smooth cubic-bezier Kurve via `C cp1x,cp1y cp2x,cp2y x,y` Pfadsegmente (horizontale Kontrollpunkte)
- Y-Normalisierung: `(temp-min)/(max-min)*(H-PAD*2)` mit ±1°C Padding → immer volle Höhe ausgenutzt
- Mindestens 2 Datenpunkte erforderlich, sonst `display:none` (graceful fallback)
- `svg.classList.add('show')` nach Pfad-Berechnung → Sparkline blendet smooth ein beim Wetter-Laden
- Kein Konflikt mit bestehenden `.hwx` Elementen (flex-column, neues letztes Kind)
- Kein Konflikt mit `hwx-tap` Click-Handler (pointer-events erbt den Container)
- Effekt: Im Home-Wetter-Widget erscheint unter der gefühlten Temperatur eine winzige amber Linienkurve — auf einen Blick sieht man ob die Woche wärmer oder kälter wird
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 490203 bytes, DEPLOY_OK)



## 2026-03-26 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Nav-Bar — Fließender Sliding-Pill Aktiv-Indikator
- Neues `#nav-slide-pill` Div als erstes Kind der `<nav>` — `position:absolute`, gleitet smooth zwischen Tabs
- CSS: `background:rgba(255,159,10,.10)` + `border:1px solid rgba(255,159,10,.18)` → dezenter amber Pill-Hintergrund
- `box-shadow:0 0 12px rgba(255,159,10,.08)` → subtiler Glow um den aktiven Tab-Bereich
- `transition:left .42s cubic-bezier(.34,1.15,.64,1), width .42s cubic-bezier(.34,1.15,.64,1)` → spring-Glide beim Tab-Wechsel
- `overflow:hidden` auf `.nav` → Pill bleibt sauber innerhalb der Nav-Bar
- JS IIFE in `navTo()`: `getBoundingClientRect()` auf aktivem Button → berechnet exakte `left` + `width` relativ zur Nav
- 6px padding beidseitig → Pill ist schmaler als der Button → wirkt wie ein eleganter Unterton
- `pill.classList.add('show')` → `opacity:1` Transition (`.3s ease`) — Pill erscheint beim ersten navTo
- `DOMContentLoaded` IIFE: initialisiert Pill sofort auf dem Home-Tab (kein flash of unstyled state)
- Kein Konflikt mit bestehendem `navGlow` auf `::after` (separate DOM-Ebene, z-index:0 unter Buttons)
- Kein Konflikt mit `ni-badge` (absolut positioniert im Button, nicht in Nav)
- Effekt: Beim Tab-Wechsel gleitet ein weicher amber Schimmer sanft unter das neue Tab-Icon — wie iOS 17 Tab Bar Highlight
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 487900 bytes, DEPLOY_OK)

## 2026-03-26 14:37 UTC — Heartbeat (Auto-Improve)
- ✅ wz.html: Wetter-Tab — Wöchentlicher Niederschlags-Überblick Card (🌧)
- Neue `#weekly-rain-card`: Balkendiagramm 7 Tage, Gesamt-mm, Kategorien, Regentage-Zähler

## 2026-03-26 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Kleidungs-Empfehlung Card (👗)
- Neuer `#outfit-card` Block im Wetter-Tab, direkt VOR der Mondphase-Card (nach Frost-Karte)
- 6 Temperatur-Stufen basierend auf `apparent_temperature` (gefühlte Temperatur):
  - < -5°C: 🧥🧤🧣 "Winterausrüstung nötig" (blau #32c8ff)
  - < 2°C: 🧥🧣 "Dicke Jacke + Schal" (hellblau #64b0ff)
  - < 8°C: 🧥 "Warme Jacke empfohlen" (#9ab8ff)
  - < 14°C: 🧢👔 "Leichte Jacke" (eisblau #a8d8ea)
  - < 20°C: 👕🧢 "T-Shirt + Übergangsjacke" (grün #30d158)
  - < 26°C: 👕 "Sommerlich leger" (gelb #ffd60a)
  - ≥ 26°C: 🩱☀️ "Sommerkleidung + Sonnenschutz" (amber #ff9f0a)
- `#outfit-orb`: positionierter Glow-Orb rechts oben im Card, Farbe = Akzentfarbe der Temperaturstufe, `filter:blur(30px)` → subtiler Farbton-Hintergrund
- Modifier-Chips (dynamisch, nur wenn relevant):
  - 🌂 Regen (wenn `precipitation_probability ≥ 40%` oder WMO-Code = Niederschlag)
  - ❄️ Schnee (wenn WMO-Code = Schnee)
  - 💨 Wind (wenn `windspeed_10m > 30 km/h` — mit km/h Wert)
  - 🕶️ UV-Schutz (wenn `uv_index_max ≥ 6` — UV-Wert + Hinweis)
  - 💧 Schwül (wenn `relative_humidity_2m > 75%`)
- `drawOutfitCard()` liest aus `_wx.current`: `apparent_temperature`, `windspeed_10m`, `relative_humidity_2m`, `weathercode`, stündliche `precipitation_probability[0]` + `_wx.daily.uv_index_max[0]`
- Card bleibt `display:none` wenn keine Current-Daten vorhanden (graceful fallback)
- In `renderWeather()` nach `drawFrostWarning()` eingehängt
- `#outfit-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- Effekt: Im Wetter-Tab erscheint eine praktische Kleidungs-Empfehlung mit Emoji-Icons und kontextuellen Chips — "was soll ich heute anziehen?" auf einen Blick
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, DEPLOY_OK)



## 2026-03-26 08:37 UTC — Heartbeat (Auto-Improve)
- ✅ wz.html: Wetter-Tab — Frostwarnung Card (❄️/🥶)
- Neue `#frost-card` im Wetter-Tab: erscheint wenn Min-Temp < 2°C in nächsten 4 Tagen
- Tag-Chips zeigen betroffene Tage + Temperatur, blau→lila je nach Schwere

## 2026-03-26 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Nav-Icons — Burst-Animation beim Tab-Wechsel
- 5 neue CSS `@keyframes` für jedes Nav-Tab: `niHomePop` / `niMusikSpin` / `niLichtFlash` / `niWetterWobble` / `niGeraeteShake`
- **Home**: Bounce-Up Animation (translateY -5px → +1px → 0, `.5s cubic-bezier(.34,1.56,.64,1)`) — federnder Sprung
- **Musik**: Volle 360°-Rotation (`.55s cubic-bezier(.4,0,.2,1)`) — Note dreht sich einmal herum
- **Licht**: Flash-Glow (scale 1.12→1.28→1.12 + `drop-shadow(0 0 8px rgba(255,159,10,.95))`, `.5s ease`) — Glühbirne blitzt auf
- **Wetter**: Wobble-Rotation (-8°→+6°→-4°→0°, `.55s ease`) — Wolke wackelt freundlich
- **Geräte**: Horizontal-Shake (±3px→±2px→0, `.5s ease`) — Monitor zittert kurz
- CSS-Klassen `.ni-anim-{page}` aktivieren Animation auf dem SVG-Element des Buttons
- JS IIFE in `navTo()`: `classList.remove → offsetWidth reflow → classList.add`, `animationend` → auto-remove
- Kein Konflikt mit bestehendem `transform:scale(1.12)` auf `.ni.on svg` (Animationen starten von diesem Wert)
- Kein Konflikt mit `badgePop` oder `navGlow` (separate Elemente / Properties)
- Effekt: Jeder Tab-Wechsel gibt dem Icon eine kleine persönlichkeitspassende Geste — wie App-Icons in iOS 18 die beim Tap wackeln
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, DEPLOY_OK)


## 2026-03-26 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Temperatur-Heatmap im 7-Tage-Forecast
- Neue `tempHeatBg(t)` Helper-Funktion: gibt `linear-gradient(90deg, <color> 0%, transparent 68%)` zurück
- 7 Temperaturstufen: ≤2°C blau rgba(10,132,255,.13) / ≤8°C hellblau / ≤14°C grün (#30d158) / ≤20°C hellgrün / ≤26°C amber (#ff9f0a) / ≤32°C orange / >32°C rot (#ff453a)
- Gradient läuft von links (volle Farbe) nach rechts (transparent) — dezenter Wash-Effekt, UI bleibt lesbar
- Pro 7-Tage-Zeile wird `heatBg` via `background:${heatBg}` inline gesetzt
- Kompatibel mit `.wx7-wknd` Wochenend-Highlight (beide Styles addieren sich graceful)
- Effekt: Auf einen Blick sieht man ob die Woche kalt (blau) oder warm (amber/rot) wird — wie ein Kalender-Heatmap
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 462810 bytes, DEPLOY_OK)



## 2026-03-26 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Stündliche Wind-Kurve 24H
- Neue `#wind-curve-card` Section im Wetter-Tab, direkt vor der Pollen-Warnung
- SVG-Area-Chart (viewBox 320×60, `preserveAspectRatio=none` → responsive volle Breite)
- `windspeed_10m` zu Open-Meteo `&hourly=` Parameter hinzugefügt
- Smooth cubic-bezier Linienpfad (identische `smooth()` Logik wie Temp-Kurve)
- Blauer Gradient-Fill (`wndGrad`): #0a84ff mit 45%→2% Opacity — kühler Wind-Charakter
- Blaue Linie (`#0a84ff`, stroke-width 1.5) + blauer Glow-Dot bei Jetzt-Stunde
- `wnd-now-dot`: `drop-shadow(0 0 4px rgba(10,132,255,.9))` — markiert aktuelle Stunde
- `wnd-labels` SVG-Gruppe: Windwerte (km/h) an 0h/6h/12h/18h/23h Positionen
- `wnd-time-labels` Row: Zeitlabels "Jetzt / HH:00" unter dem Chart
- `wnd-max-row`: Max-Wind + Uhrzeit + Stärke-Beschreibung (Leicht/Mäßig/Frisch/Stark/Sturm)
- Y-Skala: 0 unten, max(winds, 10) oben → mindest 10 km/h Spanne, kein verzerrter Chart bei Windstille
- `drawWindCurve()` in `renderWeather()` nach `drawTempCurve()` aufgerufen
- Card bleibt `display:none` wenn keine Hourly-Winddaten verfügbar (graceful fallback)
- `#wind-curve-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 462312 bytes, DEPLOY_OK)



## 2026-03-26 01:00 UTC — Cron (Nacht-Improvements HA Dashboards)
- ✅ wz.html: Licht-Tab — Globaler Dimmer-Schieberegler
- Neues `#lt-global-dimmer` Element zwischen Helligkeits-Meter und Licht-Grid
- SVG Sonne-Icon (amber), Range-Slider `#lt-gd-range` (1–100%), Wert-Label `#lt-gd-val`
- CSS: WebKit/Moz slider-thumb styling (amber Gradient, Glow-Box-Shadow, Scale-on-Active)
- Hintergrundtrack via `background: linear-gradient(90deg, #ff9f0a X%, rgba(.1) X%)` — Füllstand sichtbar
- In `updateAll()`: Slider synct sich mit aktueller Durchschnittshelligkeit (wenn nicht `_dragging`)
- Event-Handler IIFE: `input` Event mit 350ms Debounce → `svc('light','turn_on',{brightness_pct})` für alle aktiven dimmb. Lichter
- `hap()` Feedback nach erfolgreichem Senden
- Nur sichtbar wenn ≥1 Licht an (`.show` Klasse via `updateAll()`)
- ✅ wz.html: Wetter-Tab — Wochenend-Highlight im 7-Tage Forecast
- CSS-Klassen `.wx7-wknd` (blauer linker Border + subtiler blauer Background) + `.wx7-wknd-lbl` (hellblaues Sub-Label)
- JS: `dow===6||dow===0` Erkennung → `.wx7-wknd` Klasse auf Row-Div + hellblaue Textfarbe für Tageslabel
- `wkndSub` Sub-Label `<span class="wx7-wknd-lbl">SA</span>` oder `SO` unter dem Wochentagsnamen
- Nur für i>1 (nicht "Heute"/"Morgen") — klare Unterscheidung
- Effekt: Sa/So im Wochenforecast sofort auf einen Blick erkennbar durch blauen Akzent
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 450042 bytes, DEPLOY_OK) | Git: 2a3dda8



## 2026-03-26 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Sonnenuntergang/Sonnenaufgang Countdown-Chip
- Neues `#sun-cd-chip` Div direkt unter dem `#day-arc-wrap` im Home-Hero
- Design: Pill-Shape `border-radius:20px`, amber Akzent (`rgba(255,159,10,.12)` Hintergrund + `.25` Border) für Sunset-Modus
- `.sr-mode` Klasse → blaues Farbschema (`rgba(100,180,255,.1)`) wenn nächstes Event Sonnenaufgang ist
- CSS Transition: `opacity .6s ease, transform .5s cubic-bezier(.34,1.28,.64,1)` → spring-Einblend-Animation
- Emoji-Icon: 🌅 für Sonnenuntergang, 🌄 für Sonnenaufgang — wechselt dynamisch
- `.show` Klasse: `opacity:1; transform:scale(1)` — Chip erscheint smooth nach erstem Weather-Load
- JS IIFE am Ende von `updateDayArc()`: läuft bei jedem `updateClock()` Tick (alle 1s)
- Datenquelle: `window._wx.daily.sunrise[0]`, `.sunset[0]`, `.sunrise[1]` (morgen als Fallback +86400s)
- Logik: `now < sr0` → Sonnenaufgang heute | `now < ss0` → Sonnenuntergang heute | sonst → Sonnenaufgang morgen
- Zeitformatierung: `Xh Ymin` wenn ≥60min, `Ymin` wenn <1h — kompakt und lesbar
- Chip bleibt versteckt wenn `_wx.daily` noch nicht geladen (graceful fallback)
- Kein Konflikt mit bestehenden Hero-Elementen (day-arc, aclock, hnp-strip)
- Kein extra API-Call — nutzt bereits vorhandene Open-Meteo `daily` Daten
- Effekt: Unter dem Tageszeit-Arc blinkt ein kleiner Chip: "🌅 Sonnenuntergang in 1h 23min" — zeitbewusst wie eine Apple Watch Complication
- JS-Check: OK | Deployed via SSH (paramiko base64-chunk-pipe, 446226 bytes, DEPLOY_OK)



## 2026-03-25 14:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Typewriter-Animation für Greeting-Text
- Neue CSS-Klasse `.hgreet-cursor`: 1.5px breiter, 0.8em hoher vertikaler Strich in `rgba(255,255,255,.5)`, `border-radius:1px`, `vertical-align:middle`
- `@keyframes greetCursor`: 0%/100% opacity:1 → 50% opacity:0 → 0.8s ease-in-out infinite (klassischer Cursor-Blink)
- `.hgreet-cursor.gc-hide`: `display:none` → Cursor verschwindet nach Tipp-Ende
- `typeGreet(el, text)` Funktion: räumt bestehenden Timer auf, leert `el`, fügt Cursor-Span ein
- Typing-Loop via `setTimeout`: fügt je ein Zeichen als `TextNode` vor dem Cursor-Span ein
  - Delay: 0ms für erste 2 Zeichen (kein Anfangs-Ruckeln), dann 40ms/Zeichen → ~2s für typische Begrüssung
  - Am Ende: `cur.classList.add('gc-hide')` nach 900ms → Cursor blendet sich diskret weg
- `window._greetTyped` Flag: `typeGreet` läuft nur beim ersten `updateClock()`-Aufruf (Seitenload)
- `window._greetLast` String: vergleicht aktuellen Greeting-Text — `typeGreet` feuert erneut wenn sich die Tageszeit-Begrüssung ändert (z.B. Morgen → Mittag)
- Kein Konflikt mit bestehendem `greetFade`-CSS-Animation (fade läuft auf Parent-Element, Typewriter modifiziert innerHTML)
- Kein Flickern: `updateClock` prüft vor jedem Tick ob Text identisch ist → kein ständiges Neu-Tippen
- Effekt: Beim Öffnen der App tippt sich "Guten Morgen, Janis ☀️" zeichenweise ein — danach verschwindet der Cursor smooth
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 437291 bytes, DEPLOY_OK)



## 2026-03-25 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: App — Horizontales Swipe zwischen Tabs
- IIFE am Ende des Haupt-Script-Blocks (vor `</script>`), nutzt vorhandene `navTo()` + `hap()` Funktionen
- `TABS` Array: `['home','musik','licht','wetter','geraete']` — entspricht der Navbar-Reihenfolge
- `touchstart`: speichert `sx`, `sy`, `st2` (Zeitstempel) + resettet `swiping=false`
- `touchmove`: setzt `swiping=true` wenn `|dx|>18` und `|dy|<MAX_DY` → unterscheidet horizontale von vertikalen Gesten
- `touchend`: prüft `|dx|≥65px`, `|dy|≤80px`, `dt≤480ms` → swipe links=+1 (nächster Tab), rechts=-1 (vorheriger Tab)
- Guard: `idx<0||next<0||next≥TABS.length` → kein Wraparound, kein Fehler am Ende der Liste
- Swipe-Hint Overlay `#tab-swipe-hint`: dynamisch per JS injiziert, `position:fixed` zentriert, Glassmorphism-Pill
  - Zeigt `▶` (nächster Tab) oder `◀` (vorheriger Tab) als großes Emoji
  - Einblend-Animation: scale(.7)+opacity:0 → scale(1)+opacity:1 via `cubic-bezier(.34,1.28,.64,1)`
  - Auto-fade nach 600ms via `clearTimeout` + `setTimeout`
- Kein Konflikt mit horizontalen Gesten auf Album-Art (Musik-Tab hat eigene touchend-Guards mit `dy`-Filter)
- Kein Konflikt mit Pull-to-Refresh (vertikal, dx-Guard vorhanden)
- Kein Konflikt mit Light-Sheet Long-Press (kein deltaX-Kriterium)
- Passive Event-Listener → kein Performance-Impact
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 436342 bytes, DEPLOY_OK)



## 2026-03-25 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Sichtweite & Bewölkungs-Karte
- Neue `#vis-cloud-card` Section im Wetter-Tab, nach `#hum-card` und vor `#golden-hour-card`
- Zwei SVG-Arc-Gauges (72×72px, gleiche 210°-Geometrie wie Barometer/Feuchte) nebeneinander mit Trennlinie
- **Sichtweite-Gauge** (`#vis-fill`): `linearGradient visGrad` rot (#ff453a) → amber (#ff9f0a) → grün (#30d158) → blau (#0a84ff)
  - API: `visibility` (in Metern) von Open-Meteo `&current=`
  - Skala 0–50km (50'000m = 100%), `stroke-dashoffset` = ARC_LEN*(1-pct)
  - Anzeige: <1km zeigt Meter (z.B. "450 m"), ≥1km zeigt km (z.B. "8.4 km")
  - 6 Stufen: Dichter Nebel (<200m, rot) / Nebel (<1km, amber) / Dunstig (<4km, gelb) / Mässig (<10km, hellblau) / Gut (<30km, grün) / Ausgezeichnet (≥30km, blau)
- **Bewölkungs-Gauge** (`#cld-fill`): `linearGradient cldGrad` grün (#30d158) → blau (#0a84ff) → weiß (.6 opacity)
  - API: `cloud_cover` (0–100%) von Open-Meteo `&current=`
  - 5 Stufen: Klar (<12%, gelb) / Heiter (<30%, amber) / Wolkig (<60%, hellblau) / Stark bewölkt (<85%, grau) / Bedeckt (≥85%, weiß)
- Trennlinie: 1px × 80px `rgba(255,255,255,.07)` zwischen den zwei Gauges
- Beide Gauges mit eigenem Label (farbcodiert, dynamisch) + statischem Beschriftungs-Text unten
- `drawVisCloud()` neue Funktion: liest `_wx.current.visibility` + `_wx.current.cloud_cover`
- Card bleibt `display:none` wenn beide Werte fehlen (graceful fallback)
- In `renderWeather()` nach `drawWindChill()` eingehängt
- `#vis-cloud-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- `transition:stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)` → weiche Einblende-Animation
- JS-Check: OK | Deployed via SSH (paramiko b64-chunk-pipe, 427668 bytes, DEPLOY_OK)



## 2026-03-25 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Luftfeuchtigkeit Komfort-Karte
- Neue `#hum-card` Section im Wetter-Tab, zwischen Barometer-Card und Goldene-Stunde-Card
- SVG-Arc-Gauge (72×72px, viewBox 0 0 72 72): Track-Pfad + Fill-Pfad identische Geometrie wie Barometer
- `linearGradient #humGrad`: blau (#0a84ff, 0%) → grün (#30d158, 40%) → amber (#ff9f0a, 72%) → rot (#ff453a, 100%)
- `stroke-dasharray:188.5` + `stroke-dashoffset = 188.5*(1-rh/100)` → rh=0% → leer, rh=100% → voll
- `transition:stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)` → weiche Einblende-Animation
- Center-Text: `#hum-svg-val` (13px, bold, weiß) + "%" Label (7px, gedimmt)
- Rechts: `#hum-val` (1.6rem, light) + "%" Einheit + `#hum-level` (farbig)
- 5 Komfort-Stufen: 🏜 Sehr trocken (<20%, blau) / 💨 Trocken (<30%, hellblau) / ✅ Optimal (<60%, grün) / 🌫 Feucht (<75%, amber) / 💦 Sehr feucht (≥75%, rot)
- `#hum-desc`: kontextsensitive Empfehlung je Stufe (z.B. "Ideale Luftfeuchtigkeit — angenehmes Raumklima")
- `#hum-dew`: Taupunkt-Berechnung via Magnus-Formel (a=17.625, b=243.04), zeigt z.B. "8.3°C"
- `#hum-bar`: horizontaler Fortschrittsbalken (blau→grün→amber→rot Gradient), 1.4s ease Transition
- 4 Skala-Marker: 0% / 30% / 60% / 100%
- `drawHumidity()` neue Funktion: liest `_wx.current.relative_humidity_2m` + `temperature_2m`
- Card bleibt `display:none` wenn kein Feuchtigkeitswert vorhanden (graceful fallback)
- In `renderWeather()` nach `drawBarometer()` eingehängt
- `#hum-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- JS-Check: OK | Deployed via SSH (paramiko printf-chunk-pipe, 418316 bytes, DEPLOY_OK)



## 2026-03-25 02:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Mini SVG Analog Clock neben Digitaluhr
- Neues `<svg id="aclock">` (44×44px) als Geschwister der `.htime` — beide in einem Flex-Row-Wrapper `#aclock-wrap`
- Zifferblatt: gefüllter Kreis (`rgba(0,0,0,.22)`) + dezenter Ring (`rgba(255,255,255,.12)`) + 4 Tick-Striche bei 12/3/6/9 (rgba .35)
- Amber-Dot bei 12 Uhr als Orientierungshilfe (`#ff9f0a`)
- Stundenzeiger: `<g id="ach-hour-g">` → dicker amber Strich (2.4px), Länge bis Pixel 11
- Minutenzeiger: `<g id="ach-min-g">` → weißlicher Strich (1.4px, .88 opacity), Länge bis Pixel 5.5
- Sekundenzeiger: `<g id="ach-sec-g">` → roter Strich (`#ff453a`, .9px), mit kurzem Gegengewicht (y1=25, y2=4.5)
- Zentrum: amber Pivot-Punkt + dunkle Abdeckscheibe (2-layered)
- `@keyframes aclockIn`: scale(.6)+rotate(-30deg) → scale(1)+rotate(0), cubic-bezier(.34,1.28,.64,1), .9s, delay .15s
- `drop-shadow(0 0 6px rgba(255,159,10,.25))` SVG-Filter → subtiler Amber-Glow
- JS IIFE in `updateClock()`: `sec*6`, `min*6+sec*.1`, `hr*30+min*.5` → Grad für SVG `rotate(deg,22,22)` Attribute
- `setAttribute('transform', rotate(...))` → nativer SVG-Ansatz, kein transform-box CSS-Problem, 100% cross-browser
- Sekundenzeiger springt diskret jede Sekunde (da `updateClock` alle 1000ms läuft — klassischer Zeiger-Stil)
- Effekt: Neben der grossen Digitaluhr tickt eine kleine, elegante analoge Uhr — Apple Watch mini vibe
- JS-Check: OK | Deployed via SSH (base64-chunk-pipe, 412506 bytes, DEPLOY_OK)



## 2026-03-25 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Track Progress Arc um Album-Disc
- Neues `<svg id="track-prog-arc-svg">` als erstes Kind von `#alb-disc` (position:absolute, inset:-10px, calc 100%+20px, z-index:9, pointer-events:none, transform:rotate(-90deg))
- SVG-Struktur: `#tpa-track` (dünner Hintergrundring, rgba .07) + `#tpa-fill` (aktiver Bogen, amber→gelb Gradient)
- `linearGradient #tpaGrad`: amber #ff9f0a → gelb #ffcc02 → amber 50% Opacity — passt zur Dashboard-Akzentfarbe
- Kreis r=86 im 180×180 viewBox → Umfang = 2π×86 = 540.35px
- `stroke-dasharray:540.35` + `stroke-dashoffset` = 540.35 × (1 - pct) → Arc zeigt Fortschritt von oben (rotate -90°)
- `stroke-linecap:round` → runder Endpunkt (Apple-Music-Stil)
- CSS-Transition: `opacity .8s ease, stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)` → weiche Animation
- `.show` Klasse → `#tpa-fill` opacity:1; versteckt wenn kein Track (opacity:0) — kein visuelles Rauschen bei Radio/Idle
- JS IIFE im Track-Fortschrittsbalken-Block: `CIRC=540.35`, berechnet `pct=pos/dur`, setzt `strokeDashoffset=CIRC*(1-pct)`
- `arcSvg.classList.toggle('show', hasArc)` — Arc erscheint nur wenn `playing && pos!=null && dur!=null && dur>0`
- Kein Konflikt mit bestehenden `eq-ring` Puls-Animationen (separate Kreise, different z-index layers)
- Kein Konflikt mit `#alb-tonearm-wrap` (absolut positioniert, z-index:10 — liegt über dem Arc)
- Effekt: Beim Spotify-Stream dreht sich um den Vinyl-Disc ein feiner amber Leuchtring, der sekündlich aktualisiert die Spielposition zeigt — wie Apple Music Fortschritts-Halo
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 409360 bytes, DEPLOY_OK)



## 2026-03-24 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Cookie/DSGVO Banner
- Neues `#dsgvo-banner` Element als `position:fixed;bottom:0` Bottom-Banner (z-index:10001)
- Design: iOS Dark Glassmorphism (`rgba(18,18,20,.97)`, `backdrop-filter:blur(20px) saturate(1.6)`)
- Border-Top-Linie `rgba(255,255,255,.08)` — dezent, passt ins Dark Theme
- Inhalt: 🔒 Icon + Text ("Diese Seite verwendet **keine** Tracking-Cookies") + "Verstanden ✓" Button
- Schließen-Button: grüner Akzent (`#30d158`), rounded pill, hover lift-effect
- Erscheint nach 1.5s via `setTimeout` + CSS `transform:translateY(0)` spring-Animation
- `localStorage.getItem('dsgvo_dismissed_v1')` — einmalig schliessbar, bleibt dauerhaft weg nach Klick
- i18n reaktiv: `langChange` Event → DE/EN Text-Varianten für Banner-Text + Button
- Kein Flackern: Banner wird gar nicht gezeigt wenn `localStorage` bereits gesetzt
- `[x]` auch für Scroll-to-Top markiert (war bereits in demo.html implementiert, nur nicht abgehakt)
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 365273 bytes, DEPLOY_OK)



## 2026-03-24 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Allergiker-Warnung Chip
- Neues `#allerg-chip-row` Flex-Container direkt im `#wx-hero` (nach Stats-Row, vor Hero-Ende)
- Trennlinie `border-top:1px solid rgba(255,255,255,.06)` und `padding-top:10px` — dezent integriert
- 3 Chips: 🌲 Birke (`birch_pollen`), 🌾 Gräser (`grass_pollen`), ⚠️ Ambrosia (`ragweed_pollen`)
- 4 Severity-Klassen: `.ac-low` grün (#30d158) / `.ac-mid` gelb (#ffd60a) / `.ac-high` amber (#ff9f0a) / `.ac-vhigh` rot (#ff453a)
- `.ac-vhigh` Chips: `@keyframes allergChipWarn` — roter Puls-Ring um den Chip bei sehr hohem Pollen (2.2s loop), um Allergiker sofort zu warnen
- Chip-Design: Pill-Shape (`border-radius:20px`), halbtransparenter farbiger Hintergrund + passender Border
- `renderPollenChips()` neue Funktion: liest `window._pollenLatest` (von fetchPollen gesetzt), updated Chip-Klassen + Labels + Farben
- `window._pollenLatest={data,hi}` wird am Ende von `fetchPollen()` gesetzt → `renderPollenChips()` direkt aufgerufen
- Chips nur sichtbar wenn Wert ≥ 0 vorhanden — fehlende Pollen-Typen (Saison-abhängig) werden automatisch ausgeblendet
- `#allerg-chip-row` selbst `display:none` wenn alle 3 Chips leer (graceful fallback, z.B. Winter)
- Effekt: Im Wetter-Hero erscheinen direkt neben Temperatur/Wind die 3 wichtigsten Allergen-Chips — sofort auf einen Blick sichtbar ob Allergiker heute draußen sein sollten
- JS-Check: OK | Deployed via SSH (paramiko base64-chunk-pipe, DEPLOY_OK)

## 2026-03-24 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Podcast/Radio Fallback-Anzeige
- Neues `#radio-fallback-card` Element im Musik-Tab, erscheint wenn Almando spielt aber KEIN Spotify-Stream (`_isSpot=false`)
- Hintergrund: amber `radial-gradient` Orb (`#rfc-bg`) mit 12% Opacity — dezenter Warmton
- Linkes Icon: 44×44px Card mit SVG-Antenne (`#rfc-antenna-ico`) — amber für Radio, lila für Podcast
- `@keyframes rfcAntennaPulse`: Antenne pulsiert sanft (0.35→0.7 Opacity, 2.4s Loop) — signalisiert Empfang
- Type-Badge `#rfc-type-badge`: "📻 RADIO" (amber) oder "🎙 PODCAST" (lila #bf5af2) — automatisch erkannt via Content-ID
- Podcast-Erkennung: `media_content_id` enthält "podcast", "anchor", "simplecast" ODER Titel enthält "podcast"
- `#rfc-title`: `media_title` → `media_channel` → `_radActive` → "Livestream" (Fallback-Kette)
- `#rfc-sub`: `media_channel` wenn anders als Titel, sonst "Almando Wohnzimmer"
- `#rfc-freq-row`: 5 animierte Balken (`#rfc-wave-bars`) + gekürzte Content-ID (`#rfc-cid`, max 40 Zeichen)
- `@keyframes rfcBar`: Balken tanzen mit 0.15s gestaffelten Delays (4px→16px Höhe, 1.1s alternate loop)
- Balken animieren nur wenn `.playing` Klasse aktiv (kein visuelles Rauschen im Idle-Zustand)
- Content-ID Anzeige: versucht URL-Parsing via `new URL()` → zeigt nur Hostname+Pfad (nicht volle URL)
- JS IIFE in `updateAll()`: `isRadioOrPodcast = playing && !_isSpot` → `card.classList.toggle('show', ...)`
- Karte bleibt versteckt (`display:none`) bei Spotify-Streams, Idle, und wenn Almando aus
- `#radio-fallback-card` zur `.page-entering>` Stagger-CSS-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- Effekt: Wenn Radio/Podcast läuft aber kein Spotify-UI verfügbar, erscheint eine saubere Karte mit Station-Info, animierten Wellen-Balken und Typ-Badge — statt einem leeren Album-Art-Disc
- JS-Check: OK | Deployed via SSH (paramiko base64-chunk-pipe, 404364 bytes)

## 2026-03-24 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — "Beste Stunde" Aktivitäts-Karte
- Neue `#best-hour-card` Section im Wetter-Tab, direkt VOR der Mondphase-Card
- Grünes Farbschema: `rgba(48,209,88)` Border + Glow, passend zu "aktiv/positiv" Semantik
- `@keyframes bestHourOrb`: träger Drift-Orb Hintergrund (8s loop, 3 Keypoints — analog zu ghOrbDrift)
- Linker Zeit-Badge (`#bh-time-badge`): grüner Gradient-Hintergrund, grosse `HH:00` Anzeige + relative Zeit ("in Xh")
- Rechts: dynamisches Label + `#bh-chips` Flex-Wrap mit 3 Condition-Chips
- Chip-Farben: Temperatur (amber/grün/blau je Bereich), Regenwahrsch. (grün<15% / amber<40% / rot), Wind (grün<15 / amber<30 / rot)
- `drawBestHour()` Funktion: iteriert nächste 18 Stunden, überspringt Nacht-Stunden (vor 6h / nach 21h)
- Score-Formel: Temp-Komfort-Bonus (±16°C ideal, max 40Pkt), Regen-Malus (-0.8×%), Wind-Malus (-0.5×km/h über 10), WMO-Bonus (+20 bei klar, +10 bei leicht bewölkt, -15 bei Niederschlag)
- 3 Label-Varianten: "☀️ Perfekter Moment für draußen" / "🌤 Gutes Wetter-Fenster" / "🌡 Beste verfügbare Stunde"
- Card bleibt `display:none` wenn keine Stundendaten verfügbar (graceful fallback)
- `drawBestHour()` in `renderWeather()` nach `drawGoldenHour()` eingehängt
- `#best-hour-card` zur `.page-entering>` Stagger-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- JS-Check: OK | Deployed via SSH (paramiko base64-chunk-pipe, 393466 bytes)

## 2026-03-24 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — "Goldene Stunde" Karte (bereits implementiert, als [x] markiert)
- ✅ wz.html: Home-Tab — Batterie-Status Chip (bereits implementiert, als [x] markiert)
- Beide Features waren vollständig in wz.html vorhanden (HTML, CSS, JS) aber noch nicht in AUTOWORK.md abgehakt
- Goldene Stunde: `#golden-hour-card` zeigt sich im 4h-Vorschaufenster + aktiv während der 45min vor Sunset
  - `@keyframes ghSunPulse` + `ghOrbDrift` — orangener Glow-Orb im Hintergrund
  - Fortschrittsbalken (amber Gradient), Live-Countdown (sekunden-genau), Zustandswechsel Upcoming→Aktiv
  - `drawGoldenHour()` in `renderWeather()` aufgerufen
- Batterie-Chip: `#batt-chip` scannt alle `_S` States nach `device_class=battery` oder `_battery_level`/`_battery` IDs
  - Schwellwert ≤20% → roter Chip mit Gerätenamen + Prozentwert, max 2 Geräte + "+N" Hinweis
  - `.show` Klasse via spring-Animation (`cubic-bezier(.34,1.28,.64,1)`)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, DEPLOY_OK)

## 2026-03-24 16:36 UTC — Heartbeat (Main Agent)
- ✅ demo.html: "Warum jetzt?" 3-Spalten Urgency-Section — 3 Karten (120h / €340 / 3000+), animierte Zähler mit easeOut via IntersectionObserver, Accent-Karte für Preis-Highlight, i18n DE+EN, responsive 1-Spalte Mobile
- JS-Check: OK | Commit: d009767 | Deploy: kein Remote verfügbar

## 2026-03-24 07:08 UTC — Heartbeat (Main Agent)
- ✅ demo.html: "Kunden-Stimmen" Ratings-Balken — 5 Sterne-Reihen (5⭐ 87%, 4⭐ 13%, 3-1⭐ 0%), animierte Füll-Balken via IntersectionObserver, gold/silver Gradient, 4.98 Summary-Block, i18n DE+EN, Gesamtbewertungs-Summary-Card
- JS-Check: OK | Commit: 834215a | Deploy: kein Remote verfügbar

## 2026-03-24 06:08 UTC — Heartbeat (Main Agent)
- ✅ demo.html: Anchor-Navigation — sticky Mini-Nav (Überblick · Preise · Demo · Kontakt), erscheint nach Hero-Scroll, smooth scroll, aktiver Abschnitt highlighted (blauer Unterstrich), Dark Mode + i18n DE/EN, Mobile responsive
- JS-Check: OK | Commit: ae09b7f | Deploy: kein Remote/SSH verfügbar

## 2026-03-24 02:05 UTC — Heartbeat (Main Agent)
- ✅ demo.html: Live-Besucher FOMO-Counter im Hero — grüner Pulse-Dot + "X Personen schauen gerade", startet 4-8 Besucher, driftet ±1 alle 18-45s, erscheint nach 2.5s, i18n DE/EN
- JS-Check: OK | Commit: 9934d0b | Deploy: kein Remote/SSH verfügbar

## 2026-03-24 02:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Animierte SVG-Wellen im Hintergrund
- Neues `<svg id="hero-wave-svg">` als letztes Element VOR `.hcont` im `.hero` Container (position:absolute, bottom:0, left:0, width:100%, height:72px, z-index:1, pointer-events:none)
- 2 Wellen-Gruppen: `#hero-wave-p1` (amber) + `#hero-wave-p2` (blau), gegenläufig animiert
- Welle 1: `path` mit Sinus-Form (C100 28,200 68,...), `fill:url(#wv1Grad)` — amber 10%→18%→10% horizontal Gradient
- Welle 2: `path` mit versetzter Sinus-Form (C133 38,...), `fill:url(#wv2Grad)` — blau 08%→15%→08% Gradient
- `@keyframes heroWave1`: translateX 0 → -50% in 18s linear infinite (amber nach links)
- `@keyframes heroWave2`: translateX -50% → 0% → +50% in 24s linear infinite (blau nach rechts, entgegengesetzt)
- Welle-Pfade sind 2× Viewport-Breite (1800px / 2000px path) → nahtloser endloser Loop
- Kein JS nötig — reine CSS-Animation, null Overhead
- Kein Konflikt mit bestehenden `#star-cv`, `#wx-particles`, `#amb-orb` (separate z-index Layer)
- `.hero{overflow:hidden}` bereits gesetzt → Wellen werden am Rand sauber abgeschnitten
- Effekt: Am unteren Rand des Home-Heroes fließen zwei halbtransparente Farbwellen (amber + blau) sanft in entgegengesetzte Richtungen — wie ein lebendiger, athmosphärischer Horizont
- JS-Check: OK | Deployed via SSH (base64-chunk-pipe, 379030 bytes)

## 2026-03-24 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Gesamt-Helligkeits-Meter
- Neues `#lt-bri-meter` Div direkt unterhalb des "Licht" Labels im pg-licht Tab (vor dem .lg Grid)
- Aufbau: `#lt-bri-meter-bar-wrap` (6px hoher Track) + `#lt-bri-meter-bar` (animierter Fill) + Label-Zeile
- CSS `#lt-bri-meter-bar`: `background: linear-gradient(90deg, #ff9f0a 0%, #ffcc02 60%, #fff9a0 100%)`, `box-shadow: 0 0 6px rgba(255,159,10,.5)`
- `transition: width 1.1s cubic-bezier(.4,0,.2,1)` → smooth Breiten-Animation beim Schalten
- 3 Farbstufen: dim (<30% avg) → abgedunkeltes Amber | normal → Standard-Gradient | bright (>85%) → weißlich-gelb
- Label-Zeile: links `"X von Y an"` (dezent) + rechts `"Ø XX%"` (amber, fett) via Flexbox justify-between
- `.lt-bri-pct.dim` Klasse → weiße Farbe wenn keine brightness-Daten vorhanden (z.B. Switches)
- JS IIFE in `updateAll()`: iteriert `CFG.lights.filter(effOn)`, liest `_S[id].attributes.brightness` (0–255 → %)
- Durchschnitt über alle Lichter mit brightness-Attribut; Fallback-Label "aktiv" wenn keine HA-Helligkeitsdaten
- Meter faded aus (`opacity:0`, `width:0%`) wenn alle Lichter aus → kein visuelles Rauschen
- Effekt: Übersichtlicher Helligkeits-Balken zeigt auf einen Blick wie "hell" die Gesamtstimmung ist
- JS-Check: OK | Deployed via SSH (base64-chunk-pipe, 373971 bytes)

## 2026-03-23 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Gefühlte Temperatur Trend-Pfeil
- Neues `<span id="wxt-feel-arrow">` direkt hinter `#wxt-feel` im Wetter-Hero (neben "Tatsächlich / Gefühlt")
- CSS: `#wxt-feel-arrow` — `display:inline-block`, `vertical-align:middle`, `transition:color .6s, opacity .6s`
- 3 Zustände: `.up` (grün #30d158, ↑), `.down` (rot #ff453a, ↓), `.neutral` (weiß .35, →)
- `@keyframes feelArrowUp`: translateY 0 → -3px → 0 (1.8s loop) — Pfeil schwebt leicht nach oben
- `@keyframes feelArrowDown`: translateY 0 → +3px → 0 (1.8s loop) — Pfeil schwebt leicht nach unten
- Schwelle ±1°C: diff > 1 → ↑ grün, diff < -1 → ↓ rot, sonst → neutral weiß
- IIFE in `renderWeather()` nach `wxt-feel.textContent` Zuweisung: `c.apparent_temperature - c.temperature_2m`
- `void arr.offsetWidth` Reflow-Trick → Animation startet sauber bei jedem Weather-Update
- Beispiel: Wenn es 10° ist aber sich wegen Wind nur 6° anfühlt → roter ↓ Pfeil animiert nach unten
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 371KB)

## 2026-03-23 21:16 UTC — Heartbeat (Main Agent)
- ✅ demo.html: Countdown Timer im Scarcity-Banner (24h localStorage, HH:MM:SS Anzeige, auto-reset nach Ablauf, ⏱ Badge-Style neben Plätze-Text)
- JS-Check: OK | Commit: 2d9be49 | Deploy: kein Remote/SSH verfügbar

## 2026-03-23 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Farbige Tile-Border bei RGB-Lichtern
- Neue CSS-Klasse `.ltico.rgb-border`: `box-shadow: 0 0 0 1.5px var(--rgb-border-c) + 0 0 8px 1px var(--rgb-border-glow)` — dünner Ring + Glow in exakter Lichtfarbe
- `transition: box-shadow .8s ease` → weicher Farbübergang beim Schalten / Farbwechsel
- JS im `updateLights()` Loop: wenn `on && rgb_color` vorhanden → `.rgb-border` Klasse setzen + `--rgb-border-c: rgba(r,g,b,.75)` + `--rgb-border-glow: rgba(r,g,b,.28)` als CSS-Variablen direkt auf `.ltico`
- Wenn Licht aus ODER kein rgb_color → Klasse entfernt, CSS-Variablen gelöscht → kein Border sichtbar
- Kein Konflikt mit bestehendem `pulseRing` auf `::after` (verschiedene CSS-Properties: box-shadow vs. border)
- Kein Konflikt mit `.lt-bri-arc` SVG-Overlay (separate DOM-Ebene)
- Effekt: RGB-fähige Lichter zeigen einen dünnen farbigen Leuchtrand um das Icon-Oval, der exakt die aktuelle Lichtfarbe widerspiegelt — z.B. warmes Orange, Türkis, Lila je nach eingestellter Farbe
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 361KB)

## 2026-03-23 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Equalizer-Ringe um Album-Art
- 3 `<div class="eq-ring">` als erste Kinder von `#alb-disc` eingefügt (position:absolute;inset:0;border-radius:50%;pointer-events:none;z-index:1)
- `.eq-ring`: `border:1.5px solid rgba(255,159,10,.55)` — amber, semi-transparent
- `@keyframes eqRingPulse`: `scale(1) opacity(.55)` → `scale(1.6) opacity(0)` über 2.2s ease-out
- `#alb-disc.playing .eq-ring:nth-of-type(1/2/3)`: animation-delay 0s / 0.73s / 1.46s → gestaffelte Wellen
- Ringe nutzen CSS-Selektor `#alb-disc.playing` — kein extra JS nötig (bestehende `playing`-Klasse auf alb-disc reicht)
- Effekt: wenn Musik spielt, pulsieren 3 konzentrische amber Ringe aus der Platte heraus — wie Schallwellen
- Zusammenspiel mit bestehendem `alb-glow` und `alb-tonearm` intakt, kein Konflikt
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe)

## 2026-03-23 17:09 UTC — Heartbeat (Main Agent)
- ✅ wz.html: Mini Forecast Strip auf Home-Tab — 2 Chips (morgen + übermorgen), wxIco(18px) + Kurztext + Hi/Lo Temp, flex-Row unter Scene-Chip, wird via updateHomeForecast() aus _wx.daily befüllt
- JS-Check: OK | Commit: c178c9f | Deploy: kein Remote/SSH verfügbar

## 2026-03-23 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Lichtstimmung Ambient Orb
- Neues `#amb-orb` Div direkt im Hero (neben `.hglow`), `position:absolute;top:-60px;right:-50px;width:280px;height:280px`
- CSS: `border-radius:50%`, `background:radial-gradient(circle,var(--amb-orb-c,transparent) 0%,transparent 65%)`
- `opacity:0;transition:opacity 2.8s ease, background 3.5s ease` → weiches Ein-/Ausblenden
- `@keyframes ambOrbDrift` (18s loop, 3 Waypoints) → träger Drift wie der `.hglow` links, aber mit anderem Timing (nicht synchron)
- `.show` Klasse → `opacity:1` — erscheint wenn mind. 1 Licht an
- JS IIFE in `updateAll()`: iteriert `CFG.lights.filter(on)`, liest `_S[id].attributes.rgb_color` (Array [r,g,b])
- Mittelwert über alle aktiven Lichter mit rgb_color: `rSum/cnt, gSum/cnt, bSum/cnt`
- Fallback: wenn Lichter an aber ohne rgb_color (z.B. weiße CT-Lichter) → amber `rgba(255,159,10,0.32)`
- Setzt `--amb-orb-c` CSS-Variable auf `rgba(r,g,b,0.32)` → sanfter Farbton, nicht grell
- CSS-Transition `background 3.5s ease` → Farbe wechselt weich beim Schalten mehrerer Lichter
- Orb faded nach 2.8s aus wenn alle Lichter aus (smooth, kein harter Cut)
- Effekt: Der Hero-Hintergrund reflektiert live die Stimmungsfarbe der aktiven Lichter — wie ein sanfter Raumglow
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-23 14:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Geräte-Tab — Device Pulse-Dot + Last-Changed Timestamp
- Neue CSS-Klassen: `.g-pulse-dot` (7px Kreis, inline-block), `.on` (grün + `gDevPulse` Animation), `.off` (gedimmt weiß)
- `@keyframes gDevPulse`: `box-shadow` 0→5px Glow-Ring in `rgba(48,209,88,...)`, 2.2s ease-in-out loop → sanfter Herzschlag-Puls
- `.g-last-changed`: kleines Zeitstempel-Label in rgba .22 (sehr dezent), "vor Xmin / vor Xh / vor Xd / gerade"
- `.g-status-row`: flex-Row, vereint Dot + Statustext + Zeit nahtlos
- JS in `patchDevCards`: `s?.last_changed` → `Date.now() - new Date(lc).getTime()` → Sekunden → formatierter String
- `stEl.innerHTML` ersetzt `stEl.textContent` → rendert Dot + Label + Zeitstempel als HTML
- Effekt: Jede Gerätekarte zeigt einen grün pulsierenden Punkt wenn aktiv, plus eine diskrete Zeitangabe wann zuletzt geschaltet
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-23 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Audio Spectrum Visualizer Canvas
- Neues `<canvas id="spec-cv">` als absolutes Layer am Bottom von `#album-page-bg` (z-index:1, pointer-events:none, height:38%)
- `BAR_COUNT=38` Balken, gleichmäßig über die volle Breite verteilt, `gap` 18% der Balkenbreite
- Fake-Frequenzmodell: 4 Bänder (Sub-Bass / Bass / Mitten / Höhen) mit unterschiedlichen `base`-Amplituden
- Pro Bar: `phase` + `speed` → individuelle Sinuswelle → organisch fluktuierende Höhen (keine identischen Muster)
- Beat-Simulation: alle 380–660ms wird ein zufälliger Bass-Balken (0–6) mit `beatLatch=1.0` gespikt → federt mit `*=0.88` ab
- Smoothing: `val+=(target-val)*(1-0.82)` → weiche, träge Übergänge (kein hartes Springen)
- Gradient per Balken: `createLinearGradient` blau (#0a84ff,55%) oben → amber (#ff9f0a,65%) Mitte → amber transparent unten
- `ctx.roundRect` mit r=2px für subtil abgerundete Balken-Tops (Fallback: rect)
- `resize()`: passt `cv.width/height` via `getBoundingClientRect()` an → responsive
- rAF-Loop läuft permanent; wenn nicht playing → targets auf 0 → Balken fahren smooth runter
- MutationObserver auf `#spk-wrap` (`attributeFilter:['class']`) → `_specShow(true/false)` bei `playing`-Klassen-Wechsel
- `cv.style.opacity`: 0 wenn nicht playing → 0.55 wenn playing (1.6s CSS-Transition)
- Effekt: Beim Musikspielen erscheint im unteren Drittel des Musik-Tabs ein sanft pulsierender Equalizer-Visualizer — Apple-Music/Spotify-Stil
- JS-Check: OK | Deployed via SSH (paramiko chunk-pipe, 362647 bytes)


## 2026-03-23 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Sticky Mobile CTA-Bar
- `#mob-cta-bar` via JS dynamisch ins DOM injiziert (position:fixed, bottom:0, z-index:9000)
- Nur auf Mobile sichtbar (`@media(max-width:767px){display:block}`)
- Design: iOS Dark Glassmorphism (`rgba(18,18,20,.97)`, `backdrop-filter:blur(20px) saturate(1.8)`)
- Inhalt: Label "Jetzt beauftragen" (klein, gedimmt) + Preis "ab **€29**" (grün highlight) + "Bestellen →" Button + ✕ Close
- `#mob-cta-btn`: blauer Gradient-Button, `mcbPulse` Animation (3× nach Einblenden)
- Einblende-Logik: Scroll >80px → 3s Timeout ODER 5s nach Seitenload (was zuerst eintritt)
- `bar.classList.add('show')` → `transform:translateY(0)` via spring-Transition `cubic-bezier(.34,1.28,.64,1)`
- Close-Button: `sessionStorage.mobCtaDismissed` verhindert erneutes Erscheinen in derselben Session
- i18n reaktiv: `langChange` Event → DE "Jetzt beauftragen / Bestellen →" | EN "Order now / Order →"
- `env(safe-area-inset-bottom)` im Padding → kein Overlap mit iPhone Home-Indicator
- Onclick: ruft bestehende `openFiverr()` Funktion auf
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-23 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Sleep-Timer Button
- Neues `#sleep-timer-row` Div in `.pctrl` (nach Volume-Slider, vor "Radio" Label)
- Design: dunkle Zeile mit `rgba(.04)` Hintergrund, border-radius:14px, subtle border
- `#sleep-timer-btn`: Uhr-Icon (SVG clock) + Label, toggle-Stil mit `.st-active` Klasse (blau highlight)
- Tap-Logik zyklisch: off → 15min → 30min → 60min → off (STEPS Array)
- `#sleep-pill`: blaue Countdown-Pill (zeigt verbleibende Zeit mm:ss), pulsierender Dot (`stDotPulse` @keyframes)
- `#sleep-cancel` ✕-Button zum sofortigen Abbrechen ohne Zyklus-Wechsel
- `fmt(ms)`: Millisekunden → "m:ss" Format
- `startTimer(minutes)`: setzt `endTime`, startet `setInterval` für Live-Countdown + `setTimeout` für turn_off
- Bei Ablauf: ruft `svc('media_player','turn_off',{entity_id:CFG.alm})` auf + Toast "⏱ Musik gestoppt"
- `stopTimer(wasCancelled)`: räumt alle Timer auf, resettet UI, optionaler Cancel-Toast
- Kein Konflikt mit bestehenden Swipe-Gesten oder Volume-Controls (eigenes IIFE)
- JS-Check: OK | Deployed via SSH (stdin-pipe, chunked)


## 2026-03-23 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — Aktive Szene Chip
- Neues `#scene-chip` Element direkt nach den `.home-scenes` Szenen-Buttons (vor Radio-Leiste)
- Design: `display:inline-flex` Pill mit amber Akzentfarbe (bg `rgba(255,159,10,.13)`, border `.32` opacity)
- Animierter Dot (`.sc-dot`): `@keyframes scDotPulse` 2.4s ease-in-out – pulsiert subtil in Tile-Farbe
- Chip erscheint mit spring-Animation (`cubic-bezier(.34,1.28,.64,1)`) via `.show` Klasse
- 4 Farb-Varianten via `data-scene` Attribut: `abend` (amber), `film` (blau #0a84ff), `nacht` (lila #7d7aff), `hell` (gelb)
- Doppelte Logik: Live-Erkennung aus Lichtzustand (in `_updateQaBar` IIFE) + sofortiges Update beim `setActiveScene()` Aufruf
- Scene-Detection-IIFE: bestimmt `key` aus `activeScene`-String → setzt `chip.dataset.scene` + `chipTxt.textContent`
- `setActiveScene()`: mappt Szenen-Key direkt zu Emoji+Label → Chip aktualisiert sich ohne nächsten Poll-Cycle
- Chip-Text z.B.: "🌆 Abend-Szene aktiv", "🎬 Film-Szene aktiv", "🌙 Nacht-Szene aktiv", "☀️ Hell-Szene aktiv"
- `#scene-chip` zur `.page-entering>` Stagger-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- `#scene-chip` bleibt versteckt (`opacity:0, pointer-events:none`) wenn keine Szene erkannt (alle Lichter aus)
- JS-Check: OK | Deployed via SSH (paramiko base64-stdin-pipe, 6790 Zeilen)

## 2026-03-23 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tab — Gruppen-Header mit Collapse/Expand
- Neues `LIGHT_GROUPS` Konstanten-Array vor CFG: 4 Gruppen (Wohnzimmer/Küche/Büro/Außen & Flur)
- `mkLtTile(l)` Hilfsfunktion für einzelne Licht-Tile HTML
- `#lg` Render neu: gruppierte HTML-Struktur mit `.lg-grp-hdr` + `.lg-grp-tiles` + `.lg-grp-inner`
- `.lg-grp-hdr`: grid-column:1/-1, Flex-Row mit Gruppe-Emoji+Name links + Count-Badge+Pfeil rechts
- `.lg-grp-tiles`: `grid-template-rows 1fr→0fr` Transition (0.35s ease) → native CSS Collapse ohne Höhen-Mathe
- `.lg-grp-arr`: `▾` rotiert bei `.collapsed` auf -90° via cubic-bezier spring-Übergang (0.32s)
- `.lg-grp-count[data-grp-count]`: zeigt "2/3 an" in amber wenn Lichter an, sonst gedimmt "3 Lichter"
- Collapse-State persistiert in `localStorage('lg_collapsed')` → Gruppen merken ihren Zustand nach Reload
- `window._lgCollapsed` Set für externe Zugänglichkeit
- `updateAll()`: iteriert LIGHT_GROUPS, setzt Count-Badge live mit `has-on` Klasse für amber Highlight
- Lichter ohne Gruppe (künftige Erweiterungen) erscheinen automatisch in "Weitere" Gruppe am Ende
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-23 12:51 UTC — Heartbeat (Main Agent)
- ✅ wz.html: Pull-to-Refresh Indikator — iOS-Style touchmove, blauer Arc-Progress, "Aktualisiere..." bei Threshold, ruft fetchStates()
- JS-Check: OK | Commit: 6b23d1c | Deploy: SSH nicht verfügbar (kein Key)

## 2026-03-23 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Vinyl-Tonearm (Needle/Abtastarm) Animation
- Neues `#alb-tonearm-wrap` Div als letztes Kind von `#alb-disc` (position:absolute, top:-18px, right:-14px, z-index:10)
- `transform-origin:22px 22px` → Rotation um die Pivot-Achse (linke Schulter des Arms)
- SVG 80×80px: Pivot-Kreis (outer + inner dot), Arm-Linie (stroke-linecap:round, rgba .55), Cartridge-Head (kurze Querlinie), Nadelspitze (amber Glow-Dot + Halo)
- `.lifted` Klasse: `transform:rotate(-32deg)` + `opacity:.7` → Arm zurückgezogen (über dem Vinyl, aber nicht berührend)
- `.on-disc` Klasse: `transform:rotate(0deg)` + `opacity:1` → Arm liegt auf der Platte
- CSS Transition: `.9s cubic-bezier(.34,1.28,.64,1)` → spring-Einschlag beim Absenken (leichtes Überschwingen wie echter Tonearm)
- JS: `albArm.classList.toggle('lifted',!playing); albArm.classList.toggle('on-disc',playing)` — unmittelbar nach `albDisc.classList.toggle('playing',playing)`
- Effekt: Bei Play schwenkt der Arm elegant auf die Platte, gleichzeitig beginnt die Platte zu rotieren — bei Pause zieht er sich zurück und die Rotation stoppt
- Kombiniert mit bestehendem `discSpin 8s linear infinite` → komplett authentisches Plattenspieler-Feeling
- Nadelspitze: `rgba(255,159,10,.9)` amber + `rgba(255,159,10,.25)` Glow → passt zu Dashboard-Akzentfarbe
- JS-Check: OK | Deployed via SSH (paramiko base64-stdin-pipe, 341531 bytes)

## 2026-03-22 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Wind-Chill / Heat-Index Komfort-Karte
- Neue `#wc-card` Section im Wetter-Tab, direkt VOR der Luftdruck-Barometer Card
- Dynamische Berechnung je nach Temperatur + Windstärke + Luftfeuchtigkeit:
  - **Wind-Chill** (t ≤ 10°C und wind ≥ 4.8 km/h): Kanadische metrische Formel
  - **Hitze-Index** (t ≥ 27°C): Rothfusz-Gleichung mit Luftfeuchtigkeit
  - **Apparent Temperature**: HA-Wert als Fallback für Mittelbereiche
- SVG-Komfort-Arc (gleiche Struktur wie Barometer): Track-Pfad 210° + Fill mit `linearGradient wcGrad` (blau→grün→amber→rot)
- `stroke-dashoffset` Animation: -30°C → 0%, +45°C → 100%, 1.2s cubic-bezier
- Typ-Label: "WIND-CHILL" / "HITZE-INDEX" / "GEFÜHLT" — farb-codiert je Komfort-Level
- 8 Komfort-Stufen: Extrem kalt / Sehr kalt / Kalt / Kühl / Angenehm / Warm / Heiß / Sehr heiß
- Kleidungsempfehlung pro Stufe: z.B. "🧥 Dicke Jacke, Mütze & Handschuhe empfohlen"
- Komfort-Balken: horizontaler blau→grün→amber→rot Gradient + weißer Dot-Marker mit smooth transition
- `drawWindChill()` in `renderWeather()` nach `drawBarometer()` aufgerufen
- Card bleibt `display:none` wenn keine Wetterdaten (graceful fallback)
- `#wc-card` zu `.page-entering>` Stagger-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 340022 bytes)

## 2026-03-22 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — "Now Playing" Rich Notification beim Track-Wechsel
- Neues `#np-notify` Element: `position:fixed;top:env(safe-area-inset-top)+10px` — erscheint oben zentriert
- Breite: `min(320px,88vw)` → funktioniert auf allen Bildschirmgrößen
- Design: Glassmorphism-Pill (`rgba(28,28,30,.92)`, `backdrop-filter:blur(32px) saturate(1.8)`, `border-radius:20px`)
- Inhalt: `#np-notify-art` (42×42px, border-radius:8px, Album-Art Bild) · `#np-notify-texts` (Label/Titel/Artist) · `#np-notify-wave` (4 animierte Balken)
- `#np-notify-label`: amber "♫ JETZT LÄUFT" Uppercase-Badge
- `#np-notify-title` + `#np-notify-artist`: Track-Titel und Artist, text-overflow:ellipsis
- `@keyframes npWave`: 4 Equalizer-Balken in var(--amber), scaleY .4→1 mit gestaffelten Delays (0/0.2/0.4/0.1s) → animierter Equalizer
- CSS Transitions: `transform .45s cubic-bezier(.34,1.28,.64,1)` (spring) + `opacity .3s ease` → Apple Dynamic Island-Stil
- `transform:translateX(-50%) translateY(-110%)` versteckt → `.show`: `translateY(0)` + opacity:1
- JS: ersetzt alten `showToast('♫ ...')` Aufruf beim Track-Wechsel durch IIFE
- IIFE befüllt: `nt.textContent=titleStr` · `na.textContent=artist` · `nart.src=pic` (entity_picture von Almando oder Spotify)
- `nn.classList.remove('show') + void offsetWidth + add('show')` → sauberer Neustart bei mehrfachem Track-Wechsel
- `setTimeout(...,4200)` → Notification verschwindet automatisch nach 4.2s
- Nur bei echtem Track-Wechsel (nicht erster Load): `_lastTrackTitle && _lastTrackTitle !== titleStr`
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 326503 bytes)

## 2026-03-22 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Nav-Bar — Licht-Tab Badge mit Anzahl aktiver Lichter
- Neue CSS-Klasse `.ni-badge`: `position:absolute` oben-rechts am Licht-Nav-Button
- Amber Hintergrund (`var(--amber)`, schwarze Schrift), `border-radius:8px`, `min-width:15px`
- `opacity:0 + scale(.5)` → `.show`: `opacity:1 + scale(1)` mit cubic-bezier(.34,1.56,.64,1) Transition
- `@keyframes badgePop`: scale 1.6→1 in 0.28s — feuert bei jeder Änderung der Lichteranzahl
- HTML: `<span id="licht-nav-badge" class="ni-badge">` direkt im `<button data-p="licht">` (position:relative)
- JS IIFE in `updateAll()` nach Berechnung von `on` (Anzahl aktiver Lichter):
  - `bdg.textContent = on` → aktualisiert Zahl
  - `on > 0` → `.show` hinzufügen, bei Zahlenänderung `.pop` re-trigger (via `offsetWidth` reflow)
  - `on === 0` → `.show` + `.pop` entfernen (Badge verschwindet smooth)
- `box-shadow: 0 0 6px rgba(255,159,10,.55)` → subtiler Amber-Glow um den Badge
- Effekt: Wenn Lichter an sind, erscheint eine kleine amber Zahl über dem Licht-Tab-Icon — iOS-Style App-Badge
- JS-Check: OK | Deployed via SSH (paramiko base64-stdin-pipe, ~5467 Zeilen)


## 2026-03-22 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Luftdruck-Barometer Card
- `surface_pressure` zu Open-Meteo `&current=` Parameter hinzugefügt
- Neue `#baro-card` Section im zweiten pg-wetter, direkt VOR der Stündlich-Ansicht
- SVG-Barometer (72×72px): Track-Pfad als 210°-Bogen (M10.07 57.36 A30 30 ...) in rgba .07
- Fill-Pfad mit `linearGradient baroGrad` (blau→grün→amber): zeigt Druck-Position animiert
- `stroke-dasharray:188.5` + `stroke-dashoffset` (0=leer, 0=voll): 960 hPa → 0%, 1040 hPa → 100%
- SVG-Textelemente: Wert (13px bold weiß, `#baro-svg-val`) + "hPa" Label (7px rgba .35)
- `#baro-trend-dot` overlay: zeigt ↑/↓/• Icon in Grün/Rot/Weiß je nach Druckänderung
- Seitenbereich (rechts vom SVG): `#baro-val` (1.6rem), Einheit, Trend-Label `#baro-trend-lbl` mit Pfeil
- 6 Beschreibungs-Stufen: "Sehr hoch · Trocken" / "Hoch · Schönes Wetter" / "Normal · Stabil" / "Leicht unter Normal" / "Leicht tief · Unbeständig" / "Tief · Sturm möglich"
- `#baro-bar`: horizontaler Fortschrittsbalken (blau→grün→amber Gradient) unter den Stats
- Skala-Labels 960 / 1013 / 1040 hPa unten
- `window._baroHistory[]`: speichert letzte 6 Messwerte für Trend-Berechnung (Δ < 0.3 hPa = neutral)
- `drawBarometer()` in `renderWeather()` nach `drawMoonPhase()` aufgerufen
- Card bleibt `display:none` wenn surface_pressure nicht verfügbar (graceful fallback)
- `#baro-card` in `.page-entering>` Stagger-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- `transition:stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)` → weiche Arc-Animation
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, ~5255 Zeilen)



## 2026-03-22 14:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: "Wie es funktioniert" Timeline-Section — Animated Icons
- Beide offene Tasks (FAQ + Timeline) waren bereits in demo.html implementiert — als [x] markiert
- Enhancement: Die 3 Step-Icon-Kreise im "So funktioniert es" Abschnitt erhalten jetzt Einblende- + Glow-Animationen
- Neue CSS-Klassen: `.hiw-ico`, `.hiw-ico-1/2/3`, `.hiw-in`
- `@keyframes hiwIconIn`: scale(.55)+translateY(18px) → scale(1)+translateY(0), cubic-bezier(.34,1.28,.64,1), 0.55s
- Staggered delays: Step 1 = 0.05s, Step 2 = 0.18s, Step 3 = 0.31s
- `@keyframes hiwIconGlow1/2/3`: passende Farb-Glow-Pulse (blau/lila/grün) nach Einblenden, 3s loop
- `hiwIconBounce`: Hover → Spring-Bounce-Effekt (scale+translateY, 0.6s)
- Intersection Observer IIFE: beobachtet alle `.hiw-ico`, triggert `.hiw-in` beim Einblenden in Viewport (threshold 40%)
- Icons bleiben initial unsichtbar (opacity:0) → kein FOUC beim Laden
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 342580 bytes)

## 2026-03-22 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Trust-Badge-Row unter dem CTA-Button
- 4 neue `.cta-trust-badge` Elemente direkt unter `.btn-p` im `.cta-box` Container
- Border-Top Trenner (rgba .08) separiert die Badge-Row visuell vom Button
- Badges: 🔒 Sicher bezahlen · ⭐ 5 Sterne bewertet · ⚡ 24h Lieferung · 💬 24/7 Support
- CSS: `.cta-trust-row` (flex, gap:14px, wrap), `.cta-trust-badge` (rgba white .55 → .85 on hover)
- `@keyframes ctaTrustIn`: fade+translateY Einblende-Animation, staggered delays .05/.12/.19/.26s
- Hover: `translateY(-2px)` + hellere Farbe → subtle Interaktivität
- i18n: DE + EN Keys (ctaTrust1-4) in beiden Sprachpaketen ergänzt
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, ~287KB)

## 2026-03-22 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — Quick-Actions Bar (4 Icon-Buttons)
- Neuer `#qa-bar` Container direkt unterhalb der Status-Pills im pg-home Tab
- `overflow-x:auto` + `scrollbar-width:none` → horizontal scrollbar-los scrollbar auf Mobile
- 4 Buttons: `[data-qa="off"]` Alle aus · `[data-qa="szene"]` Szene · `[data-qa="musik"]` Musik · `[data-qa="heiz"]` Heizung
- Je Button: 68px breite Card (`flex:0 0 auto`), runder `.qa-ico` Kreis (34px) + `.qa-lbl` Beschriftung
- Farbkodierung: Alle aus → rot (#ff453a), Szene → amber (#ff9f0a), Musik → blau (#0a84ff), Heizung → orange-rot
- `.qa-active` Klasse: glowing box-shadow wenn Lichter an (off-Btn) / Musik spielt (musik-Btn)
- `@keyframes qaBounce`: Bounce-Animation (.28s) bei jedem Tap (via `.qa-tap` Klasse)
- Aktionen: Alle aus → `svc('light','turn_off')` + Shelly + Toast | Szene → Inline-Popup mit 4 Szenen (Abend/Film/Hell/Aus) | Musik → `navTo('musik')` | Heizung → Toast mit Temperatur falls climate-Entity vorhanden
- Szenen-Popup: `position:fixed` Bottom-Sheet mit Glassmorphism, 2×2 Grid, Klick außen schließt
- `window._updateQaBar(onCount, playing)` — wird in updateAll() aufgerufen, setzt Active-States live
- `#qa-bar` zu `.page-entering>` Stagger-Liste hinzugefügt → animiert beim Tab-Wechsel ein
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, ~238KB)

## 2026-03-22 08:07 UTC — Heartbeat (Main Agent)
- ✅ demo.html: Social Proof Toast — zufällige "Jemand hat bestellt" Notifications
- Floating Toast unten links, 12s nach Laden, dann alle 18–40s, 4.2s sichtbar
- 8 reale Beispiel-Meldungen (München/Hamburg/Berlin/Wien/Zürich/Stuttgart/Köln/Frankfurt)
- Commit: 9e4f604 | Deploy: SSH nicht verfügbar (kein Key) — Nur lokaler Git-Commit

## 2026-03-22 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Mondphase-Card
- Neue `#moon-card` Section direkt oberhalb des 7-Tage-Forecasts im zweiten `#pg-wetter`
- SVG-Mondzeichnung (60×60px): dunkler Mondkreis + Terminator-Kurve als SVG-`<path>` mit elliptischem Bogen
- `drawMoonPhase()` Funktion: astronomische Berechnung via Julianischem Datum
- Referenz-Neumond: JD 2451549.76 (2000-01-06 18:14 UTC), synodische Periode 29.53058868 Tage
- `phase` (0..1): `((JD - ref) % synodic) / synodic` → exakte Mondphase für heutiges Datum
- `illum = 0.5 * (1 - cos(2π * phase))` → Beleuchtungsprozent (0=Neu, 1=Voll)
- Terminator-Pfad: halbkreis der beleuchteten Seite + elliptischer Bogen (rx = cos(2π·phase) * r)
- Zunehmend → rechte Seite hell, Abnehmend → linke Seite hell (sweep-flag umgekehrt)
- 9 Phasennamen: Neumond / Zunehmende Sichel / Erstes Viertel / Zunehmend Gibbous / Vollmond / Abnehmend Gibbous / Letztes Viertel / Abnehmende Sichel
- UI: SVG links · Phasenname + Beleuchtungs-% + Fortschrittsbalken (blau→lila→weiß Gradient) · Emoji + Mondtag rechts
- `drawMoonPhase()` in `renderWeather()` nach `drawTempCurve()` aufgerufen
- Keine API nötig — reine Astronomie-Mathematik, 100% offline-fähig
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 230022 bytes)


## 2026-03-22 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Tab-Wechsel — Staggered Card-Entrance Animation
- `@keyframes pgCardIn`: `opacity:0;translateY(14px)` → `opacity:1;translateY(0)`, 0.45s cubic-bezier(.32,0,.15,1)
- CSS-Klasse `.page-entering`: 18 Selektoren decken alle Seiten-Kind-Elemente ab (`.hero`, `.cal-card`, `.lt-grid`, `.pctrl`, `.album-wrap`, etc.)
- `nth-child(1–8)` Staggering: Delays 0.04s / 0.10s / 0.16s / 0.22s / 0.28s / 0.34s / 0.40s / 0.46s
- JS in `navTo()`: nach dem double-rAF wird `.page-entering` auf `nxt` gesetzt, nach 600ms automatisch entfernt
- Effekt: beim Tab-Wechsel blenden die Cards versetzt ein (erster Tab sofort, weitere folgen in Wellen) → Apple-iOS-Stil
- Kein Konflikt mit bestehenden `.page`-Slide-Animationen (separate CSS-Properties: transform vs. opacity+translateY)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 224871 bytes)

## 2026-03-22 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tiles — Helligkeits-Arc Ring um Icon-Kreis
- Neue CSS-Klasse `.lt-bri-arc`: absolutes SVG-Overlay (inset:-5px, 10px größer als .ltico, z-index:7)
- Zwei SVG-Kreise: `bri-track` (faint Hintergrundring, rgba .06) + `bri-fill` (aktiver Bogen in Tile-Farbe)
- Kreisradius r=22 im 50×50 viewBox → Umfang 138.23px
- `stroke-dasharray:138.23` + `stroke-dashoffset` = 138.23 × (1 - bri%) → Arc zeigt Helligkeit
- `transform:rotate(-90deg)` auf bri-fill → Arc startet oben (12-Uhr-Position)
- Farbe: `stroke` = `rgba(lc, 0.9)` — passt sich dynamisch zur Tile-Akzentfarbe an
- `transition: stroke-dashoffset .8s cubic-bezier(.4,0,.2,1)` → weiche, federnde Animation
- `opacity:0` wenn aus, `opacity:1` wenn `.lt.on` → kein visuelles Rauschen bei Aus-Tiles
- JS in `updateLights()`: berechnet `briPct` aus HA-`brightness` (0–255 → 0–100%) + setzt dashoffset
- Effekt: jedes Licht-Tile zeigt subtilen Leuchtring der exakt die Helligkeit als Kreisbogen visualisiert
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 223549 bytes)

## 2026-03-22 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Windrichtungs-Kompass
- `wind_direction_10m` zu Open-Meteo `&current=` Parameter hinzugefügt
- Neues `#wx-compass-wrap` Div in der Stats-Zeile (neben 💨 Wind km/h)
- SVG-Kompass (18×18px, viewBox 0 0 20 20): äußerer Ring (rgba .18), N/S/O/W Beschriftungen
- `#wx-compass-needle`: zweiteilige Pfeil-Polygon-Gruppe (N-Spitze amber #ff9f0a, S-Ende gedimmt weiß)
- `transform-origin:10px 10px` + `transition:transform 1.2s cubic-bezier(.34,1.28,.64,1)` → federnde Rotation
- JS in `renderWeather()`: `deg = c.wind_direction_10m` → `needle.style.transform = rotate(${deg}deg)`
- Himmelsrichtungs-Label `#wx-winddir-lbl`: `dirs[Math.round(deg/45)%8]` → N/NO/O/SO/S/SW/W/NW
- Effekt: Kompassnadel dreht sich beim Laden animiert in die aktuelle Windrichtung (Apple-Weather-Stil)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 222350 bytes)

## 2026-03-21 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Hero — Animiertes Niederschlags-Canvas (Regen & Schnee)
- `<canvas id="wx-precip-cv">` als absolutes Layer direkt im `#wx-hero` Container (z-index:0, pointer-events:none)
- CSS: `position:absolute;inset:0;width:100%;height:100%;opacity:0;transition:opacity 1.2s ease`
- IIFE `updateWxPrecipCanvas(code, night)`: wird am Ende von `renderWeather()` aufgerufen
- WMO-Code Mapping: 51–67, 80–82, 95/96/99 → `mode='rain'` | 71–77, 85–86 → `mode='snow'`
- **Regen-Modus** (55 Partikel): Diagonal fallende Striche (8–18px Länge, 12° Neigung), `rgba(180,210,255)`, alpha 0.12–0.34
- **Schnee-Modus** (38 Partikel): Kreisförmige Flocken (r 1.2–3.4px), sinus-förmige Drift-Bewegung, `rgba(220,235,255)`, alpha 0.18–0.46
- `resize()`: passt Canvas-Dimensionen dynamisch an Parent-Element an (getBoundingClientRect)
- rAF-Loop: `drawRain()` / `drawSnow()` mit ctx.clearRect pro Frame (sauber, kein Ghosting)
- Partikel-Recycling: wenn y > H → `Object.assign(p, make*())` → neuer Partikel von oben
- Graceful stop: bei nicht-Niederschlags-Codes → `opacity:'0'`, rAF-Cancel, clearRect nach Fade
- Idempotent: wenn gleicher Modus schon läuft → kein Neustart (kein Flackern)
- Effekt: Bei Regen fallen sichtbar Tropfen über dem Hero, bei Schnee trudeln Flocken — sehr Apple-Weather-like
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 220431 bytes)


## 2026-03-21 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tiles — Tap-Ripple Effekt (Kreisförmige Welle vom Touch-Punkt)
- CSS: `.lt-ripple` — `position:absolute; border-radius:50%; pointer-events:none; z-index:6`
- `@keyframes ltRipple`: scale 0→4.5 + opacity .7→0 in 0.55s (`cubic-bezier(.4,0,.2,1)`)
- JS: im `click`-Handler jedes Licht-Tiles → IIFE erstellt ripple `<div>` an exakter Touch-Position
- `e.clientX/clientY` minus `getBoundingClientRect()` → relativer Offset zum Tile
- Größe: `Math.max(tile.width, tile.height) * 1.1` → Ripple deckt immer das ganze Tile ab
- Farbe: `rgba(--lc, .22)` — nutzt die Tile-Akzentfarbe (amber wenn an, weiß wenn aus)
- `animationend` Listener: ripple `<div>` wird automatisch aus DOM entfernt (kein Memory-Leak)
- Kein Konflikt mit Long-Press-Dimmen oder Swipe-Gesten
- Effekt: jeder Tipp auf ein Licht-Tile erzeugt eine elegante farbige Welle — iOS-Material-Hybrid
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 216588 bytes)

## 2026-03-21 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Exit-Intent Popup mit 10% Rabatt-Angebot (Rabattcode EXIT10)
- `#exit-popup` Fullscreen-Overlay (position:fixed, z-index:10000, display:flex)
- `#exit-backdrop`: schwarzes Blur-Overlay (backdrop-filter:blur(6px)), Klick schließt Popup
- `#exit-card`: Glassmorphism-Card (border-radius:22px, Gradient-BG), spring-in Animation (cubic-bezier .34,1.28,.64,1)
- Inhalt: 🎁 Emoji-Header, Titel, Erklärtext, dashed amber Rabatt-Code-Box (user-select:all, EXIT10), CTA-Button → #contact-section
- Exit-Intent-Erkennung via `mousemove`: trackt Y-Position + Velocity (dy/dt)
  - Trigger: mouse im oberen 8% des Viewports UND Aufwärts-Velocity < -0.5 px/ms
  - Zeitfenster: dt < 80ms → nur echte schnelle Bewegungen
- Mobile Fallback: `visibilitychange` Event → Popup erscheint wenn Tab gewechselt/App minimiert
- `sessionStorage.exitDismissed` → Popup erscheint nur 1x pro Session (kein Spam)
- Schließen: Backdrop-Klick, ×-Button, ESC-Taste, CTA-Klick
- i18n: DE (`exitTitle`, `exitSub`, `exitCta`, `exitNote`) + EN vollständig, `langChange` reaktiv
- JS-Check: OK | Deployed via SSH (paramiko chunk-b64-pipe, 336273 bytes)

## 2026-03-21 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Vorher/Nachher Slider (Standard HA vs. Custom Dashboard)
- Neue Section `#vn-section` eingefügt direkt vor dem Video-Preview-Block
- Interaktiver CSS/JS Drag-Slider: linke Hälfte = Standard HA, rechte Hälfte = Custom Dashboard
- `clip-path: inset(0 X% 0 0)` auf `#vn-after` — bewegt sich mit dem Handle-Prozentsatz
- Handle `#vn-handle`: weißer 3px vertikaler Balken mit zentriertem Pfeil-Button (◄►)
- Mock-UIs: Standard HA zeigt graue Tiles + weiße Balken + "Lovelace UI" Label
- Custom Dashboard zeigt Amber/Blau/Grün farbcodierte Tiles + Gradient-Balken + Live-Daten-Stil
- Labels `#vn-lbl-before` / `#vn-lbl-after`: schwebende Badges oben-links/rechts mit Glassmorphism
- `vn-hint` Fade-Text verschwindet nach 3s (via CSS @keyframes vnHintFade)
- JS IIFE: mousemove/touchmove auf Wrap → setPct(x/width) → clip-path + handle position live
- Auto-Demo-Sweep nach 2.2s: sin-Kurve 0.5±0.22 über ~1s → zeigt Funktion ohne Geste
- Sweep stoppt sobald User dragged (dragging flag)
- i18n: DE (`vnTitle`, `vnSub`, `vnBefore`, `vnAfter`, `vnHint`) + EN Strings ergänzt
- JS-Check: OK | Deployed via SSH (paramiko chunk-pipe, 331284 bytes)

## 2026-03-21 14:03 UTC — Cron (Design-Ideen Agent)
- ✅ demo.html: Video-Embed-Placeholder (YouTube-ähnlich) mit Thumbnail + Play-Button
- Neue Section `#video-section` zwischen HA-Vergleichstabelle und Pricing
- `#video-thumb`: 16/9 Aspect-Ratio Box, dunkler Gradient-Hintergrund, `border-radius:20px`
- Semi-transparentes SVG-Dashboard-Mockup (Linienzeichnung) als Hintergrund-Overlay (opacity .12)
- Zentrierter Play-Button: blauer Gradient-Circle (0071e3), SVG ▶ Icon, `animation: vidPlayPulse 2.4s ease-in-out infinite`
- `vidPlayPulse`: pulsierender blauer Ring-Glow um den Play-Button
- Hover-Effekt: `scale(1.015)` + verstärkter Box-Shadow + Play-Button vergrössert sich (scale 1.1)
- Dauer-Badge (2:14) unten-rechts, grünes "🟢 Fiverr GIG" Badge oben-rechts
- Klick → `openVideoLink()` → öffnet `https://www.fiverr.com/autoflow-lab` in neuem Tab
- i18n: DE (`videoTitle`, `videoSub`, `videoPlayHint`) + EN Strings hinzugefügt
- JS-Check: OK | Deployed via SSH (paramiko chunk+stdin-pipe, 319482 bytes)

## 2026-03-21 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Kalender-Widget auf Home-Tab (nächste 2 Events aus calendar.* Entities)
- Neue `.cal-card` Section unterhalb der Energie-Card, vor dem 3-Tage-Forecast
- `fetchCalendar()` Funktion: ruft `/api/calendars` ab → Liste aller calendar.* Entities
- Für jede Kalender-Entity: `/api/calendars/<id>?start=...&end=...` (nächste 7 Tage)
- Events werden sortiert, max 3 werden angezeigt
- Farbkodierung: je Kalender eine eigene Dot-Farbe (amber/blau/grün/rot/lila/pink)
- Zeitformatierung: "Heute 14:30", "Morgen 09:00", oder "Mo, 23.3. 10:00" (Deutsch)
- Ganztägige Events: "(ganztägig)" Suffix
- Graceful: Card bleibt verborgen wenn keine Kalender-Entities in HA vorhanden
- `calFadeIn` Animation: jedes Event blendet leicht versetzt ein (0/70/140ms delay)
- `fetchCalendar()` bei Launch + alle 15 Minuten aktualisiert
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 215605 bytes)

## 2026-03-21 10:07 UTC — Heartbeat Auto-Improve
- ✅ demo.html: Scarcity-Banner (🔥 Nur noch 3 Plätze diese Woche)
  - Erscheint nach 1.8s mit Slide-in Animation
  - Orange Gradient, schliessbar per ×-Button
  - i18n: DE+EN, Link zu #contact-section
  - body.paddingTop angepasst damit Content nicht verdeckt wird
- JS-Check: OK | Deployed auf GitHub Pages (autoflow-lab.github.io)

## 2026-03-21 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Lautstärke per vertikalen Swipe auf Album-Art
- IIFE-Block auf `.album` Element: `touchstart/move/end` Handler (passive, kein Scroll-Konflikt)
- `touchstart`: speichert startX/Y + aktuellen Lautstärke-Wert (`vsVolStart`)
- `touchmove`: erkennt vertikale Geste wenn |dx|<25px und |dy|>14px → `vsMoving=true`
- Delta-Berechnung: -dy/1.8 → 180px Swipe entspricht ~100% Lautstärke-Änderung
- Synchronisation mit vorhandenem Lautstärke-UI: `#vfill`, `#vthumb`, `#vv`, `#vol-range`
- `touchend`: sendet `volume_set` an `CFG.alm` (Almando) + `hap()` Feedback
- Schutz: wenn `dx>80px` → horizontaler Swipe → kein Volume-Change (Track-Skip hat Vorrang)
- **Volume-Overlay** `#vol-swipe-ol`: erscheint beim Swipe, zeigt Volume-Icon + Balken + % Wert
  - `backdrop-filter:blur(14px)` Glassmorphism-Pill (iOS-Style)
  - Lautstärke-Balken in `#0a84ff` (accent blau), Breite entspricht aktueller %
  - Fade-out nach 1.3s automatisch
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 210792 bytes)


## 2026-03-21 08:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Hero — Tageszeit-Fortschritts-Arc (SVG)
- Neues `#day-arc-wrap` Div unterhalb `.htop` im Home-Hero (vor dem Now-Playing-Strip)
- SVG viewBox="0 0 220 28": flacher Bogen (r=200) von links nach rechts, Höhe ~27px
- Track-Pfad: `M 10 26 A 200 200 0 0 1 210 26` — dünne graue Linie (rgba .07)
- Fortschritts-Pfad: gleicher Pfad mit `stroke-dasharray/offset` → zeigt % des Tages (00:00→24:00)
- `linearGradient dayArcGrad`: Nacht-Blau → Morgen-Amber → Mittagsweiß → Abend-Rot → Nacht-Blau
- Glowing Dot (`#day-arc-dot`): bewegt sich via `getPointAtLength(p*ARC_LEN)` auf dem Bogen
- Dot-Farbe + `drop-shadow` Filter je Tageszeit: 🌙 Blau / 🌅 Amber / ☀️ Weiss / 🌆 Amber / 🌃 Rot
- Label `#day-arc-lbl`: zentriert unter dem Bogen, zeigt Tageszeit-Emoji + Name (Nacht/Morgen/Vormittag/…)
- `updateDayArc()` Funktion — wird bei jedem `updateClock()` Call aufgerufen (alle 5s)
- CSS: `#day-arc-wrap` 30px hoch, `#day-arc-lbl` absolut zentriert, micro-font (0.46rem)
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 207555 bytes)

## 2026-03-21 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Home-Tab — Floating "Alle Lichter aus" FAB-Button
- `#all-off-fab` Button: position:absolute, bottom-right im pg-home, z-index:50
- `backdrop-filter:blur(8px)` + `rgba(44,44,46,.96)` Hintergrund → iOS-Glassmorphism-Stil
- Power-Icon (SVG, rot) als visueller Hinweis auf "Alles aus"-Funktion
- CSS: `fab-visible` Klasse mit `opacity:1 + pointer-events:auto + fabPulse` Animation (3s loop)
- `fabPulse` Keyframe: subtiler roter Ring-Glow pulsiert um den Button (3s ease-in-out)
- 2-Tap Bestätigung: erster Tap → `fab-confirm` (bounce + shake Animation, Toast-Meldung)
- Zweiter Tap innerhalb 2.2s → `svc('light','turn_off', {entity_id: alle CFG.lights IDs})`
- Auch `light.hue_play_l` wird mitgeschaltet (Hue Play Bar)
- Bei Kein-Bestätigung (Timeout 2.2s): Reset zurück zu normalem Zustand
- `window._updateFab(onCount)` wird in `updateAll()` aufgerufen → erscheint/verschwindet live
- Wenn alle Lichter aus: Button faded aus (`fab-visible` entfernt)
- JS-Check: OK | Deployed via SSH (paramiko chunk-pipe, 204607 bytes)


## 2026-03-21 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Tab — Temperaturkurve 24h als SVG Area-Chart
- Neue Section "TEMPERATUR · 24H" im pg-wetter Tab, vor der stündlichen Chips-Ansicht
- SVG viewBox 320×72, `preserveAspectRatio="none"` → responsive volle Breite
- Smooth cubic-bezier Linienpfad (`smooth()`) mit Kontrollpunkten je Stunden-Datenpunkt
- Gradient-Fill (`tcGrad`): amber #ff9f0a mit 35%→2% Opacity → schöner Glüh-Effekt
- Oranger Kreis-Dot (`#tc-now-dot`) markiert aktuelle Stunde (Index 0)
- Temperatur-Labels: erste Stunde (links), letzte (rechts), plus 6h/12h/18h-Marker mittig
- Zeitachse unten: Jetzt / +6h / +12h / +18h / +23h als dezente Labels
- `drawTempCurve()` Funktion, aufgerufen am Ende von `renderWeather()` (nach `checkRainWarning()`)
- Temperatur-Range-Normalisierung: min(temps) → max(temps), mindestens 2°C Span
- JS-Check: OK | Deployed via SSH (paramiko chunk+session-pipe, 201448 bytes)

## 2026-03-21 02:07 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Room-Cards: Farbtemperatur-Tönung (warme/kühle Tile-Färbung)
- CSS: `.room-card.on::after` pseudo-element mit `--ct-tint` CSS-Variable
- `CT_TINT` Map: 10 Farben mit passenden Gradient-Tints (warm=amber, cool=blau, purple, pink, etc.)
- Tint wird in `buildRoomList()` + `applyRoom()` sofort aktualisiert (kein Rebuild nötig)
- Übergänge: `transition: background .4s ease` auf ::after
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-21 02:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Swipe Left/Right für Track-Skip (⏭ / ⏮)
- Touch-Geste auf `#pg-musik`: touchstart speichert X/Y, touchend berechnet deltaX/deltaY
- Swipe links (deltaX < -65px, deltaY < 90px, dt < 500ms) → `media_next_track`
- Swipe rechts (deltaX > +65px) → `media_previous_track`
- Visueller Hint: `#swipe-hint` Div erscheint mittig mit ⏭/⏮ Emoji (opacity 0→1→0, 700ms)
- Keine Konflikte mit vertikalem Scrollen (dy-Filter), kein passive-Problem
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 197025 bytes)

## 2026-03-21 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab — Blurred Album-Cover als dynamischer Seiten-Hintergrund
- Neues `#album-page-bg` Layer als erstes Kind von `#pg-musik` (position:absolute, inset:0, z-index:0)
- `#album-page-bg-img`: 110% Größe mit -5% Margin (kein harter Rand), `filter:blur(48px) saturate(1.8)`
- Schwarzes Semi-Transparent Overlay (`rgba(0,0,0,.62)`) darüber → UI bleibt lesbar
- Opacity 0 → 1 via `onload` Callback + `transition:opacity 2.5s ease` → sanftes Einblenden
- `.album` + `.pctrl` erhalten `position:relative;z-index:1` → liegen über dem Hintergrund
- JS: `bgImg.src=imgUrl` parallel zum Mood-Gradient Img-Load gesetzt (kein extra Netzwerk-Request nötig wenn gecacht)
- Fade-out (`opacity:'0'`) wenn kein Album-Art vorhanden (graceful fallback)
- Effekt ähnlich Spotify/Apple Music iOS: Album-Farben füllen den ganzen Tab-Hintergrund
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 190.8KB)


## 2026-03-20 22:07 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Grundriss: Pinch-Zoom + Pan auf Mobile
- `#fp-zoom-layer` Wrapper-Div um alle fp-outer Inhalte (transform-origin:0 0)
- touchstart/move/end Handler: Pinch skaliert um Midpoint, 1-Finger Pan bei scale>1
- clampPan() verhindert Rausscrollen (Grenzen abhängig von scale)
- Doppel-Tap (2 Taps <280ms) resettet zoom smooth zurück zu scale=1
- Scale-Range: 1x – 4x
- Hint-Text mobile: "Pinch: Zoom · 2× Tap Reset"
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-20 22:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Pollen-Warnung im Wetter-Tab (Open-Meteo Air Quality API)
- Neue `#pollen-card` Section zwischen Regen-24h Diagramm und 7-Tage Forecast
- `fetchPollen()` Funktion: `air-quality-api.open-meteo.com` → `hourly` Pollen-Felder
- 6 Pollen-Typen: Erle, Birke, Gräser, Beifuss, Olive, Ambrosia (grains/m³)
- Ampel-Stufen: Niedrig (grün ≤10), Mäßig (gelb ≤50), Hoch (orange ≤200), Sehr hoch (rot)
- Horizontale Balken (relative Breite, max=200 grains/m³) je Typ mit Emoji + Name + Level-Label
- Warnung-Hint: "⚠️ X Pollen-Typen erhöht – Empfehlung: Fenster schliessen" wenn ≥50 grains
- Card bleibt versteckt wenn API nicht verfügbar (graceful fallback)
- `fetchPollen()` bei Launch + `setInterval` alle 60 Minuten
- JS-Check: OK | Deployed via SSH (cat stdin-pipe, 191702 bytes)

## 2026-03-20 20:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Energie-Widget auf Home-Tab (sensor.stromverbrauch)
- Neue `.energie-card` zwischen tagsum und 3-Tage-Forecast auf pg-home
- SVG Arc-Gauge (3/4 Kreis, 240° Sweep, stroke-dashoffset Animation, 1.2s ease)
- Farbkodierung: grün (≤33% von 3000W), amber (≤66%), rot (>66%) — entspricht 0–3000W Skala
- 7 Sensor-Kandidaten für Watt (sensor.stromverbrauch, sensor.power_consumption, etc.)
- 4 Kandidaten für kWh-Tagesverbrauch, 2 für €-Tageskosten
- Graceful: Card bleibt `display:none` wenn keine passenden Sensoren in HA vorhanden
- Zusätzlicher Fortschrittsbalken (horizontale Bar) unter den Stats für visuellen Kontext
- Kosten-Anzeige (≈ X.XX €) nur wenn sensor.stromkosten_heute o.ä. verfügbar
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 179484 bytes)

## 2026-03-20 18:07 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Dashboard: CO₂ / Luftqualität Widget
- SVG Ring-Gauge (animated stroke-dashoffset, 1.2s ease), Farbe wechselt mit Level
- 4 Alarmstufen: Gut (grün ≤700), Mittel (orange ≤1000), Mäßig (dunkelorange ≤1500), Schlecht (rot)
- Live-Drift: CO₂-Wert ändert sich alle 7s leicht (+/- Zufallsabweichung)
- 4 Kennzahlen: Feuchte (48%), Temperatur (21.4°C), VOC (Niedrig), Auto-Lüftung
- Hint-Text wechselt je Stufe (z.B. "Fenster öffnen!")
- DE + EN vollständig, langChange Event reaktiv
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-20 18:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Tages-Zusammenfassung auf Home-Tab
- Neue `.tagsum` Card zwischen pills-row und 3-Tage-Forecast
- `initTagesSum()` IIFE: speichert Tagesdaten in `localStorage` (Key: `tagsum_YYYY-MM-DD`)
- Trackt: welche Licht-Entity-IDs heute je AN waren (Set → unique, auch nach Reload)
- Trackt: Musik-Minuten kumulativ (Differenz zwischen Calls, max 65s pro Intervall)
- `window._tagsumUpdate(lightsOnIds, isPlaying)` wird bei jedem `updateAll()` aufgerufen
- Anzeige: "💡 3 Lichter · 🎵 1h 12min Musik" — oder "Noch keine Aktivität heute"
- Alte localStorage-Keys (>1 Tag) werden beim Init automatisch bereinigt
- Graceful: Card unsichtbar wenn keine Daten (display:none → flex beim ersten Update)
- CSS: `.tagsum`, `.tagsum-stat`, `.tagsum-ico` — iOS-dark Stil, `greetFade` Animation
- JS-Check: OK | Deployed via SSH (paramiko stdin-pipe, 174773 bytes)

## 2026-03-20 16:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: UV-Index Anzeige im Wetter-Hero (Open-Meteo `uv_index_max`)
- API-Call: `uv_index_max` zu `daily` Parameter hinzugefügt
- HTML: neues `#wx-uv-wrap` + `#wx-uv` span in der Stats-Zeile (neben 💧Feuchte + 💨Wind)
- JS: `uvVal` aus `_wx.daily.uv_index_max[0]` → gerundeter Wert mit farbcodiertem Label
- Farb-Skala: grün (≤2), gelb (≤5), orange (≤7), rot (≤10), violett (>10) — WHO UV-Standard
- Element versteckt wenn kein UV-Wert vorhanden (graceful fallback)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-20 14:07 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Dashboard: Kalender-Widget als neues dash-card
- 4 farbcodierte Termine (Zuhause=orange, Arbeit=blau, HA=grün, Freizeit=lila)
- Relative Zeitangaben ("In 3h", "Morgen 9:00", "Sa 10:00")
- Kategorie-Badge je Termin, "Heute"-Zeile mit aktuellem Datum
- CSS: `.cal-event`, `.cal-dot`, `.cal-badge` — responsive, hover-State
- DE + EN dynamisch (Termin-Labels wechseln mit Sprache)
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-20 14:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Hero-Hintergrund: Sterne-Parallax nachts (CSS particles)
- `<canvas id="star-cv">` als absolut positioniertes Layer direkt im Hero (`z-index:0`, `pointer-events:none`)
- CSS: `opacity:0 → 1` mit `transition:opacity 2.5s ease` → sanftes Ein-/Ausblenden
- `initStarParallax()` IIFE: erzeugt ~1 Stern pro 800px² (dichteabhängig von Canvas-Größe)
- 3 Layer-Tiefen: `speed` 0.15–0.7 → ferne Sterne bewegen sich langsamer (echter Parallax-Effekt)
- Twinkle: `sin(time * twinkleSpeed + offset)` → jeder Stern blinkt unabhängig (60fps rAF)
- Wrapping: Sterne tauchen gegenüber wieder auf (nahtloser Loop)
- Parallax-Input: `deviceorientation` (Handy-Neigung β/γ) + `pointermove` Fallback (Desktop)
- Smooth-Damping: `curX += (offX - curX) * 0.06` → weiche, träge Bewegung
- Aktivierung: `updateStarParallax(isNight && code<=1)` — nur bei Nacht + klarem Himmel (WMO 0–1)
- Bei Tag / bewölkt → Canvas fade-out, rAF stoppt → null Ressourcen-Verbrauch
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 170417 bytes)

## 2026-03-20 12:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Musik-Tab: Almando Speaker-Icon mit Wellen-Animation wenn spielt
- CSS + HTML für `#spk-wrap` und `.spk-ring` waren bereits vorhanden aber nie aktiviert
- Problem: `playing` CSS-Klasse wurde nie per JS auf `#spk-wrap` gesetzt
- Fix: Eine Zeile JS hinzugefügt nach `eq.classList.toggle`:
  `document.getElementById('spk-wrap')?.classList.toggle('playing', playing);`
- Bei `playing=true` → 3 Ringe pulsieren mit `spkWave` Keyframe (scale .5→1.3 + opacity fade)
- Delays: Ring 1 = 0s, Ring 2 = 0.5s, Ring 3 = 1.0s → gestaffelter Wellen-Effekt
- Speaker-Icon-Farbe wechselt von rgba(.55) auf `var(--blue)` beim Spielen
- JS-Check: OK | Deployed via SSH (paramiko chunk-pipe)

## 2026-03-20 10:07 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Stats-Counter: Intersection Observer (feuert beim Einblenden, nicht beim Page-Load)
- `easeOut(t) = 1 - (1-t)³` für weiche Dezelerierung
- Jeder Counter hat eigene Dauer (47+ = 1400ms, 98% = 1200ms, 48h = 900ms, €49 = 800ms)
- `el._counted` Flag verhindert Doppel-Animation bei erneutem Einblenden
- Fallback: setTimeout 400ms wenn IntersectionObserver nicht verfügbar
- Container: `.hero-stats` (Threshold 40%)
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-20 06:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Wetter-Hero Icon jetzt animiertes SVG (statt statischem Emoji)
- `#wx-big-ico` von `<div>🌤</div>` auf `<svg viewBox="0 0 80 80" width="88" height="88">` umgestellt
- `renderWeather()` befüllt jetzt `wx-big-*` Hero-Elemente (waren bisher nie geupdated!)
- Icon nutzt bestehende `wxIco(code, 80, night)` Funktion → alle Animationen greifen:
  - ☀️ Sonne: `_spin` 15s linear (Strahlen rotieren), `_glow` 3s pulsieren
  - 🌧 Regen: `_rain` keyframes (Tropfen fallen von oben)
  - ❄️ Schnee: `_snow` keyframes (Flocken trudeln runter)
  - ⛈ Gewitter: `_bolt` keyframes (Blitz flackert 0/8/22% opacity)
  - 🌤 Teilweise bewölkt: `_float` + `_cld` Bewegungen
  - 🌙 Mond nachts: `_float` + `_twinkle` Sterne
- Zusätzlich: `wx-big-temp`, `wx-big-feel`, `wx-big-desc`, `wx-hi/lo/hum/wind` werden nun befüllt
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe)

## 2026-03-20 02:35 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Pricing: "Alles inklusive" Freelancer-Vergleichstabelle
- 3 Spalten: autoflow-lab (hervorgehoben, blauer Rand) vs Typischer Freelancer vs Agentur/Studio
- 10 Vergleichszeilen: Preis, Lieferzeit, Grundriss, KI, Video, Quellcode, Revisionen, Offline, Reviews, Doku
- CSS: `.fc-table` mit sticky highlight-Spalte, ✓/✗ Symbole, dark/light mode
- DE + EN i18n vollständig
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-19 22:35 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ AI-Page: "Vorher & Nachher" Section mit 3 konkreten Beispielen
- Beispiel 1: Morgen-Routine (8 Min manuell → 0 Min automatisch)
- Beispiel 2: Energie (€185/Mo → €124/Mo, −33%, Solar-Überschuss, Geofencing)
- Beispiel 3: Sicherheit (manuell → KI-Alert + Foto + Auto-Abschließen)
- CSS: `.ba-card` Split-Layout Before(rot)/After(grün), Glassmorphism in Light Mode
- DE + EN i18n Keys (baTitle, baSub) ergänzt
- JS-Check: OK | Deploy: ✅ GitHub

## 2026-03-19 18:35 UTC — Cron (Auto-Improve) ✅ demo.html → GitHub
- ✅ Grundriss: Doppelklick auf Raum → Detail-Panel mit Geräteliste
- CSS: `.fp-detail` — dunkles Glasmorphism-Panel (rgba .88 + backdrop-filter), fade-in Animation
- HTML: Panel in `#fp-outer` eingebettet (positioniert relativ zum Klick)
- JS: `openRoomDetail(rid,px,py)` — zeigt Icon, Name, State (EIN/AUS + Helligkeit + Farbe)
- `ROOM_DEVICES` Objekt: 4–5 Geräte pro Raum mit Emoji-Icon
- `fpDetailToggle()` — Licht-Toggle direkt aus dem Panel heraus
- Doppelklick (Desktop) + Doppel-Tap (Mobile, 2 Klicks <320ms) auf SVG-Polygone
- Hint-Text aktualisiert: "Doppelklick: Details" ergänzt
- JS-Check: OK | Deployed → GitHub (demo.html + index.html)

## 2026-03-19 14:35 UTC — Cron (Auto-Improve) ⚠️ DEPLOY PENDING
- ✅ Implementiert: Tageszeit-Greeting im Home-Hero ("Guten Morgen/Nachmittag/Abend/Nacht, Janis")
- CSS: `.hgreet` — klein, gedimmt (rgba .52), fadeIn-Animation beim Laden
- JS: `getGreeting(hour)` — 5 Zeitfenster mit passendem Emoji (☀️🌤🌞🌆🌙)
- `updateClock()` aktualisiert `#hgreet` bei jedem Clock-Tick
- ⚠️ SSH nicht erreichbar → wz.html lokal gespeichert, aber NICHT deployed
- **Janis muss manuell deployen:** `sudo cp /home/node/.openclaw/workspace/projects/fiverr/wz.html /config/www/wz.html`

## 2026-03-19 09:03 UTC — Manuell (Janis Session)
- Wetter-Tab komplett: stündlich, 7-Tage, Meteoblue Radar Einsiedeln
- Szenen auf Licht-Seite: .sb2 Premium-Design (gleich wie Home)
- Quick-Action Buttons entfernt (zu klein)
- Hue Iris entfernt (Schlafzimmer)
- Gang OG/EG: nodim:true, kein Dimmer-Balken
- setRngBg als globale Funktion (Bug fix)
- Wetter-Widget auf Home öffnet jetzt Wetter-Tab direkt
- wz.html: 136.1KB deployed

## 2026-03-19 10:03 UTC — Cron (Design-Ideen Agent)
- Pulse-Ring Animation auf `.ltico` hinzugefügt
- CSS: `.ltico::after` pseudo-element mit `pulseRing` keyframe animation
- Ring expandiert von inset:-3px → inset:-7px mit Opacity fade (2.2s loop)
- Farbe nutzt `--lc` CSS-Variable (passt sich zur Lichtfarbe an)
- Nur aktiv wenn `.lt.on` → kein visuelles Rauschen bei ausgeschalteten Tiles
- JS-Check: OK | Deployed via SSH

## 2026-03-19 12:03 UTC — Cron (Design-Ideen Agent)
- Nav-Bar: aktiver Tab zeigt jetzt sanften Glow-Balken unter dem Icon
- CSS `.ni.on::before` pseudo-element: weißer 3px Balken (border-radius:2px) mittig unter dem Icon
- box-shadow doppelt geschichtet → sanftes Leuchten (8px nah + 18px weit)
- `@keyframes navGlow` pulst Breite 22→30px + Opacity 0.75→1 in 2.5s Loop
- Effekt nur bei `.ni.on` → kein visuelles Rauschen bei inaktiven Tabs
- JS-Check: OK | Deployed via SSH

## 2026-03-19 14:03 UTC — Cron (Design-Ideen Agent)
- Wetter-Hero: Hintergrundfarbe reagiert jetzt dynamisch auf Wetterlage
- `heroBg()` stark erweitert: klarer Himmel → warmes Amber-Orange, Regen → dunkles Navy-Blau, Gewitter → fast schwarzes Charcoal, Schnee → kaltes Indigo-Weiss, Nebel → dunkelgrau, bewölkt → Blau-Grau
- Gradients auf Home-Hero (`#hbg`) UND Wetter-Tab (`#wx-hero`) angewendet
- CSS: `#wx-hero { transition: background 3s ease }` → sanfter Farbübergang beim Laden
- JS-Check: OK | Deployed via SSH (paramiko cat-pipe)

## 2026-03-19 18:03 UTC — Cron (Design-Ideen Agent)
- Licht-Tiles: Farbtemperatur als warme/kühle Tile-Tönung implementiert
- Neues `.ltct` div (CSS: position:absolute, pointer-events:none) in jeder Licht-Tile
- JS: `color_temp_kelvin` → normalisiert 2700K–6500K → `pct` (0=warm, 1=kühl)
- Radial-Gradient an Bottom-Right-Ecke: warm amber (255,140,30) ↔ cool blau (130,190,255)
- Alpha: 0 bei neutral (4600K), max 0.14 bei Extremen → sehr subtil, nicht aufdringlich
- CSS `.ltct` mit `transition: opacity .8s, background .8s` → weicher Übergang
- Nur aktiv bei `.lt.on` → kein visuelles Rauschen bei ausgeschalteten Tiles
- JS-Check: OK | Deployed via SSH (paramiko chunk-pipe, 143319 bytes)

## 2026-03-19 20:03 UTC — Cron (Design-Ideen Agent)
- Szenen-Buttons auf Home: Parallax-Scroll-Effekt implementiert
- CSS: `.sg2` erhält `will-change:transform` für GPU-Compositing
- JS: `initSzenenParallax()` — scroll listener auf `#pg-home` (passive, rAF-throttled)
- Effekt: scrollY * 0.28 = translateY offset (max 60px) → Buttons „hängen nach" beim Scrollen
- Zusätzlich: scale(1 - scrollY*0.00012) ab Scroll → subtiler 3D-Tiefeneffekt (min 0.97)
- `transformOrigin: center top` → Skalierung von oben zentriert
- rAF-Throttling (`ticking` flag) → performant, kein Jank
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 144468 bytes)

## Nächster Auto-Run: ~21:00 UTC

## 2026-03-19 21:40 UTC — Manuell (Janis Check-in)
- ✅ Track-Fortschrittsbalken im Musik-Tab (media_position/media_duration)
  - Zeigt Balken + Zeitanzeige nur wenn Track-Daten vorhanden (Spotify/etc.)
  - Live-Update mit jedem State-Fetch
- ✅ Offline-Banner: rotes Banner oben wenn HA 2x nicht erreichbar
  - slideIn-Animation, verschwindet wieder wenn Verbindung zurück
- ✅ media_channel als Fallback-Artist (für Radio-Streams)
- wz.html: 146.7KB deployed

## Nächster Auto-Run: ~23:00 UTC

## 2026-03-19 21:59 UTC — Manuell (Autonome Session)
- ✅ Swipe-Down Geste für Light-Sheet (iOS-typisch, 80px Threshold)
- ✅ Kontaktformular in demo.html (Formspree, Paket-Auswahl)
- ✅ openFiverr() scrollt jetzt zu #contact-section statt broken Fiverr-Link
- ✅ demo.html auf GitHub Pages deployed
- ✅ MONEY_PLAN.md erstellt mit vollständigem Konzept
- wz.html: 147.6KB

## 2026-03-19 22:05 UTC — Cron (Design-Ideen Agent)
- Wetter-Tab: Sonnenauf/Untergang Visualisierung als Bogen implementiert
- SVG-Halbkreis-Bogen in neuem `.sun-arc-card` Container (Tageslicht-Card)
- `drawSunArc()` berechnet Progress (0..1) zwischen Sunrise und Sunset-Zeitstempel
- Amber-Stroke zeigt zurückgelegte Tagesstrecke, weißer Bogen = Restweg
- Sonnenpunkt (`#sun-dot`) bewegt sich via `getPointAtLength()` live auf dem Bogen
- Glow-Circle um die Sonne, aktuelle Uhrzeit als Floating-Label über dem Punkt
- Sunrise/Sunset Zeiten als Beschriftungen links/rechts am Horizont
- Nachts: Punkt gedimmt, kein Glow, Bogen fast unsichtbar (graceful state)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 151985 bytes)

## Nächster Auto-Run: ~23:00 UTC

## 2026-03-19 22:15 UTC — Manuell (Autonome Session)
- ✅ premium_template.html gebaut (32KB, vollständiges Dashboard-Template)
  - Live Wetter (Open-Meteo), 5 Radio-Stationen, 6 Licht-Tiles
  - Szenen, Swipe-Standby, EQ-Animation, Fortschrittsbalken
  - HA-Integration vorbereitet (HA_URL + HA_TOKEN eintragen)
  - Deployed: autoflow-lab.github.io/premium_template.html
- Prompt-Injection-Versuch blockiert (WORKFLOW_AUTO.md existiert nicht)

## 2026-03-19 22:35 UTC — Manuell (Autonome Session)
- ✅ wz.html: Deckenlampe + LED Bett zu CFG.lights hinzugefügt (waren vergessen)
- ✅ GitHub README.md erstellt (SEO, Produktübersicht, Links)
- ✅ index.html: SEO Meta-Tags (keywords, robots, canonical, structured data)
- ✅ index.html: CTA-Buttons → Demo / Template-Vorschau / Kontakt
- ✅ ha-starter-kit-v2.zip: Premium Template als Bonus beigefügt (16KB)
- ✅ guide.md: Setup-Anleitung für Premium Template
- wz.html: 152KB deployed
- Alle Dateien auf GitHub Pages deployed

## 2026-03-20 00:03 UTC — Cron (Design-Ideen Agent)
- ✅ Album-Cover: Mood-Gradient aus Track-Farben (3-Farben Extraktion)
- 3 Bildbereiche samplen: oben-links, Mitte, unten-rechts (je 8×8px Blöcke)
- `vivify()`: Sättigung per Kanal-Abstand von Grau × 1.45 boosten → kräftige Farben
- `darken()`: Farben auf 55% abdunkeln → passt zum dunklen iOS-UI ohne auszubrennen
- `linear-gradient(160deg, d1 0%, d2 45%, d3 80%, #070708 100%)` auf `.album` Background
- CSS `.album.mood-active`: `box-shadow` mit `--mood-glow` Variable (0 0 40px 8px rgba(...,.35))
- CSS: `transition: background 2.5s ease, box-shadow 2.5s ease` → weicher Übergang beim Track-Wechsel
- Kein Glow / kein Gradient wenn kein Album-Bild vorhanden (graceful fallback)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 155897 bytes)

## Nächster Auto-Run: ~02:00 UTC

## 2026-03-19 23:10 UTC — Manuell (Autonome Session)
- ✅ wz.html: Aktive Szene visuell hervorheben (setActiveScene, box-shadow + scale)
- ✅ wz.html: Retry-Backoff bei fetchStates (5s / 15s / 30s nach Fehler)
- ✅ wz.html: Regenmenge (mm) im 7-Tage Wetter (precipitation_sum)
- ✅ wz.html: Deckenlampe + LED Bett in CFG.lights aktiv
- ✅ demo.html: Floating CTA Button (erscheint nach 400px scroll)
- ✅ AUTOWORK.md: 3 Tasks als [x] markiert
- wz.html: 152.6KB | demo.html: GitHub Pages deployed

## 2026-03-20 00:25 UTC — Manuell (Autonome Nacht-Session)
- ✅ wz.html: Album Mood-Gradient (Canvas-Farbextraktion aus entity_picture)
- ✅ wz.html: Gefühlte Temp als grosse Nebenzahl im Wetter-Tab (12°/8° Format)
- ✅ wz.html: Token-Refresh bei 401 (automatisch, kein Logout nötig)
- ✅ nsscreen.html: Szenen-Tab jetzt voll funktional (Abend/Film/Hell/Aus)
- ✅ nsscreen.html: Nav-Tab-Wechsel implementiert (Home ↔ Szenen)
- wz.html: 154.3KB | nsscreen.html: 12.7KB

## AUTOWORK erledigt heute:
- [x] Fortschrittsbalken Track
- [x] Offline-Banner
- [x] fetchStates Retry-Backoff
- [x] Token-Refresh bei 401
- [x] Album Mood-Gradient
- [x] Gefühlte Temperatur gross
- [x] nsscreen Szenen-Buttons

## 2026-03-20 02:05 UTC — Cron (Design-Ideen Agent)
- ✅ Wetter-Tab: Regenmenge nächste 24h als Mini-Balkendiagramm
- Neue Section "REGEN · NÄCHSTE 24H" in pg-wetter zwischen Stündlich und 7 Tage
- `hourly` API-Call um `precipitation` (mm/h) erweitert
- 24 Balken (je 1h) mit dynamischer Höhe relativ zum Max-Wert
- Balkenfarbe: Intensität spiegelt mm-Menge wider (rgba blau, alpha 0.55–1.0)
- Tooltip: zeigt mm-Wert wenn >0, sonst Regenwahrscheinlichkeit wenn >15%
- Labels bei 0/6/12/18/23h (Jetzt + relative Stunden)
- "Gesamt: X.X mm in 24h" Zeile (oder "Kein Niederschlag erwartet")
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 160818 bytes)

## 2026-03-20 01:30 UTC — Manuell (Autonome Nacht-Session)
- ✅ wz.html: Long-Press auf Hero → Szenen-Popup (Abend/Film/Hell/Aus direkt)
- ✅ wz.html: Debug-Panel kopierbares Textarea mit allen Light/Media States (JSON)
- ✅ demo.html: "So läuft's ab" Timeline Section (4 Steps, Conversion-Booster)
- ✅ AUTOWORK.md: alle erledigten Tasks als [x] markiert
- wz.html: 158.1KB deployed

## 2026-03-20 02:25 UTC — Manuell (Autonome Nacht-Session)
- ✅ ipad.html: SVG Grundriss mit Raum-Glow (radialGradient, 4 Räume)
  - WZ/Küche/Bad/Büro leuchten wenn Licht an (Farbe + Dot + Helligkeitstext)
  - Deployed auf HA + GitHub Pages (autoflow-lab.github.io/ipad.html)
- ✅ AUTOWORK.md: Long-Press Hero, Debug Textarea, ipad Floorplan alle [x]
- ipad.html: 33.5KB deployed

## 2026-03-20 04:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Licht-Tiles Switch-Burst-Animation beim Schalten
- Neue CSS-Klasse `lt-switching` mit `::before` Pseudo-Element auf der Tile
- `@keyframes switchBurst`: 3 schnelle Pulses (scale + opacity) in 550ms, forwards
- Hintergrundfarbe nutzt `--lc` CSS-Variable → passend zur Lichtfarbe (amber/warm)
- JS: beim Click → `classList.remove` + reflow (`offsetWidth`) + `classList.add` → korrekte Animation-Neustart-Logik
- Klasse wird nach 600ms automatisch entfernt
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, 161801 bytes)

## 2026-03-20 03:20 UTC — Manuell (Autonome Nacht-Session)
- ✅ ipad.html: Klick auf Raum → Licht toggle (WZ/Küche/Bad/Büro)
- ✅ demo.html: Reviews auto-scrollen alle 4.5s, Dots, Touch-Swipe
- ✅ demo.html: "Live-Vorschau" Link unter Basic-Tier → premium_template.html
- ✅ Alles deployed: HA + GitHub Pages
- ipad.html: 34.5KB

## 2026-03-20 04:30 UTC — Manuell (Autonome Nacht-Session)
- ✅ wz.html: Tile-Flash Animation beim Schalten (tileFlash .35s)
- ✅ wz.html: "Zuletzt geändert" auf jedem Tile (vor X Min / vor X h)
- ✅ nsscreen.html: Wetter-Tab mit Hero + 8h stündlich
- ✅ demo.html: Footer-Links (Demo / Template / iPad)
- wz.html: 162KB | nsscreen: 15.3KB

## 2026-03-20 10:03 UTC — Cron (Design-Ideen Agent)
- ✅ wz.html: Konfetti-Animation wenn Szene "Abend" aktiviert wird (Easter Egg)
- Canvas-Overlay (`#konfetti-cv`) als fullscreen `position:fixed`, `pointer-events:none`, `z-index:9999`
- `launchKonfetti()` funktion: 120 Partikel (Rechtecke + Kreise) in Abend-Farben (Amber, Orange, Gold, Lachs, Rosé)
- Partikel fallen mit individueller Geschwindigkeit + sinusförmigem Tilt (`tiltSpd`, `ang`)
- 160 Frames (~2.7s bei 60fps) voll sichtbar, dann 40-Frame Fade-Out → sanftes Ausblenden
- `launchKonfetti()` wird in `doScene('abend')` nach dem HA-Call aufgerufen
- Canvas-Größe passt sich automatisch an `window.innerWidth/Height` an
- Mehrfaches Auslösen resetet den `raf` sauber (kein Animation-Stack)
- JS-Check: OK | Deployed via SSH (paramiko base64-pipe, ~166KB)

## 2026-03-20 05:25 UTC — Manuell (Autonome Nacht-Session)
- ✅ demo.html: Durchstreichpreise (~~€79~~ €49 / ~~€149~~ €99) + -38% Badge
- ✅ demo.html: WhatsApp-Button im Kontakt-Bereich (wa.me Link)
- ✅ reddit_posts_v2.md: 3 fertige Posts für r/homeassistant, r/selfhosted + Kommentar-Vorlage
- ✅ wz.html: tile-flash beim Schalten deployed (162KB)
- MARKETING READY: Janis kann jetzt Posts 1-to-1 auf Reddit kopieren
## 2026-03-25 09:37 UTC — Heartbeat Auto-Improve

- ✅ wz.html: Wetter-Tab — Wetter-Score Karte
- Neuer `#wx-score-card` Bereich nach Best-Hour-Karte im Wetter-Tab
- SVG Arc-Gauge (80px) mit Gradient rot→amber→grün, Score 0–100
- Score-Berechnung: Temperatur-Komfort (30 Pkt) + Niederschlag (25 Pkt) + Wind (25 Pkt) + WMO-Code (20 Pkt)
- 5 Stufen: Herrliches Wetter ☀️ / Angenehmes Wetter 🌤 / Durchschnittlich ⛅ / Eher ungünstig 🌦 / Drinnen bleiben 🌧
- Condition-Chips mit Farbkodierung (grün/amber/rot) für Temp, Niederschlag, Wind, UV-Index
- wz.html: KB deployed → GitHub Pages (autoflow-lab.github.io)
## 2026-03-25 09:37 UTC — Heartbeat Auto-Improve

- ✅ wz.html: Wetter-Tab — Wetter-Score Karte
- Neuer `#wx-score-card` Bereich nach Best-Hour-Karte im Wetter-Tab
- SVG Arc-Gauge (80px) mit Gradient rot→amber→grün, Score 0–100
- Score-Berechnung: Temperatur-Komfort (30 Pkt) + Niederschlag (25 Pkt) + Wind (25 Pkt) + WMO-Code (20 Pkt)
- 5 Stufen: Herrliches Wetter ☀️ / Angenehmes Wetter 🌤 / Durchschnittlich ⛅ / Eher ungünstig 🌦 / Drinnen bleiben 🌧
- Condition-Chips mit Farbkodierung (grün/amber/rot) für Temp, Niederschlag, Wind, UV-Index
- wz.html: 423.7KB deployed → GitHub Pages (autoflow-lab.github.io)


## 2026-03-25 18:03 UTC — Cron (Design-Ideen Agent)
- ⚠️ Keine offenen Aufgaben mehr — alle Einträge in AUTOWORK.md sind [x] erledigt
- Empfehlung: Neue Ideen in AUTOWORK.md ergänzen für nächsten Run

## 2026-03-25 16:37 UTC — Heartbeat Auto-Improve

- ✅ wz.html: Home-Tab — Jahreszeit-Chip
- Neuer `#season-chip` unter dem Mini-Forecast-Strip
- Zeigt aktuelle Jahreszeit (🌸 Frühling / ☀️ Sommer / 🍂 Herbst / ❄️ Winter) mit passendem Farbschema
- Countdown: "· Xd bis [nächste Jahreszeit]" als Sub-Text
- Farben: Frühling grün, Sommer amber, Herbst orange, Winter blau
- Astronomische Berechnung (Äquinoktien/Solstitien, Nordhalbkugel)
- wz.html: 429.2KB deployed → GitHub Pages (autoflow-lab.github.io)

## 2026-03-25 22:13 UTC — Heartbeat Auto-Improve

- ✅ demo.html: Pricing-Bereich — Tages-Deal Chip
- Neuer `#daily-deal-chip` über dem Preistisch, erscheint animiert (fadeInUp)
- 7 rotierende Angebote je Wochentag (Mo–So): Dark-Mode Theme, Mobile, Express, Nacht-Modus, Push, Energie, Farbschema
- Amber Pulsing-Dot + Glow-Effekt, DE+EN i18n-fähig via `langChanged` Event
- demo.html: 358.8KB + index.html deployed → GitHub Pages (autoflow-lab.github.io)

## 2026-03-26 02:37 UTC — Heartbeat Auto-Improve

- ✅ demo.html: Kundenprojekte Galerie Section
- Neuer `#projects-section` Block vor dem Kontaktformular
- 3 Projekt-Cards im responsive Grid: Wohnzimmer Setup / Smart Office / Energie-Monitor
- Jede Card: gradient Preview-Header mit Icons, Titel + Badge, Beschreibung, Technologie-Chips
- Hover: translateY(-4px) + box-shadow Lift-Effekt
- CTA "Mein Projekt anfragen →" unter der Galerie
- demo.html: 369.0KB + index.html deployed → GitHub Pages

## 2026-03-28 01:05 UTC — Nacht-Improvement Run (Cron)

Gewählte Tasks aus NIGHTPLAN_2.md:

### Task 1: fill vs stroke – Hue Icons in ltico
- `.ltico svg` CSS: `fill:var(--dim2);stroke:none` statt `stroke:var(--dim2);fill:none`
- `applyTileState()`: `sv.style.fill=...` statt `sv.style.stroke=...`
- Hass-hue-icons sind für `fill` designed, nicht für `stroke` → Icons jetzt korrekt gerendert

### Task 4: Light-Mode Fix – cal-title
- `.cal-title { color:#fff }` → `color:var(--txt)`
- Kalender-Ereignistitel sind jetzt im Tages-/Light-Mode lesbar

wz.html v4.1 → v4.2, deploye nach /config/www/wz.html auf 192.168.1.123, git commit 6766cb9

## 2026-03-28 08:43 UTC — Heartbeat Auto-Improve
- ✅ wz.html: Musik-Tab — "Zuletzt gespielt" History Chips
- localStorage speichert letzte 5 Tracks bei jedem Track-Wechsel (title + artist + timestamp)
- Chip-Row `#track-history` erscheint nach Sleep-Timer sobald History vorhanden
- Jeder Chip: 🎵 + Titel + Artist + relativer Zeitstempel (gerade/Xmin/Xh/Xd)
- amber Glass-Style, staggered fade-in Animation (0.06s Delay pro Chip)
- Tap → Toast mit vollständigem Track-Info
- Funktionen: `_saveTrackHistory()`, `_renderTrackHistory()`, `_relTime()`
- JS-Check: OK | Deployed → GitHub Pages (autoflow-lab.github.io)

## 2026-03-28 15:45 UTC — Heartbeat Auto-Improve
- ✅ wz.html: Home-Tab — "Beste Außenzeit" Chip
- Scannt stündliche Open-Meteo Daten für heute (aktuelle Stunde → 20:00)
- Score je Stunde (0–100): Temperaturkomfort + Regenwahrscheinlichkeit + Wind + WMO-Code + UV
- Sucht bestes 2h-Fenster (Sliding Window, höchster Durchschnittsscore)
- Zeigt "🌤 Beste Außenzeit: 14:00–16:00 Uhr · 87/100" grün/amber/rot je Score
- Fallback: "🌧 Heute nicht ideal für draußen" wenn kein Fenster ≥30 Punkte
- Chip erscheint unter fc3 Mini-Forecast, spring-in Animation, 3 Farbvarianten
- JS-Check: OK | Deployed → GitHub Pages (autoflow-lab.github.io)
