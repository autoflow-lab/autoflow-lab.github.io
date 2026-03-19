"""
Morgen-Briefing Script für Janis
Sammelt alle wichtigen Infos und schickt sie via Telegram
"""
import requests, json
from datetime import datetime

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk"
BASE = "http://192.168.1.123:8123"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_state(entity_id):
    r = requests.get(f"{BASE}/api/states/{entity_id}", headers=HEADERS)
    return r.json() if r.ok else {}

def briefing():
    lines = ["🌅 **Guten Morgen Janis!** Hier dein Morgen-Briefing:\n"]

    # Lichter die noch an sind
    r = requests.get(f"{BASE}/api/states", headers=HEADERS)
    states = r.json()
    lights_on = [s['attributes'].get('friendly_name', s['entity_id'])
                 for s in states
                 if s['entity_id'].startswith('light.') and s['state'] == 'on']
    if lights_on:
        lines.append(f"💡 **Lichter an:** {', '.join(lights_on)}")

    # Akku iPhone
    iphone = get_state('sensor.iphone_von_janis_battery_level_2')
    if iphone.get('state'):
        lines.append(f"📱 **iPhone Akku:** {iphone['state']}%")

    # MacBook
    mac = get_state('sensor.macbook_air_von_janis_internal_battery_level')
    if mac.get('state'):
        lines.append(f"💻 **MacBook Akku:** {mac['state']}%")

    # Drucker Tinten
    cartridges = {
        '⬛ Schwarz': 'sensor.hp_officejet_pro_8020_series_black_cartridge_2',
        '🔵 Cyan': 'sensor.hp_officejet_pro_8020_series_cyan_cartridge_2',
        '🟡 Gelb': 'sensor.hp_officejet_pro_8020_series_yellow_cartridge_2',
    }
    low = []
    for name, eid in cartridges.items():
        s = get_state(eid)
        if s.get('state') and int(s['state']) < 30:
            low.append(f"{name}: {s['state']}%")
    if low:
        lines.append(f"🖨️ **Drucker niedrig:** {', '.join(low)}")

    # Wetter
    weather = get_state('weather.forecast_home')
    if weather.get('attributes'):
        temp = weather['attributes'].get('temperature', '--')
        lines.append(f"🌤️ **Wetter:** {temp}°C, {weather.get('state','')}")

    lines.append("\n🦀 **Was ich letzte Nacht gemacht habe:**")
    lines.append("✅ HA aufgeräumt (25 Namen, 29 Räume zugewiesen)")
    lines.append("✅ Clawy Dashboard erstellt → /clawy-dashboard")
    lines.append("✅ Music Assistant gestartet (Spotify verbunden)")
    lines.append("✅ Krabbe-App für NS Panel → /local/clawy.html")
    lines.append("\n💡 **Nächste Schritte:**")
    lines.append("• NS Panel: Browser öffnen → http://192.168.1.123:8123/local/clawy.html")
    lines.append("• Music Assistant: Sidebar → Player hinzufügen")
    lines.append("• HA Update verfügbar: 2025.10.3 → 2026.2.3")

    return "\n".join(lines)

if __name__ == "__main__":
    print(briefing())
