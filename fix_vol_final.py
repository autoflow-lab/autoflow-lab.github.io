import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

# ══════════════════════════════════════════
# 1. Vol-Wrap HTML: opacity:0 input über visual
# ══════════════════════════════════════════
old_vw_start = c.find('<div id="vol-wrap"')
depth = 0
old_vw_end = -1
for i in range(old_vw_start, min(old_vw_start+2000, len(c))):
    if c[i:i+4] == '<div': depth += 1
    elif c[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            old_vw_end = i + 6
            break

old_vw = c[old_vw_start:old_vw_end]
print(f"vol-wrap HTML: {old_vw_start}–{old_vw_end}")

new_vw = '''<div id="vol-wrap" style="padding:8px 0 12px">
            <div style="position:relative;height:44px;display:flex;align-items:center">
              <div style="position:absolute;left:0;right:0;height:5px;background:rgba(255,255,255,.15);border-radius:3px">
                <div id="vfill" style="height:100%;width:40%;background:linear-gradient(90deg,#0a84ff,rgba(10,132,255,.7));border-radius:3px;transition:width .08s"></div>
                <div id="vthumb" style="position:absolute;left:40%;top:50%;width:24px;height:24px;background:#fff;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.45),0 0 0 3px rgba(10,132,255,.3);transform:translate(-50%,-50%);pointer-events:none;transition:left .08s"></div>
              </div>
              <input type="range" id="vol-range" min="0" max="100" value="40"
                style="position:absolute;left:0;width:100%;height:100%;opacity:0;cursor:pointer;margin:0;padding:0;touch-action:none">
            </div>
            <div style="display:flex;justify-content:space-between;padding:0 2px;margin-top:4px">
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Leise</span>
              <span id="vv" style="font-size:.7rem;font-weight:600;color:rgba(255,255,255,.6)">40%</span>
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Laut</span>
            </div>
          </div>'''

c = c.replace(old_vw, new_vw)
print("HTML: vol-wrap ersetzt ✓")

# ══════════════════════════════════════════
# 2. syncVolUI: vfill + vthumb + vv updaten
# ══════════════════════════════════════════
old_sync = """function syncVolUI(pct){
    const vr=document.getElementById('vol-range');
    if(vr){vr.value=pct;vr.style.background='linear-gradient(90deg,#0a84ff '+pct+'%,rgba(255,255,255,.15) '+pct+'%)';}
    const vv=document.getElementById('vv');
    if(vv)vv.textContent=pct+'%';
  }"""

new_sync = """function syncVolUI(pct){
    const fill=document.getElementById('vfill');
    const thumb=document.getElementById('vthumb');
    const vv=document.getElementById('vv');
    const vr=document.getElementById('vol-range');
    if(fill) fill.style.width=pct+'%';
    if(thumb) thumb.style.left=pct+'%';
    if(vv) vv.textContent=pct+'%';
    if(vr) vr.value=pct;
  }"""

if old_sync in c:
    c = c.replace(old_sync, new_sync)
    print("JS: syncVolUI (vfill+vthumb) ✓")
else:
    print("WARN: syncVolUI match failed")
    # Fallback: finde und ersetze
    idx = c.find('function syncVolUI(pct)')
    end = c.find('\n  }', idx) + 4
    c = c[:idx] + new_sync + c[end:]
    print("JS: syncVolUI fallback ✓")

# ══════════════════════════════════════════
# 3. vol-slider CSS entfernen (nicht mehr nötig)
# ══════════════════════════════════════════
old_css = """
/* ── Volume Slider ── */
.vol-slider{
  -webkit-appearance:none;appearance:none;
  width:100%;height:5px;border-radius:3px;outline:none;
  background:linear-gradient(90deg,#0a84ff 40%,rgba(255,255,255,.15) 40%);
  touch-action:none;cursor:pointer;display:block;
}
.vol-slider::-webkit-slider-thumb{
  -webkit-appearance:none;appearance:none;
  width:28px;height:28px;border-radius:50%;background:#fff;
  box-shadow:0 2px 10px rgba(0,0,0,.55),0 0 0 3px rgba(10,132,255,.35);
  cursor:grab;margin-top:-12px;
}
.vol-slider:active::-webkit-slider-thumb{cursor:grabbing;transform:scale(1.1);}
"""
if old_css in c:
    c = c.replace(old_css, '\n')
    print("CSS: vol-slider CSS entfernt ✓")
else:
    print("CSS: vol-slider nicht gefunden (ok)")

# ══════════════════════════════════════════
# 4. vol-range event handler (native input)
# ══════════════════════════════════════════
old_vr_js = """  // Volume — nativer range input (iOS-kompatibel, kein Scroll-Konflikt)
  const _vr=document.getElementById('vol-range');
  if(_vr){
    _vr.addEventListener('input',function(){
      var p=parseInt(this.value);
      syncVolUI(p);
      _volDrag=true;
      clearTimeout(_volTimer);
      _volTimer=setTimeout(function(){
        svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});
      },200);
    });
    _vr.addEventListener('pointerdown',function(){_volDrag=true;});
    _vr.addEventListener('pointerup',function(){
      _volDrag=false;
      svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:parseInt(_vr.value)/100*0.6});
    });
    _vr.addEventListener('pointercancel',function(){_volDrag=false;});
  }"""

new_vr_js = """  // Volume — opacity:0 native input über visual vfill/vthumb
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

if old_vr_js in c:
    c = c.replace(old_vr_js, new_vr_js)
    print("JS: vol-range handler ✓")
else:
    print("WARN: vol-range handler match failed")
    idx = c.find('const _vr=document.getElementById')
    if idx > 0:
        end = c.find('\n  }', idx) + 4
        c = c[:idx-2] + new_vr_js + c[end:]
        print("JS: vol-range handler fallback ✓")

# ══════════════════════════════════════════
# 5. pg-musik: overflow-y explizit sicherstellen
# ══════════════════════════════════════════
# Die .page Klasse hat overflow-y:auto — aber extra sichern
pg_m = c.find('<div class="page" id="pg-musik">')
if pg_m > 0:
    # pg-musik braucht keine Änderung — .page CSS regelt es
    print(f"pg-musik @ {pg_m} (kein overflow fix nötig — .page CSS)")

# ══════════════════════════════════════════
# VERIFY
# ══════════════════════════════════════════
print("\n=== VERIFY ===")
print("  vol-wrap HTML:", 'id="vol-wrap"' in c)
print("  vfill div:", 'id="vfill"' in c)
print("  vthumb div:", 'id="vthumb"' in c)
print("  vol-range opacity:0:", 'opacity:0' in c[c.find('id="vol-range"')-5:c.find('id="vol-range"')+200])
print("  syncVolUI vfill:", 'fill.style.width' in c)
print("  syncVolUI vthumb:", 'thumb.style.left' in c)
print("  vol-slider CSS gone:", '.vol-slider{' not in c)
print("  touch-action:none on input:", "input[type=range]{touch-action:none}" in c)
print("  no vol-swipe album:", '// Volume Swipe (vertikal)' not in c)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fvfinal.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fvfinal.js'], capture_output=True, text=True)
print(f"  JS: {'OK ✓' if r.returncode==0 else 'ERR: '+r.stderr[:200]}")

if r.returncode == 0:
    data = c.encode()
    print(f"\nDeploy: {len(data):,} bytes")
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
    subprocess.run(['git','commit','-m','wz.html: vol opacity:0 overlay, syncVolUI vfill+vthumb, remove vol-slider CSS'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
