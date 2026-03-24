import re, subprocess

c = open('/tmp/fam_base.html').read()

c = c.replace("const APP_VERSION='v2.5';", "const APP_VERSION='v2.6';")
c = c.replace(">v2.5<", ">v2.6<")

old_svg = """// SVG Bibliothek
const SVG = {
  bulb: '<path d="M9 21h6M12 3a6 6 0 0 1 6 6c0 2.5-1.3 4.7-3 6.1V17a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1v-1.9C7.3 13.7 6 11.5 6 9a6 6 0 0 1 6-6z"/>',
  strip: '<path d="M4 10h16M8 10V7a4 4 0 0 1 8 0v3"/><rect x="4" y="10" width="16" height="4" rx="2"/><path d="M4 14v1a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-1"/>',
  home:  '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
  sun:   '<circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.78" y2="19.78"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>',
  bed:   '<path d="M2 4v16M2 8h20a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/>',
  sofa:  '<path d="M20 9V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v2"/><path d="M2 11v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v2H6v-2a2 2 0 0 0-4 0z"/>',
  lamp:  '<path d="M9 21h6M12 3a6 6 0 0 1 6 6c0 2.5-1.3 4.7-3 6.1V17a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1v-1.9C7.3 13.7 6 11.5 6 9a6 6 0 0 1 6-6z"/><line x1="12" y1="17" x2="12" y2="21"/>',
  ceil:  '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>',
  wc:    '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"/><path d="M12 8v8M8 12h8"/>',
  tree:  '<path d="M17 14l3-3-3-3M7 14l-3-3 3-3"/><path d="M14 3l-2 18-2-18"/>',
};"""

new_svg = """const SVG = {
  ledstrip_h: '<rect x="2" y="9" width="20" height="6" rx="3"/><circle cx="6.5" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="10.5" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="14.5" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="18.5" cy="12" r="1.5" fill="currentColor" stroke="none"/>',
  ledstrip_v: '<rect x="9" y="2" width="6" height="20" rx="3"/><circle cx="12" cy="6.5" r="1.5" fill="currentColor" stroke="none"/><circle cx="12" cy="10.5" r="1.5" fill="currentColor" stroke="none"/><circle cx="12" cy="14.5" r="1.5" fill="currentColor" stroke="none"/><circle cx="12" cy="18.5" r="1.5" fill="currentColor" stroke="none"/>',
  ceiling: '<line x1="12" y1="2" x2="12" y2="6"/><path d="M5 6h14l-2 8H7L5 6z"/><line x1="8" y1="14" x2="6" y2="20"/><line x1="16" y1="14" x2="18" y2="20"/><line x1="6" y1="20" x2="18" y2="20"/>',
  hueplay: '<rect x="3" y="8" width="18" height="8" rx="4"/><circle cx="8" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="16" cy="12" r="2" fill="currentColor" stroke="none"/>',
  orb: '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="3" fill="currentColor" stroke="none"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>',
  moon: '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
  bedstrip: '<rect x="2" y="9" width="20" height="5" rx="2"/><path d="M4 6h5a2 2 0 0 1 2 2v1H4V6z"/><line x1="5" y1="14" x2="5" y2="18"/><line x1="19" y1="14" x2="19" y2="18"/>',
  wardrobe: '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="12" y1="3" x2="12" y2="21"/><path d="M8 12h1.5M14.5 12H16"/>',
  sconce: '<path d="M14 3H9a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h5"/><path d="M14 3c0 5 4 7 4 12M14 17c0-4 4-6 4-12"/>',
  corridor: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><line x1="9" y1="22" x2="9" y2="16"/><line x1="15" y1="22" x2="15" y2="16"/><line x1="9" y1="16" x2="15" y2="16"/>',
  wc: '<path d="M12 2a5 5 0 1 1 0 10A5 5 0 0 1 12 2z"/><path d="M4 22c0-4.4 3.6-8 8-8s8 3.6 8 8"/>',
  outdoor: '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/>',
};"""

c = c.replace(old_svg, new_svg)

