import subprocess, re, paramiko, time, sys
sys.path.insert(0, '/home/node/.openclaw/workspace')
from new_musik_page import NEW_MUSIK

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()

# Ersetze pg-musik Block
pg_start = c.find('<div class="page" id="pg-musik">')
pg_end = c.find('<div class="page"', pg_start + 100)
print(f"Replacing pg-musik: {pg_start}–{pg_end} ({pg_end-pg_start} chars)")

c = c[:pg_start] + NEW_MUSIK + '\n    ' + c[pg_end:]

# CSS: disc spin animation + EQ bars für neue Disc
old_disc_css_marker = '/* ── Album Disc ── */'
if old_disc_css_marker in c:
    # Füge disc-spin zu bestehenden CSS
    pass

# Füge disc-spin CSS hinzu falls nicht vorhanden
if '@keyframes discSpin' not in c:
    spin_css = '\n/* Album disc spin */\n@keyframes discSpin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}\n#alb-disc.playing{animation:discSpin 4s linear infinite}\n'
    c = c.replace('</style>', spin_css + '</style>', 1)
    print("Added discSpin CSS ✓")

# Checke ob JS für alb-disc.classList.add('playing') noch funktioniert
disc_js = c.find("alb-disc")
print(f"alb-disc in JS: {disc_js > 0}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fdm.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fdm.js'], capture_output=True, text=True)
print(f"JS: {'OK ✓' if r.returncode==0 else 'ERR: '+r.stderr[:300]}")

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
    subprocess.run(['git','commit','-m','wz.html: compact music page - mini player, radio always visible, simple disc'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
