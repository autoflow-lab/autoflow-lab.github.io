import asyncio, json, websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk"
WS_URL = "ws://192.168.1.123:8123/api/websocket"

DASHBOARD_CONFIG = {
    "title": "Zuhause 🏠",
    "views": [
        {
            "title": "Übersicht",
            "icon": "mdi:home",
            "path": "overview",
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
                        {"type": "light", "entity": "light.hue_play_l", "name": "Hue Play L"},
                        {"type": "light", "entity": "light.color_temperature_light_1", "name": "LED Bett"},
                        {"type": "light", "entity": "light.h618a", "name": "Sofa"},
                        {"type": "light", "entity": "light.h618a_2", "name": "Küche"},
                    ]
                },
                {
                    "type": "markdown",
                    "content": "## 🔌 Schalter"
                },
                {
                    "type": "entities",
                    "entities": [
                        {"entity": "switch.shelly1_98cdac0ca9b2", "name": "💡 Shelly Büro"},
                        {"entity": "switch.shelly1_3c6105fdf196", "name": "🚽 Shelly Gäste WC"},
                        {"entity": "switch.shelly1_98cdac0d4f2e", "name": "🌿 Shelly Garten"},
                        {"entity": "switch.shellyplus1pm_a0dd6c31333c_switch_0", "name": "Gang EG"},
                        {"entity": "switch.shellyplus1pm_7c87ce71a43c_switch_0", "name": "Gang OG"},
                    ]
                }
            ]
        },
        {
            "title": "Medien",
            "icon": "mdi:music",
            "path": "media",
            "cards": [
                {"type": "media-control", "entity": "media_player.spotify_janisss", "name": "🎵 Spotify"},
                {"type": "media-control", "entity": "media_player.nest", "name": "🔊 Google Nest"},
                {"type": "media-control", "entity": "media_player.denon_avr", "name": "📻 DENON AVR"},
                {"type": "media-control", "entity": "media_player.lg_webos_tv_oled65g49ls_2", "name": "📺 LG OLED TV"},
                {
                    "type": "entities",
                    "title": "Weitere Lautsprecher",
                    "entities": [
                        {"entity": "media_player.wohnzimmer_2", "name": "Wohnzimmer"},
                        {"entity": "media_player.schlafzimmer_2", "name": "Schlafzimmer"},
                        {"entity": "media_player.eltern_schlafzimmer", "name": "Eltern SZ"},
                        {"entity": "media_player.nestmini3793", "name": "Nest Mini 1"},
                        {"entity": "media_player.nestmini7548", "name": "Nest Mini 2"},
                    ]
                }
            ]
        },
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
                            "type": "grid", "columns": 3, "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.schlafzimmer_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                                {"type": "button", "entity": "scene.schlafzimmer_lesen", "name": "Lesen", "icon": "mdi:book-open"},
                                {"type": "button", "entity": "scene.schlafzimmer_netflix", "name": "Netflix", "icon": "mdi:television-play"},
                                {"type": "button", "entity": "scene.schlafzimmer_nachtlicht", "name": "Nachtlicht", "icon": "mdi:weather-night"},
                                {"type": "button", "entity": "scene.schlafzimmer_konzentrieren", "name": "Fokus", "icon": "mdi:brain"},
                                {"type": "button", "entity": "scene.schlafzimmer_chill", "name": "Chill", "icon": "mdi:music-note"},
                            ]
                        }
                    ]
                },
                {
                    "type": "vertical-stack",
                    "cards": [
                        {"type": "markdown", "content": "## 🛏️ Eltern Schlafzimmer"},
                        {
                            "type": "grid", "columns": 3, "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_lesen", "name": "Lesen", "icon": "mdi:book-open"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_nachtlicht", "name": "Nachtlicht", "icon": "mdi:weather-night"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_konzentrieren", "name": "Fokus", "icon": "mdi:brain"},
                                {"type": "button", "entity": "scene.eltern_schlafzimmer_gedimmt", "name": "Gedimmt", "icon": "mdi:brightness-4"},
                            ]
                        }
                    ]
                },
                {
                    "type": "vertical-stack",
                    "cards": [
                        {"type": "markdown", "content": "## 🖥️ Büro"},
                        {
                            "type": "grid", "columns": 2, "square": True,
                            "cards": [
                                {"type": "button", "entity": "scene.buro_read", "name": "Lesen", "icon": "mdi:book-open"},
                                {"type": "button", "entity": "scene.buro_entspannen", "name": "Entspannen", "icon": "mdi:sofa"},
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Status",
            "icon": "mdi:information",
            "path": "status",
            "cards": [
                {
                    "type": "entities",
                    "title": "📱 Geräte & Akku",
                    "entities": [
                        {"entity": "sensor.iphone_von_janis_battery_level_2", "name": "iPhone"},
                        {"entity": "sensor.macbook_air_von_janis_internal_battery_level", "name": "MacBook Air"},
                        {"entity": "sensor.smarthome_display_battery_level", "name": "SmartHome Display"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🖨️ Druckerpatronen",
                    "entities": [
                        {"entity": "sensor.hp_officejet_pro_8020_series_black_cartridge_2", "name": "⬛ Schwarz"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_cyan_cartridge_2", "name": "🔵 Cyan"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_magenta_cartridge_2", "name": "🔴 Magenta"},
                        {"entity": "sensor.hp_officejet_pro_8020_series_yellow_cartridge_2", "name": "🟡 Gelb"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "⚡ Stromverbrauch",
                    "entities": [
                        {"entity": "sensor.shellyplus1pm_a0dd6c31333c_switch_0_power", "name": "Gang EG (W)"},
                        {"entity": "sensor.shellyplus1pm_7c87ce71a43c_switch_0_power", "name": "Gang OG (W)"},
                    ]
                },
                {
                    "type": "entities",
                    "title": "🌐 Netzwerk",
                    "entities": [
                        {"entity": "binary_sensor.sagemcom_f3896lg_wan_status", "name": "Internet"},
                        {"entity": "sensor.sagemcom_f3896lg_externe_ip", "name": "Externe IP"},
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
                    ]
                },
            ]
        }
    ]
}

async def main():
    async with websockets.connect(WS_URL) as ws:
        # Auth flow
        msg = json.loads(await ws.recv())
        assert msg["type"] == "auth_required"
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        msg = json.loads(await ws.recv())
        assert msg["type"] == "auth_ok", f"Auth failed: {msg}"
        print("✅ Authentifiziert")

        # Step 1: Create new dashboard
        await ws.send(json.dumps({
            "id": 1,
            "type": "lovelace/dashboards/create",
            "url_path": "clawy-dashboard",
            "title": "Clawy 🦀",
            "icon": "mdi:home-automation",
            "show_in_sidebar": True,
            "require_admin": False,
            "mode": "storage"
        }))
        resp = json.loads(await ws.recv())
        print("Dashboard erstellt:", resp.get("success"), resp.get("error", ""))

        # Step 2: Save config to that dashboard
        await ws.send(json.dumps({
            "id": 2,
            "type": "lovelace/config/save",
            "url_path": "clawy-dashboard",
            "config": DASHBOARD_CONFIG
        }))
        resp = json.loads(await ws.recv())
        print("Config gespeichert:", resp.get("success"), resp.get("error", ""))

asyncio.run(main())
