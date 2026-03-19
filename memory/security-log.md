# HA Security Log

## 2026-03-18 18:30 UTC — Erster Check

### Gefundene Ereignisse

| Zeit (UTC) | Typ | IP | Bewertung |
|---|---|---|---|
| 18:46:43 | **Banned IP** | 84.72.122.4 | 🔴 KRITISCH (extern) |
| 19:22:00 | Login attempt (invalid auth) | fe80::147a:8660:8aa:126a | 🟡 Lokal (iPhone HA App) |
| 19:22:40 | Login attempt (invalid auth) | fe80::147a:8660:8aa:126a | 🟡 Lokal (iPhone HA App) |
| 19:24:13 | Login attempt (invalid auth) | fe80::147a:8660:8aa:126a | 🟡 Lokal (iPhone HA App) |
| 19:25:04 | Login attempt (invalid auth) | fe80::147a:8660:8aa:126a | 🟡 Lokal (iPhone HA App) |

## 2026-03-18 19:00 UTC — Check (SSH fehlgeschlagen)

- SSH-Zugriff nicht möglich (sshpass nicht verfügbar in diesem Cron-Kontext)
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 18:30 UTC

## 2026-03-18 19:30 UTC — Check (SSH fehlgeschlagen)

- SSH-Zugriff erneut nicht möglich (sshpass: Permission denied in Cron-Kontext)
- HA API (192.168.1.123) ebenfalls geblockt (private IP nicht erlaubt)
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 18:30 UTC

## 2026-03-18 20:00 UTC — Check (HA API erfolgreich)

### Gefundene Ereignisse (NEU seit 19:30 UTC)

| Zeit (UTC) | Typ | IP | Host | User-Agent | Bewertung |
|---|---|---|---|---|---|
| 19:59:29 | Login attempt (invalid auth) | 192.168.1.44 | lokal | Safari macOS 10.15.7 | 🟡 Lokal |
| 19:59:30 | Login attempt (invalid auth) | 192.168.1.44 | lokal | Safari macOS 10.15.7 | 🟡 Lokal |
| 19:59:31 | Login attempt (invalid auth) | 192.168.1.44 | lokal | Safari macOS 10.15.7 | 🟡 Lokal |
| 19:59:32 | Login attempt (invalid auth) | 192.168.1.44 | lokal | Safari macOS 10.15.7 | 🟡 Lokal |
| 20:22:09 | Login attempt (invalid auth) | 84.72.122.4 | 84-72-122-4.dclient.hispeed.ch | Safari macOS | 🔴 KRITISCH (extern, bereits gebannt) |
| 20:22:12 | Login attempt (invalid auth) | 84.72.122.4 | 84-72-122-4.dclient.hispeed.ch | Safari macOS | 🔴 KRITISCH (extern) |
| 20:27:59 | Login attempt (invalid auth) | 84.72.122.4 | 84-72-122-4.dclient.hispeed.ch | python-requests/2.32.5 | 🔴 KRITISCH (extern, scripted) |
| 20:28:00 | Login attempt (invalid auth) | 84.72.122.4 | 84-72-122-4.dclient.hispeed.ch | python-requests/2.32.5 | 🔴 KRITISCH (extern, scripted) |

### Analyse
- **192.168.1.44**: Lokales Gerät (MacBook/Mac mit Safari auf macOS Catalina 10.15.7) — 4 Versuche in ~3 Sek. Vermutlich gespeicherte Credentials veraltet.
- **84.72.122.4**: Bereits bekannte externe IP (hispeed.ch / Schweiz). Trotz HA-Bann neue Versuche — jetzt auch mit Python-Script (`python-requests`). Verhaltensänderung deutet auf automatisierten Angriff hin. Telegram-Alert gesendet.

---

### Notizen
- 84.72.122.4 ist eine externe IP → wurde von HA gebannt. Telegram-Alert gesendet.
- fe80::147a:8660:8aa:126a ist eine link-local IPv6 Adresse (lokales Netz). User-Agent zeigt iPhone mit HA App 2026.2.1 → vermutlich Janis' eigenes Gerät mit falschem Token/Passwort.

## 2026-03-18 20:30 UTC — Check (SSH + API nicht verfügbar)

- SSH-Zugriff: sshpass nicht verfügbar (Permission denied in Cron-Kontext)
- HA API: private IP geblockt
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 20:00 UTC

## 2026-03-18 21:00 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich
- Letzter Log-Eintrag: 20:28:00 UTC (84.72.122.4 — bereits bekannt, bereits gemeldet)
- **Keine neuen Ereignisse seit 20:30 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-18 21:30 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 21:00 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-18 22:00 UTC — Check (SSH + API nicht verfügbar)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: private IP geblockt
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 21:30 UTC

## 2026-03-18 22:30 UTC — Check (HA API erfolgreich)

### Gefundene Ereignisse (NEU seit 22:00 UTC)

| Zeit (UTC) | Typ | IP | Host | User-Agent | Bewertung |
|---|---|---|---|---|---|
| 22:36:49 | Login attempt (invalid auth) | 192.168.1.44 | lokal | Safari macOS 26.3.1 | 🟡 Lokal |

### Analyse
- **192.168.1.44**: Bekanntes lokales Gerät (MacBook/Mac mit Safari). Erneuter Versuch — gespeicherte Credentials weiterhin veraltet. Kein externer Angreifer, aber persistentes Problem. Telegram-Alert gesendet.

## 2026-03-18 23:00 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 22:30 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-18 23:30 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 23:00 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-19 00:00 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 23:30 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-19 00:30 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 00:00 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-19 01:00 UTC — Check (SSH + API nicht verfügbar)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: private IP geblockt
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 00:30 UTC

## 2026-03-19 01:30 UTC — Check (HA API erfolgreich)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: Zugriff erfolgreich, error_log ohne neue Login/Banned-Einträge
- **Keine neuen Sicherheitsereignisse seit 01:00 UTC**
- Kein Alert gesendet → alles OK

## 2026-03-19 02:00 UTC — Check (SSH + API nicht verfügbar)

- SSH: nicht verfügbar (sshpass: Permission denied)
- HA API: private IP geblockt
- Kein neuer Log-Stand abrufbar → kein Alert gesendet
- Status: unverändert gegenüber 01:30 UTC
