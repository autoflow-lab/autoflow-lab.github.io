import subprocess, re, paramiko, time

creds = dict(l.strip().split('=',1) for l in open('/home/node/.openclaw/workspace/secure/ha_creds.txt').read().split('\n') if '=' in l)
c = open('/home/node/.openclaw/workspace/projects/fiverr/wz.html').read()
fixes = []

# ══════════════════════════════════════════════════════════════
# FIX: Szenen-System vereinheitlichen
# Problem: setActiveScene + _updateQaBar verwalten beide den Chip
#          → Race conditions, Konflikte, falsche Anzeige
# Lösung:  Ein System: setActiveScene(key, fromDetection=false)
#          Nach manuellem Trigger: 10s "Lock" → keine Auto-Überschreibung
# ══════════════════════════════════════════════════════════════

# 1. setActiveScene() ersetzen — vollständige neue Version
old_setScene = """let _activeScene=null;
function setActiveScene(s){
  _activeScene=s;
  document.querySelectorAll('.sb2[data-s]').forEach(el=>{
    const active=el.dataset.s===s;
    el.style.boxShadow=active?'0 0 0 2px rgba(255,159,10,.6)':'';
    el.style.transform=active?'scale(1.03)':'';
  });
  // Chip sofort bei manuellem Szenen-Trigger aktualisieren
  const chip=document.getElementById('scene-chip');
  const chipTxt=document.getElementById('scene-chip-txt');
  if(!chip||!chipTxt) return;
  const sceneEmoji={abend:'🌆',hell:'☀️',film:'🎬',nacht:'🌙'};
  const sceneLabel={abend:'Abend-Szene aktiv',hell:'Hell-Szene aktiv',film:'Film-Szene aktiv',nacht:'Nacht-Szene aktiv'};
  if(!s){chip.classList.remove('show');chip.removeAttribute('data-scene');return;}
  const key=s.toLowerCase();
  chipTxt.textContent=(sceneEmoji[key]||'✦')+'\u2009'+( sceneLabel"""

# Finde den Block komplett
start = c.find('let _activeScene=null;')
end = c.find('\nfunction doScene(', start)
old_full = c[start:end]
print(f"setActiveScene block: {start}–{end} ({len(old_full)} chars)")

new_setScene = """// ── Szenen-System (unified) ──────────────────────────────────
let _activeScene=null;
let _sceneLockUntil=0; // ms timestamp: nach manuellem Trigger kein Auto-Override

function setActiveScene(key, fromDetection){
  // fromDetection=true: aus updateAll() → 10s nach manuellem Trigger ignorieren
  if(fromDetection && Date.now()<_sceneLockUntil) return;
  if(_activeScene===key) return; // keine Änderung nötig

  _activeScene=key;

  // .sb2 Buttons updaten
  document.querySelectorAll('.sb2[data-s]').forEach(function(el){
    const on=el.dataset.s===key;
    el.style.boxShadow=on?'0 0 0 2px rgba(255,159,10,.6)':'';
    el.style.transform=on?'scale(1.03)':'';
  });
  // home-scenes Zeile (.home-scene-btn falls vorhanden)
  document.querySelectorAll('[data-scene-key]').forEach(function(el){
    el.classList.toggle('active', el.dataset.sceneKey===key);
  });

  // Chip updaten
  const chip=document.getElementById('scene-chip');
  const chipTxt=document.getElementById('scene-chip-txt');
  if(!chip||!chipTxt) return;
  if(!key){chip.classList.remove('show');chip.removeAttribute('data-scene');return;}
  const EMOJI={abend:'🌆',hell:'☀️',film:'🎬',nacht:'🌙',morgen:'🌅',nacht2:'🌙✨',off:'🌑'};
  const LABEL={abend:'Abend',hell:'Hell',film:'Film',nacht:'Nacht',morgen:'Guten Morgen',nacht2:'Gute Nacht',off:'Alles aus'};
  chipTxt.textContent=(EMOJI[key]||'✦')+'\u2009—\u2009'+(LABEL[key]||key)+' aktiv';
  chip.dataset.scene=key;
  chip.classList.remove('show');
  void chip.offsetWidth;
  chip.classList.add('show');
}

"""

