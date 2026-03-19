import asyncio, json, websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk"
WS_URL = "ws://192.168.1.123:8123/api/websocket"

# Friendly name fixes: entity_id -> new name
RENAME = {
    "switch.shellyplus1pm_a0dd6c31333c_switch_0": "Shelly Gang EG",
    "switch.shellyplus1pm_7c87ce71a43c_switch_0": "Shelly Gang OG",
    "switch.shelly1_98cdac0ca9b2": "Shelly Büro",
    "switch.shelly1_c45bbe47adb9": "Shelly Kleiderschrank",
    "switch.shelly1_3c6105fdf196": "Shelly Gäste WC",
    "switch.shelly1_98cdac0d4f2e": "Shelly Garten",
    "light.shelly1_c45bbe47adb9": "Licht Kleiderschrank",
    "media_player.spotify_janisss": "Spotify Janis",
    "media_player.nestmini3793": "Nest Mini Wohnzimmer",
    "media_player.nestmini7548": "Nest Mini Küche",
    "media_player.nestmini1153": "Nest Mini Schlafzimmer",
    "media_player.wohnzimmer_2": "Sonos Wohnzimmer",
    "media_player.altes_2": "Sonos Alt",
    "media_player.schlafzimmer_2": "Sonos Schlafzimmer",
    "media_player.wohnzimmer_alm": "Almando Wohnzimmer",
    "media_player.lg_webos_tv_oled65g49ls_2": "LG OLED TV",
    "light.schlafzimmer_2": "Hue Schlafzimmer",
    "light.color_temperature_light_1": "LED Streifen Bett",
    "light.h618a_2": "Govee Küche",
    "light.h61e1": "Govee Wand",
    "light.h618a": "Govee Sofa",
    "sensor.shellyplus1pm_a0dd6c31333c_switch_0_power": "Stromverbrauch Gang EG",
    "sensor.shellyplus1pm_a0dd6c31333c_switch_0_energy": "Energie Gang EG (kWh)",
    "sensor.shellyplus1pm_7c87ce71a43c_switch_0_power": "Stromverbrauch Gang OG",
    "sensor.shellyplus1pm_7c87ce71a43c_switch_0_energy": "Energie Gang OG (kWh)",
}

# Area assignments: entity_id -> area_id
AREAS = {
    # Büro
    "light.buro": "buro",
    "switch.shelly1_98cdac0ca9b2": "buro",
    # Schlafzimmer
    "light.schlafzimmer": "schlafzimmer",
    "light.schlafzimmer_2": "schlafzimmer",
    "light.color_temperature_light_1": "schlafzimmer",
    "media_player.schlafzimmer_2": "schlafzimmer",
    "media_player.nestmini1153": "schlafzimmer",
    # Eltern Schlafzimmer
    "light.eltern_schlafzimmer": "eltern_schlafzimmer",
    "media_player.eltern_schlafzimmer": "eltern_schlafzimmer",
    # Wohnzimmer
    "light.hue_iris": "wohnzimmer",
    "light.hue_play": "wohnzimmer",
    "light.hue_play_l": "wohnzimmer",
    "light.deckenlampe": "wohnzimmer",
    "light.h618a": "wohnzimmer",
    "light.h61e1": "wohnzimmer",
    "media_player.wohnzimmer_2": "wohnzimmer",
    "media_player.wohnzimmer_alm": "wohnzimmer",
    "media_player.denon_avr": "wohnzimmer",
    "media_player.lg_webos_tv_oled65g49ls_2": "wohnzimmer",
    "media_player.nestmini3793": "wohnzimmer",
    "switch.shellyplus1pm_a0dd6c31333c_switch_0": "gang_eg",
    "switch.shellyplus1pm_7c87ce71a43c_switch_0": "gang",
    # Küche
    "light.h618a_2": "kuche",
    "media_player.nestmini7548": "kuche",
    # Garage
    "switch.smart_garage_door_opener_doorenable_1": "garage",
    # Gäste WC
    "switch.shelly1_3c6105fdf196": "gaste_wc",
    # Garten
    "switch.shelly1_98cdac0d4f2e": "garten",
    # Kleiderschrank
    "switch.shelly1_c45bbe47adb9": "schlafzimmer",
    "light.shelly1_c45bbe47adb9": "schlafzimmer",
}

async def main():
    async with websockets.connect(WS_URL) as ws:
        msg = json.loads(await ws.recv())
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        msg = json.loads(await ws.recv())
        assert msg["type"] == "auth_ok"
        print("✅ Verbunden\n")

        # First get all entity registry entries
        await ws.send(json.dumps({"id": 1, "type": "config/entity_registry/list"}))
        resp = json.loads(await ws.recv())
        entities = {e["entity_id"]: e for e in resp.get("result", [])}
        print(f"📋 {len(entities)} Entitäten im Registry\n")

        msg_id = 2
        renamed = 0
        area_set = 0

        for entity_id, new_name in RENAME.items():
            if entity_id in entities:
                await ws.send(json.dumps({
                    "id": msg_id,
                    "type": "config/entity_registry/update",
                    "entity_id": entity_id,
                    "name": new_name
                }))
                resp = json.loads(await ws.recv())
                if resp.get("success"):
                    print(f"  ✏️  {entity_id} → '{new_name}'")
                    renamed += 1
                msg_id += 1

        print(f"\n✅ {renamed} Entitäten umbenannt\n")

        for entity_id, area_id in AREAS.items():
            if entity_id in entities:
                await ws.send(json.dumps({
                    "id": msg_id,
                    "type": "config/entity_registry/update",
                    "entity_id": entity_id,
                    "area_id": area_id
                }))
                resp = json.loads(await ws.recv())
                if resp.get("success"):
                    area_set += 1
                msg_id += 1

        print(f"✅ {area_set} Entitäten einem Raum zugewiesen\n")
        print("🎉 Fertig!")

asyncio.run(main())
