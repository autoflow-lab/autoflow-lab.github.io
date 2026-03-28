import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══════════════════════════════════════════════════════════
# FIX 1: Film-Szene — Picker ZUERST, kein pre-emptives turn_off
# Vorher: turn_off alle → TV an → Picker (HA-Automation feuert dazwischen → Weiss)
# Nachher: TV an + Shelly/Hue aus → Picker SOFORT zeigen → User wählt → Govees setzen
# ══════════════════════════════════════════════════════════
old_film = """  if(s==='film'){
    // Film: Alle aus außer Govees, TV an → dann Farb-Picker
    CFG.lights.forEach(l=>svc('light','turn_off',{entity_id:l.id}));
    svc('switch','turn_off',{entity_id:'switch.shelly1_98cdac0ca9b2'});
    svc('media_player','turn_on',{entity_id:TV});
    setTimeout(()=>showFilmPicker(),350);
  }"""

new_film = """  if(s==='film'){
    // Film: TV an, Shelly+Hue aus, Govees NICHT vorab ausschalten
    // (verhindert weissen Flash durch HA-Automation die nach TV-an feuert)
    svc('media_player','turn_on',{entity_id:TV});
    svc('switch','turn_off',{entity_id:'switch.shelly1_98cdac0ca9b2'});
    svc('light','turn_off',{entity_id:'light.hue_play_l'});
    // Picker sofort zeigen — Lichter erst nach Mood-Wahl ändern
    setTimeout(()=>showFilmPicker(),200);
  }"""

if old_film in c:
    c = c.replace(old_film, new_film)
    fixes.append("FIX 1: Film-Szene — kein pre-emptives turn_off Govees")
else:
    print("WARN: Film scene nicht gefunden")

# ══════════════════════════════════════════════════════════
# FIX 2: "Hell"-Szene — Govees mit RGB statt color_temp_kelvin
# color_temp_kelvin auf RGB-only Govees → HA mapped zu Weiss
# ══════════════════════════════════════════════════════════
old_hell = """  else if(s==='hell'){
    // Hell: alles an, Tageslicht 4000K
    CFG.lights.forEach(l=>svc('light','turn_on',{entity_id:l.id,brightness_pct:100,color_temp_kelvin:4000}));
    svc('switch','turn_on',{entity_id:'switch.shelly1_98cdac0ca9b2'});
    toast('Volle Helligkeit ☀️');
  }"""

new_hell = """  else if(s==='hell'){
    // Hell: alles an — Govees mit RGB (Warmweiss), Hue mit color_temp
    // Govees sind RGB-only → color_temp_kelvin erzeugt sonst weissen Fallback
    const GOV=['light.h61e1','light.h618a','light.h618a_2'];
    GOV.forEach(id=>svc('light','turn_on',{entity_id:id,brightness_pct:100,rgb_color:[255,220,160]}));
    // Hue + andere Lichter: color_temp ok
    CFG.lights.filter(l=>!GOV.includes(l.id)).forEach(l=>
      svc('light','turn_on',{entity_id:l.id,brightness_pct:100,color_temp_kelvin:4000}));
    svc('switch','turn_on',{entity_id:'switch.shelly1_98cdac0ca9b2'});
    toast('Volle Helligkeit ☀️');
  }"""

if old_hell in c:
    c = c.replace(old_hell, new_hell)
    fixes.append("FIX 2: Hell-Szene — RGB für Govees (kein color_temp Weiss)")
else:
    print("WARN: Hell scene nicht gefunden")

# ══════════════════════════════════════════════════════════
# FIX 3: Film-Picker Mood-Wahl — beim Wählen auch vorher turn_off
# aber erst beim Wählen, nicht beim Öffnen des Pickers
# ══════════════════════════════════════════════════════════
old_mood_apply = """GOVEES.forEach(id=>svc('light','turn_on',{entity_id:id,brightness_pct:m.bri,rgb_color:m.rgb}));
        setTimeout(()=>GOVEES.forEach(id=>svc('light','turn_on',{entity_id:id,brightness_pct:m.bri,rgb_color:m.rgb})),2500);"""

new_mood_apply = """// Erst kurz ausschalten damit keine Übergangs-Weiss durch vorherigen Zustand
        GOVEES.forEach(id=>svc('light','turn_off',{entity_id:id}));
        // Dann nach 300ms mit gewählter Farbe an
        setTimeout(()=>{
          GOVEES.forEach(id=>svc('light','turn_on',{entity_id:id,brightness_pct:m.bri,rgb_color:m.rgb}));
        },300);
        // Re-send nach 2.5s gegen HA-Automation-Override
        setTimeout(()=>GOVEES.forEach(id=>svc('light','turn_on',{entity_id:id,brightness_pct:m.bri,rgb_color:m.rgb})),2800);"""

if old_mood_apply in c:
    c = c.replace(old_mood_apply, new_mood_apply)
    fixes.append("FIX 3: Film-Picker — turn_off dann +300ms turn_on mit Farbe")
else:
    print("WARN: Mood apply nicht gefunden")

# ══════════════════════════════════════════════════════════
# FIX 4: Govee Licht-Kachel manuelles Einschalten 
# Wenn h61e1 per Kachel eingeschaltet wird ohne Farbe → warmes Amber als Default
# ══════════════════════════════════════════════════════════
# Finde den Licht-Toggle Code
# Govee-spezifisch: turn_on ohne rgb → könnte weiss sein
# Lösung: wenn nodim:false und !norgb → last_color aus Attributen lesen, fallback warm

# Das ist im toggleLight Handler
lt_toggle_idx = c.find("function toggleLight(")
if lt_toggle_idx < 0: lt_toggle_idx = c.find("'light','turn_on',{entity_id:eid")
print(f"toggleLight @ {lt_toggle_idx}")

# Suche den spezifischen turn_on ohne Farbe im Tile-Click
for needle in ["svc('light','turn_on',{entity_id:eid}", "svc('light','turn_on',{entity_id:id}"]:
    idx = c.find(needle)
    while idx > 0:
        ctx = c[idx:idx+150]
        if 'rgb' not in ctx and 'color_temp' not in ctx:
            print(f"turn_on ohne Farbe @ {idx}: {ctx[:100]}")
        idx = c.find(needle, idx+1)

print("\nFixes:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/flsc.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/flsc.js'], capture_output=True, text=True)
print(f"\nJS: {'OK ✓' if r.returncode==0 else 'ERR: '+r.stderr[:300]}")

if r.returncode == 0:
    data = c.encode()
    print(f"Deploy: {len(data):,}")
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect('192.168.1.123', port=22, username='hassio', password=creds['SSH_PW'], timeout=15)
    stdin, _ = cl.exec_command('cat > /tmp/_wz.html', timeout=120)[:2]
    for i in range(0, len(data), 16384): stdin.write(data[i:i+16384])
    stdin.channel.shutdown_write()
    time.sleep(15)
    _, o2, _ = cl.exec_command('sudo cp /tmp/_wz.html /config/www/wz.html && wc -c /config/www/wz.html')
    time.sleep(2)
    print("Server:", o2.read().decode().strip())
    cl.close()
    open('/home/node/.openclaw/workspace/projects/fiverr/wz.html','w').write(c)
    subprocess.run(['git','add','-A'], cwd='/home/node/.openclaw/workspace')
    subprocess.run(['git','commit','-m','wz.html: fix white flash - Film picker first, hell scene RGB, mood re-send'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