old_rooms = """const LIGHT_ROOMS = [
  { room: '🛋️ Wohnzimmer', lights: [
    {id:'light.h61e1',   name:'Holzwand',  svg:SVG.strip},
    {id:'light.h618a',   name:'Sofa LED',  svg:SVG.sofa},
  ]},
  { room: '🍳 Küche', lights: [
    {id:'light.h618a_2', name:'Oberschrank LED', svg:SVG.strip},
  ]},
  { room: '🛏️ Schlafzimmer', lights: [
    {id:'light.schlafzimmer', name:'Schlafzimmer', svg:SVG.bulb},
    {id:'light.deckenlampe',  name:'Deckenlampe',  svg:SVG.ceil},
    {id:'light.hue_play',     name:'Hue Play',     svg:SVG.lamp},
    {id:'light.hue_iris',     name:'Hue Iris',     svg:SVG.lamp},
  ]},
  { room: '🛏️ Eltern SZ', lights: [
    {id:'light.eltern_schlafzimmer',       name:'Eltern SZ',      svg:SVG.bulb},
    {id:'light.color_temperature_light_1', name:'LED Bett',        svg:SVG.strip},
    {id:'light.shelly1_c45bbe47adb9',      name:'Kleiderschrank', svg:SVG.bulb, dom:'light'},
  ]},
  { room: '💼 Büro', lights: [
    {id:'switch.shelly1_98cdac0ca9b2', name:'Wandlampe', svg:SVG.lamp, dom:'switch'},
    {id:'light.hue_play_l',            name:'Hue Play',  svg:SVG.lamp},
  ]},
  { room: '🚪 Gänge & WC', lights: [
    {id:'light.gang_eg_licht',  name:'Gang EG',   svg:SVG.home, nodim:true},
    {id:'light.gang_og_licht',  name:'Gang OG',   svg:SVG.home, nodim:true},
    {id:'light.gaste_wc_licht', name:'Gäste WC',  svg:SVG.wc,   nodim:true},
  ]},
  { room: '🌿 Außen', lights: [
    {id:'light.garten_licht', name:'Fassade', svg:SVG.sun, nodim:true},
  ]},
];"""

new_rooms = """const LIGHT_ROOMS = [
  { room: '🛋️ Wohnzimmer', lights: [
    {id:'light.h61e1',  name:'Holzwand',    svg:SVG.ledstrip_h, caps:'rgb'},
    {id:'light.h618a',  name:'Sofa LED',    svg:SVG.ledstrip_h, caps:'rgb'},
  ]},
  { room: '🍳 Küche', lights: [
    {id:'light.h618a_2', name:'Oberschrank', svg:SVG.ledstrip_v, caps:'rgb'},
  ]},
  { room: '🛏️ Schlafzimmer', lights: [
    {id:'light.schlafzimmer', name:'Decke',    svg:SVG.ceiling, caps:'ct'},
    {id:'light.deckenlampe',  name:'Pendel',   svg:SVG.ceiling, caps:'ct'},
    {id:'light.hue_play',     name:'Hue Play', svg:SVG.hueplay, caps:'color'},
    {id:'light.hue_iris',     name:'Hue Iris', svg:SVG.orb,     caps:'color'},
  ]},
  { room: '🛏️ Eltern SZ', lights: [
    {id:'light.eltern_schlafzimmer',       name:'Decke',         svg:SVG.ceiling,  caps:'ct'},
    {id:'light.color_temperature_light_1', name:'LED Bett',      svg:SVG.bedstrip, caps:'ct'},
    {id:'light.shelly1_c45bbe47adb9',      name:'Kleiderschrank',svg:SVG.wardrobe, caps:'onoff', dom:'light'},
  ]},
  { room: '💼 Büro', lights: [
    {id:'switch.shelly1_98cdac0ca9b2', name:'Wandlampe', svg:SVG.sconce,  caps:'onoff', dom:'switch'},
    {id:'light.hue_play_l',            name:'Hue Play',  svg:SVG.hueplay, caps:'color'},
  ]},
  { room: '🚪 Gänge & WC', lights: [
    {id:'light.gang_eg_licht',  name:'Gang EG',  svg:SVG.corridor, caps:'onoff', nodim:true},
    {id:'light.gang_og_licht',  name:'Gang OG',  svg:SVG.corridor, caps:'onoff', nodim:true},
    {id:'light.gaste_wc_licht', name:'Gäste WC', svg:SVG.wc,       caps:'onoff', nodim:true},
  ]},
  { room: '🌿 Außen', lights: [
    {id:'light.garten_licht', name:'Fassade', svg:SVG.outdoor, caps:'onoff', nodim:true},
  ]},
];"""

