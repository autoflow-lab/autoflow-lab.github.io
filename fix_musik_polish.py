import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══════════════════════════════════════════
# FIX 1: "Läuft…" → Radio-Sender-Name zeigen
# ══════════════════════════════════════════
old_titleStr = "const titleStr=s?.attributes?.media_title||(playing?'Läuft\u2026':'Bereit');"
new_titleStr = "const titleStr=s?.attributes?.media_title||(_radActive?_radActive:null)||(playing?'\u25b6\ufe0f Läuft':'Bereit');"
if old_titleStr in c:
    c = c.replace(old_titleStr, new_titleStr)
    fixes.append("FIX 1: titleStr zeigt Radio-Sender-Name")

# ══════════════════════════════════════════
# FIX 2: btn-prev/next display:none statt nur opacity:0
# (verhindert off-center play button)
# ══════════════════════════════════════════
old_btns = "if(_prevBtn){_prevBtn.style.opacity=_isSpot?'1':'0';_prevBtn.style.pointerEvents=_isSpot?'auto':'none';}\n  if(_nextBtn){_nextBtn.style.opacity=_isSpot?'1':'0';_nextBtn.style.pointerEvents=_isSpot?'auto':'none';}"
new_btns = "if(_prevBtn){_prevBtn.style.display=_isSpot?'flex':'none';}\n  if(_nextBtn){_nextBtn.style.display=_isSpot?'flex':'none';}"
if old_btns in c:
    c = c.replace(old_btns, new_btns)
    fixes.append("FIX 2: btn-prev/next display:none → play bleibt zentriert")

# ══════════════════════════════════════════
# FIX 3: Volume slider — opacity:0.01 statt 0 (iPad touch fix)
# ══════════════════════════════════════════
c = c.replace('opacity:0;cursor:pointer;margin:0;padding:0;touch-action:none', 
              'opacity:0.01;cursor:pointer;margin:0;padding:0;touch-action:none')
fixes.append("FIX 3: Vol-slider opacity:0.01 für iPad touch")

# ══════════════════════════════════════════
# FIX 4: spec-cv — auf 0px Höhe setzen (keine riesige Overlay-Visualisierung)
# ══════════════════════════════════════════
old_spec = 'style="position:absolute;bottom:0;left:0;width:100%;height:38%;opacity:0;pointer-events:none;transition:opacity 1.2s ease"'
new_spec = 'style="position:absolute;bottom:0;left:0;width:100%;height:0;opacity:0;pointer-events:none;display:none"'
if old_spec in c:
    c = c.replace(old_spec, new_spec)
    fixes.append("FIX 4: spec-cv canvas versteckt (kein Overlay)")

