import requests, time, random

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlZWEzY2ViZWM2NDM0ZDc3YTUzYmRjZDUxYWQwZmFiMiIsImlhdCI6MTc3MjIzNTkzNywiZXhwIjoyMDg3NTk1OTM3fQ.NWPIQwbtUJlmHzuMwkIIPjzLQcukT997SmL4rW-xQnk"
URL = "http://192.168.1.123:8123/api/services/light/turn_on"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

COLORS = [
    [255,0,0],[0,255,0],[0,0,255],[255,255,0],
    [255,0,255],[0,255,255],[255,128,0],[128,0,255],
    [255,20,147],[0,255,128],[255,69,0],[100,149,237]
]

for i in range(40):
    color = random.choice(COLORS)
    requests.post(URL, headers=HEADERS, json={
        "entity_id": "light.buro",
        "rgb_color": color,
        "brightness": 255,
        "transition": 0
    })
    time.sleep(0.3)

print("Disco over 🎉")
