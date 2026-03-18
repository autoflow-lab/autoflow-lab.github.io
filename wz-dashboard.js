/* ═══════════════════════════════════════════════════════
   WZ Dashboard v2 — iOS-style SPA, multi-page
   autoflow-lab · Clawy 🦀
═══════════════════════════════════════════════════════ */

const WZ_ICONS = {
  home:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12L12 3l9 9"/><path d="M5 10v9a1 1 0 001 1h4v-4h4v4h4a1 1 0 001-1v-9"/></svg>`,
  music:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="18" r="2"/><circle cx="18" cy="16" r="2"/><path d="M10 18V8l10-2v10"/></svg>`,
  lights:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6M12 3a6 6 0 016 6c0 2.5-1.5 4.5-3 6H9c-1.5-1.5-3-3.5-3-6a6 6 0 016-6z"/><path d="M9 17h6"/></svg>`,
  plan:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`,
  play:    `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>`,
  pause:   `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`,
  stop:    `<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="1"/></svg>`,
  prev:    `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zm3.5 6 8.5 6V6z"/></svg>`,
  next:    `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zm2.5-6V9l5.5 3-5.5 3zM16 6h2v12h-2z"/></svg>`,
  volDown: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.54 8.46a5 5 0 010 7.07"/></svg>`,
  volUp:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.54 8.46a5 5 0 010 7.07M19.07 4.93a10 10 0 010 14.14"/></svg>`,
  sun:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`,
  moon:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>`,
  power:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18.36 6.64a9 9 0 11-12.73 0M12 2v10"/></svg>`,
  spotify: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.586 14.424a.622.622 0 01-.857.207c-2.348-1.435-5.304-1.76-8.785-.964a.623.623 0 01-.277-1.215c3.809-.87 7.077-.496 9.712 1.115a.623.623 0 01.207.857zm1.223-2.722a.779.779 0 01-1.072.257c-2.687-1.652-6.785-2.131-9.965-1.166a.779.779 0 01-.973-.52.779.779 0 01.52-.972c3.632-1.102 8.147-.568 11.233 1.328a.779.779 0 01.257 1.073zm.105-2.835c-3.223-1.914-8.54-2.09-11.618-1.156a.935.935 0 11-.543-1.79c3.532-1.072 9.404-.865 13.115 1.338a.935.935 0 01-.954 1.608z"/></svg>`,
  radio:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h18M3 7l2-4h14l2 4M5 7v12a2 2 0 002 2h10a2 2 0 002-2V7"/><circle cx="12" cy="13" r="3"/><line x1="18" y1="9" x2="18" y2="9.01"/></svg>`,
  bulb:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6M12 3a6 6 0 016 6c0 2.5-1.5 4.5-3 6H9c-1.5-1.5-3-3.5-3-6a6 6 0 016-6z"/><path d="M9 17h6"/></svg>`,
  tv:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="14" rx="2"/><path d="M8 20h8M12 18v2"/></svg>`,
  strip:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="2"/><path d="M6 10V8M10 10V6M14 10V8M18 10V6"/></svg>`,
  scene:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`,
};

const RADIO_STATIONS = [
  { name:'SRF 1',   color:'#4a9eff', url:'http://stream.srg-ssr.ch/m/drs1/mp3_128' },
  { name:'SRF 3',   color:'#ff6b35', url:'http://stream.srg-ssr.ch/m/drs3/mp3_128' },
  { name:'Pop',     color:'#ff3b8a', url:'http://stream.srg-ssr.ch/m/rsp/mp3_128' },
  { name:'Energy',  color:'#f7c948', url:'https://energyzurich.ice.infomaniak.ch/energyzurich-high.mp3' },
  { name:'R.24',    color:'#a855f7', url:'https://radio24.ice.infomaniak.ch/radio24-high.mp3' },
];

const LIGHTS_CFG = [
  { id:'light.deckenlampe', name:'Decke',    icon:'bulb',  colorOn:'#ffe8a0' },
  { id:'light.h618a',       name:'Sofa',     icon:'strip', colorOn:'#ff9f40' },
  { id:'light.h618a_2',     name:'Küche',    icon:'strip', colorOn:'#ff7040' },
  { id:'media_player.lg_webos_tv_oled65g49ls_2', name:'TV', icon:'tv', colorOn:'#60b0ff' },
];

class WzDashboard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode:'open' });
    this._hass = null;
    this._page = 'home';   // home | music | lights | plan
    this._activeRadio = null;
    this._dark = new Date().getHours() < 7 || new Date().getHours() >= 21;
    this._built = false;
    this._clockTimer = null;
  }

  set hass(h) {
    this._hass = h;
    if (!this._built) { this._render(); this._built=true; }
    else this._patch();
  }

  connectedCallback() {
    this._clockTimer = setInterval(() => {
      const el = this.shadowRoot.getElementById('wz-clock');
      if (el) {
        const n = new Date();
        el.textContent = `${String(n.getHours()).padStart(2,'0')}:${String(n.getMinutes()).padStart(2,'0')}`;
      }
    }, 10000);
  }

  disconnectedCallback() { clearInterval(this._clockTimer); }

  _t(id, attr) {
    if (!this._hass) return null;
    const s = this._hass.states[id];
    if (!s) return null;
    return attr ? s.attributes[attr] : s;
  }
  _state(id) { return this._t(id)?.state || 'unavailable'; }
  _attr(id, a) { return this._t(id)?.attributes?.[a]; }
  _svc(domain, service, data) { this._hass?.callService(domain, service, data); }

  _css() {
    const d = this._dark;
    return `
:host { display:block; width:100%; height:100vh; overflow:hidden; }
* { box-sizing:border-box; margin:0; padding:0;
    font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif;
    -webkit-tap-highlight-color:transparent; user-select:none; }

.root {
  height:100vh; width:100%; display:flex; flex-direction:column;
  background:${d
    ? 'radial-gradient(ellipse at 15% 85%,#1a083844 0%,transparent 55%),radial-gradient(ellipse at 85% 15%,#06183044 0%,transparent 50%),linear-gradient(160deg,#0b0b1d 0%,#07070f 100%)'
    : 'linear-gradient(160deg,#f0f4ff 0%,#e8f0fb 50%,#f4f0ff 100%)'};
  color:${d ? '#f0f0f5' : '#1d1d1f'};
}

/* ── PAGE ── */
.page { flex:1; overflow-y:auto; overflow-x:hidden; padding:clamp(20px,4vw,40px) clamp(16px,4vw,36px) 20px; }
.page-hidden { display:none !important; }

/* ── GLASS CARD ── */
.card {
  background:${d ? 'rgba(255,255,255,0.055)' : 'rgba(255,255,255,0.72)'};
  backdrop-filter:blur(28px); -webkit-backdrop-filter:blur(28px);
  border:1px solid ${d ? 'rgba(255,255,255,0.09)' : 'rgba(0,0,0,0.07)'};
  border-radius:20px;
  padding:clamp(16px,3vw,24px);
  transition:background .35s;
}

/* ── SECTION LABEL ── */
.lbl {
  font-size:.58rem; font-weight:700; letter-spacing:2.5px; text-transform:uppercase;
  color:${d ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.3)'};
  margin-bottom:14px;
}

/* ══ HOME PAGE ══ */
.home-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.clock-card { grid-column:1/2; }
.weather-card { grid-column:2/3; }
.status-card { grid-column:1/3; }

.clock-big {
  font-size:clamp(3.2rem,12vw,5rem); font-weight:100; letter-spacing:-3px; line-height:1;
  color:${d ? '#fff' : '#1d1d1f'};
}
.clock-date { font-size:.7rem; color:${d ? 'rgba(255,255,255,0.38)' : 'rgba(0,0,0,0.38)'}; letter-spacing:1.5px; text-transform:uppercase; margin-top:6px; }

.w-row { display:flex; align-items:center; gap:10px; }
.w-icon { font-size:2.2rem; }
.w-temp { font-size:clamp(1.8rem,6vw,2.8rem); font-weight:100; }
.w-sub { font-size:.65rem; color:${d ? 'rgba(255,255,255,0.38)' : 'rgba(0,0,0,0.38)'}; margin-top:2px; }

.status-row { display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
.status-pill {
  display:flex; align-items:center; gap:7px;
  padding:8px 14px; border-radius:24px;
  background:${d ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)'};
  border:1px solid ${d ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.07)'};
  font-size:.72rem; font-weight:500;
}
.status-dot { width:7px; height:7px; border-radius:50%; }

/* ══ MUSIC PAGE ══ */
.radio-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-bottom:16px; }
.radio-btn {
  display:flex; flex-direction:column; align-items:center; gap:7px;
  padding:14px 6px; border-radius:18px; cursor:pointer;
  border:1.5px solid ${d ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.07)'};
  background:${d ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.6)'};
  transition:all .15s;
}
.radio-btn:active { transform:scale(.92); }
.radio-btn.active { border-width:2px; }
.radio-dot { width:10px; height:10px; border-radius:50%; }
.radio-name { font-size:.58rem; font-weight:600; color:${d ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.45)'}; text-align:center; }

.now-title { font-size:1rem; font-weight:500; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.now-sub { font-size:.72rem; color:${d ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)'}; margin-top:3px; }

.ctrl-row { display:flex; align-items:center; gap:clamp(8px,3vw,20px); margin-top:16px; }
.ctrl-btn {
  display:flex; align-items:center; justify-content:center;
  background:none; border:none; cursor:pointer;
  color:${d ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.65)'};
  padding:8px; border-radius:50%; transition:all .15s;
  flex-shrink:0;
}
.ctrl-btn:active { transform:scale(.85); }
.ctrl-btn.play {
  background:${d ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
  width:52px; height:52px; border-radius:50%;
  color:${d ? '#fff' : '#1d1d1f'};
}
.ctrl-btn svg { width:22px; height:22px; }
.ctrl-btn.sm svg { width:18px; height:18px; }
.ctrl-btn.lg svg { width:26px; height:26px; }

.spacer { flex:1; }

.vol-row { display:flex; align-items:center; gap:10px; margin-top:14px; }
.vol-btn { display:flex; align-items:center; justify-content:center; background:none; border:none; cursor:pointer; color:${d ? 'rgba(255,255,255,0.45)' : 'rgba(0,0,0,0.4)'}; flex-shrink:0; }
.vol-btn svg { width:20px; height:20px; }
.vol-slider {
  flex:1; height:4px; border-radius:2px; -webkit-appearance:none; appearance:none;
  background:${d ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.12)'};
  outline:none; cursor:pointer; touch-action:pan-x;
}
.vol-slider::-webkit-slider-thumb {
  -webkit-appearance:none; width:18px; height:18px; border-radius:50%;
  background:${d ? '#fff' : '#1d1d1f'};
  box-shadow:0 2px 6px rgba(0,0,0,.2); cursor:pointer;
}
.vol-pct { font-size:.68rem; color:${d ? 'rgba(255,255,255,0.38)' : 'rgba(0,0,0,0.38)'}; min-width:30px; text-align:right; }

.spotify-row {
  display:flex; align-items:center; gap:12px; padding:14px 16px;
  border-radius:16px; cursor:pointer;
  background:rgba(29,185,84,${d ? '0.09' : '0.07'});
  border:1.5px solid rgba(29,185,84,${d ? '0.22' : '0.18'});
  transition:all .15s; margin-top:12px;
}
.spotify-row:active { transform:scale(.98); background:rgba(29,185,84,0.18); }
.spotify-icon svg { width:28px; height:28px; color:#1db954; }
.spotify-title { font-size:.85rem; font-weight:600; color:#1db954; }
.spotify-sub { font-size:.65rem; color:rgba(29,185,84,.6); margin-top:1px; }

/* ══ LIGHTS PAGE ══ */
.lights-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.light-card {
  display:flex; flex-direction:column; gap:12px;
  padding:18px 16px; border-radius:20px; cursor:pointer;
  border:1.5px solid ${d ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.06)'};
  background:${d ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.65)'};
  backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px);
  transition:all .2s;
}
.light-card:active { transform:scale(.97); }
.light-card.on { border-color:rgba(255,200,60,0.35); background:${d ? 'rgba(255,200,60,0.08)' : 'rgba(255,200,60,0.1)'}; }
.light-icon-wrap {
  width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center;
  background:${d ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.06)'};
  transition:all .25s;
}
.light-card.on .light-icon-wrap { background:rgba(255,200,60,0.18); }
.light-icon-wrap svg { width:22px; height:22px; color:${d ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.45)'}; }
.light-card.on .light-icon-wrap svg { color:#ffc040; }
.light-name { font-size:.78rem; font-weight:600; }
.light-status { font-size:.65rem; color:${d ? 'rgba(255,255,255,0.35)' : 'rgba(0,0,0,0.35)'}; }
.light-card.on .light-status { color:${d ? 'rgba(255,200,60,0.7)' : 'rgba(180,130,0,0.7)'}; }

.bright-slider {
  width:100%; height:3px; border-radius:2px; -webkit-appearance:none; appearance:none;
  outline:none; cursor:pointer; touch-action:pan-x;
  background:${d ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.1)'};
}
.bright-slider::-webkit-slider-thumb {
  -webkit-appearance:none; width:14px; height:14px; border-radius:50%;
  background:#ffc040; box-shadow:0 1px 4px rgba(0,0,0,.2); cursor:pointer;
}

.scenes-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:14px; }
.scene-btn {
  display:flex; flex-direction:column; align-items:center; gap:6px;
  padding:14px 8px; border-radius:16px; cursor:pointer;
  background:${d ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.65)'};
  border:1.5px solid ${d ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.07)'};
  transition:all .15s; backdrop-filter:blur(16px);
}
.scene-btn:active { transform:scale(.93); }
.scene-btn svg { width:20px; height:20px; color:${d ? 'rgba(255,255,255,0.55)' : 'rgba(0,0,0,0.5)'}; }
.scene-btn span { font-size:.65rem; font-weight:600; color:${d ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.5)'}; }
.scene-btn.off-btn svg, .scene-btn.off-btn span { color:rgba(255,70,70,0.7); }

/* ══ BOTTOM NAV ══ */
.nav {
  display:flex; align-items:center; justify-content:space-around;
  padding:10px 20px ${CSS.supports('padding-bottom','env(safe-area-inset-bottom)') ? 'max(10px,env(safe-area-inset-bottom))' : '10px'};
  background:${d ? 'rgba(10,10,20,0.88)' : 'rgba(248,248,255,0.88)'};
  backdrop-filter:blur(28px); -webkit-backdrop-filter:blur(28px);
  border-top:1px solid ${d ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.07)'};
  flex-shrink:0;
}
.nav-btn {
  display:flex; flex-direction:column; align-items:center; gap:4px;
  padding:6px 16px; border-radius:14px; border:none;
  background:none; cursor:pointer; transition:all .18s;
  color:${d ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.3)'};
  min-width:60px;
}
.nav-btn svg { width:22px; height:22px; transition:all .18s; }
.nav-btn span { font-size:.55rem; font-weight:600; letter-spacing:.5px; text-transform:uppercase; transition:all .18s; }
.nav-btn.active { color:${d ? '#fff' : '#1d1d1f'}; }
.nav-btn.active svg { transform:scale(1.1); }
    `;
  }

  _weatherIcon(s) {
    return {sunny:'☀️','clear-night':'🌙',partlycloudy:'⛅',cloudy:'☁️',fog:'🌫️',
            rainy:'🌧️',snowy:'❄️',windy:'💨',lightning:'⛈️',pouring:'🌧️'}[s] || '🌤️';
  }

  _renderHome() {
    const weather = this._t('weather.forecast_home');
    const wState = weather?.state || '';
    const temp = this._attr('weather.forecast_home','temperature') ?? '—';
    const n = new Date();
    const time = `${String(n.getHours()).padStart(2,'0')}:${String(n.getMinutes()).padStart(2,'0')}`;
    const date = n.toLocaleDateString('de-CH',{weekday:'long',day:'numeric',month:'long'});
    const alm = this._state('media_player.wohnzimmer_alm');
    const lightsOn = LIGHTS_CFG.filter(l => this._state(l.id) === 'on').length;
    const almTitle = this._attr('media_player.wohnzimmer_alm','media_title');
    const mac = this._state('sensor.macbook_air_von_janis_internal_battery_level');

    return `
    <div class="home-grid">
      <div class="card clock-card">
        <div class="clock-big" id="wz-clock">${time}</div>
        <div class="clock-date">${date}</div>
      </div>
      <div class="card weather-card">
        <div class="w-row">
          <span class="w-icon">${this._weatherIcon(wState)}</span>
          <div>
            <div class="w-temp">${temp}°</div>
            <div class="w-sub">Egg SZ</div>
          </div>
        </div>
      </div>
      <div class="card status-card">
        <div class="status-row">
          <div class="status-pill">
            <div class="status-dot" style="background:${lightsOn > 0 ? '#ffc040' : '#888'}"></div>
            ${lightsOn > 0 ? lightsOn + ' Licht' + (lightsOn > 1 ? 'er an' : ' an') : 'Alles aus'}
          </div>
          ${alm === 'playing' ? `<div class="status-pill">
            <div class="status-dot" style="background:#4a9eff;animation:pulse 1.5s ease-in-out infinite"></div>
            ${almTitle || 'Musik läuft'}
          </div>` : ''}
          ${mac !== 'unavailable' ? `<div class="status-pill">💻 ${mac}%</div>` : ''}
        </div>
      </div>
    </div>
    <style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}</style>`;
  }

  _renderMusic() {
    const alm = this._t('media_player.wohnzimmer_alm');
    const almState = alm?.state || 'off';
    const almTitle = alm?.attributes?.media_title || (almState === 'playing' ? 'Läuft...' : 'Bereit');
    const almArtist = alm?.attributes?.media_artist || 'Almando Wohnzimmer';
    const almVol = Math.round((alm?.attributes?.volume_level ?? 0.5) * 100);
    const spot = this._t('media_player.spotify_janisss');
    const spotTitle = spot?.attributes?.media_title || '';
    const spotArtist = spot?.attributes?.media_artist || '';

    const radioHTML = RADIO_STATIONS.map(r => `
      <div class="radio-btn${this._activeRadio===r.name?' active':''}"
           style="${this._activeRadio===r.name ? `border-color:${r.color}55;` : ''}"
           data-r-url="${r.url}" data-r-name="${r.name}">
        <div class="radio-dot" style="background:${r.color}"></div>
        <div class="radio-name">${r.name}</div>
      </div>`).join('');

    const playIcon = almState === 'playing' ? WZ_ICONS.pause : WZ_ICONS.play;

    return `
    <div class="card" style="margin-bottom:14px">
      <div class="lbl">Radio</div>
      <div class="radio-grid">${radioHTML}</div>
    </div>
    <div class="card">
      <div class="lbl">Jetzt läuft</div>
      <div class="now-title">${almTitle}</div>
      <div class="now-sub">${almArtist}</div>
      <div class="ctrl-row">
        <button class="ctrl-btn lg" id="btn-prev">${WZ_ICONS.prev}</button>
        <button class="ctrl-btn play" id="btn-play">${playIcon}</button>
        <button class="ctrl-btn sm" id="btn-stop">${WZ_ICONS.stop}</button>
        <div class="spacer"></div>
      </div>
      <div class="vol-row">
        <button class="vol-btn" id="btn-vd">${WZ_ICONS.volDown}</button>
        <input type="range" class="vol-slider" id="vol-slider" min="0" max="100" value="${almVol}">
        <button class="vol-btn" id="btn-vu">${WZ_ICONS.volUp}</button>
        <span class="vol-pct" id="vol-pct">${almVol}%</span>
      </div>
    </div>
    <div class="spotify-row" id="btn-spotify">
      <span class="spotify-icon">${WZ_ICONS.spotify}</span>
      <div>
        <div class="spotify-title">Spotify${spot?.state === 'playing' ? ' · läuft' : ''}</div>
        <div class="spotify-sub">${spotTitle ? spotTitle + (spotArtist ? ' – ' + spotArtist : '') : 'Tippen zum öffnen'}</div>
      </div>
    </div>`;
  }

  _renderLights() {
    const lightsHTML = LIGHTS_CFG.map(l => {
      const on = this._state(l.id) === 'on';
      const bri = Math.round((this._attr(l.id,'brightness') ?? 0) / 2.55);
      return `
      <div class="light-card${on?' on':''}" data-light-id="${l.id}">
        <div style="display:flex;align-items:center;gap:10px">
          <div class="light-icon-wrap">${WZ_ICONS[l.icon] || WZ_ICONS.bulb}</div>
          <div>
            <div class="light-name">${l.name}</div>
            <div class="light-status">${on ? (bri ? bri+'%' : 'An') : 'Aus'}</div>
          </div>
        </div>
        ${on && l.id.startsWith('light.') ? `
        <input type="range" class="bright-slider" min="1" max="100" value="${bri||100}"
               data-bri-id="${l.id}" onclick="event.stopPropagation()">` : ''}
      </div>`;
    }).join('');

    return `
    <div class="card">
      <div class="lbl">Licht & Geräte</div>
      <div class="lights-grid">${lightsHTML}</div>
    </div>
    <div class="card" style="margin-top:14px">
      <div class="lbl">Szenen</div>
      <div class="scenes-grid">
        <div class="scene-btn" data-scene="abend">
          ${WZ_ICONS.moon}<span>Abend</span>
        </div>
        <div class="scene-btn" data-scene="film">
          ${WZ_ICONS.tv}<span>Film</span>
        </div>
        <div class="scene-btn off-btn" data-scene="off">
          ${WZ_ICONS.power}<span>Alles aus</span>
        </div>
      </div>
    </div>`;
  }

  _renderPlan() {
    return `<div class="card" style="text-align:center;padding:60px 24px">
      <div style="font-size:2.5rem;margin-bottom:16px">🗺</div>
      <div style="font-size:1rem;font-weight:500;margin-bottom:8px">Grundriss kommt bald</div>
      <div style="font-size:.78rem;opacity:.45">Interaktiver Floor Plan mit Lichtkontrolle</div>
    </div>`;
  }

  _navHTML() {
    const pages = [
      { id:'home',   label:'Home',   icon:'home'   },
      { id:'music',  label:'Musik',  icon:'music'  },
      { id:'lights', label:'Licht',  icon:'lights' },
      { id:'plan',   label:'Plan',   icon:'plan'   },
    ];
    return pages.map(p => `
      <button class="nav-btn${this._page===p.id?' active':''}" data-nav="${p.id}">
        ${WZ_ICONS[p.icon]}
        <span>${p.label}</span>
      </button>`).join('');
  }

  _render() {
    this.shadowRoot.innerHTML = `
      <style>${this._css()}</style>
      <div class="root">
        <div class="page" id="wz-page">${this._pageHTML()}</div>
        <nav class="nav">${this._navHTML()}</nav>
      </div>`;
    this._bindEvents();
  }

  _pageHTML() {
    switch(this._page) {
      case 'home':   return this._renderHome();
      case 'music':  return this._renderMusic();
      case 'lights': return this._renderLights();
      case 'plan':   return this._renderPlan();
      default:       return this._renderHome();
    }
  }

  _patch() {
    const pg = this.shadowRoot.getElementById('wz-page');
    if (pg) { pg.innerHTML = this._pageHTML(); this._bindPageEvents(); }
    const nav = this.shadowRoot.querySelector('.nav');
    if (nav) { nav.innerHTML = this._navHTML(); this._bindNavEvents(); }
  }

  _bindEvents() {
    this._bindNavEvents();
    this._bindPageEvents();
  }

  _bindNavEvents() {
    this.shadowRoot.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this._page = btn.dataset.nav;
        this._patch();
      });
    });
  }

  _bindPageEvents() {
    const root = this.shadowRoot;
    // Radio
    root.querySelectorAll('.radio-btn').forEach(b => {
      b.addEventListener('click', () => {
        this._activeRadio = b.dataset.rName;
        this._svc('media_player','play_media',{
          entity_id:'media_player.wohnzimmer_alm',
          media_content_id:b.dataset.rUrl,
          media_content_type:'audio/mp4'
        });
        this._patch();
      });
    });
    // Play/Stop
    root.getElementById('btn-play')?.addEventListener('click', () =>
      this._svc('media_player','media_play_pause',{entity_id:'media_player.wohnzimmer_alm'}));
    root.getElementById('btn-stop')?.addEventListener('click', () => {
      this._activeRadio = null;
      this._svc('media_player','media_stop',{entity_id:'media_player.wohnzimmer_alm'});
    });
    root.getElementById('btn-prev')?.addEventListener('click', () =>
      this._svc('media_player','media_previous_track',{entity_id:'media_player.wohnzimmer_alm'}));
    // Volume
    const vs = root.getElementById('vol-slider');
    if (vs) {
      vs.addEventListener('input', e => {
        const pct = root.getElementById('vol-pct');
        if (pct) pct.textContent = e.target.value + '%';
      });
      vs.addEventListener('change', e =>
        this._svc('media_player','volume_set',{entity_id:'media_player.wohnzimmer_alm',volume_level:parseInt(e.target.value)/100}));
    }
    root.getElementById('btn-vd')?.addEventListener('click', () =>
      this._svc('media_player','volume_down',{entity_id:'media_player.wohnzimmer_alm'}));
    root.getElementById('btn-vu')?.addEventListener('click', () =>
      this._svc('media_player','volume_up',{entity_id:'media_player.wohnzimmer_alm'}));
    // Spotify
    root.getElementById('btn-spotify')?.addEventListener('click', () =>
      this.dispatchEvent(new CustomEvent('hass-more-info',{bubbles:true,composed:true,detail:{entityId:'media_player.spotify_janisss'}})));
    // Lights
    root.querySelectorAll('.light-card').forEach(c => {
      c.addEventListener('click', () => {
        const id = c.dataset.lightId;
        const dom = id.startsWith('light.') ? 'light' : 'media_player';
        this._svc(dom, dom==='light' ? 'toggle' : (this._state(id)==='on'?'turn_off':'turn_on'), {entity_id:id});
      });
    });
    // Brightness sliders
    root.querySelectorAll('.bright-slider').forEach(sl => {
      sl.addEventListener('click', e => e.stopPropagation());
      sl.addEventListener('change', e =>
        this._svc('light','turn_on',{entity_id:e.target.dataset.briId,brightness_pct:parseInt(e.target.value)}));
    });
    // Scenes
    root.querySelectorAll('.scene-btn').forEach(b => {
      b.addEventListener('click', () => {
        const s = b.dataset.scene;
        if (s === 'off') {
          this._svc('light','turn_off',{entity_id:['light.deckenlampe','light.h618a','light.h618a_2']});
          this._svc('media_player','turn_off',{entity_id:'media_player.wohnzimmer_alm'});
        } else if (s === 'abend') {
          this._svc('light','turn_on',{entity_id:'light.deckenlampe',brightness_pct:30,kelvin:2700});
          this._svc('light','turn_on',{entity_id:'light.h618a',brightness_pct:50});
        } else if (s === 'film') {
          this._svc('light','turn_off',{entity_id:'light.deckenlampe'});
          this._svc('light','turn_on',{entity_id:'light.h618a',brightness_pct:20});
          this._svc('media_player','turn_on',{entity_id:'media_player.lg_webos_tv_oled65g49ls_2'});
        }
      });
    });
  }

  getCardSize() { return 15; }
  static getStubConfig() { return {}; }
}

customElements.define('wz-dashboard', WzDashboard);
window.customCards = window.customCards || [];
window.customCards.push({ type:'wz-dashboard', name:'WZ Dashboard', description:'iOS-style Wohnzimmer Control Center' });
