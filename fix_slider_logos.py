import subprocess, re, paramiko, time, base64

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══════════════════════════════════════════════════════
# FIX 1: Volume Slider — Touch Events statt Pointer Events
# iOS Safari: setPointerCapture funktioniert nicht zuverlässig
# touchstart {passive:false} + preventDefault() ist der iOS-Standard
# ══════════════════════════════════════════════════════
old_vol_js = """  // Volume — custom pointer handler (100% touch-kompatibel, kein native range needed)
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

new_vol_js = """  // Volume — Touch + Mouse Events (iOS-sicher, passive:false für e.preventDefault)
  (function(){
    var vc=document.getElementById('vol-container');
    if(!vc)return;
    var dragging=false,lastP=40;
    function getPct(clientX){
      var r=vc.getBoundingClientRect();
      return Math.max(0,Math.min(100,Math.round((clientX-r.left)/r.width*100)));
    }
    function commit(p){
      lastP=p;
      svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:p/100*0.6});
    }
    // ── Touch Events (iOS) ──
    vc.addEventListener('touchstart',function(e){
      e.preventDefault(); // verhindert Scroll während Slider
      dragging=true;_volDrag=true;
      var p=getPct(e.touches[0].clientX);
      syncVolUI(p);
    },{passive:false});
    vc.addEventListener('touchmove',function(e){
      e.preventDefault();
      if(!dragging)return;
      var p=getPct(e.touches[0].clientX);
      syncVolUI(p);
    },{passive:false});
    vc.addEventListener('touchend',function(e){
      dragging=false;_volDrag=false;
      var p=getPct(e.changedTouches[0].clientX);
      syncVolUI(p);commit(p);
    },{passive:false});
    vc.addEventListener('touchcancel',function(){dragging=false;_volDrag=false;});
    // ── Mouse Events (Desktop) ──
    vc.addEventListener('mousedown',function(e){
      dragging=true;_volDrag=true;
      var p=getPct(e.clientX);syncVolUI(p);
      function onMove(e){if(dragging){var p=getPct(e.clientX);syncVolUI(p);}}
      function onUp(e){dragging=false;_volDrag=false;var p=getPct(e.clientX);syncVolUI(p);commit(p);document.removeEventListener('mousemove',onMove);document.removeEventListener('mouseup',onUp);}
      document.addEventListener('mousemove',onMove);
      document.addEventListener('mouseup',onUp);
    });
  })();"""

if old_vol_js in c:
    c = c.replace(old_vol_js, new_vol_js)
    fixes.append("FIX 1: Volume → Touch Events (passive:false, preventDefault)")
else:
    print("WARN: vol JS nicht gefunden, suche Alternative...")
    idx = c.find("// Volume — custom pointer handler")
    if idx > 0:
        end = c.find("  })();", idx) + 7
        c = c[:idx] + new_vol_js + c[end:]
        fixes.append("FIX 1: vol touch events (fallback)")

# ══════════════════════════════════════════════════════
# FIX 2: Radio Logo + Emoji Bug — display:none ohne Semicolon
# Bug: style="...;display:nonedisplay:flex..." → beide sichtbar
# ══════════════════════════════════════════════════════
old_rb_html = """      <div class="rbico" style="background:rgba(${r.r},.15);border:1px solid rgba(${r.r},.25);position:relative;overflow:hidden">
        ${r.logo?`<img src="${r.logo}" alt="${r.n}" style="width:100%;height:100%;object-fit:contain;border-radius:10px;image-rendering:auto" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`:''}
        <span style="font-size:1.3rem;${r.logo?'display:none':''}display:flex;align-items:center;justify-content:center;width:100%;height:100%">${_radioEmoji[r.n]||'📻'}</span>
      </div>"""

new_rb_html = """      <div class="rbico" style="background:rgba(${r.r},.15);border:1px solid rgba(${r.r},.25);display:flex;align-items:center;justify-content:center;overflow:hidden">
        ${r.logo
          ?`<img src="${r.logo}" alt="${r.n}" style="width:100%;height:100%;object-fit:cover;border-radius:10px" onerror="this.style.display='none'">`
          :`<span style="font-size:1.5rem;line-height:1">${_radioEmoji[r.n]||'📻'}</span>`
        }
      </div>"""

if old_rb_html in c:
    c = c.replace(old_rb_html, new_rb_html)
    fixes.append("FIX 2: rbico — nur Logo ODER Emoji, kein Overlap")
else:
    print("WARN: rbico HTML nicht gefunden")
    idx = c.find("onerror=\"this.style.display='none';this.nextElementSibling")
    if idx > 0: print(f"  ähnlich @ {idx}: {c[idx-50:idx+100]}")

# ══════════════════════════════════════════════════════
# FIX 3: Track-Name grösser + besser positioniert
# ══════════════════════════════════════════════════════
old_title_style = 'class="nptitle" id="np-t" style="font-size:.92rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;line-height:1.25"'
new_title_style = 'class="nptitle" id="np-t" style="font-size:1.15rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;line-height:1.2;letter-spacing:-.3px"'
if old_title_style in c:
    c = c.replace(old_title_style, new_title_style)
    fixes.append("FIX 3: Track-Titel grösser (1.15rem)")

# ══════════════════════════════════════════════════════
# FIX 4: Sleep Timer — kleine Pill in Ecke (top-right des Cards)
# ══════════════════════════════════════════════════════
old_sleep = """        <!-- Sleep Timer — eigene Zeile -->
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
        </div>"""

new_sleep = """        <!-- Sleep Timer — kleine Pill rechts oben am Card-Rand -->
        <div id="sleep-timer-row" style="position:absolute;top:10px;right:12px;z-index:5;display:flex;gap:6px;align-items:center">
          <button id="sleep-timer-btn" title="Sleep-Timer" style="display:flex;align-items:center;gap:3px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:3px 8px 3px 6px;color:rgba(255,255,255,.4);font-size:.6rem;cursor:pointer;touch-action:manipulation;transition:background .2s,color .2s">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <span id="sleep-btn-lbl">Sleep</span>
          </button>
          <div id="sleep-pill" style="display:none;align-items:center;gap:4px;background:rgba(10,132,255,.2);border:1px solid rgba(10,132,255,.4);border-radius:20px;padding:3px 8px">
            <div id="sleep-pill-dot" style="width:5px;height:5px;border-radius:50%;background:#0a84ff;animation:pulse 1.2s ease-in-out infinite"></div>
            <span id="sleep-pill-txt" style="font-size:.65rem;color:#0a84ff;font-weight:700;min-width:30px">00:00</span>
            <button id="sleep-cancel" style="background:none;border:none;color:rgba(255,255,255,.3);font-size:.7rem;cursor:pointer;padding:0 0 0 2px;touch-action:manipulation;line-height:1">✕</button>
          </div>
        </div>"""

if old_sleep in c:
    c = c.replace(old_sleep, new_sleep)
    fixes.append("FIX 4: Sleep Timer — absolute Ecke top-right")
else:
    print("WARN: sleep timer row nicht gefunden")
    idx = c.find('id="sleep-timer-row"')
    print(f"  @ {idx}: {c[idx:idx+100]}")

# ══════════════════════════════════════════════════════
# FIX 5: Premium EQ Visualizer — CSS Wellen die gut aussehen
# Größere Bars, glow, Apple-Stil
# ══════════════════════════════════════════════════════
# EQ Container in der Now-Playing Card größer machen
old_eq_container = '<!-- EQ Bars -->\n            <div class="eq" id="eq" style="margin-top:5px"><i></i><i></i><i></i><i></i><i></i></div>'
new_eq_container = '''<!-- EQ Visualizer — Lottie-Style Wellen -->
            <div class="eq" id="eq" style="margin-top:8px;height:28px"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'''
if old_eq_container in c:
    c = c.replace(old_eq_container, new_eq_container)
    fixes.append("FIX 5: EQ 10 Bars, größer")

# EQ CSS Premium — tausche aus
old_eq_css_block = c.find('.eq{display:flex;align-items:flex-end;gap:2.5px;height:22px;overflow:hidden}')
if old_eq_css_block > 0:
    eq_css_end = c.find('@keyframes eqBar{', old_eq_css_block)
    eq_css_end = c.find('}', c.find('}', eq_css_end+1)+1) + 1
    
    new_eq_css = """.eq{display:flex;align-items:flex-end;gap:2px;height:28px;overflow:visible}