# ══════════════════════════════════════════
# FIX 5: Premium EQ Bars CSS (gradient, glow, rounded)
# ══════════════════════════════════════════
old_eq_css_marker = c.find('.eq{')
if old_eq_css_marker > 0:
    old_eq_block_end = c.find('}', old_eq_css_marker) + 1
    old_eq_block = c[old_eq_css_marker:old_eq_block_end]
    
    old_eq_i = c.find('.eq i{', old_eq_block_end-10)
    old_eq_i_end = c.find('}', old_eq_i) + 1
    
    old_eq_on = c.find('.eq.on i{', old_eq_i_end-5)
    old_eq_on_end = c.find('}', old_eq_on) + 1 if old_eq_on>0 else old_eq_i_end

    print(f"EQ CSS: eq@{old_eq_css_marker}, eq-i@{old_eq_i}, eq-on@{old_eq_on}")
    
    new_eq_css = """.eq{display:flex;align-items:flex-end;gap:2.5px;height:22px;overflow:hidden}
.eq i{
  display:inline-block;width:3px;border-radius:2px 2px 1px 1px;
  background:linear-gradient(to top,#ff9f0a 0%,#ff6b35 40%,#0a84ff 100%);
  box-shadow:0 0 5px rgba(10,132,255,.35),0 0 2px rgba(255,159,10,.4);
  min-height:3px;
  animation:eqIdle .9s ease-in-out infinite alternate;
}
.eq i:nth-child(1){height:8px;animation-delay:0s;animation-duration:.7s}
.eq i:nth-child(2){height:14px;animation-delay:.15s;animation-duration:.85s}
.eq i:nth-child(3){height:18px;animation-delay:.05s;animation-duration:.95s}
.eq i:nth-child(4){height:12px;animation-delay:.25s;animation-duration:.75s}
.eq i:nth-child(5){height:7px;animation-delay:.35s;animation-duration:1s}
.eq.on i{animation:eqBar .55s ease-in-out infinite alternate}
.eq.on i:nth-child(1){animation-delay:0s;animation-duration:.55s}
.eq.on i:nth-child(2){animation-delay:.1s;animation-duration:.7s}
.eq.on i:nth-child(3){animation-delay:.05s;animation-duration:.48s}
.eq.on i:nth-child(4){animation-delay:.2s;animation-duration:.62s}
.eq.on i:nth-child(5){animation-delay:.28s;animation-duration:.58s}
@keyframes eqIdle{from{transform:scaleY(.3)}to{transform:scaleY(.7)}}
@keyframes eqBar{
  0%{transform:scaleY(.2)}
  25%{transform:scaleY(.9)}
  50%{transform:scaleY(.5)}
  75%{transform:scaleY(1)}
  100%{transform:scaleY(.4)}
}"""
    
    # Ersetze alte EQ CSS
    # Suche alle zusammenhängenden EQ CSS Regeln
    eq_all_end = old_eq_on_end if old_eq_on > 0 else old_eq_i_end
    old_eq_all = c[old_eq_css_marker:eq_all_end]
    c = c[:old_eq_css_marker] + new_eq_css + '\n' + c[eq_all_end:]
    fixes.append("FIX 5: Premium EQ bars CSS (gradient + glow + animation)")

# ══════════════════════════════════════════
# FIX 6: Radio Logos in CFG.radio
# ══════════════════════════════════════════
LOGOS = {
    'SRF 1':    'https://www.google.com/s2/favicons?domain=srf.ch&sz=128',
    'SRF 3':    'https://www.google.com/s2/favicons?domain=srf.ch&sz=128',
    'Swiss Pop':'https://www.google.com/s2/favicons?domain=swissradio.ch&sz=128',
    'Kiss FM':  'https://www.google.com/s2/favicons?domain=kissfm.de&sz=128',
    'U1 Tirol': 'https://u1-radio.at/wp-content/uploads/2022/03/u1_favicon512x512-150x150.png',
    'Melody':   'https://cdn.radiobrowser.info/img/radio-melody.png',
}

# SRF 1 und SRF 3 haben gleiche Domain — etwas unterschiedlichere Logos
LOGOS['SRF 3'] = 'https://www.google.com/s2/favicons?domain=srf3.ch&sz=128'

# Logo-URL in CFG.radio einfügen
# CFG.radio items haben n, u, c, r — wir fügen logo hinzu
radio_idx = c.find("CFG.radio=[")
if radio_idx < 0: radio_idx = c.find("radio:[")
print(f"CFG.radio @ {radio_idx}")
radio_end = c.find("];", radio_idx)
print(f"CFG.radio block: {radio_idx}–{radio_end}")
print(c[radio_idx:radio_end+2][:400])

# Radio in buildUI: rg.innerHTML = CFG.radio.map(r => ...)
# Füge Logo-img hinzu im Radio-Button HTML
rg_build = c.find("document.getElementById('rg').innerHTML=CFG.radio.map")
rg_build_end = c.find(").join('')", rg_build) + 10
rg_html_block = c[rg_build:rg_build_end]
print(f"\nrg build @ {rg_build}–{rg_build_end}")
print(rg_html_block[:500])

fixes_count = len(fixes)
print(f"\nSo far: {fixes_count} fixes")
for f in fixes: print(f"  ✓ {f}")

import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

