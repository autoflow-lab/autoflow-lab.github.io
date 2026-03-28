import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══ FIX 1: "Läuft…" → media_channel oder _radActive ══
old_t = "const titleStr=s?.attributes?.media_title||(playing?'Läuft\u2026':'Bereit');"
new_t = "const titleStr=s?.attributes?.media_title||s?.attributes?.media_channel||(_radActive||null)||(playing?'\u25b6 Läuft':'Bereit');"
if old_t in c: c=c.replace(old_t,new_t); fixes.append("titleStr → channel/_radActive")

# ══ FIX 2: btn-prev/next display:none ══
old_b = "if(_prevBtn){_prevBtn.style.opacity=_isSpot?'1':'0';_prevBtn.style.pointerEvents=_isSpot?'auto':'none';}\n  if(_nextBtn){_nextBtn.style.opacity=_isSpot?'1':'0';_nextBtn.style.pointerEvents=_isSpot?'auto':'none';}"
new_b = "if(_prevBtn){_prevBtn.style.display=_isSpot?'flex':'none';}\n  if(_nextBtn){_nextBtn.style.display=_isSpot?'flex':'none';}"
if old_b in c: c=c.replace(old_b,new_b); fixes.append("btn-prev/next display:none")

# ══ FIX 3: Custom Volume Slider (pointer events, kein native range) ══
# HTML: ersetze input[type=range] container durch custom div
old_vol_html = """<div style="flex:1;position:relative;height:36px;display:flex;align-items:center">
            <div style="position:absolute;left:0;right:0;height:4px;background:rgba(255,255,255,.12);border-radius:2px">
              <div id="vfill" style="height:100%;width:40%;background:linear-gradient(90deg,#0a84ff,rgba(10,132,255,.6));border-radius:2px;transition:width .08s"></div>
              <div id="vthumb" style="position:absolute;left:40%;top:50%;width:18px;height:18px;background:#fff;border-radius:50%;box-shadow:0 1px 6px rgba(0,0,0,.4);transform:translate(-50%,-50%);pointer-events:none;transition:left .08s"></div>
            </div>
            <input type="range" id="vol-range" min="0" max="100" value="40" style="position:absolute;left:0;width:100%;height:100%;opacity:0;cursor:pointer;margin:0;padding:0;touch-action:none">
          </div>"""

new_vol_html = """<div id="vol-container" style="flex:1;position:relative;height:44px;display:flex;align-items:center;cursor:pointer;touch-action:none;-webkit-user-select:none;user-select:none">
            <div style="position:absolute;left:0;right:0;height:4px;background:rgba(255,255,255,.12);border-radius:2px;pointer-events:none">
              <div id="vfill" style="height:100%;width:40%;background:linear-gradient(90deg,#0a84ff,rgba(10,132,255,.6));border-radius:2px"></div>
              <div id="vthumb" style="position:absolute;left:40%;top:50%;width:20px;height:20px;background:#fff;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.45),0 0 0 2px rgba(10,132,255,.3);transform:translate(-50%,-50%);pointer-events:none;transition:box-shadow .1s"></div>
            </div>
            <input type="range" id="vol-range" min="0" max="100" value="40" style="position:absolute;opacity:0;width:0;height:0;pointer-events:none">
          </div>"""

if old_vol_html in c: c=c.replace(old_vol_html,new_vol_html); fixes.append("vol-container custom pointer")
else: print("WARN: vol HTML not matched exactly")

# JS: Ersetze den vol-range event handler durch custom pointer handler
old_vol_js = """  // Volume — opacity:0 native input über visual vfill/vthumb
  (function(){
    var vr=document.getElementById('vol-range');
    if(!vr) return;
    vr.addEventListener('input',function(){
      var p=parseInt(this.value);
      syncVolUI(p);
      _volDrag=true;
      clearTimeout(_volTimer);
      _volTimer=setTimeout(function(){
        svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});
      },250);
    });
    vr.addEventListener('change',function(){
      _volDrag=false;
      svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:parseInt(vr.value)/100*0.6});
    });
    vr.addEventListener('pointerdown',function(){_volDrag=true;});
    vr.addEventListener('pointerup',function(){_volDrag=false;});
    vr.addEventListener('pointercancel',function(){_volDrag=false;});
  })();"""

