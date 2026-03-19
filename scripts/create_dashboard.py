import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk"
BASE = "http://192.168.1.123:8123"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

dashboard = {
    "title": "Zuhause 🏠",
    "views": [
        # ── VIEW 1: Übersicht ────────────────────────────────────────────
        {
            "title": "Übersicht",
            "icon": "mdi:home",
            "path": "overview",
            "cards": [
                # Schnellzugriff Lichter
                {
                    "type": "vertical-stack",
                    "cards": [
                        {
                            "type": "markdown",
                            "content": "## 💡 Lichter"
                        },
                        {
                            "type": "grid",
                            "columns": 3,
                            "square": False,
                            "cards": [
                                {"type": "light", "entity": "light.buro", "name": "Büro"},
                                {"type": "light", "entity": "light.deckenlampe", "name": "Deckenlampe"},
                                {"type": "light", "entity": "light.schlafzimmer", "name": "Schlafzimmer"},
                                {"type": "light", "entity": "light.eltern_schlafzimmer", "name": "Eltern SZ"},
                                {"type": "light", "entity": "light.hue_iris", "name": "Hue Iris"},
                                {"type": "light", "entity": "light.hue_play", "name": "Hue Play"},
                                {"type": "light", "entity": "light.hue_play_l", "name": "Hue Play L"},
                                {"type": "light", "entity": "light.color_temperature_light_1", "name": "LED Bett"},
                                {"type": "light", "entity": "light.h618a", "name": "Sofa"},
                                {"type": "light", "entity": "light.h61e1", "name": "Wand"},
                                {"type": "light", "entity": "light.h618a_2", "name": "Küche"},
                                {"type": "light", "entity": "light.schlafzimmer_2", "name": "SZ 2"},
                            ]
                        }
                    ]
                },
                # Switches
                {
                    "type": "vertical-stack",
                    "cards": [
                        {
                            "type": "markdown",
                            "content": "## 🔌 Schalter"
                        },
                        {
                            "type": "entities",
                            "entities": [
                                {"entity": "switch.shelly1_98cdac0ca9b2", "name": "Shelly Büro"},
                                {"entity": "switch.shelly1_c45bbe47adb9", "name": "Shelly Kleiderschrank"},
                                {"entity": "switch.shelly1_3c6105fdf196", "name": "Shelly Gäste WC"},
                                {"entity": "switch.shelly1_98cdac0d4f2e", "name": "Shelly Garten"},
                                {"entity": "switch.shellyplus1pm_a0dd6c31333c_switch_0", "name": "Shelly Gang EG"},
                                {"entity": "switch.shellyplus1pm_7c87ce71a43c_switch_0", "name": "Shelly Gang OG"},
                            ]
                        }
                    ]
                },
            ]
        },

        # ── VIEW 2: Medien ───────────────────────────────────────────────
        {
            "title": "Medien",
            "icon": "mdi:music",
            "path": "media",
            "cards": [
                {
                    "type": "media-control",
                    "entity": "media_player.spotify_janisss",
                    "name": "Spotify"
                },
                {
                    "type": "media-control",
                    "entity": "media_player.nest",
                    "name": "Google Nest"
                },
                {
                    "type": "media-control",
                    "entity": "media_player.denon_avr",
                    "name": "DENON AVR"
                },
                {
                    "type": "media-control",
                    "entity": "media_player.lg_webos_tv_oled65g49ls_2",
                    "name": "LG OLED TV"
                },
                {
                    "type": "entities",
                    "title": "Alle Lautsprecher",
                    "entities": [
                        {"entity": "media_player.wohnzimmer_2", "name": "Wohnzimmer"},
                        {"entity": "media_player.schlafzimmer_2", "name": "Schlafzimmer"},
                        {"entity": "media_player.eltern_schlafzimmer", "name": "Eltern Schlafzimmer"},
                        {"entity": "media_player.nestmini3793", "name": "Nest Mini 1"},
                        {"entity": "media_player.nestmini7548", "name": "Nest Mini 2"},
                        {"entity": "media_player.nestmini1153", "name": "Nest Mini 3"},
                    ]
                }
            ]
        },

        # ── VIEW 3: Szenen ───────────────────────────────────────────────
        {
            "title": "Szenen",
            "icon": "mdi:palette",
            "path": "scenes",
            "cards": [
                {
                    "type": "vertical-stack",
                    "cards": [
                        {"type": "markdown", "content": "## 🛏️ Schlafzimmer"},
                        {
                            "type": "grid",
                            "columns": 3,
                            "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.schlafzimmer_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                                {"type": "button", "entity": "scene.schlafzimmer_lesen", "name": "Lesen", "icon": "mdi:book"},
                                {"type": "button", "entity": "scene.schlafzimmer_netflix", "name": "Netflix", "icon": "mdi:netflix"},
                                {"type": "button", "entity": "scene.schlafzimmer_nachtlicht", "name": "Nachtlicht", "icon": "mdi:weather-night"},
                                {"type": "button", "entity": "scene.schlafzimmer_konzentrieren", "name": "Fokus", "icon": "mdi:brain"},
                                {"type": "button", "entity": "scene.schlafzimmer_chill", "name": "Chill", "icon": "mdi:music"},
                            ]
                        }
                    ]
                },
                {
                    "type": "vertical-stack",
                    "cards": [
                        {"type": "markdown", "content": "## 🛏️ Eltern Schlafzimmer"},
                        {
                            "type": "grid",
                            "columns": 3,
                            "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_lesen", "name": "Lesen", "icon": "mdi:book"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_nachtlicht", "name": "Nachtlicht", "icon": "mdi:weather-night"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_konzentrieren", "name": "Fokus", "icon": "mdi:brain"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_gedimmt", "name": "Gedimmt", "icon": "mdi:brightness-4"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_energie_tanken", "name": "Energie", "icon": "mdi:lightning-bolt"},
                            ]
                        }
                    ]
                },
                {
                    "type": "vertical-stack",
                    "cards": [
                        {"type": "markdown", "content": "## 🖥️ Büro"},
                        {
                            "type": "grid",
                            "columns": 2,
                            "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.buro_read", "name": "Lesen", "icon": "mdi:book"},
                                {"type": "button", "entity": "scene.buro_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                            ]
                        }
                    ]
                }
            ]
        },

        # ── VIEW 4: Status & Geräte ──────────────────────────────────────
        {
            "title": "Status",
            "icon": "mdi:chart-bar",
            "path": "status",
            "cards": [
                {
                    "type": "entities",
                    "title": "📱 Geräte",
                    "entities": [
                        {"entity": "sensor.iphone_von_janis_battery_level_2", "name": "iPhone Akku"},
                        {"entity": "sensor.macbook_air_von_janis_internal_battery_level", "name": "MacBook Akku"},
                        {"entity": "sensor.smarthome_display_battery_level", "name": "SmartHome Display Akku"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🖨️ Drucker",
                    "entities": [
                        {"entity": "sensor.hp_officejet_pro_8020_series_black_cartridge_2", "name": "Schwarz"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_cyan_cartridge_2", "name": "Cyan"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_magenta_cartridge_2", "name": "Magenta"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_yellow_cartridge_2", "name": "Gelb"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🌐 Netzwerk",
                    "entities": [
                        {"entity": "binary_sensor.sagemcom_f3896lg_wan_status", "name": "Internet"},
                        {"entity": "sensor.sagemcom_f3896lg_externe_ip", "name": "Externe IP"},
                        {"entity": "sensor.sagemcom_f3896lg_download_geschwindigkeit", "name": "Download"},
                        {"entity": "sensor.sagemcom_f3896lg_upload_geschwindigkeit", "name": "Upload"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🔋 Hue Batterien",
                    "entities": [
                        {"entity": "sensor.hue_dimmer_switch_1_batterie", "name": "Dimmer Switch"},
                        {"entity": "sensor.hue_wall_switch_module_1_batterie", "name": "Wall Switch"},
                        {"entity": "sensor.hue_tap_dial_switch_1_batterie", "name": "Tap Dial 1"},
                        {"entity": "sensor.hue_tap_dial_switch_3_batterie", "name": "Tap Dial 3"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "⚡ Stromverbrauch",
                    "entities": [
                        {"entity": "sensor.shellyplus1pm_a0dd6c31333c_switch_0_power", "name": "Gang EG (W)"},
                        {"entity": "sensor.shellyplus1pm_7c87ce71a43c_switch_0_power", "name": "Gang OG (W)"},
                        {"entity": "sensor.shellyplus1pm_a0dd6c31333c_switch_0_energy", "name": "Gang EG Gesamt (kWh)"},
                        {"entity": "sensor.shellyplus1pm_7c87ce71a43c_switch_0_energy", "name": "Gang OG Gesamt (kWh)"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🚗 Garage",
                    "entities": [
                        {"entity": "cover.smart_garage_door_2207188115870761070148e1e99a76de_cover", "name": "Garagentor"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🤖 Automationen",
                    "entities": [
                        {"entity": "switch.automation_schlafen_arbeit", "name": "Schlafen (Arbeit)"},
                        {"entity": "switch.automation_schlafen", "name": "Schlafen"},
                        {"entity": "switch.automation_aufwachen_arbeiten", "name": "Aufwachen Mo-Fr"},
                        {"entity": "switch.automation_aufwachen_wochenende", "name": "Aufwachen Wochenende"},
                        {"entity": "switch.automation_aufwachen_spezial", "name": "Aufwachen Spezial"},
                    ]
                }
            ]
        }
    ]
}

# Push to HA
r = requests.post(
    f"{BASE}/api/lovelace/dashboards",
    headers=HEADERS,
    json={
        "url_path": "clawy",
        "title": "Clawy Dashboard",
        "icon": "mdi:crab",
        "show_in_sidebar": True,
        "require_admin": False,
        "mode": "storage"
    }
)
print("Dashboard erstellt:", r.status_code, r.text[:200])

# Now push the view config
r2 = requests.post(
    f"{BASE}/api/lovelace/config",
    headers={**HEADERS, "X-Lovelace-Dashboard": "clawy"},
    json=dashboard
)
print("Config gepusht:", r2.status_code, r2.text[:200])