c = c.replace(old_rooms, new_rooms)

new_css = """
/* ─── LIGHT DETAIL SHEET ─── */
#ld-bg{position:fixed;inset:0;background:rgba(0,0,0,.65);backdrop-filter:blur(12px);z-index:220;display:flex;align-items:flex-end;justify-content:center;opacity:0;pointer-events:none;transition:opacity .25s}
#ld-bg.show{opacity:1;pointer-events:all}
#ld-sheet{background:#1c1c1e;border-radius:26px 26px 0 0;padding:0 0 max(24px,env(safe-area-inset-bottom)) 0;width:100%;max-width:480px;transform:translateY(100%);transition:transform .35s cubic-bezier(.34,1.1,.64,1);max-height:90vh;overflow-y:auto}
#ld-bg.show #ld-sheet{transform:translateY(0)}
.ld-handle{width:40px;height:4px;background:rgba(255,255,255,.18);border-radius:2px;margin:12px auto 0}
.ld-head{display:flex;align-items:center;gap:14px;padding:18px 22px 0}
.ld-light-ico{width:54px;height:54px;border-radius:16px;background:rgba(255,255,255,.07);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .3s}
.ld-light-ico.on{background:rgba(255,159,10,.18)}
.ld-light-ico svg{width:26px;height:26px;stroke:rgba(255,255,255,.4);fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;transition:stroke .3s}
.ld-light-ico.on svg{stroke:#ff9f0a}
.ld-title{flex:1;min-width:0}
.ld-light-name{font-size:1.1rem;font-weight:700}
.ld-light-room{font-size:.68rem;color:rgba(255,255,255,.35);margin-top:2px}
.ld-power{width:50px;height:50px;border-radius:50%;border:2px solid rgba(255,255,255,.12);cursor:pointer;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.06);transition:all .25s;touch-action:manipulation;flex-shrink:0}
.ld-power:active{transform:scale(.88)}
.ld-power.on{background:rgba(255,159,10,.18);border-color:rgba(255,159,10,.4)}
.ld-power svg{width:22px;height:22px;stroke:rgba(255,255,255,.4);fill:none;stroke-width:2;stroke-linecap:round;transition:stroke .3s}
.ld-power.on svg{stroke:#ff9f0a}
.ld-body{padding:20px 22px 0}
.ld-sec{margin-bottom:24px}
.ld-sec-title{font-size:.56rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,.28);margin-bottom:12px}
.ld-bri-wrap{display:flex;align-items:center;gap:10px}
.ld-ico-sm{font-size:.85rem;flex-shrink:0}
input[type=range].ld-slider{-webkit-appearance:none;appearance:none;width:100%;height:7px;border-radius:4px;outline:none;cursor:pointer;flex:1}
input[type=range].ld-slider::-webkit-slider-thumb{-webkit-appearance:none;width:28px;height:28px;border-radius:50%;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.5);cursor:pointer;transition:transform .1s;border:2px solid rgba(255,255,255,.3)}
input[type=range].ld-slider:active::-webkit-slider-thumb{transform:scale(1.15)}
#ld-bri-slider{background:linear-gradient(to right,#333,rgba(255,159,10,.9))}
#ld-ct-slider{background:linear-gradient(to right,#ffb347,#fff5e0,#fff,#d4eaff,#a8d8ff)}
.ld-bri-val{font-size:.82rem;font-weight:700;color:rgba(255,255,255,.55);min-width:38px;text-align:right}
.ld-colors{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.ld-swatch{height:44px;border-radius:12px;cursor:pointer;border:2.5px solid transparent;touch-action:manipulation;transition:transform .15s,border-color .2s;box-shadow:inset 0 0 0 1px rgba(0,0,0,.2)}
.ld-swatch:active{transform:scale(.87)}
.ld-swatch.active{border-color:#fff;box-shadow:0 0 0 2px rgba(255,255,255,.3),inset 0 0 0 1px rgba(0,0,0,.2)}
.ld-presets{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding-bottom:4px}
.ld-preset{padding:14px 12px;border-radius:16px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);cursor:pointer;touch-action:manipulation;transition:background .2s;text-align:left}
.ld-preset:active{background:rgba(255,159,10,.1)}
.ld-preset-ico{font-size:1.3rem;margin-bottom:5px}
.ld-preset-name{font-size:.75rem;font-weight:600}
.ld-preset-desc{font-size:.6rem;color:rgba(255,255,255,.35);margin-top:2px}
.lt-tile{position:relative;overflow:hidden;user-select:none}
.lt-tile::after{content:'';position:absolute;inset:0;background:rgba(255,159,10,.1);opacity:0;border-radius:16px;transition:opacity .1s;pointer-events:none}
.lt-tile.pressing::after{opacity:1}
"""
c = c.replace('/* ─── FOOTER ─── */', new_css + '\n/* ─── FOOTER ─── */')

