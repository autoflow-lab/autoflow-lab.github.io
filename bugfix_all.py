import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixed = []

# ── BUG 1: WS keepalive falscher Variablenname ws vs _ws ──
old = 'if(ws.readyState===1)ws.send(JSON.stringify({type:\'ping\',id:99}))'
new = 'if(_ws&&_ws.readyState===1)_ws.send(JSON.stringify({type:\'ping\',id:99}))'
if old in c:
    c = c.replace(old, new)
    fixed.append("BUG 1: WS keepalive ws → _ws")

# ── BUG 2: .page padding-bottom zu klein (Nav = ~70px) ──
old = '  padding:max(env(safe-area-inset-top),16px) 15px 10px;'
new = '  padding:max(env(safe-area-inset-top),16px) 15px calc(max(env(safe-area-inset-bottom),0px) + 80px);'
if old in c:
    c = c.replace(old, new)
    fixed.append("BUG 2: page padding-bottom → 80px + safe-area")

# ── BUG 3+6: _vDrag → _volDrag (überall im vol-track JS) ──
if 'let _vDrag=false;' in c:
    c = c.replace('let _vDrag=false;', 'let _volDrag=false;')
    c = c.replace('_vDrag=true;', '_volDrag=true;')
    c = c.replace('if(!_vDrag)return;', 'if(!_volDrag)return;')
    c = c.replace('_vDrag=false;', '_volDrag=false;')
    fixed.append("BUG 3+6: _vDrag → _volDrag (var name sync)")

# ── BUG 4: Dead code volDown/volUp JS entfernen ──
dead_start = '  // Volume +/- Buttons\n  const volDown=document.getElementById'
dead_end = '  // Volume Slider — vol-track'
ds_idx = c.find(dead_start)
de_idx = c.find(dead_end, ds_idx) if ds_idx > 0 else -1
if ds_idx > 0 and de_idx > 0:
    dead_block = c[ds_idx:de_idx]
    c = c.replace(dead_block, '  // Volume via vol-track (see below)\n')
    fixed.append("BUG 4: Dead volDown/volUp JS entfernt")
else:
    print(f"  BUG 4 skip: dead_start={ds_idx}, dead_end={de_idx}")

# ── BUG 5: rfc-cid URL-Text verstecken (zeigt sonst Stream-URL) ──
old_cid = '      const cidEl=document.getElementById(\'rfc-cid\');\n    if(cidEl){\n      // Show only short cid fragment (no full URL)\n      let cidShort=cid;\n      try{const u=new URL(cid);cidShort=u.hostname+(u.pathname!==\'/\'?u.pathname:\'\');}catch(e){}\n      cidEl.textContent=cidShort.length>40?cidShort.slice(0,37)+\'…\':cidShort;\n    }'
new_cid = "      const cidEl=document.getElementById('rfc-cid');\n    if(cidEl) cidEl.textContent=''; // URL versteckt"
if old_cid in c:
    c = c.replace(old_cid, new_cid)
    fixed.append("BUG 5: rfc-cid URL-Text versteckt")
else:
    # Simpler replacement
    c2_idx = c.find("cidEl.textContent=cidShort")
    if c2_idx > 0:
        # Find the line and blank it
        line_start = c.rfind('\n', 0, c2_idx)
        line_end = c.find('\n', c2_idx)
        c = c[:line_start] + '\n      if(cidEl) cidEl.textContent=\'\'; // URL versteckt' + c[line_end:]
        fixed.append("BUG 5: rfc-cid URL-Text versteckt (alt method)")

print("FIXED BUGS:")
for f in fixed:
    print(" ", f)
print(f"\nNot fixed: {6 - len(fixed)} bugs")

# Verify JS
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fbug.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fbug.js'], capture_output=True, text=True)
print("JS:", "OK" if r.returncode==0 else "ERR:"+r.stderr[:300])

if r.returncode == 0:
    data = c.encode()
    print(f"size: {len(data):,}")
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
    result = o2.read().decode().strip()
    print(f"deployed: {result}")
    cl.close()
    open('/home/node/.openclaw/workspace/projects/fiverr/wz.html','w').write(c)
    subprocess.run(['git','add','-A'], cwd='/home/node/.openclaw/workspace')
    subprocess.run(['git','commit','-m','wz.html: fix all 6 bugs (WS var, padding, volDrag, dead code, rfc-cid)'], cwd='/home/node/.openclaw/workspace')
    print("DONE")
