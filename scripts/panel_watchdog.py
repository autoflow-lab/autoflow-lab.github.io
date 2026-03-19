#!/usr/bin/env python3
"""
NS Panel Pro Watchdog — Clawy
Läuft als Cron alle 10min, stellt sicher dass das Dashboard immer vorne ist
"""
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import sys, time

KEY='/home/node/.openclaw/workspace/config/adbkey'
URL='http://192.168.1.123:8123/local/panel.html'

try:
    signer=PythonRSASigner.FromRSAKeyPath(KEY)
    dev=AdbDeviceTcp('192.168.1.119',5555)
    dev.connect(rsa_keys=[signer],auth_timeout_s=8)
    
    focus=dev.shell('dumpsys window | grep mCurrentFocus').strip()
    
    # Kiosk-Browser (WebView Kiosk) ist die primäre App
    KIOSK_PKG='uk.nktnet.webviewkiosk'
    
    if KIOSK_PKG in focus:
        print(f"OK: {focus[:60]}")
    else:
        # Kiosk-App starten
        dev.shell(f'am start -n {KIOSK_PKG}/.MainActivity -d "{URL}"')
        print(f"Relaunched kiosk (was: {focus[:60]})")
    
    # Immersive mode immer aktiv halten
    dev.shell('settings put global policy_control immersive.full=*')
    dev.close()
except Exception as e:
    print(f"Panel offline: {e}", file=sys.stderr)
    sys.exit(1)
