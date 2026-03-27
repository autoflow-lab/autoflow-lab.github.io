import subprocess, re, paramiko, time
creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = 0

if 'maximum-scale=1' not in c:
    c = c.replace('initial-scale=1,viewport-fit=cover','initial-scale=1,maximum-scale=1,viewport-fit=cover')
    fixes+=1; print("Fix 1: max-scale")

if 'touches.length>1' not in c:
    c = c.replace('\nboot();',"\ndocument.addEventListener('touchmove',function(e){if(e.touches&&e.touches.length>1)e.preventDefault();},{passive:false});\nboot();")
    fixes+=1; print("Fix 2: pinch-zoom")

marker = 'n:relative;height:44px;display:flex;align-items:center'
idx = c.find(marker)
if idx > 0:
    tag_start = c.rfind('<div', 0, idx)
    depth = 0
    for i in range(tag_start, min(tag_start+2000, len(c))):
        if c[i:i+4] == '<div': depth+=1
        elif c[i:i+6] == '</div>':
            depth-=1
            if depth==0:
                old_html = c[tag_start:i+6]
                new_html = '<div style="display:flex;align-items:center;gap:10px;padding:6px 0"><button id="vol-down" style="width:46px;height:46px;border-radius:50%;border:none;background:rgba(255,255,255,.12);color:#fff;font-size:1.5rem;line-height:1;display:flex;align-items:center;justify-content:center;touch-action:manipulation;cursor:pointer;flex-shrink:0">&#8722;</button><div style="flex:1;position:relative;height:5px;background:rgba(255,255,255,.12);border-radius:3px;overflow:hidden"><div id="vfill" style="height:100%;width:40%;background:#0a84ff;border-radius:3px;transition:width .2s"></div></div><span id="vv" style="font-size:.78rem;font-weight:600;color:rgba(255,255,255,.55);min-width:34px;text-align:center">40%</span><button id="vol-up" style="width:46px;height:46px;border-radius:50%;border:none;background:rgba(255,255,255,.12);color:#fff;font-size:1.5rem;line-height:1;display:flex;align-items:center;justify-content:center;touch-action:manipulation;cursor:pointer;flex-shrink:0">+</button><input id="vol-range" type="range" min="0" max="100" value="40" style="display:none"></div>'
                c = c.replace(old_html, new_html)
                fixes+=1; print("Fix 3: Vol +/- buttons OK, replaced "+str(len(old_html))+" chars")
                break
else:
    print("Fix 3: marker not found")

print("vol-down:", 'id="vol-down"' in c)
print("max-scale:", 'maximum-scale=1' in c)
print("pinch:", 'touches.length>1' in c)
print("fixes:", fixes)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/t4check.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/t4check.js'], capture_output=True, text=True)
print("JS:", "OK" if r.returncode==0 else "ERR:"+r.stderr[:200])

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
    subprocess.run(['git','commit','-m','wz.html: vol +/- HTML, pinch-zoom, max-scale'],cwd='/home/node/.openclaw/workspace')
    print("DONE")