new_vol_js = """  // Volume — custom pointer handler (100% touch-kompatibel, kein native range needed)
  (function(){
    var vc=document.getElementById('vol-container');
    if(!vc)return;
    var dragging=false;
    function pct(e){
      var r=vc.getBoundingClientRect();
      return Math.max(0,Math.min(100,Math.round((e.clientX-r.left)/r.width*100)));
    }
    function commit(p){
      svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});
    }
    vc.addEventListener('pointerdown',function(e){
      dragging=true;_volDrag=true;
      vc.setPointerCapture(e.pointerId);
      var p=pct(e);syncVolUI(p);
    });
    vc.addEventListener('pointermove',function(e){
      if(!dragging)return;
      var p=pct(e);syncVolUI(p);
    });
    vc.addEventListener('pointerup',function(e){
      if(!dragging)return;
      dragging=false;_volDrag=false;
      var p=pct(e);syncVolUI(p);
      commit(p);
    });
    vc.addEventListener('pointercancel',function(){dragging=false;_volDrag=false;});
  })();"""

if old_vol_js in c: c=c.replace(old_vol_js,new_vol_js); fixes.append("vol custom pointer handler")
else: 
    print("WARN: vol JS not matched — searching...")
    idx = c.find("var vr=document.getElementById('vol-range')")
    if idx>0:
        block_end = c.find("  })();", idx)+7
        c = c[:idx-54] + new_vol_js + c[block_end:]
        fixes.append("vol custom pointer (fallback)")

# ══ FIX 4: Sleep Timer Layout — rechts außen, klarer ══
old_sleep = """          <!-- Sleep Timer inline -->
          <div id="sleep-timer-row" style="margin-left:4px">
            <button id="sleep-timer-btn" title="Sleep-Timer" class="bsml">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
              <span id="sleep-btn-lbl" style="display:none">Sleep</span>
            </button>
            <div id="sleep-pill" style="display:none;align-items:center;gap:4px;background:rgba(10,132,255,.2);border-radius:20px;padding:3px 8px">
              <div id="sleep-pill-dot" style="width:6px;height:6px;border-radius:50%;background:#0a84ff"></div>
              <span id="sleep-pill-txt" style="font-size:.65rem;color:#0a84ff;font-weight:600">00:00</span>
              <button id="sleep-cancel" title="Abbrechen" style="background:none;border:none;color:rgba(255,255,255,.4);font-size:.7rem;cursor:pointer;padding:0 0 0 2px">✕</button>
            </div>
          </div>"""
new_sleep = ""  # entfernen aus btns-row, separat platzieren

# Platziere Sleep Timer als eigene Zeile unter den Controls
if old_sleep in c:
    c = c.replace(old_sleep, "")
    # Suche <div class="btns" und füge Sleep NACH der btns div ein
    after_btns = c.find("        <!-- Volume -->", c.find('id="btn-stop"'))
    new_sleep_row = """        <!-- Sleep Timer — eigene Zeile -->
        <div id="sleep-timer-row" style="display:flex;align-items:center;justify-content:flex-end;gap:8px;margin:-4px 0 8px">
          <button id="sleep-timer-btn" title="Sleep-Timer" style="display:flex;align-items:center;gap:5px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:4px 10px;color:rgba(255,255,255,.5);font-size:.68rem;cursor:pointer;touch-action:manipulation">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <span id="sleep-btn-lbl">Sleep</span>
          </button>
          <div id="sleep-pill" style="display:none;align-items:center;gap:5px;background:rgba(10,132,255,.18);border:1px solid rgba(10,132,255,.3);border-radius:20px;padding:4px 10px">
            <div id="sleep-pill-dot" style="width:6px;height:6px;border-radius:50%;background:#0a84ff;animation:pulse 1s infinite"></div>
            <span id="sleep-pill-txt" style="font-size:.7rem;color:#0a84ff;font-weight:700;min-width:36px">00:00</span>
            <button id="sleep-cancel" style="background:none;border:none;color:rgba(255,255,255,.4);font-size:.75rem;cursor:pointer;padding:0 0 0 4px;touch-action:manipulation">✕</button>
          </div>
        </div>
"""
    c = c[:after_btns] + new_sleep_row + c[after_btns:]
    fixes.append("sleep timer eigene Zeile rechts")

