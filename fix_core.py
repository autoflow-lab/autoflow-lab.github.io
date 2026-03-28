import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══════════════════════════════════════════════════
# FIX 1: KRITISCH — Light tile toggle benutzt falsche Domain
# switch.shelly wird als svc('light','toggle',..) aufgerufen → fehler
# Fix: entity domain direkt aus id ableiten
# ══════════════════════════════════════════════════
old_dom = "const dom2=CFG.lights.find(l=>l.id===lid)?.domain||'light'; svc(dom2,'toggle',{entity_id:lid});"
new_dom = "svc(lid.split('.')[0],'toggle',{entity_id:lid});"
if old_dom in c:
    c = c.replace(old_dom, new_dom)
    fixes.append("FIX 1: entity domain direkt aus id (switch.toggle, light.toggle)")
else:
    print("WARN: dom2 not found exactly")
    idx = c.find("?.domain||'light'")
    if idx>0: print(f"  found at {idx}: {c[idx-40:idx+60]}")

# ══════════════════════════════════════════════════
# FIX 2: quickRefresh — HTTP-Fetch nicht wenn WS connected
# verhindert dass fetchStates() kurz nach toggle alte Werte überschreibt
# ══════════════════════════════════════════════════
old_qr = """function quickRefresh(){if(window._authFailed)return;[500,1200,2500].forEach(ms=>setTimeout(fetchStates,ms));}"""
new_qr = """function quickRefresh(){
  if(window._authFailed)return;
  // Wenn WS verbunden: WS state_changed reicht, kein HTTP nötig (würde race conditions verursachen)
  if(_wsOk){setTimeout(fetchStates,1500);return;}
  [500,1200,2500].forEach(ms=>setTimeout(fetchStates,ms));
}"""
if old_qr in c:
    c = c.replace(old_qr, new_qr)
    fixes.append("FIX 2: quickRefresh kein Race-Condition wenn WS ok")

# ══════════════════════════════════════════════════
# FIX 3: Nav — Doppel-Markierung entfernen
# nav-slide-pill entfernen, nur .ni::after line behalten
# ══════════════════════════════════════════════════
# nav-slide-pill HTML entfernen
old_pill_html = c[c.find('<div id="nav-slide-pill"'):c.find('</div>', c.find('<div id="nav-slide-pill"'))+6]
if 'nav-slide-pill' in old_pill_html:
    c = c.replace(old_pill_html, '')
    fixes.append("FIX 3a: nav-slide-pill HTML entfernt")

# nav-slide-pill JS (updateNavPill / positionPill) deaktivieren
old_pill_js = c.find('function updateNavPill(')
if old_pill_js < 0: old_pill_js = c.find('navPill')
print(f"navPill in JS @ {c.find('navPill')}")

# Einfacher: CSS nav-slide-pill display:none
if '#nav-slide-pill' in c:
    c = c.replace('#nav-slide-pill{', '#nav-slide-pill{display:none!important;')
    fixes.append("FIX 3b: nav-slide-pill CSS display:none")

# ══════════════════════════════════════════════════
# FIX 4: Wetter Tab — wx-7days wird von fetchWeather befüllt
# Prüfe ob fetchWeather läuft und zeige Debug-Tage hardcoded als Fallback
# ══════════════════════════════════════════════════
# Zeige fetchWeather error handling
fw = c.find('function fetchWeather(')
print(f"\nfetchWeather @ {fw}")
# Add error logging
old_fw_catch = "}).catch(e=>console.warn('weather err:',e));"
if old_fw_catch in c:
    new_fw_catch = """}).catch(e=>{console.warn('weather err:',e);
    // Fallback: zeige Platzhalter im 7-Tage-Widget
    const d7=document.getElementById('wx-7days');
    if(d7&&!d7.innerHTML.trim()){
      d7.innerHTML='<div style="padding:14px;text-align:center;color:rgba(255,255,255,.3);font-size:.75rem">⚠️ Wetterdaten nicht verfügbar</div>';
    }
  });"""
    c = c.replace(old_fw_catch, new_fw_catch)
    fixes.append("FIX 4: weather error fallback")

# ══════════════════════════════════════════════════
# FIX 5: Licht Tab Header aufräumen — lt-bri-meter & lt-global-dimmer kompakter
# ══════════════════════════════════════════════════
# Finde den Header des Licht-Tabs (zwischen label und lt-groups)
licht_start = c.find('<div class="page" id="pg-licht">')
licht_label_end = c.find('<span class="lbl">Licht</span>', licht_start) + 30

# Was steht zwischen label und erstem .c oder .lg?
first_group = c.find('id="lt-groups"', licht_start)
header_html = c[licht_label_end:first_group]
print(f"\nLicht header ({len(header_html)} chars):")
print(header_html[:500])

# ══════════════════════════════════════════════════
# FIX 6: effOn — Robuster ohne 4s-Pending-Problem
# Problem: falscher initialer State → pending falsch gesetzt → 4s hängt
# Lösung: pending auf 2.5s reduzieren, WS state_changed cleared pending sofort
# ══════════════════════════════════════════════════
old_effon = "function effOn(id){const p=_pending[id];return(p&&p.until>Date.now())?p.on:_S[id]?.state==='on';}"
new_effon = """function effOn(id){
  const p=_pending[id];
  if(p&&p.until>Date.now()) return p.on;
  const st=_S[id]?.state;
  return st==='on';  // direct HA state
}"""
if old_effon in c:
    c = c.replace(old_effon, new_effon)
    fixes.append("FIX 6: effOn direkt, klar")

# Pending Dauer von 4000 auf 2500ms reduzieren
c = c.replace('_pending[lid]={on:newOn,until:Date.now()+4000};',
              '_pending[lid]={on:newOn,until:Date.now()+2500};')
fixes.append("FIX 6b: pending 4s→2.5s")

# WS state_changed: pending sofort löschen wenn state bestätigt
old_ws_sc = """const ns=d.event?.data?.new_state;
            if(ns){_S[ns.entity_id]=ns;}
            if(typeof updateAll==='function')setTimeout(updateAll,0);"""
new_ws_sc = """const ns=d.event?.data?.new_state;
            if(ns){
              _S[ns.entity_id]=ns;
              // Pending sofort löschen wenn HA Zustand bestätigt
              const p=_pending[ns.entity_id];
              if(p&&p.on===(ns.state==='on')) delete _pending[ns.entity_id];
            }
            if(typeof updateAll==='function')setTimeout(updateAll,0);"""
if old_ws_sc in c:
    c = c.replace(old_ws_sc, new_ws_sc)
    fixes.append("FIX 6c: WS state_changed löscht pending wenn bestätigt")
else:
    # Alternative suche
    idx = c.find('_S[ns.entity_id]=ns;')
    print(f"\n_S[ns.entity_id]=ns @ {idx}: {c[idx:idx+100]}")

print("\nFixes:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fcore.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fcore.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: fix light domain, pending→WS, nav double, quickRefresh race, effOn'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
