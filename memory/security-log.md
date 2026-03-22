# HA Security Log

## 2026-03-22 08:07 UTC — ⚠️ Externe IP erkannt

**Externe IP:** `138.199.35.8` (unn-138-199-35-8.datapacket.com)
- Zeitpunkt: 2026-03-21 23:30:35
- URL: `/media/wp-includes/wlwmanifest.xml` (WordPress-Scan)
- User-Agent: Chrome 78 / Win10 (typischer Bot/Scanner)
- Kein Anmeldeversuch mit gültigen Daten, nur Scan

**Interne IP gebannt:** `192.168.1.54`
- Gerät mit abgelaufenem/falschem Token hat /api/states abgefragt (Safari macOS)
- Wurde um 19:25 Uhr gebannt (zu viele Versuche)
- Wahrscheinlich ein lokales Gerät mit veralteter HA-Integration

---

## 2026-03-22 10:00 UTC — Security Check

**Neue Ereignisse seit letztem Check (08:07 UTC):**

**Interne IP:** `192.168.1.54`
- 3× Login-Versuch um 10:43:42 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie zuvor)
- Bewertung: Wiederkehrendes Problem, internes Gerät mit veraltetem Token

**Interne IP:** `192.168.1.254`
- 1× Login-Versuch um 11:00:12 UTC
- URL: `/api/`, User-Agent: `curl/7.88.1`
- Bewertung: Unbekannte Quelle, möglicherweise Router oder Skript — intern, aber auffällig

---

## 2026-03-22 10:30 UTC — Security Check

**Neue Ereignisse seit letztem Check (10:00 UTC):**

**Interne IP:** `192.168.1.54`
- 2× Login-Versuch um 11:19:09–10 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie zuvor)
- Bewertung: Gerät mit veraltetem/ungültigem Token, wiederkehrendes Problem — kein externer Angriff
- Empfehlung: Token auf dem Mac-Gerät erneuern oder Integration prüfen

---

---

## 2026-03-22 11:00 UTC — Security Check

**Neue Ereignisse seit letztem Check (10:30 UTC):**

**Interne IP:** `192.168.1.54`
- 2× Login-Versuch um 11:43:22 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie zuvor)
- Bewertung: Gerät mit veraltetem/ungültigem Token — wiederkehrendes Problem, intern
- Empfehlung: Token auf dem Mac-Gerät dringend erneuern

---

## 2026-03-22 08:07 UTC — Security Check durchgeführt