c = c[:start] + new_setScene + c[end:]
fixes.append("FIX 1: setActiveScene() vereinheitlicht + Lock-Mechanismus")

# 2. doScene: Lock setzen + setActiveScene aufrufen
# Suche doScene(s){ am Anfang (nach morgen/nacht2 werden schon gesetzt)
# Wir fügen am ANFANG von doScene den Lock ein + setActiveScene call am Ende
scene_fn = c.find('\nfunction doScene(s){')
# Finde das Ende der Funktion
depth = 0
i = scene_fn + 1
while i < len(c):
    if c[i] == '{': depth += 1
    elif c[i] == '}':
        depth -= 1
        if depth == 0:
            scene_fn_end = i + 1
            break
    i += 1

old_doScene_start = c[scene_fn:scene_fn+30]
print(f"\ndoScene @ {scene_fn}–{scene_fn_end}")

# Lock-Zeile am Anfang einfügen (nach der öffnenden Klammer)
open_brace = c.find('{', scene_fn)
lock_line = '\n  // 10s Lock: auto-Szenen-Erkennung überschreibt nicht direkt nach Trigger\n  _sceneLockUntil=Date.now()+10000;\n'

# Füge Lock als erste Zeile ein (außer bei morgen/nacht2 → die haben return)
insert_pos = open_brace + 1
c = c[:insert_pos] + lock_line + c[insert_pos:]
fixes.append("FIX 2: doScene() setzt 10s Lock")

# 3. _updateQaBar: chip-Update ersetzen durch setActiveScene(key, true)
# Ersetze das komplette chip-Update-Block in _updateQaBar

old_chip_block = """      const sc=document.getElementById('scene-hint');
      if(sc){sc.textContent=activeScene;sc.style.opacity=activeScene?'1':'0';}
      // Aktive Szene Chip updaten
      (function(){
        const chip=document.getElementById('scene-chip');
        const chipTxt=document.getElementById('scene-chip-txt');
        if(!chip||!chipTxt) return;
        if(!activeScene){chip.classList.remove('show');chip.removeAttribute('data-scene');return;}
        // Szene → key+label+text
        const scMap={
          '🎬 Film':  {key:'film',  label:'Film-Szene aktiv'},
          '🌙 Nacht': {key:'nacht', label:'Nacht-Szene aktiv'},
          '☀️ Hell':  {key:'hell',  label:'Hell-Szene aktiv'},
          '🌆 Abend': {key:'abend', label:'Abend-Szene aktiv'},
        };
        const meta=scMap[activeScene]||{key:'abend',label:activeScene+' aktiv'};
        chipTxt.textContent=activeScene+'\u2009—\u2009'+meta.label.replace(activeScene+' ','');
        chip.dataset.scene=meta.key;
        if(!chip.classList.contains('show')){
          chip.classList.remove('show'); void chip.offsetWidth; chip.classList.add('show');
        }
      })();"""

new_chip_block = """      const sc=document.getElementById('scene-hint');
      if(sc){sc.textContent=activeScene;sc.style.opacity=activeScene?'1':'0';}
      // Szene-Erkennung → unified setActiveScene (fromDetection=true → respektiert Lock)
      const _autoSceneMap={'🎬 Film':'film','🌙 Nacht':'nacht','☀️ Hell':'hell','🌆 Abend':'abend'};
      setActiveScene(activeScene?(_autoSceneMap[activeScene]||''):null, true);"""

if old_chip_block in c:
    c = c.replace(old_chip_block, new_chip_block)
    fixes.append("FIX 3: _updateQaBar → setActiveScene(key, true)")
else:
    print("WARN: chip block not found exactly")
    # Fallback: suche den Teil
    idx = c.find('const scMap={')
    print(f"  scMap @ {idx}: {c[idx:idx+60]}")

print("\nFixes:")
for f in fixes: print(f"  ✓ {f}")

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
with open('/tmp/fscene.js','w') as f: f.write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fscene.js'], capture_output=True, text=True)
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
    subprocess.run(['git','commit','-m','wz.html: unified scene system, 10s trigger lock, no double-active'], cwd='/home/node/.openclaw/workspace')
    print("DONE ✓")
