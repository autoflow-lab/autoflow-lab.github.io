# AUTOWORK.md — Autonomer Verbesserungs-Agent für autoflow-lab.github.io

## Deine Aufgabe
Du bist ein autonomer Code-Agent. Du verbesserst die Fiverr-Portfolio-Website von autoflow-lab selbstständig.
Du bekommst diese Datei als Kontext + hast Zugriff auf alle Tools.

## Kontext
- **Live URL**: https://autoflow-lab.github.io/
- **Lokale Datei**: /home/node/.openclaw/workspace/projects/fiverr/demo.html
- **GitHub Repo**: autoflow-lab/autoflow-lab.github.io
- **GitHub Token**: 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
- **E-Mail**: clawy.studio@gmail.com
- **Fiverr**: https://www.fiverr.com/autoflow-lab

## Deploy-Snippet (Python)
```python
import requests, base64
T='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'
H={'Authorization':f'token {T}','Accept':'application/vnd.github.v3+json'}
R='autoflow-lab/autoflow-lab.github.io'
with open('/home/node/.openclaw/workspace/projects/fiverr/demo.html','rb') as f:
    c=base64.b64encode(f.read()).decode()
for fn in ['demo.html','index.html']:
    r=requests.get(f'https://api.github.com/repos/{R}/contents/{fn}',headers=H)
    sha=r.json().get('sha')
    r2=requests.put(f'https://api.github.com/repos/{R}/contents/{fn}',headers=H,json={
        'message':'auto-improve: <beschreibung>','content':c,'sha':sha})
    print(f"{'OK' if r2.status_code==200 else 'FAIL'} {fn}")
```

## Floor Plan — Kritische Info
- Technik: SVG Radial-Gradient Overlay mit mix-blend-mode:screen
- **KEIN filter="url(#roomBloom)"** auf Polygon-Elementen — führt zu Licht-Bleeding außerhalb der Räume
- Raum-Polygone (viewBox 0 0 1376 768):
  - bed1:   688,148 992,193 992,328 688,283
  - bath:   993,215 1148,258 1148,428 993,388
  - living: 530,245 688,283 992,328 992,515 530,415 (5-Punkte)
  - dining: 812,422 1080,492 1080,608 812,548
  - bed2:   225,328 482,388 482,528 225,468
  - office: 482,452 658,498 658,608 482,562
- Lampen-Positionen: L1(840,178)bed1, L2(800,222)bed1, L3(895,240)bed1, L4(380,393)bed2-Stehlampe, L5(302,360)bed2, L6(678,285)living, L7(760,348)living, L8(580,520)office, L9(1072,268)bath, L11(900,478)dining

## Ideen-Liste (Priorität: oben = wichtiger)
Wähle bei jedem Run eine Aufgabe aus dieser Liste, implementiere sie, hake sie ab (ersetze [ ] mit [x]) und deploye.

### UI / Design
- [ ] Grundriss-Polygone feiner abstimmen — isometrische Wände sollen exakt gefüllt werden
- [x] Dark Mode: animierte Neon-Linien/Grid-Hintergrund im Hero
- [x] Light Mode: subtile Glasmorphism-Cards mit echtem backdrop-filter blur
- [x] Floating Labels auf den Lampen-Dots (Raumnamen einblenden beim Hover)
- [ ] Mobile: Grundriss vertikal zoombarer mit Pinch-Zoom (CSS touch-action)
- [x] Scroll-to-top Button mit smooth animation
- [x] Hero: animierte Typing-Effekt für den Subtitle-Text
- [x] Portfolio-Cards: 3D tilt-effect mit Maus-Tracking (transform perspective)
- [x] Pricing-Section: Toggle Monatlich/Einmalig mit Preisanimation
- [x] Footer: Social Links (GitHub, LinkedIn) hinzufügen

### Features
- [ ] Grundriss: Doppelklick auf Raum öffnet Detail-Panel mit Geräteliste
- [ ] Grundriss: Räume haben "Aktive Geräte" Zähler-Badge
- [x] Dashboard: Live-Uhr Widget (lokale Zeit des Besuchers)
- [ ] Dashboard: CO2 / Luftqualität Widget
- [ ] Dashboard: Kalender-Integration Widget (nächste 3 Termine als Platzhalter)
- [x] "How it works" Section mit 3-Step-Prozess und Animations
- [x] Vergleichstabelle: HA vs Alexa vs Google Home (Vorteile zeigen)
- [x] Testimonial-Carousel mit Auto-Scroll
- [ ] Zurück-zum-Anfang nach Tab-Wechsel smooth animieren
- [x] Contact-Formular (mailto-basiert, kein Backend)

### SEO & Performance
- [x] Meta OG-Tags (og:image, og:title, og:description) für Social Sharing
- [x] Structured Data JSON-LD (LocalBusiness/Service Schema)
- [ ] Loading Skeleton für Weather/News statt einfachem Spinner
- [ ] Lazy-load für Floor Plan Bild (loading="lazy" ist schon da, aber intersection observer trigger)
- [ ] Service Worker für Offline-Grundriss (nur Floor Plan cachen)

### Content
- [x] Mehr Bewertungen (6 statt 4, mit spezifischeren Projektreferenzen)
- [x] "Technologie-Stack" Section: Icons für HA, N8N, Zigbee, Matter, etc.
- [ ] FAQ erweitern: Was kostet HA selbst? Wie lange dauert Einrichtung?
- [ ] AI-Page: Konkrete Beispiele mit Before/After Automation
- [ ] Pricing: "Alles inklusive" Vergleich mit anderen Freelancern

## Arbeitsweise
1. Lies AUTOWORK.md und PLAN.md (falls vorhanden)
2. Wähle eine [ ] Aufgabe die du in einem Run erledigen kannst
3. Lies die aktuelle demo.html
4. Implementiere die Verbesserung sauber
5. Deploye zu GitHub (beide Dateien: demo.html + index.html)
6. Markiere die Aufgabe als [x] in dieser Datei
7. Schreibe einen kurzen Bericht in PROGRESS.md
8. Fertig — kein weiterer Input nötig

## Qualitäts-Regeln
- Kein Framework, kein Build-Step — reines HTML/CSS/JS
- Alle neuen Texte müssen in BEIDEN Sprachen (de/en) in den T-Objekt
- Dark Mode muss immer mitberücksichtigt werden
- Mobile-First — alles muss auf 375px funktionieren
- Grundriss: NIEMALS filter="url(#roomBloom)" auf Polygon-Elementen
- Vor dem Deploy: Prüfen ob HTML valide (öffnende/schließende Tags balanced)
