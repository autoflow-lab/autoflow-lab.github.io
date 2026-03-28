import subprocess, re, paramiko, time
creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

# ======================================================
# FIX A: Volume HTML — ersetze +/- Buttons durch Slider
# ======================================================
old_vol_html = '<div style="display:flex;align-items:center;gap:10px;padding:6px 0"><button id="vol-down" style="width:46px;height:46px;border-radius:50%;border:none;background:rgba(255,255,255,.12);color:#fff;font-size:1.5rem;line-height:1;display:flex;align-items:center;justify-content:center;touch-action:manipulation;cursor:pointer;flex-shrink:0">&#8722;</button><div style="flex:1;position:relative;height:5px;background:rgba(255,255,255,.12);border-radius:3px;overflow:hidden"><div id="vfill" style="height:100%;width:40%;background:#0a84ff;border-radius:3px;transition:width .2s"></div></div><span id="vv" style="font-size:.78rem;font-weight:600;color:rgba(255,255,255,.55);min-width:34px;text-align:center">40%</span><button id="vol-up" style="width:46px;height:46px;border-radius:50%;border:none;background:rgba(255,255,255,.12);color:#fff;font-size:1.5rem;line-height:1;display:flex;align-items:center;justify-content:center;touch-action:manipulation;cursor:pointer;flex-shrink:0">+</button><input id="vol-range" type="range" min="0" max="100" value="40" style="display:none"></div>'

new_vol_html = '''<div id="vol-wrap" style="padding:12px 0 8px;touch-action:pan-y">
            <div id="vol-track" style="position:relative;height:5px;background:rgba(255,255,255,.15);border-radius:3px;margin:16px 0;touch-action:none;cursor:pointer">
              <div id="vfill" style="height:100%;width:40%;background:linear-gradient(90deg,rgba(10,132,255,.8),#0a84ff);border-radius:3px;pointer-events:none"></div>
              <div id="vthumb" style="position:absolute;left:40%;top:50%;width:26px;height:26px;border-radius:50%;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.5),0 0 0 3px rgba(10,132,255,.3);transform:translate(-50%,-50%);touch-action:none;pointer-events:none"></div>
            </div>
            <div style="display:flex;justify-content:space-between;padding:0 1px">
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Leise</span>
              <span id="vv" style="font-size:.68rem;font-weight:600;color:rgba(255,255,255,.5)">40%</span>
              <span style="font-size:.62rem;color:rgba(255,255,255,.28)">Laut</span>
            </div>
            <input id="vol-range" type="range" min="0" max="100" value="40" style="display:none">
          </div>'''

if old_vol_html in c:
    c = c.replace(old_vol_html, new_vol_html)
    print("Fix A: Vol Slider HTML OK")
else:
    print("Fix A: HTML nicht gefunden!")

# ======================================================
# FIX B: Volume JS — ersetze +/- Handler durch Track-Drag
# ======================================================
old_vol_js_start = '  // Volume +/- Buttons\n  const volDown=document.getElementById'
vol_js_idx = c.find(old_vol_js_start)
if vol_js_idx < 0:
    # Versuche Variante
    old_vol_js_start = '  // Volume +/- (kein Slider'
    vol_js_idx = c.find(old_vol_js_start)
    
