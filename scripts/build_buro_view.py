import asyncio, json, websockets

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk'

def icon_btn(icon, top, left, service, data, color='white'):
    """Icon button only (no label - label type not supported in Cast)"""
    return [{
        'type': 'icon',
        'icon': icon,
        'tap_action': {
            'action': 'call-service',
            'service': service,
            'service_data': data,
        },
        'style': {
            'top': top, 'left': left,
            'color': color,
            '--mdc-icon-size': '38px',
            'background': 'rgba(25,25,45,0.85)',
            'border': '1px solid rgba(255,255,255,0.2)',
            'border-radius': '16px',
            'padding': '16px',
            'cursor': 'pointer',
            'transform': 'translate(-50%,-50%)',
        }
    }]

elements = [
    # ── UHRZEIT ──
    {
        'type': 'state-label',
        'entity': 'sensor.time',
        'style': {
            'top': '20%', 'left': '23%',
            'font-size': '86px',
            'font-weight': '100',
            'color': 'white',
            'font-family': 'sans-serif',
            'letter-spacing': '-3px',
            'text-shadow': '0 0 30px rgba(167,139,250,0.6)',
            'transform': 'translate(-50%,-50%)',
        }
    },
    # ── DATUM ──
    {
        'type': 'state-label',
        'entity': 'sensor.date',
        'style': {
            'top': '35%', 'left': '16%',
            'font-size': '13px',
            'color': 'rgba(255,255,255,0.4)',
            'font-family': 'sans-serif',
            'letter-spacing': '2px',
            'transform': 'translate(-50%,-50%)',
        }
    },
    # ── WETTER ICON ──
    {
        'type': 'state-icon',
        'entity': 'weather.forecast_home',
        'style': {
            'top': '14%', 'left': '67%',
            'color': 'white',
            '--mdc-icon-size': '44px',
            'transform': 'translate(-50%,-50%)',
        }
    },
    # ── TEMPERATUR ──
    {
        'type': 'state-label',
        'entity': 'weather.forecast_home',
        'attribute': 'temperature',
        'suffix': '°',
        'style': {
            'top': '14%', 'left': '80%',
            'font-size': '50px',
            'font-weight': '100',
            'color': 'white',
            'font-family': 'sans-serif',
            'transform': 'translate(-50%,-50%)',
        }
    },
    # ── WETTER TEXT ──
    {
        'type': 'state-label',
        'entity': 'weather.forecast_home',
        'style': {
            'top': '30%', 'left': '74%',
            'font-size': '13px',
            'color': 'rgba(255,255,255,0.5)',
            'font-family': 'sans-serif',
            'transform': 'translate(-50%,-50%)',
        }
    },
    # ── MACBOOK AKKU ──
    {
        'type': 'state-label',
        'entity': 'sensor.macbook_air_von_janis_internal_battery_level',
        'prefix': '💻  ',
        'suffix': '%',
        'style': {
            'top': '90%', 'left': '88%',
            'font-size': '15px',
            'color': 'rgba(255,255,255,0.6)',
            'font-family': 'sans-serif',
            'transform': 'translate(-50%,-50%)',
        }
    },
]

# Add icon buttons
elements += icon_btn('mdi:book-open-variant',      '72%', '15%', 'light.turn_on',  {'entity_id': 'light.buro', 'kelvin': 3000, 'brightness': 180})
elements += icon_btn('mdi:coffee',                '72%', '35%', 'light.turn_on',  {'entity_id': 'light.buro', 'kelvin': 2200, 'brightness': 70})
elements += icon_btn('mdi:power',                 '72%', '55%', 'light.turn_off', {'entity_id': 'light.buro'})
elements += icon_btn('mdi:spotify',               '72%', '75%',
    'media_player.play_media',
    {'entity_id': 'media_player.wohnzimmer_alm', 'media_content_id': 'http://stream.srg-ssr.ch/m/drs3/mp3_128', 'media_content_type': 'music'},
    color='#1DB954')

buro_view = {
    'title': 'Buero',
    'path': 'buro',
    'panel': True,
    'cards': [{
        'type': 'picture-elements',
        'image': '/local/buro_bg.png',
        'elements': elements
    }]
}

async def main():
    async with websockets.connect('ws://192.168.1.123:8123/api/websocket') as ws:
        await ws.recv()
        await ws.send(json.dumps({'type': 'auth', 'access_token': TOKEN}))
        await ws.recv()

        await ws.send(json.dumps({'id': 1, 'type': 'lovelace/config', 'url_path': 'clawy-dashboard'}))
        r = json.loads(await ws.recv())
        config = r['result']

        config['views'] = [v for v in config['views'] if v.get('path') != 'buro']
        config['views'].append(buro_view)

        await ws.send(json.dumps({'id': 2, 'type': 'lovelace/config/save', 'url_path': 'clawy-dashboard', 'config': config}))
        r2 = json.loads(await ws.recv())
        print('Saved:', r2.get('success'), r2.get('error'))

asyncio.run(main())
