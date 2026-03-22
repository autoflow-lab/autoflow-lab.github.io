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

## 2026-03-22 11:30 UTC — Security Check

**Neue Ereignisse seit letztem Check (11:00 UTC):**

**Interne IP:** `192.168.1.54`
- 2× Login-Versuch um 12:12:46 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie zuvor)
- Bewertung: Wiederkehrendes Problem — internes Gerät mit veraltetem/ungültigem Token
- Empfehlung: Token auf dem Mac-Gerät dringend erneuern oder HA-Integration reparieren

---

## 2026-03-22 12:00 UTC — Security Check

**Neue Ereignisse seit letztem Check (11:30 UTC):**

**Interne IP:** `192.168.1.54`
- 4× Login-Versuch um 12:46:42 und 12:49:17 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie zuvor)
- Bewertung: Wiederkehrendes Problem — internes Gerät mit veraltetem/ungültigem Token
- Empfehlung: Token auf dem Mac-Gerät **dringend erneuern** — dieses Problem besteht seit heute Morgen!

---

## 2026-03-22 13:00 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veraltetem Token), letzte Aktivität 12:46–12:49 UTC.
Kein neuer Fund, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 12:30 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veraltetem Token), letzte Aktivität 12:46–12:49 UTC.
Kein neuer Fund, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 13:30 UTC — Security Check

**Neue Ereignisse seit letztem Check (13:00 UTC):**

**Interne IP:** `192.168.1.54`
- 1× Login-Versuch um 13:45:51 UTC
- 2× Login-Versuch um 14:04:45 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie den ganzen Tag)
- Bewertung: Wiederkehrendes Problem — Token auf diesem Gerät immer noch veraltet
- ⚠️ Dieses Problem besteht seit heute ~08:00 UTC — **Token-Erneuerung dringend empfohlen!**

---

## 2026-03-22 14:00 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veralteter Token), letzte bekannte Aktivität 14:04 UTC.
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 14:30 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veralteter Token), letzte bekannte Aktivität 14:04 UTC.
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 15:00 UTC — Security Check

**Neue Ereignisse seit letztem Check (14:30 UTC):**

**Interne IP:** `192.168.1.54`
- 2× Login-Versuch + Ban um 15:38:05 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie den ganzen Tag)
- Bewertung: Fortlaufendes Problem seit ~08:00 UTC — Token auf diesem Mac-Gerät ist veraltet/ungültig
- ⚠️ Gerät wurde erneut gebannt. Token-Erneuerung **dringend notwendig**.

---

## 2026-03-22 15:30 UTC — Security Check

**Neue Ereignisse seit letztem Check (15:00 UTC):**

**Interne IP:** `192.168.1.54`
- 1× Login-Versuch um 16:04:34 UTC
- 1× Login-Versuch um 16:06:24 UTC
- URL: `/api/states`, Safari macOS (selbes Gerät wie den ganzen Tag)
- Bewertung: Fortlaufendes Problem seit ~08:00 UTC — Token auf diesem Mac-Gerät ist weiterhin veraltet/ungültig
- ⚠️ Dieses Problem besteht nun seit über 8 Stunden — Token-Erneuerung dringend notwendig!

---

## 2026-03-22 16:00 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veralteter Token), letzte bekannte Aktivität 16:06 UTC.
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 16:30 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` wiederholt (veralteter Token), letzte bekannte Aktivität 16:06 UTC.
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 17:00 UTC — Security Check

**Neue Ereignisse seit letztem Check (16:30 UTC):**

**Interne IP:** `192.168.1.54`
- 7× Login-Versuch um 17:06:21 UTC
- 1× Login-Versuch um 17:08:33 UTC
- URL: `/api/states`, Safari macOS — bekanntes Gerät mit veraltetem Token
- Bewertung: Fortlaufendes Problem seit ~08:00 UTC

**Interne IP:** `192.168.1.17` ⚠️ NEU
- 1× Login-Versuch um 17:11:26 UTC (URL: `/auth/login_flow/...`)
- 1× Login-Versuch um 17:25:49 UTC (URL: `/auth/login_flow/...`)
- User-Agent: Safari macOS 10_15_7 / Version 16.6.1
- Bewertung: Neue interne IP — möglicherweise weiteres Gerät mit falschem Passwort/Token
- Intern (192.168.1.x) — nicht kritisch, aber zu beobachten

---

## 2026-03-22 17:30 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` neu aufgetaucht (17:11–17:25 UTC).
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 18:00 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 18:30 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht installiert/erlaubt) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Kein neuer Fund verifizierbar, keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 19:00 UTC — Security Check

**Keine neuen Security-Events.** HA-Log zeigte nur Custom-Integration-Warnungen (HACS, meross_lan, spotcast, extended_openai_conversation) und einen Denon Media Player Timeout.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 19:30 UTC — Security Check

**Keine neuen Security-Events.** HA-Log zeigte nur Music Assistant Versionswarnung.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 20:00 UTC — Security Check

**SSH nicht verfügbar** (`sshpass` nicht erlaubt) — Log konnte nicht geladen werden.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Keine neuen Events bekannt. Keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 20:30 UTC — Security Check

**Keine neuen Security-Events.** HA-Log zeigt keine Login-Versuche, gebannten IPs oder unauthorized-Einträge.
Letzter bekannter Status: `192.168.1.54` (veralteter Token, seit ~08:00 UTC), `192.168.1.17` (17:11–17:25 UTC).
Keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 08:07 UTC — Security Check durchgeführt
## 2026-03-22 21:00 UTC — Security Check

**Keine neuen Security-Events.** HA-Log zeigt nur Chromecast-Verbindungsfehler (192.168.1.217, 192.168.1.161) und Automations-Fehler (media_stop). Keine Login-Versuche, gebannte IPs oder unauthorized-Einträge.
Keine Telegram-Benachrichtigung gesendet.

---

## 2026-03-22 21:30 UTC — Security Check

**Keine neuen Security-Events.** HA-Log zeigt nur Music Assistant Versionsmismatch (Schema 28). Keine Login-Versuche, gebannte IPs oder unauthorized-Einträge.
Keine Telegram-Benachrichtigung gesendet.

---

## Security Check — 2026-03-22 21:07 UTC

**Status:** Security OK

- Keine Login-Versuche, gebannte IPs oder unauthorized-Einträge gefunden
- Logs zeigen nur normale Warnungen: fehlende Scenes, Chromecast-Verbindungsfehler, Music Assistant Versionsmismatch
- Alle IPs im Log sind lokal (192.168.1.x)
- SSH-Zugriff nicht möglich (sshpass nicht verfügbar), Check via HA REST API /error_log durchgeführt

