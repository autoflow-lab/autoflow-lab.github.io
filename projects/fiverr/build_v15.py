#!/usr/bin/env python3
"""
v15: Complete rebuild of demo.html with:
  1. Real photo floor plan (fp_off.png base + per-room lit overlays via SVG <image> + clipPath)
  2. Multilingual EN/DE with toggle in nav
  3. Full mobile optimization
  4. Color picker per room with hue-rotate CSS filter
  5. Design polish
"""

# ─────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────
BASE_URL = 'https://autoflow-lab.github.io'
EMAIL = 'clawy.studio@gmail.com'
FIVERR_URL = 'https://www.fiverr.com/autoflow-lab'

ROOM_COLORS = {
    'warm':   'saturate(0.25) sepia(0.75) brightness(1.05)',
    'cool':   'saturate(0.35) hue-rotate(22deg) brightness(1.08)',
    'white':  'saturate(0.1) brightness(1.18)',
    'cyan':   'hue-rotate(0deg) saturate(1.0)',
    'blue':   'hue-rotate(60deg) saturate(1.15)',
    'purple': 'hue-rotate(90deg) saturate(1.2)',
    'pink':   'hue-rotate(100deg) saturate(1.25)',
    'red':    'hue-rotate(180deg) saturate(1.1)',
    'amber':  'saturate(0.5) sepia(0.45) brightness(1.0)',
    'green':  'hue-rotate(300deg) saturate(1.1)',
}

# Room clip polygon coordinates (from image analysis, 1376×768)
ROOM_CLIPS = {
    'bed1':   '695,148 990,195 990,335 695,290',
    'bath':   '1000,200 1145,250 1145,430 1000,380',
    'living': '530,240 990,340 990,520 530,420',
    'dining': '810,420 1080,490 1080,610 810,545',
    'bed2':   '230,330 480,390 480,530 230,470',
    'office': '485,450 660,500 660,610 485,565',
    'hall':   '480,290 695,340 695,560 480,510',
}

# Lamp positions in the 1376×768 image
LAMPS = {
    'L1':  {'cx':840, 'cy':178, 'room':'bed1',   'label_de':'Hängelampe',      'label_en':'Pendant',      'zone_de':'Schlafzimmer', 'zone_en':'Bedroom'},
    'L2':  {'cx':802, 'cy':222, 'room':'bed1',   'label_de':'Nachttisch L',    'label_en':'Bedside L',    'zone_de':'Schlafzimmer', 'zone_en':'Bedroom'},
    'L3':  {'cx':895, 'cy':240, 'room':'bed1',   'label_de':'Nachttisch R',    'label_en':'Bedside R',    'zone_de':'Schlafzimmer', 'zone_en':'Bedroom'},
    'L4':  {'cx':380, 'cy':395, 'room':'bed2',   'label_de':'Stehlampe',       'label_en':'Floor Lamp',   'zone_de':'Zimmer 2',     'zone_en':'2nd Room'},
    'L5':  {'cx':302, 'cy':360, 'room':'bed2',   'label_de':'Wandlampe',       'label_en':'Wall Sconce',  'zone_de':'Zimmer 2',     'zone_en':'2nd Room'},
    'L6':  {'cx':678, 'cy':285, 'room':'living', 'label_de':'Küchenlampe',     'label_en':'Kitchen Light','zone_de':'Küche',        'zone_en':'Kitchen'},
    'L7':  {'cx':760, 'cy':348, 'room':'living', 'label_de':'Kücheninsel',     'label_en':'Island Light', 'zone_de':'Küche',        'zone_en':'Kitchen'},
    'L8':  {'cx':580, 'cy':520, 'room':'office', 'label_de':'Schreibtischlampe','label_en':'Desk Lamp',   'zone_de':'Büro',         'zone_en':'Office'},
    'L9':  {'cx':1072,'cy':268, 'room':'bath',   'label_de':'Spiegellampe',    'label_en':'Mirror Light', 'zone_de':'Bad',          'zone_en':'Bathroom'},
    'L10': {'cx':1068,'cy':310, 'room':'bath',   'label_de':'Deckenlampe',     'label_en':'Ceiling',      'zone_de':'Bad',          'zone_en':'Bathroom'},
    'L11': {'cx':900, 'cy':478, 'room':'dining', 'label_de':'Pendellampe',     'label_en':'Pendant',      'zone_de':'Esszimmer',    'zone_en':'Dining'},
}

# ─────────────────────────────────────────────────────────
#  FLOOR PLAN SVG SECTION
# ─────────────────────────────────────────────────────────

