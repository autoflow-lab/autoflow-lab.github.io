import subprocess, re, paramiko, time
creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = 0

# Fix 1: WebSocket Keepalive Ping alle 50s (Cloudflare hat 100s timeout)
old_ws_open = "ws.onopen=()=>{"
ws_idx = c.find(old_ws_open)
if ws_idx > 0:
    # Finde das Ende von onopen
    brace_start = c.find('{', ws_idx + len(old_ws_open) - 1)
    # Suche ping code oder fuege es am Ende von onopen ein
    onopen_end = c.find('\n  ws.onmessage', ws_idx)
    onopen_block = c[ws_idx:onopen_end]
    if '_wsPing' not in onopen_block:
        # Fuege vor ws.onmessage ein
        ping_code = """  // Keepalive ping alle 50s (Cloudflare WS timeout = 100s)
  let _wsPing=null;
  ws.onopen=()=>{
    conn(true);_wsOk=true;
    if(_wsPing)clearInterval(_wsPing);
    _wsPing=setInterval(()=>{try{if(ws.readyState===1)ws.send(JSON.stringify({type:'ping',id:Math.floor(Date.now()/1000)}));}catch{}},50000);
    ws.send(JSON.stringify({type:'auth',access_token:tok}));
  };
"""
        # Ersetze alten ws.onopen Block
        old_onopen = c[ws_idx:onopen_end]
        c = c.replace(old_onopen, ping_code)
        fixes+=1; print("Fix 1: WS Keepalive Ping")

# Fix 2: ws.onclose — Ping stoppen
old_onclose = "ws.onclose=(ev)=>{"
close_idx = c.find(old_onclose)
if close_idx > 0 and '_wsPing' not in c[close_idx:close_idx+200]:
    close_end = c.find('\n  ', close_idx+20)
    # Fuege clearInterval in onclose ein
    c = c.replace('ws.onclose=(ev)=>{\n    conn(false);_wsOk=false;',
                  'ws.onclose=(ev)=>{\n    if(_wsPing){clearInterval(_wsPing);_wsPing=null;}\n    conn(false);_wsOk=false;')
    fixes+=1; print("Fix 2: WS onclose ping cleanup")

# Fix 3: iOS :active Feedback — touchstart auf .lt und .ni Elemente
# Der einfachste Weg: document touchstart listener ist schon da
# Aber spezifisch fuer lt tiles: füge CSS hinzu
active_css = """\n/* iOS :active fix für Tiles */\n.lt{-webkit-tap-highlight-color:transparent}\n.lt:active,.ni:active,[data-s]:active,.rb:active{transform:scale(.93)!important;transition:transform .08s!important}\n"""
if '-webkit-tap-highlight-color:transparent' not in c:
    c = c.replace('</style>', active_css + '</style>', 1)
    fixes+=1; print("Fix 3: iOS active CSS")

# Fix 4: Banner - zeige "Verbunden" wenn conn(true) und verstecke Banner nach 2s
conn_true_idx = c.find("function conn(ok){")
if conn_true_idx > 0:
    print("conn() function:")
    print(c[conn_true_idx:conn_true_idx+300])

print("fixes:", fixes)
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/f4.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/f4.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: WS keepalive ping 50s, iOS active feedback CSS'],cwd='/home/node/.openclaw/workspace')
    print("DONE")
