#!/usr/bin/env python3
import urllib.request
import json
import datetime
import os
import time
import sys

# 1. Fetch Wetterdaten
url = "https://api.open-meteo.com/v1/forecast?latitude=47.170&longitude=8.783&hourly=precipitation_probability,precipitation&timezone=Europe%2FZurich&forecast_days=1"
try:
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"API_ERROR")
    sys.exit(1)

hourly = data.get('hourly', {})
times = hourly.get('time', [])
probs = hourly.get('precipitation_probability', [])

if not times or not probs:
    print("DATA_ERROR")
    sys.exit(1)

# 2. Finde aktuelle Stunde (UTC: 1:25 → 01:00)
now_utc = datetime.datetime.utcnow()
current_hour_utc = now_utc.replace(minute=0, second=0, microsecond=0)
current_hour_utc_str = current_hour_utc.isoformat()

# In Zurich ist es UTC+2 (CEST) → 3:25 → 03:00
current_hour_zurich = current_hour_utc + datetime.timedelta(hours=2)
current_hour_zurich_str = current_hour_zurich.isoformat()

# Finde Index in times (ISO format mit T)
cur_idx = -1
for i, t in enumerate(times):
    if t.startswith(current_hour_zurich_str[:13]):  # Vergleich bis HH
        cur_idx = i
        break

if cur_idx == -1:
    print("TIME_MATCH_ERROR")
    sys.exit(1)

# 3. Prüfe aktuelle Stunde (wenn schon >50%, ist Regen schon im Gang)
current_prob = probs[cur_idx] if cur_idx < len(probs) else 0
if current_prob > 50:
    print("REGEN_LAUFT_BEREITS")
    sys.exit(0)

# 4. Prüfe nächste 2 Stunden (curIdx+1 und curIdx+2)
next_2_hours = []
for offset in [1, 2]:
    idx = cur_idx + offset
    if idx < len(probs):
        next_2_hours.append((idx, times[idx], probs[idx]))

warn_hour_idx = -1
warn_hour_str = None
for idx, time_str, prob in next_2_hours:
    if prob > 60:
        warn_hour_idx = idx
        warn_hour_str = time_str
        break

if warn_hour_idx == -1:
    print("KEIN_REGEN")
    sys.exit(0)

# 5. Lese HA Token
token_file = "/home/node/.openclaw/workspace/secure/ha_creds.txt"
ha_token = None
try:
    with open(token_file, 'r') as f:
        for line in f:
            if line.startswith("HA_TOKEN="):
                ha_token = line.split("=", 1)[1].strip()
                break
except:
    print("TOKEN_ERROR")
    sys.exit(1)

if not ha_token:
    print("TOKEN_NOT_FOUND")
    sys.exit(1)

# 6. Prüfe rain_warn_sent.txt im workspace
warn_log = "/home/node/.openclaw/workspace/tmp/rain_warn_sent.txt"
if os.path.exists(warn_log):
    try:
        with open(warn_log, 'r') as f:
            last_ts = int(f.read().strip())
            age_seconds = time.time() - last_ts
            if age_seconds < 3 * 3600:  # < 3h
                print("BEREITS_GEWARNT")
                sys.exit(0)
    except:
        pass

# 7. Extrahiere Stunde aus warn_hour_str (z.B. "2026-04-10T05:00")
warn_hour = warn_hour_str.split("T")[1].split(":")[0]

message = f"Achtung, es beginnt um {warn_hour} Uhr zu regnen. Bitte nimm die Kissen rein und deck die Lounge zu!"

ha_url = "http://192.168.1.123:8123/api/services/tts/cloud_say"
headers = {
    "Authorization": f"Bearer {ha_token}",
    "Content-Type": "application/json"
}
payload = {
    "entity_id": "media_player.nestmini3793",
    "message": message,
    "language": "de-DE"
}

req = urllib.request.Request(
    ha_url,
    data=json.dumps(payload).encode('utf-8'),
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        status_code = response.status
        if status_code not in [200, 201]:
            print("HA_ERROR")
            sys.exit(1)
except Exception as e:
    print("HA_REQUEST_ERROR")
    sys.exit(1)

# 8. Schreibe Timestamp
try:
    with open(warn_log, 'w') as f:
        f.write(str(int(time.time())))
except:
    print("LOG_WRITE_ERROR")
    sys.exit(1)

# 9. Status
print("WARNUNG_GESENDET")