detail_html = """
<!-- Light Detail Sheet -->
<div id="ld-bg">
  <div id="ld-sheet">
    <div class="ld-handle"></div>
    <div class="ld-head">
      <div class="ld-light-ico" id="ld-ico">
        <svg id="ld-ico-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"></svg>
      </div>
      <div class="ld-title">
        <div class="ld-light-name" id="ld-name">–</div>
        <div class="ld-light-room" id="ld-room">–</div>
      </div>
      <button class="ld-power" id="ld-power" aria-label="Ein/Aus">
        <svg viewBox="0 0 24 24"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/></svg>
      </button>
    </div>
    <div class="ld-body">
      <div class="ld-sec" id="ld-bri-sec">
        <div class="ld-sec-title">Helligkeit</div>
        <div class="ld-bri-wrap">
          <span class="ld-ico-sm">🌑</span>
          <input type="range" class="ld-slider" id="ld-bri-slider" min="1" max="100" value="80">
          <span class="ld-ico-sm">☀️</span>
          <span class="ld-bri-val" id="ld-bri-val">80%</span>
        </div>
      </div>
      <div class="ld-sec" id="ld-ct-sec">
        <div class="ld-sec-title">Farbtemperatur</div>
        <div class="ld-bri-wrap">
          <span class="ld-ico-sm">🕯️</span>
          <input type="range" class="ld-slider" id="ld-ct-slider" min="2700" max="6500" value="3000">
          <span class="ld-ico-sm" style="filter:hue-rotate(180deg)">💡</span>
        </div>
      </div>
      <div class="ld-sec" id="ld-col-sec">
        <div class="ld-sec-title">Farbe</div>
        <div class="ld-colors" id="ld-colors"></div>
      </div>
      <div class="ld-sec" id="ld-presets-sec">
        <div class="ld-sec-title">Stimmungen</div>
        <div class="ld-presets" id="ld-presets"></div>
      </div>
    </div>
  </div>
</div>
"""
c = c.replace('\n<!-- Floating Feedback Button -->', detail_html + '\n<!-- Floating Feedback Button -->')

old_buildfn = """function buildLights(){
  const container=document.getElementById('lights-grid');
  let html='';
  LIGHT_ROOMS.forEach(room=>{
    html+=`<div class="room-label">${room.room}</div><div class="lights-grid-inner">`;
    html+=room.lights.map(l=>`
      <div class="lt-tile" data-id="${l.id}" data-dom="${l.dom||'light'}" data-nodim="${l.nodim||false}">
        <div class="lt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${l.svg}</svg></div>
        <div>
          <div class="lt-name">${l.name}</div>
          <div class="lt-state">Aus</div>
        </div>
      </div>`).join('');
    html+=`</div>`;
  });
  container.innerHTML=html;
  container.querySelectorAll('.lt-tile').forEach(t=>{
    t.addEventListener('click',()=>{
      const on=t.classList.contains('on');
      const dom=t.dataset.dom;
      svc(dom,on?'turn_off':'turn_on',{entity_id:t.dataset.id});
      t.classList.toggle('on',!on);
      const stEl=t.querySelector('.lt-state');
      if(stEl)stEl.textContent=!on?'Ein':'Aus';
    });
  });
}"""

