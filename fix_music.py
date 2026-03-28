import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

# ══════════════════════════════════════════════════════
# SCHRITT 1: CSS — vol-slider + range input Styling
# ══════════════════════════════════════════════════════
vol_css = """
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
if '.vol-slider{' not in c:
    c = c.replace('</style>', vol_css + '</style>', 1)
    print("CSS: vol-slider hinzugefügt")

# ══════════════════════════════════════════════════════
# SCHRITT 2: HTML — ersetze vol-wrap mit native range
# ══════════════════════════════════════════════════════
# Finde alten vol-wrap start
vw_start = c.find('<div id="vol-wrap"')
# Finde Ende (schliessende </div> auf gleicher Ebene)
depth = 0
vw_end = -1
for i in range(vw_start, min(vw_start+3000, len(c))):
    if c[i:i+4] == '<div': depth += 1
    elif c[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            vw_end = i + 6
            break

print(f"vol-wrap: {vw_start} – {vw_end} ({vw_end-vw_start} chars)")
old_vw = c[vw_start:vw_end]

new_vw = '''<div id="vol-wrap" style="padding:6px 0 10px">
            <input type="range" class="vol-slider" id="vol-range"
              min="0" max="100" value="40"
              style="width:100%;margin:10px 0 6px">
            <div style="display:flex;justify-content:space-between;padding:0 2px">
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Leise</span>
              <span id="vv" style="font-size:.7rem;font-weight:600;color:rgba(255,255,255,.6)">40%</span>
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Laut</span>
            </div>
          </div>'''

c = c.replace(old_vw, new_vw)
print(f"HTML: vol-wrap ersetzt ({len(old_vw)} → {len(new_vw)} chars)")

# ══════════════════════════════════════════════════════
# SCHRITT 3: syncVolUI updaten
# ══════════════════════════════════════════════════════
old_sync = """function syncVolUI(pct){
    const fill=document.getElementById('vfill');
    const thumb=document.getElementById('vthumb');
    const vv=document.getElementById('vv');
    if(fill)fill.style.width=pct+'%';
    if(thumb){thumb.style.left=pct+'%';}
    if(vv)vv.textContent=pct+'%';
    if(volRange)volRange.value=pct;
  }"""

new_sync = """function syncVolUI(pct){
    const vr=document.getElementById('vol-range');
    if(vr){vr.value=pct;vr.style.background='linear-gradient(90deg,#0a84ff '+pct+'%,rgba(255,255,255,.15) '+pct+'%)';}
    const vv=document.getElementById('vv');
    if(vv)vv.textContent=pct+'%';
  }"""

if old_sync in c:
    c = c.replace(old_sync, new_sync)
    print("JS: syncVolUI aktualisiert")
else:
    print("WARN: syncVolUI exact match failed")

# ══════════════════════════════════════════════════════
# SCHRITT 4: vol-track JS ersetzen mit nativem Handler
# ══════════════════════════════════════════════════════
old_vt_js = """  // Volume Slider via vol-track (touch-action:none auf Track, pan-y auf Wrapper)
  const volTrack=document.getElementById('vol-track');
  if(volTrack){
    let _volDrag=false;
    function _vpct(cx){const r=volTrack.getBoundingClientRect();return Math.max(0,Math.min(100,Math.round((cx-r.left)/r.width*100)));}
    volTrack.addEventListener('pointerdown',function(e){e.stopPropagation();_volDrag=true;volTrack.setPointerCapture(e.pointerId);syncVolUI(_vpct(e.clientX));});
    volTrack.addEventListener('pointermove',function(e){if(!_volDrag)return;var p=_vpct(e.clientX);syncVolUI(p);clearTimeout(_volTimer);_volTimer=setTimeout(function(){svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});},150);});
    volTrack.addEventListener('pointerup',function(e){if(!_volDrag)return;_volDrag=false;var p=_vpct(e.clientX);syncVolUI(p);svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});});
    volTrack.addEventListener('pointercancel',function(){_volDrag=false;});
  }"""

new_vt_js = """  // Volume — nativer range input (iOS-kompatibel, kein Scroll-Konflikt)
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

if old_vt_js in c:
    c = c.replace(old_vt_js, new_vt_js)
    print("JS: vol-track → nativer Handler")
else:
    print("WARN: vol-track JS exact match failed — suche alternativ")
    vt2 = c.find('const volTrack=document.getElementById')
    if vt2 > 0:
        end2 = c.find('\n  }', vt2) + 4
        print(f"  Fallback: ersetze {vt2}–{end2}")
        c = c[:vt2] + new_vt_js.strip() + c[end2:]
        print("  Fallback ersetzt")

# ══════════════════════════════════════════════════════
# SCHRITT 5: input[type=range] touch-action fix (global CSS override)
# ══════════════════════════════════════════════════════
# Der * selector setzt touch-action:manipulation — das bricht range inputs
# range inputs brauchen touch-action:none für horizontales Ziehen
if 'input[type=range]{touch-action:none' not in c:
    c = c.replace(
        'touch-action:manipulation}',
        'touch-action:manipulation}\ninput[type=range]{touch-action:none}',
        1
    )
    print("CSS: input[type=range] touch-action:none")

# ══════════════════════════════════════════════════════
# VERIFIZIEREN
# ══════════════════════════════════════════════════════
print("\n=== VERIFY ===")
print("  vol-slider CSS:", '.vol-slider{' in c)
print("  vol-range HTML:", 'id="vol-range"' in c and 'class="vol-slider"' in c)
print("  vv HTML:", 'id="vv"' in c)
print("  vfill/vthumb gone:", 'id="vfill"' not in c and 'id="vthumb"' not in c)
print("  syncVolUI native:", 'vr.style.background=' in c)
print("  _vr handler:", "_vr=document.getElementById('vol-range')" in c)
print("  no vol-track:", 'id="vol-track"' not in c)
print("  no touch-action:none div:", 'height:44px;display:flex;align-items:center;touch-action:none' not in c)
print("  input range no touch-manipulation:", 'input[type=range]{touch-action:none}' in c)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fmusic.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fmusic.js'], capture_output=True, text=True)
print(f"  JS: {'OK' if r.returncode==0 else 'ERR: '+r.stderr[:300]}")

if r.returncode == 0:
    data = c.encode()
    print(f"\nDeploy: {len(data):,} bytes")
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect('192.168.1.123', port=22, username='hassio', password=creds['SSH_PW'], timeout=15)
    stdin, _ = cl.exec_command('cat > /tmp/_wz.html', timeout=120)[:2]
    for i in range(0, len(data), 16384):
        stdin.write(data[i:i+16384])
    stdin.channel.shutdown_write()
    time.sleep(15)
    _, o2, _ = cl.exec_command('sudo cp /tmp/_wz.html /config/www/wz.html && wc -c /config/www/wz.html')
    time.sleep(2)
    print("Server:", o2.read().decode().strip())
    cl.close()
    open('/home/node/.openclaw/workspace/projects/fiverr/wz.html','w').write(c)
    subprocess.run(['git','add','-A'], cwd='/home/node/.openclaw/workspace')
    subprocess.run(['git','commit','-m','wz.html: native vol range input, no more touch-action:none div blocking scroll'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