print(f"Vol JS @ {vol_js_idx}")
if vol_js_idx > 0:
    # Finde Ende des Blocks
    vol_js_end = c.find('\n  function confirmVol(', vol_js_idx)
    if vol_js_end < 0:
        vol_js_end = c.find('\n  // ──', vol_js_idx + 100)
    print(f"Vol JS end @ {vol_js_end}")
    old_vol_js = c[vol_js_idx:vol_js_end]
    print(f"Ersetze {len(old_vol_js)} chars Vol JS")
    
    new_vol_js = """  // Volume Slider via vol-track (nur Track-Bereich, kein Scroll-Konflikt)
  const volTrack=document.getElementById('vol-track');
  if(volTrack){
    let _vDrag=false;
    function _vpct(clientX){
      const r=volTrack.getBoundingClientRect();
      return Math.max(0,Math.min(100,Math.round((clientX-r.left)/r.width*100)));
    }
    volTrack.addEventListener('pointerdown',function(e){
      e.stopPropagation();
      _vDrag=true;
      volTrack.setPointerCapture(e.pointerId);
      syncVolUI(_vpct(e.clientX));
    });
    volTrack.addEventListener('pointermove',function(e){
      if(!_vDrag)return;
      var pct=_vpct(e.clientX);
      syncVolUI(pct);
      clearTimeout(_volTimer);
      _volTimer=setTimeout(function(){svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:pct/100*0.6});},150);
    });
    volTrack.addEventListener('pointerup',function(e){
      if(!_vDrag)return;
      _vDrag=false;
      var pct=_vpct(e.clientX);
      syncVolUI(pct);
      svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:pct/100*0.6});
    });
    volTrack.addEventListener('pointercancel',function(){_vDrag=false;});
  }
"""
    c = c.replace(old_vol_js, new_vol_js)
    print("Fix B: Vol Slider JS OK")

# ======================================================
# FIX C: syncVolUI — vthumb Position updaten
# ======================================================
old_sync = """function syncVolUI(pct){
    const fill=document.getElementById('vfill');
    const thumb=document.getElementById('vthumb');
    const vv=document.getElementById('vv');
    if(fill)fill.style.width=pct+'%';
    if(thumb)thumb.style.left=pct+'%';
    if(vv)vv.textContent=pct+'%';
    if(volRange)volR"""

# Finde vollstaendige Funktion
sync_idx = c.find('function syncVolUI(pct){')
if sync_idx > 0:
    sync_end = c.find('\n  }', sync_idx) + 4
    old_sync_full = c[sync_idx:sync_end]
    new_sync_full = old_sync_full.replace(
        "if(thumb)thumb.style.left=pct+'%';",
        "if(thumb){thumb.style.left=pct+'%';}"
    )
    c = c.replace(old_sync_full, new_sync_full)
    print("Fix C: syncVolUI OK")

# ======================================================
# FIX D: vol-wrap scroll-protection
# vol-wrap hat touch-action:pan-y, vol-track hat touch-action:none
# Das ist correct: scrollen geht an Browser, track-drag geht an JS
# ======================================================

# PRÜFEN
print("\nVerify:")
print("  vol-track in HTML:", 'id="vol-track"' in c)
print("  vol-wrap in HTML:", 'id="vol-wrap"' in c)
print("  vthumb:", 'id="vthumb"' in c)
print("  volTrack JS:", 'volTrack=document.getElementById' in c)
print("  vol-down gone:", 'id="vol-down"' not in c)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/ffinal.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/ffinal.js'], capture_output=True, text=True)
print("JS:", "OK" if r.returncode==0 else "ERR:"+r.stderr[:400])

if r.returncode==0:
    data=c.encode()
    print("size:", len(data))
    cl=paramiko.SSHClient(); cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect('192.168.1.123',port=22,username='hassio',password=creds['SSH_PW'],timeout=15)
    stdin,_=cl.exec_command('cat > /tmp/_wz.html',timeout=120)[:2]
    for i in range(0,len(data),16384): stdin.write(data[i:i+16384])
    stdin.channel.shutdown_write(); time.sleep(15)
    _,o2,_=cl.exec_command('sudo cp /tmp/_wz.html /config/www/wz.html && wc -c /config/www/wz.html')
    time.sleep(2); print("deployed:", o2.read().decode().strip())
    cl.close()
    open('/home/node/.openclaw/workspace/projects/fiverr/wz.html','w').write(c)
    subprocess.run(['git','add','-A'],cwd='/home/node/.openclaw/workspace')
    subprocess.run(['git','commit','-m','wz.html: vol-track slider (touch-action:none auf Track, pan-y auf Wrapper)'],cwd='/home/node/.openclaw/workspace')
    print("DONE")