.eq i{
  display:inline-block;width:3px;min-height:3px;border-radius:3px 3px 1px 1px;
  background:linear-gradient(to top,rgba(255,159,10,.9) 0%,rgba(255,100,50,.8) 35%,rgba(10,132,255,.9) 100%);
  box-shadow:0 0 6px rgba(10,132,255,.5),0 0 2px rgba(255,159,10,.4);
  transform-origin:bottom center;
  animation:eqWave .9s ease-in-out infinite alternate;
}
.eq i:nth-child(1){height:8px;animation-delay:0s;animation-duration:.65s}
.eq i:nth-child(2){height:18px;animation-delay:.08s;animation-duration:.8s}
.eq i:nth-child(3){height:24px;animation-delay:.16s;animation-duration:.55s}
.eq i:nth-child(4){height:14px;animation-delay:.24s;animation-duration:.72s}
.eq i:nth-child(5){height:20px;animation-delay:.32s;animation-duration:.6s}
.eq i:nth-child(6){height:10px;animation-delay:.4s;animation-duration:.85s}
.eq i:nth-child(7){height:22px;animation-delay:.48s;animation-duration:.7s}
.eq i:nth-child(8){height:16px;animation-delay:.56s;animation-duration:.58s}
.eq i:nth-child(9){height:12px;animation-delay:.64s;animation-duration:.78s}
.eq i:nth-child(10){height:7px;animation-delay:.72s;animation-duration:.92s}
.eq.on i{animation:eqBeat .42s ease-in-out infinite alternate}
.eq.on i:nth-child(odd){animation-duration:.38s}
.eq.on i:nth-child(even){animation-duration:.52s}
@keyframes eqWave{0%{transform:scaleY(.25)}100%{transform:scaleY(.65)}}
@keyframes eqBeat{
  0%{transform:scaleY(.15)}
  30%{transform:scaleY(1.0);filter:brightness(1.3)}
  60%{transform:scaleY(.55)}
  100%{transform:scaleY(.85)}
}"""
    c = c[:old_eq_css_block] + new_eq_css + '\n' + c[eq_css_end:]
    fixes.append("FIX 5b: EQ CSS Premium (10 bars, glow, Lottie-Style)")

print("\nFixes:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fsl.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fsl.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: touch events vol, rbico logo fix, title bigger, sleep corner, eq 10bars premium'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