# ══ FIX 5: spec-cv verstecken ══
c = c.replace(
    'style="position:absolute;bottom:0;left:0;width:100%;height:38%;opacity:0;pointer-events:none;transition:opacity 1.2s ease"',
    'style="display:none"'
)
fixes.append("spec-cv hidden")

# ══ FIX 6: Radio Logos — Premium SVG inline statt Google Favicon ══
# Keine externen Logos — eigene schöne SVG-Badges mit Farbe + Abkürzung
LOGO_SVGS = {
    'SRF 1': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#d90000"/><text x="22" y="17" text-anchor="middle" font-size="9" font-weight="900" fill="white" font-family="Arial,sans-serif">SRF</text><text x="22" y="33" text-anchor="middle" font-size="18" font-weight="900" fill="white" font-family="Arial,sans-serif">1</text></svg>',
    'SRF 3': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#e8650a"/><text x="22" y="17" text-anchor="middle" font-size="9" font-weight="900" fill="white" font-family="Arial,sans-serif">SRF</text><text x="22" y="33" text-anchor="middle" font-size="18" font-weight="900" fill="white" font-family="Arial,sans-serif">3</text></svg>',
    'Swiss Pop': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#e11d48"/><text x="22" y="16" text-anchor="middle" font-size="8" font-weight="900" fill="white" font-family="Arial,sans-serif">SWISS</text><text x="22" y="33" text-anchor="middle" font-size="12" font-weight="900" fill="white" font-family="Arial,sans-serif">POP</text></svg>',
    'Kiss FM': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#1a1a2e"/><text x="22" y="19" text-anchor="middle" font-size="11" font-weight="900" fill="#e11d48" font-family="Arial,sans-serif">KISS</text><text x="22" y="33" text-anchor="middle" font-size="10" font-weight="700" fill="white" font-family="Arial,sans-serif">FM</text></svg>',
    'U1 Tirol': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#2563eb"/><text x="22" y="19" text-anchor="middle" font-size="16" font-weight="900" fill="white" font-family="Arial,sans-serif">U1</text><text x="22" y="33" text-anchor="middle" font-size="8" font-weight="600" fill="rgba(255,255,255,.7)" font-family="Arial,sans-serif">TIROL</text></svg>',
    'Melody': '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg"><rect width="44" height="44" rx="10" fill="#7c3aed"/><text x="22" y="20" text-anchor="middle" font-size="9" font-weight="900" fill="white" font-family="Arial,sans-serif">MELO</text><text x="22" y="33" text-anchor="middle" font-size="9" font-weight="900" fill="white" font-family="Arial,sans-serif">DY</text></svg>',
}

import base64
for name, svg in LOGO_SVGS.items():
    b64 = base64.b64encode(svg.encode()).decode()
    data_url = f"data:image/svg+xml;base64,{b64}"
    # Ersetze Google Favicon URL mit data URL
    goog_url = {'SRF 1':'https://www.google.com/s2/favicons?domain=srf.ch&sz=128',
                'SRF 3':'https://www.google.com/s2/favicons?domain=srf3.ch&sz=128',
                'Swiss Pop':'https://www.google.com/s2/favicons?domain=swissradio.ch&sz=128',
                'Kiss FM':'https://www.google.com/s2/favicons?domain=kissfm.de&sz=128',
                'U1 Tirol':'https://u1-radio.at/wp-content/uploads/2022/03/u1_favicon512x512-150x150.png',
                'Melody':'https://cdn.radiobrowser.info/img/radio-melody.png'}.get(name,'')
    if goog_url and goog_url in c:
        c = c.replace(f"logo:'{goog_url}'", f"logo:'{data_url}'")
        fixes.append(f"SVG logo: {name}")

