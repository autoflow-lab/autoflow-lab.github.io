# HA Security Log

## 2026-03-28 15:00 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 14:30 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `84.72.122.4` (hispeed.ch) um 12:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität.**

---


## 2026-03-28 14:30 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 14:00 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `84.72.122.4` (hispeed.ch) um 12:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität.**

---


## 2026-03-28 14:00 UTC — ⚠️ Externe Login-Aktivität (hispeed.ch)

Prüfzeitraum: seit 13:30 UTC (letzter Check)

### Login-Versuche gefunden:
- `84.72.122.4` (84-72-122-4.dclient.hispeed.ch) — ungültige Auth, `/api/websocket` — **2026-03-28 12:56:56 UTC**
  - User-Agent: macOS Safari 605.1.15
  - Bewertung: **Extern (nicht 192.168.1.x)** — jedoch CH ISP hispeed.ch, wahrscheinlich Janis

### Bewertung:
- Gleiche IP wie bereits um 00:13 UTC (damals geloggt), erneuter Versuch um 12:56 UTC
- Kein Banning ausgelöst, kein Brute-Force-Muster
- Wahrscheinlich Janis mit falschem Passwort von extern

**→ Janis per Telegram benachrichtigt (externe IP, nicht kritisch eingestuft)**

---



## 2026-03-28 13:30 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 13:00 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität.**

---


## 2026-03-28 13:00 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 12:30 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität.**

---


## 2026-03-28 12:30 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 12:00 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität.**

---


## 2026-03-28 12:00 UTC — Security OK (SSH nicht erreichbar)

Prüfzeitraum: seit 11:30 UTC (letzter Check)

### SSH-Zugriff:
Fehlgeschlagen — kein Key hinterlegt, sshpass nicht verfügbar. Kein direkter Log-Zugriff möglich.

### Login-Versuche:
Nicht prüfbar. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue verifizierte Aktivität. SSH-Zugang weiterhin nicht möglich.**

---


## 2026-03-28 11:30 UTC — Security OK

Prüfzeitraum: seit 11:00 UTC (letzter Check)

### Login-Versuche:
Keine neuen Einträge. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue Aktivität. Stille = alles OK.**

---


## 2026-03-28 11:00 UTC — Security OK

Prüfzeitraum: seit 10:30 UTC (letzter Check)

### Login-Versuche:
Keine neuen Einträge. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue Aktivität. Stille = alles OK.**

---


## 2026-03-28 10:30 UTC — Security OK

Prüfzeitraum: seit 10:00 UTC (letzter Check)

### Login-Versuche:
Keine neuen Einträge. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue Aktivität. Stille = alles OK.**

---


## 2026-03-28 10:00 UTC — Security OK

Prüfzeitraum: seit 09:30 UTC (letzter Check)

### Login-Versuche:
Keine neuen Einträge. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue Aktivität. Stille = alles OK.**

---


## 2026-03-28 09:30 UTC — Security OK

Prüfzeitraum: seit 09:00 UTC (letzter Check)

### Login-Versuche:
Keine neuen Einträge. Letzter bekannter Eintrag bleibt `192.168.1.50` (intern) um 09:56 UTC — bereits geloggt.

**→ Keine neue Aktivität. Stille = alles OK.**

---


## 2026-03-28 09:00 UTC — Security Check

Prüfzeitraum: seit 08:09 UTC (letzter Check)

### Login-Versuche gefunden:
- `192.168.1.50` (intern, LAN) — ungültige Auth, `/auth/login_flow/...` — 2026-03-28 09:56 UTC
  - User-Agent: iPhone (iOS 26.3.1), Chrome Mobile
  - Bewertung: **intern (192.168.1.x)** — wahrscheinlich Janis oder Gerät im Heimnetz

### Bewertung:
- Nur interne IP, kein externer Angreifer
- Kein Banning ausgelöst
- Könnte falsches Passwort auf dem iPhone sein

**→ Neue Aktivität erkannt — Janis benachrichtigt**

---


## 2026-03-28 08:09 UTC — Security OK

Letzten 30 Zeilen von `/config/home-assistant.log` geprüft (via HA API error_log).

### Login-Versuche gefunden:
- `192.168.1.17` (intern) — ungültige Auth, `/auth/token` — 2026-03-27 21:50 UTC
- `84.72.122.4` (dclient.hispeed.ch) — ungültige Auth, `/api/websocket` — 2026-03-28 00:13 UTC

### Bewertung:
- hispeed.ch = wahrscheinlich Janis selbst (CH ISP)
- 192.168.1.17 = internes LAN-Gerät
- Keine externen unbekannten IPs, kein Banning, kein Brute-Force

**→ Security OK**