def make_clip_defs():
    defs = ''
    for room_id, pts in ROOM_CLIPS.items():
        defs += f'      <clipPath id="clip-{room_id}"><polygon points="{pts}"/></clipPath>\n'
    return defs

def make_room_overlays():
    out = ''
    for room_id in ROOM_CLIPS:
        out += f'''      <g id="rl-{room_id}" opacity="0"
         style="transition:opacity .65s cubic-bezier(.4,0,.2,1)">
        <image id="ri-{room_id}"
               href="{BASE_URL}/fp_cyan.png"
               width="1376" height="768"
               clip-path="url(#clip-{room_id})"
               preserveAspectRatio="none"
               style="transition:filter .45s ease"/>
      </g>\n'''
    return out

def make_lamp_fixtures():
    # Build SVG lamp fixtures
    out = ''
    for lid, l in LAMPS.items():
        cx, cy = l['cx'], l['cy']
        out += f'''      <g id="lamp-{lid}" class="lamp-fix" data-lamp="{lid}" data-room="{l['room']}"
         onclick="lampClick('{lid}',event)" oncontextmenu="lampLongPress('{lid}',event)"
         ontouchstart="lampTouchStart('{lid}',event)" ontouchend="lampTouchEnd(event)"
         style="cursor:pointer">
        <circle cx="{cx}" cy="{cy}" r="14" fill="rgba(0,0,0,0)" class="lamp-hitzone"/>
        <circle id="lc-{lid}" cx="{cx}" cy="{cy}" r="5.5"
                fill="#6a6a6a" class="lamp-bulb"
                style="transition:fill .4s,filter .4s,r .25s"/>
        <circle id="lr-{lid}" cx="{cx}" cy="{cy}" r="10"
                fill="none" stroke="#6a6a6a" stroke-width="1" opacity=".15"
                class="lamp-ring" style="transition:all .4s"/>
      </g>\n'''
    return out

FP_SECTION = f'''            <div class="fp-hint" data-i18n="fp_hint">Klick: An/Aus · Rechtsklick: Farbe wählen</div>
            <div class="photo-fp" id="fp-container">

  <!-- Color picker popover -->
  <div class="color-popover" id="color-popover">
    <div class="cp-title" id="cp-room-label">Raum</div>
    <div class="cp-swatches" id="cp-swatches"></div>
    <div class="cp-brightness">
      <label data-i18n="brightness">Helligkeit</label>
      <input type="range" min="10" max="100" value="80" id="cp-bright"
             oninput="applyBrightness(this.value)">
    </div>
    <button onclick="closeColorPicker()"
            style="margin-top:6px;width:100%;padding:6px;border-radius:7px;
                   border:1px solid var(--border2);background:var(--bg2);
                   color:var(--text);font-size:.72rem;cursor:pointer;font-family:inherit"
            data-i18n="close">Schließen</button>
  </div>

  <!-- ── Base: no-lights image ── -->
  <img id="fp-base"
       src="{BASE_URL}/fp_off.png"
       alt="Smart Home Floor Plan"
       style="width:100%;display:block;border-radius:12px;
              user-select:none;-webkit-user-drag:none;pointer-events:none">

  <!-- ── SVG: Room light overlays + lamp fixtures ── -->
  <svg id="fp-lights" viewBox="0 0 1376 768"
       xmlns="http://www.w3.org/2000/svg"
       style="position:absolute;inset:0;width:100%;height:100%;
              z-index:2;border-radius:12px;pointer-events:none">
    <defs>
{make_clip_defs()}
      <!-- Lamp glow filter -->
      <filter id="lamp-glow" x="-80%" y="-80%" width="360%" height="360%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <!-- Ring pulse -->
    </defs>

    <!-- ── ROOM LIGHT OVERLAYS (lit image, clipped per room) ── -->
{make_room_overlays()}
    <!-- ── LAMP FIXTURES (pointer-events enabled) ── -->
    <g style="pointer-events:all">
{make_lamp_fixtures()}    </g>

    <!-- ── LABELS (visible on hover) ── -->
    <g id="fp-labels" style="pointer-events:none;opacity:0;transition:opacity .3s">
{"".join(f'      <text x="{l["cx"]}" y="{l["cy"]-14}" text-anchor="middle" font-size="10" font-family="Inter,sans-serif" font-weight="700" fill="rgba(255,255,255,.85)">{lid}</text>\n' for lid,l in LAMPS.items())}    </g>
  </svg>
</div>'''

print("FP section built:", len(FP_SECTION), "chars")

# Save for use in main script
with open('/tmp/fp_section.html','w') as f:
    f.write(FP_SECTION)

