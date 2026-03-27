import subprocess, re, paramiko, time
creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

# Entferne den _volTrack Block exakt
marker_start = 'teuert Lautstärke, kein Scroll-Konflikt\n  const _volTrack=volRange?volRange.parentElement:null;'
marker_end = '  _volTrack.addEventListener(\'pointercancel\',()=>{_volDrag=false;_vCommitted=false;});\n  }'
start_idx = c.find(marker_start)
end_idx = c.find(marker_end, start_idx) + len(marker_end) if start_idx > 0 else -1
print("Block:", start_idx, "-", end_idx)
if start_idx > 0 and end_idx > len(marker_end):
    old = c[start_idx:end_idx]
    print("Removing:", len(old), "chars, preview:", repr(old[:60]))
    c = c.replace(old, 'teuert Lautstärke — +/- Buttons (kein Slider)\n  // _volTrack entfernt')
    print("Fix: _volTrack removed")
    print("_vStartX gone:", '_vStartX' not in c)
else:
    print("Block nicht gefunden mit exaktem match")
    # Zeige Zeilen 340-380 Tausend chars
    idx = c.find('const _volTrack=volRange')
    if idx > 0:
        # Finde end: suche nach naechstem '  }' nach dem Block
        end2 = c.find('\n  function confirmVol(', idx)
        print("Alt end:", end2)
        if end2 > idx:
            old2 = c[idx:end2]
            print("Alt block:", len(old2), repr(old2[:80]))

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/f3.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/f3.js'], capture_output=True, text=True)
print("JS:", "OK" if r.returncode==0 else "ERR:"+r.stderr[:300])
if r.returncode==0:
    data=c.encode()
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
    subprocess.run(['git','commit','-m','wz.html: remove _volTrack conflict'],cwd='/home/node/.openclaw/workspace')
    print("DONE")