new_buildfn = """// ─── LIGHT DETAIL PANEL ───
let _ldLight=null;
const COLORS=[
  {name:'Warmweiß',  rgb:[255,210,140], ct:2700},
  {name:'Neutral',   rgb:[255,248,220], ct:4000},
  {name:'Kaltweiß',  rgb:[200,225,255], ct:6500},
  {name:'Rot',       rgb:[255,40,40]},
  {name:'Orange',    rgb:[255,140,0]},
  {name:'Gelb',      rgb:[255,230,0]},
  {name:'Grün',      rgb:[0,200,80]},
  {name:'Türkis',    rgb:[0,200,200]},
  {name:'Blau',      rgb:[30,100,255]},
  {name:'Lila',      rgb:[160,40,255]},
  {name:'Pink',      rgb:[255,40,160]},
  {name:'Weiß',      rgb:[255,255,255]},
];
const PRESETS=[
  {ico:'🌅',name:'Entspannen', desc:'Warm & gedimmt',   bri:35, ct:2700},
  {ico:'📖',name:'Lesen',      desc:'Hell & neutral',   bri:90, ct:4000},
  {ico:'🎬',name:'Film',       desc:'Ambient & dunkel', bri:12, ct:2700},
  {ico:'⚡',name:'Fokus',      desc:'Kalt & hell',      bri:100,ct:5500},
];
function debounce(fn,ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms);};}
const _sendBri=debounce((id,v)=>svc('light','turn_on',{entity_id:id,brightness_pct:v,transition:0.3}),240);
const _sendCT =debounce((id,v)=>svc('light','turn_on',{entity_id:id,color_temp_kelvin:v,transition:0.3}),300);
const _sendRGB=debounce((id,v)=>svc('light','turn_on',{entity_id:id,rgb_color:v,transition:0.5}),150);

function showLightDetail(light,room){
  _ldLight=light;
  const st=_S[light.id]||{};
  const on=st.state==='on';
  const a=st.attributes||{};
  document.getElementById('ld-name').textContent=light.name;
  document.getElementById('ld-room').textContent=room;
  document.getElementById('ld-ico-svg').innerHTML=light.svg;
  document.getElementById('ld-ico').classList.toggle('on',on);
  document.getElementById('ld-power').classList.toggle('on',on);
  const caps=light.caps||'onoff';
  const hasBri=caps!=='onoff';
  const hasCT=caps==='ct'||caps==='color'||caps==='rgb';
  const hasCol=caps==='rgb'||caps==='color';
  document.getElementById('ld-bri-sec').style.display=hasBri?'':'none';
  document.getElementById('ld-ct-sec').style.display=hasCT?'':'none';
  document.getElementById('ld-col-sec').style.display=hasCol?'':'none';
  document.getElementById('ld-presets-sec').style.display=hasBri?'':'none';
  if(hasBri){
    const bri=Math.round((a.brightness||200)/2.55);
    document.getElementById('ld-bri-slider').value=bri;
    document.getElementById('ld-bri-val').textContent=bri+'%';
  }
  if(hasCT){
    const ct=a.color_temp_kelvin||3000;
    document.getElementById('ld-ct-slider').value=Math.min(6500,Math.max(2700,ct));
  }
  if(hasCol){
    const cols=document.getElementById('ld-colors');
    cols.innerHTML=COLORS.map((col,i)=>`<div class="ld-swatch" data-i="${i}" style="background:rgb(${col.rgb.join(',')})" title="${col.name}"></div>`).join('');
    cols.querySelectorAll('.ld-swatch').forEach(sw=>{
      sw.addEventListener('click',()=>{
        cols.querySelectorAll('.ld-swatch').forEach(x=>x.classList.remove('active'));
        sw.classList.add('active');
        const col=COLORS[+sw.dataset.i];
        if(col.ct) _sendCT(light.id,col.ct);
        else _sendRGB(light.id,col.rgb);
      });
    });
  }
  if(hasBri){
    const pp=document.getElementById('ld-presets');
    pp.innerHTML=PRESETS.map((p,i)=>`<div class="ld-preset" data-pi="${i}"><div class="ld-preset-ico">${p.ico}</div><div class="ld-preset-name">${p.name}</div><div class="ld-preset-desc">${p.desc}</div></div>`).join('');
    pp.querySelectorAll('.ld-preset').forEach(el=>{
      el.addEventListener('click',()=>{
        const p=PRESETS[+el.dataset.pi];
        svc('light','turn_on',{entity_id:light.id,brightness_pct:p.bri,color_temp_kelvin:p.ct,transition:1});
        document.getElementById('ld-bri-slider').value=p.bri;
        document.getElementById('ld-bri-val').textContent=p.bri+'%';
        document.getElementById('ld-ct-slider').value=p.ct;
        toast(p.ico+' '+p.name);
      });
    });
  }
  document.getElementById('ld-bg').classList.add('show');
}
document.getElementById('ld-bg').addEventListener('click',e=>{if(e.target===e.currentTarget)document.getElementById('ld-bg').classList.remove('show');});
document.getElementById('ld-power').addEventListener('click',()=>{
  if(!_ldLight)return;
  const on=document.getElementById('ld-power').classList.contains('on');
  const dom=_ldLight.dom||'light';
  svc(dom,on?'turn_off':'turn_on',{entity_id:_ldLight.id});
  document.getElementById('ld-power').classList.toggle('on',!on);
  document.getElementById('ld-ico').classList.toggle('on',!on);
  setTimeout(fetchAndUpdate,900);
});
document.getElementById('ld-bri-slider').addEventListener('input',e=>{
  document.getElementById('ld-bri-val').textContent=e.target.value+'%';
  if(_ldLight)_sendBri(_ldLight.id,+e.target.value);
});
document.getElementById('ld-ct-slider').addEventListener('input',e=>{if(_ldLight)_sendCT(_ldLight.id,+e.target.value);});

function buildLights(){
  const container=document.getElementById('lights-grid');
  let html='';
  LIGHT_ROOMS.forEach(room=>{
    html+=`<div class="room-label">${room.room}</div><div class="lights-grid-inner">`;
    html+=room.lights.map(l=>`
      <div class="lt-tile" data-id="${l.id}" data-dom="${l.dom||'light'}" data-nodim="${l.nodim||false}">
        <div class="lt-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${l.svg}</svg></div>
        <div><div class="lt-name">${l.name}</div><div class="lt-state">Aus</div></div>
      </div>`).join('');
    html+=`</div>`;
  });
  container.innerHTML=html;
  container.querySelectorAll('.lt-tile').forEach(t=>{
    const lCfg=LIGHTS.find(l=>l.id===t.dataset.id);
    const rCfg=LIGHT_ROOMS.find(r=>r.lights.some(l=>l.id===t.dataset.id));
    let pressTimer=null,didLong=false;
    t.addEventListener('touchstart',()=>{
      didLong=false;t.classList.add('pressing');
      pressTimer=setTimeout(()=>{
        didLong=true;t.classList.remove('pressing');
        navigator.vibrate&&navigator.vibrate(25);
        if(lCfg)showLightDetail(lCfg,rCfg?.room||'');
      },550);
    },{passive:true});
    t.addEventListener('touchend',()=>{clearTimeout(pressTimer);t.classList.remove('pressing');});
    t.addEventListener('touchmove',()=>{clearTimeout(pressTimer);t.classList.remove('pressing');});
    t.addEventListener('click',()=>{
      if(didLong){didLong=false;return;}
      const on=t.classList.contains('on'),dom=t.dataset.dom;
      svc(dom,on?'turn_off':'turn_on',{entity_id:t.dataset.id});
      t.classList.toggle('on',!on);
      const s=t.querySelector('.lt-state');if(s)s.textContent=!on?'Ein':'Aus';
    });
  });
}"""

c = c.replace(old_buildfn, new_buildfn)

scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
open('/tmp/fc.js','w').write('\n'.join(scripts))
r = subprocess.run(['node','--check','/tmp/fc.js'], capture_output=True, text=True)
print(f"JS: {'OK' if r.returncode==0 else r.stderr[:400]}")
print(f"Size: {len(c)}")
with open('/tmp/family_v26.html','w') as f: f.write(c)
