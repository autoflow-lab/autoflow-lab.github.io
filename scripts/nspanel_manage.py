#!/usr/bin/env python3
"""
NS Panel Pro Manager — Clawy
Verwaltet das Sonoff NS Panel Pro via ADB (192.168.1.119)
"""
import sys
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

KEY = '/home/node/.openclaw/workspace/config/adbkey'
IP  = '192.168.1.119'
PORT = 5555

def connect():
    signer = PythonRSASigner.FromRSAKeyPath(KEY)
    dev = AdbDeviceTcp(IP, PORT)
    dev.connect(rsa_keys=[signer], auth_timeout_s=10)
    return dev

def block_updates(dev):
    """Deaktiviert alle OTA/Auto-Update Mechanismen"""
    cmds = [
        'settings put global auto_update_packages 0',
        'settings put global ota_disable_automatic_update 1',
        'settings put global package_verifier_enable 0',
        # Block update server via DNS workaround
        'settings put global captive_portal_detection_enabled 0',
    ]
    for cmd in cmds:
        dev.shell(cmd)
    print("✅ Updates blockiert")

def install_apk(dev, apk_url):
    """Installiert APK aus URL"""
    dev.shell(f'am start -a android.intent.action.VIEW -d "{apk_url}"')
    print(f"📦 APK-Installation gestartet: {apk_url}")

def launch_kiosk(dev, url):
    """Öffnet URL im Browser (Kiosk-Modus)"""
    dev.shell(f'am start -a android.intent.action.VIEW -d "{url}"')
    print(f"🖥️ Browser geöffnet: {url}")

def launch_ha_dashboard(dev):
    """Öffnet das Clawy HA Dashboard"""
    launch_kiosk(dev, 'http://192.168.1.123:8123/local/clawy_panel.html')

def screenshot(dev, out='/tmp/panel_screen.png'):
    """Screenshot vom Panel"""
    dev.shell('screencap -p /sdcard/screen.png')
    # Pull via adb
    import subprocess
    subprocess.run(['adb', '-s', f'{IP}:{PORT}', 'pull', '/sdcard/screen.png', out])
    print(f"📸 Screenshot: {out}")

def status(dev):
    """Zeigt Panel-Status"""
    print("Model:", dev.shell('getprop ro.product.model').strip())
    print("Android:", dev.shell('getprop ro.build.version.release').strip())
    print("App:", dev.shell('dumpsys window windows | grep mCurrentFocus').strip()[:80])
    print("IP:", dev.shell("ip addr show wlan0 | grep 'inet '").strip()[:60])
    print("eWeLink ver:", dev.shell('dumpsys package com.eWeLinkControlPanel | grep versionName').strip())

if __name__ == '__main__':
    dev = connect()
    print("✅ NS Panel Pro verbunden!")
    
    cmd = sys.argv[1] if len(sys.argv)>1 else 'status'
    
    if cmd == 'status':    status(dev)
    elif cmd == 'block':   block_updates(dev)
    elif cmd == 'dashboard': launch_ha_dashboard(dev)
    elif cmd == 'shell':   
        r = dev.shell(' '.join(sys.argv[2:]))
        print(r)
    
    dev.close()
