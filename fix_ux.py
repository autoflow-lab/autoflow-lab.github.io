import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ═══════════════════════════════════════════
# FIX 1: HA-Banner — kein Retry wenn WS läuft
# ═══════════════════════════════════════════
old_retry = """    if(!_wsOk || _offlineCount>=2)showOfflineBanner(true,_offlineCount);
    // Retry-Backoff: 5s, 15s, 30s
    const delay=[5000,15000,30000][Math.min(_offlineCount-1,2)];
    _offlineNextRetry=Date.now()+delay;
    setTimeout(fetchStates, delay);"""

new_retry = """    // Nur Banner + Retry wenn WS NICHT verbunden
    if(!_wsOk){
      if(_offlineCount>=2) showOfflineBanner(true,_offlineCount);
      const delay=[5000,15000,30000][Math.min(_offlineCount-1,2)];
      _offlineNextRetry=Date.now()+delay;
      setTimeout(fetchStates, delay);
    }
    // Wenn WS läuft, werden States via get_states geholt — kein HTTP-Retry nötig"""

if old_retry in c:
    c = c.replace(old_retry, new_retry)
    fixes.append("FIX 1: Banner nur wenn WS disconnected")

# ═══════════════════════════════════════════
# FIX 2: Musik-Seite kompakter
# Album-Disc kleiner + weniger Padding
# ═══════════════════════════════════════════
# Album disc noch kleiner
c = c.replace(
    'width:clamp(110px,28vw,145px);height:clamp(110px,28vw,145px);margin:10px auto 8px;',
    'width:clamp(80px,20vw,110px);height:clamp(80px,20vw,110px);margin:6px auto 6px;'
)
fixes.append("FIX 2a: Album disc 80-110px")

# .pctrl padding reduzieren
c = c.replace('.pctrl{padding:16px 22px}', '.pctrl{padding:8px 16px}')
fixes.append("FIX 2b: pctrl padding reduziert")

# .np padding reduzieren
c = c.replace(
    '.np{padding:6px 20px 20px;position:relative;z-index:1;text-align:center;width:100%}',
    '.np{padding:4px 16px 12px;position:relative;z-index:1;text-align:center;width:100%}'
)
fixes.append("FIX 2c: np padding reduziert")

# .album margin-bottom reduzieren
c = c.replace(
    '.album{\n  border-radius:18px;overflow:hidden;margin-bottom:10px;',
    '.album{\n  border-radius:18px;overflow:hidden;margin-bottom:6px;'
)
fixes.append("FIX 2d: album margin-bottom 6px")

# ═══════════════════════════════════════════
# FIX 3: Licht-Feedback — .pressing Klasse
# iOS :active ist unzuverlässig, eigene Klasse zuverlässiger
# ═══════════════════════════════════════════
# CSS für .pressing Klasse hinzufügen
pressing_css = """\n/* iOS Tap-Feedback via .pressing Klasse */\n.lt.pressing{transform:scale(.93)!important;transition:transform .06s ease!important}\n"""
if '.lt.pressing{' not in c:
    c = c.replace('</style>', pressing_css + '</style>', 1)
    fixes.append("FIX 3a: .lt.pressing CSS")

# JS: touchstart/touchend auf .lt Tiles für .pressing Klasse
# Einfügen nach querySelectorAll('.lt').forEach block, am Ende von buildUI Handler
lt_press_js = """
  // Licht-Feedback: .pressing Klasse für zuverlässiges iOS Touch-Feedback
  document.querySelectorAll('.lt').forEach(function(tile){
    tile.addEventListener('touchstart',function(){tile.classList.add('pressing');},{passive:true});
    tile.addEventListener('touchend',function(){setTimeout(function(){tile.classList.remove('pressing');},120);},{passive:true});
    tile.addEventListener('touchcancel',function(){tile.classList.remove('pressing');},{passive:true});
  });
"""
# Einfügen vor dem letzten </script>
if 'tile.classList.add(\'pressing\')' not in c:
    last_script = c.rfind('</script>')
    c = c[:last_script] + lt_press_js + '\n' + c[last_script:]
    fixes.append("FIX 3b: .pressing touchstart/end JS")

print("Fixes:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fux.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fux.js'], capture_output=True, text=True)
print(f"\nJS: {'OK ✓' if r.returncode==0 else 'ERR: '+r.stderr[:200]}")

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
    subprocess.run(['git','commit','-m','wz.html: banner fix (kein Retry wenn WS ok), kompaktes Layout, .pressing feedback'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