# ══ FIX 7: U1 Tirol + Melody: 'blocked' nur setzen wenn zuhause UND debug NICHT gesetzt ══
# Im Debug-Menü: Radio Blocked Toggle
# Suche blocked:true in CFG
# Füge debug-toggle Logik hinzu: wenn localStorage('dbg-radio-all')==='1' → ignored blocked
rg_build_idx = c.find("document.getElementById('rg').innerHTML=CFG.radio.map")
old_blocked_check = "${r.blocked?'<span style=\"font-size:.4rem;color:rgba(255,255,255,.2);position:absolute;top:5px;right:5px\">🏠</span>':''}"
new_blocked_check = "${r.blocked&&!window._dbgRadioAll?'<span title=\"Nur im Heimnetz\" style=\"position:absolute;top:3px;right:3px;font-size:.5rem\">🏠</span>':''}"
c = c.replace(old_blocked_check, new_blocked_check)

# rb click handler: wenn blocked und NICHT debug → skip
old_rb_click = "if(r.blocked&&!isJanisHome()){toast('\\u26a0\\ufe0f Nur im Heimnetz',2200);return;}"
new_rb_click = "if(r.blocked&&!isJanisHome()&&!window._dbgRadioAll){toast('\\u26a0\\ufe0f Nur im Heimnetz',2200);return;}"
if old_rb_click in c: 
    c=c.replace(old_rb_click,new_rb_click)
    fixes.append("blocked: debug override _dbgRadioAll")
else:
    # Suche alternative
    idx = c.find("Nur im Heimnetz")
    if idx>0:
        print(f"'Nur im Heimnetz' @ {idx}: {c[max(0,idx-80):idx+60]}")

# Debug Menü: Toggle hinzufügen
dbg_toggle = """
  // Debug: Radio alle deblockieren
  window._dbgRadioAll = localStorage.getItem('dbg-radio-all')==='1';
  const dbg_radio_btn = document.getElementById('dbg-radio-toggle');
  if(dbg_radio_btn){
    dbg_radio_btn.textContent = window._dbgRadioAll ? '🔓 Radio: alle AN' : '🔒 Radio: Heimnetz-only';
    dbg_radio_btn.addEventListener('click',function(){
      window._dbgRadioAll = !window._dbgRadioAll;
      localStorage.setItem('dbg-radio-all', window._dbgRadioAll?'1':'0');
      this.textContent = window._dbgRadioAll ? '🔓 Radio: alle AN' : '🔒 Radio: Heimnetz-only';
      document.getElementById('rg').innerHTML=''; buildUI();
      toast(window._dbgRadioAll?'📻 Alle Sender aktiv':'📻 Nur Heimnetz-Sender');
    });
  }
"""
# Debug Menü Button im HTML suchen
dbg_menu = c.find('id="dbg-')
if dbg_menu > 0:
    # Füge button ins Debug Menü ein
    dbg_close = c.find('</div>', dbg_menu)
    # Find the last button in debug menu
    debug_section = c.find('<div id="debug-overlay"')
    if debug_section < 0: debug_section = c.find('id="dbg-panel"')
    if debug_section > 0:
        # Find where the debug section ends and add button
        first_dbg_btn_end = c.find('</button>', debug_section) + 9
        new_dbg_btn = '\n    <button id="dbg-radio-toggle" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:8px;padding:8px 14px;color:#fff;font-size:.8rem;cursor:pointer;touch-action:manipulation;margin-top:6px">🔒 Radio: Heimnetz-only</button>'
        c = c[:first_dbg_btn_end] + new_dbg_btn + c[first_dbg_btn_end:]
        fixes.append("Debug: Radio-unlock button")
    
    # JS hinzufügen
    last_script = c.rfind('</script>')
    c = c[:last_script] + dbg_toggle + c[last_script:]

print("\nFixes angewendet:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fall.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fall.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: vol custom pointer, sleep layout, SVG logos, titleStr, radio debug toggle'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
