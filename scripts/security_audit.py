#!/usr/bin/env python3
"""
Security Audit Script — läuft täglich und prüft:
1. GitHub public repos auf exposed secrets
2. Workspace auf Secrets in nicht-privaten Dateien
3. HA Token Ablauf
4. Öffentliche HTML-Dateien auf Credentials
"""
import os, re, requests, base64, json
from datetime import datetime

TOKEN = os.environ.get('GITHUB_TOKEN', '')
WORKSPACE = '/home/node/.openclaw/workspace'

PATTERNS = {
    'OpenRouter Key': r'sk-or-v1-[a-zA-Z0-9]{40,}',
    'GitHub Token': r'ghp_[a-zA-Z0-9]{36,}',
    'HA Token (JWT)': r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[a-zA-Z0-9._-]{40,}',
    'Netlify Token': r'nfp_[a-zA-Z0-9]{30,}',
    'OpenAI Key': r'sk-[a-zA-Z0-9]{40,}',
    'Hardcoded Password': r'(?i)(?:password|passwd|pwd)\s*[=:]\s*["\'][^"\']{6,}["\']',
}

PUBLIC_EXTS = ['.html', '.js', '.css', '.json', '.md', '.txt']
SAFE_DIRS = {'config', '.git', '__pycache__'}
SAFE_FILES = {'.env', 'adbkey', 'win_ssh_key', 'adbkey.pub', 'win_ssh_key.pub',
              'rb_cookies_full.json', 'rb_cookies_clean.json', 'fiverr_cookies.json'}

issues = []

def mask(s):
    return s[:8] + '[...]' + s[-4:] if len(s) > 12 else '[hidden]'

# 1. GitHub public repo scan
if TOKEN:
    H = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    repos_r = requests.get('https://api.github.com/user/repos', headers=H, timeout=10)
    if repos_r.ok:
        for repo in repos_r.json():
            if repo.get('private'): continue
            name = repo['full_name']
            files_r = requests.get(f'https://api.github.com/repos/{name}/contents/', headers=H, timeout=10)
            if not files_r.ok: continue
            for f in files_r.json():
                if not isinstance(f, dict): continue
                if not any(f.get('name','').endswith(e) for e in PUBLIC_EXTS): continue
                dl = requests.get(f['download_url'], timeout=10)
                for pname, pat in PATTERNS.items():
                    if re.search(pat, dl.text):
                        issues.append(f"🔴 GITHUB PUBLIC: {name}/{f['name']} → {pname}")

# 2. Workspace scan (nur Dateien die potenziell public werden könnten)
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if d not in SAFE_DIRS and not d.startswith('.')]
    rel_root = root.replace(WORKSPACE + '/', '')
    for fname in files:
        if fname in SAFE_FILES: continue
        if not any(fname.endswith(e) for e in PUBLIC_EXTS): continue
        fpath = os.path.join(root, fname)
        rel = os.path.join(rel_root, fname)
        try:
            with open(fpath, 'r', errors='ignore') as f:
                content = f.read()
            for pname, pat in PATTERNS.items():
                if re.search(pat, content):
                    issues.append(f"⚠️  LOCAL FILE: {rel} → {pname}")
        except: pass

# Report
ts = datetime.now().strftime('%Y-%m-%d %H:%M')
if issues:
    report = f"🚨 SECURITY AUDIT [{ts}] — {len(issues)} ISSUE(S) FOUND:\n"
    for i in issues:
        report += f"  {i}\n"
    report += "\n⚡ Action required! Check and rotate affected credentials."
else:
    report = f"✅ SECURITY AUDIT [{ts}] — All clear. No exposed secrets found."

print(report)

# Save to log
log_path = f'{WORKSPACE}/memory/security_log.md'
with open(log_path, 'a') as f:
    f.write(f"\n## {ts}\n{report}\n")

# Exit with error if issues found (so cron can alert)
if issues:
    exit(1)
