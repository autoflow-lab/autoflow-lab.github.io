import subprocess, re, paramiko, time
creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = 0

# Fix 1: Entferne alten _volTrack pointer-handler komplett
start = c.find('\n  // Volume Slider — nur horizontal')
if start < 0:
    start = c.find('\n  // Volume — +/- Buttons\n  const _volTrack')
end = c.find('\n  function confirmVol(', start) if start > 0 else -1
if start > 0 and end > 0:
    old_block = c[start:end]
    print("Remove _volTrack block:", len(old_block), "chars")
    # Behalte nur den neuen +/- Handler
    new_block = """
  // Volume +/- (kein Slider-Konflikt)
"""
    c = c.replace(old_block, new_block)
    fixes+=1; print("Fix 1: _volTrack handler entfernt")
else:
    print("Fix 1: block start/end:", start, end)

# Fix 2: vol-down/up JS sicherstellen (falls durch Fix 1 entfernt)
if 'volDown=document.getElementById' not in c:
    confirm_idx = c.find('\n  function confirmVol(')
    insert = """
  // Volume +/- Buttons
  const volDown=document.getElementById('vol-down');
  const volUp=document.getElementById('vol-up');
  let _volTimer2=null;
  function _sendVol2(pct){clearTimeout(_volTimer2);_volTimer2=setTimeout(function(){svc('media_player','volume_set',{entity_id:CFG.alm,volume_level:pct/100*0.6});},80);}
  if(volDown){volDown.addEventListener('click',function(){hap();var v=Math.max(0,(parseInt(document.getElementById('vv').textContent)||40)-5);syncVolUI(v);_sendVol2(v);});}
  if(volUp){volUp.addEventListener('click',function(){hap();var v=Math.min(100,(parseInt(document.getElementById('vv').textContent)||40)+5);syncVolUI(v);_sendVol2(v);});}
"""
    c = c[:confirm_idx] + insert + c[confirm_idx:]
    fixes+=1; print("Fix 2: Vol +/- JS eingefuegt")
else:
    print("Fix 2: Vol +/- JS bereits vorhanden")

# Fix 3: Pull-to-Refresh auf pg-musik deaktivieren
# Suche den Pull-Refresh IIFE und deaktiviere es fuer pg-musik
ptr_idx = c.find('if(!el||el.scrollTop>2) return;')
if ptr_idx > 0:
    # Finde den IIFE Start
    iife_start = c.rfind('(function(){', 0, ptr_idx)
    # Fuege Musik-Check am Anfang ein
    old_iife_open = c[iife_start:iife_start+80]
    if 'pg-musik' not in c[iife_start:ptr_idx]:
        # Nach dem ersten { des IIFE einen Check einfuegen
        first_brace = c.find('{', iife_start) + 1
        c = c[:first_brace] + "\n    if(document.getElementById('pages')?.querySelector('.page.cur')?.id==='pg-musik')return;" + c[first_brace:]
        fixes+=1; print("Fix 3: Pull-to-Refresh disabled fuer Musik-Tab")
else:
    print("Fix 3: Pull-Refresh nicht gefunden")

# Fix 4: pg-musik overflow sicherstellen
old_pg_cur = ".page.cur{opacity:1;pointer-events:auto}"
if old_pg_cur in c:
    # Behalte Musik-Page scroll
    print("Fix 4: .page.cur OK")

print("Checks:")
print("  _vStartX gone:", '_vStartX' not in c)
print("  vol-down JS:", 'volDown.addEventListener' in c)
print("  fixes:", fixes)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/f2.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/f2.js'], capture_output=True, text=True)
print("JS:", "OK" if r.returncode==0 else "ERR:"+r.stderr[:300])

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
    subprocess.run(['git','commit','-m','wz.html: remove _volTrack handler, disable ptr-refresh on musik, vol fix'],cwd='/home/node/.openclaw/workspace')
    print("DONE")
