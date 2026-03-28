import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

fixes = []

# ═══════════════════════════════════════════
# FIX 1: Duplicate id="vv" — erste umbenennen
# ═══════════════════════════════════════════
# Erste id="vv" ist das Header-Label, zweite ist im vol-wrap
first_vv = c.find('id="vv"')
second_vv = c.find('id="vv"', first_vv + 1)
if first_vv > 0 and second_vv > 0:
    # Erste id="vv" umbenennen zu "vv-hdr"
    c = c[:first_vv] + 'id="vv-hdr"' + c[first_vv+7:]
    fixes.append("FIX 1: duplicate id=vv → vv-hdr")

# Auch syncVolUI anpassen: vv-hdr ebenfalls updaten
old_sync = """function syncVolUI(pct){
    const fill=document.getElementById('vfill');
    const thumb=document.getElementById('vthumb');
    const vv=document.getElementById('vv');
    const vr=document.getElementById('vol-range');
    if(fill) fill.style.width=pct+'%';
    if(thumb) thumb.style.left=pct+'%';
    if(vv) vv.textContent=pct+'%';
    if(vr) vr.value=pct;
  }"""

new_sync = """function syncVolUI(pct){
    const fill=document.getElementById('vfill');
    const thumb=document.getElementById('vthumb');
    const vv=document.getElementById('vv');
    const vvh=document.getElementById('vv-hdr');
    const vr=document.getElementById('vol-range');
    if(fill) fill.style.width=pct+'%';
    if(thumb) thumb.style.left=pct+'%';
    if(vv) vv.textContent=pct+'%';
    if(vvh) vvh.textContent=pct+'%';
    if(vr) vr.value=pct;
  }"""

if old_sync in c:
    c = c.replace(old_sync, new_sync)
    fixes.append("FIX 1b: syncVolUI updatet vv-hdr")

# ═══════════════════════════════════════════
# FIX 2: .rg → horizontal scrollbar
# Radio-Sender horizontal statt vertikal → kein Verticalscroll nötig
# ═══════════════════════════════════════════
old_rg_css = ".rg{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}"
new_rg_css = ".rg{display:flex;flex-direction:row;gap:8px;margin-bottom:12px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:4px}.rg::-webkit-scrollbar{display:none}"
if old_rg_css in c:
    c = c.replace(old_rg_css, new_rg_css)
    fixes.append("FIX 2: .rg horizontal scroll")

# .rb min-width damit horizontal scroll sinnvoll
old_rb_end = "  position:relative;overflow:hidden;\n}"
if old_rb_end in c:
    c = c.replace(old_rb_end, "  position:relative;overflow:hidden;\n  min-width:75px;flex-shrink:0;\n}")
    fixes.append("FIX 2b: .rb min-width")

# ═══════════════════════════════════════════
# FIX 3: Album kompakter auf kleinen Screens
# ═══════════════════════════════════════════
old_tilt = 'style="display:block;width:clamp(130px,38vw,160px);height:clamp(130px,38vw,160px);margin:14px auto 10px;'
new_tilt = 'style="display:block;width:clamp(110px,28vw,145px);height:clamp(110px,28vw,145px);margin:10px auto 8px;'
if old_tilt in c:
    c = c.replace(old_tilt, new_tilt)
    fixes.append("FIX 3: Album-Disc kleiner")

print("Fixes angewendet:")
for f in fixes:
    print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fcompact.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fcompact.js'], capture_output=True, text=True)
print(f"\nJS: {'OK ✓' if r.returncode==0 else 'ERR: '+r.stderr[:200]}")

if r.returncode==0:
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
    subprocess.run(['git','commit','-m','wz.html: horizontal radio scroll, fix dup vv, compact album'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