LOGOS = {
    'SRF 1':    'https://www.google.com/s2/favicons?domain=srf.ch&sz=128',
    'SRF 3':    'https://www.google.com/s2/favicons?domain=srf3.ch&sz=128',
    'Swiss Pop':'https://www.google.com/s2/favicons?domain=swissradio.ch&sz=128',
    'Kiss FM':  'https://www.google.com/s2/favicons?domain=kissfm.de&sz=128',
    'U1 Tirol': 'https://u1-radio.at/wp-content/uploads/2022/03/u1_favicon512x512-150x150.png',
    'Melody':   'https://cdn.radiobrowser.info/img/radio-melody.png',
}

# FIX 6: Logo in radio-Button HTML einbauen (img statt emoji)
old_rg = """document.getElementById('rg').innerHTML=CFG.radio.map(r=>`
    <div class="rb" data-u="${r.u}" data-n="${r.n}" style="--rc:${r.c};--rr:${r.r}">
      <div class="rbico" style="background:rgba(${r.r},.12);border:1px solid rgba(${r.r},.18)">
        ${_radioEmoji[r.n]||'📻'}
      </div>
      <span class="rbn">${r.n}</span>
      ${r.blocked?'<span style="font-size:.4rem;color:rgba(255,255,255,.2);position:absolute;top:5px;right:5px">🏠</span>':''}
    </div>`).join('')"""

new_rg = """document.getElementById('rg').innerHTML=CFG.radio.map(r=>`
    <div class="rb" data-u="${r.u}" data-n="${r.n}" style="--rc:${r.c};--rr:${r.r}">
      <div class="rbico" style="background:rgba(${r.r},.15);border:1px solid rgba(${r.r},.25);position:relative;overflow:hidden">
        ${r.logo?`<img src="${r.logo}" alt="${r.n}" style="width:100%;height:100%;object-fit:contain;border-radius:10px;image-rendering:auto" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`:''}
        <span style="font-size:1.3rem;${r.logo?'display:none':''}display:flex;align-items:center;justify-content:center;width:100%;height:100%">${_radioEmoji[r.n]||'📻'}</span>
      </div>
      <span class="rbn">${r.n}</span>
      ${r.blocked?'<span style="font-size:.4rem;color:rgba(255,255,255,.2);position:absolute;top:5px;right:5px">🏠</span>':''}
    </div>`).join('')"""

if old_rg in c:
    c = c.replace(old_rg, new_rg)
    print("FIX 6: Radio logos img ✓")

# Logo-URLs in CFG.radio einfügen
for name, logo_url in LOGOS.items():
    # {n:'SRF 1', ...} → {n:'SRF 1', logo:'URL', ...}
    old_entry_patterns = [
        f"{{n:'{name}',",
        f"{{n:'{name}' ,",
    ]
    for pat in old_entry_patterns:
        if pat in c:
            c = c.replace(pat, f"{{n:'{name}',logo:'{logo_url}',", 1)
            print(f"FIX 6: logo added for {name}")
            break

# FIX 7: rbico CSS etwas größer und schöner
old_rbico = '.rbico{'
rbico_start = c.find(old_rbico)
rbico_end = c.find('}', rbico_start) + 1
print(f"rbico CSS: {c[rbico_start:rbico_end]}")
new_rbico = '.rbico{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;overflow:hidden;flex-shrink:0}'
c = c[:rbico_start] + new_rbico + c[rbico_end:]
print("FIX 7: rbico CSS updated")

# FIX 8: .rb CSS — grid-layout, 3 stations per row
old_rb_layout = '.rg{display:flex;flex-direction:row;gap:8px;margin-bottom:12px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:4px}.rg::-webkit-scrollbar{display:none}'
new_rb_layout = '.rg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;position:relative;z-index:1}.rg::-webkit-scrollbar{display:none}'
if old_rb_layout in c:
    c = c.replace(old_rb_layout, new_rb_layout)
    print("FIX 8: Radio grid 3 cols ✓")
# remove min-width from .rb
c = c.replace('  min-width:75px;flex-shrink:0;\n}', '}')

# VERIFY
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fmp.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fmp.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: premium EQ, radio logos, play center, Läuft fix, spec-cv hide, vol-slider touch'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
