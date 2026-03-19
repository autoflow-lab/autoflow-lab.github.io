/* ═══════════════════════════════════════════════════════════════
   WZ Dashboard v3 — Premium Apple-style
   autoflow-lab · Clawy 🦀
═══════════════════════════════════════════════════════════════ */

const RADIO = [
  { name:'SRF 1',  color:'#4a9eff', url:'http://stream.srg-ssr.ch/m/drs1/mp3_128' },
  { name:'SRF 3',  color:'#ff6b35', url:'http://stream.srg-ssr.ch/m/drs3/mp3_128' },
  { name:'Pop',    color:'#ff3b8a', url:'http://stream.srg-ssr.ch/m/rsp/mp3_128' },
  { name:'Energy', color:'#f7c948', url:'https://energyzurich.ice.infomaniak.ch/energyzurich-high.mp3' },
  { name:'R. 24',  color:'#a855f7', url:'https://radio24.ice.infomaniak.ch/radio24-high.mp3' },
];

const LIGHTS = [
  { id:'light.h618a',   name:'Sofa',   color:'#ff9f40' },
  { id:'light.h618a_2', name:'Küche',  color:'#ff7040' },
  { id:'light.hue_play_l', name:'Büro Hue', color:'#c060ff' },
];

const TV = 'media_player.lg_webos_tv_oled65g49ls_2';
const ALM = 'media_player.wohnzimmer_alm';
const SPOT = 'media_player.spotify_janisss';
const SHELLY = 'switch.shelly1_98cdac0ca9b2';

class WzDashboard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._page = 'home';
    this._built = false;
    this._timer = null;
    this._activeRadio = null;
  }

  set hass(h) {
    this._hass = h;
    if (!this._built) { this._build(); this._built = true; }
    else this._update();
  }

  connectedCallback() {
    this._timer = setInterval(() => this._tickClock(), 15000);
  }
  disconnectedCallback() { clearInterval(this._timer); }

  _state(id) { return this._hass?.states[id]?.state || 'off'; }
  _attr(id, k) { return this._hass?.states[id]?.attributes?.[k]; }
  _svc(d, s, data) { this._hass?.callService(d, s, data); }

  _hour() { return new Date().getHours(); }
  _isDay() { const h = this._hour(); return h >= 7 && h < 22; }

  /* ─── COLORS ─── */
  _C() {
    return this._isDay() ? {
      bg:      'linear-gradient(145deg, #f5f7ff 0%, #eef1fb 40%, #f3eeff 100%)',
      fg:      '#1a1a2e',
      fg2:     'rgba(26,26,46,0.5)',
      fg3:     'rgba(26,26,46,0.25)',
      glass:   'rgba(255,255,255,0.72)',
      glassB:  'rgba(0,0,0,0.06)',
      navBg:   'rgba(245,247,255,0.92)',
      navB:    'rgba(0,0,0,0.08)',
      accent:  '#5c5ce0',
    } : {
      bg:      'linear-gradient(145deg,#070711 0%,#0d0d1f 50%,#0a0a18 100%)',
      fg:      '#e8e8ff',
      fg2:     'rgba(232,232,255,0.45)',
      fg3:     'rgba(232,232,255,0.18)',
      glass:   'rgba(255,255,255,0.055)',
      glassB:  'rgba(255,255,255,0.09)',
      navBg:   'rgba(7,7,17,0.92)',
      navB:    'rgba(255,255,255,0.09)',
      accent:  '#7b7bff',
    };
  }

  /* ─── CSS ─── */
  _css() {
    const C = this._C();
    return `
:host { display:block; font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text',sans-serif; }
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; -webkit-tap-highlight-color:transparent; }

.root {
  height:100dvh; width:100%; display:flex; flex-direction:column; overflow:hidden;
  background:${C.bg}; color:${C.fg};
  --fg:${C.fg}; --fg2:${C.fg2}; --fg3:${C.fg3};
  --glass:${C.glass}; --glassB:${C.glassB}; --accent:${C.accent};
}

/* ── PAGE ── */
.page {
  flex:1; overflow-y:auto; overflow-x:hidden;
  padding:28px 20px 12px;
  -webkit-overflow-scrolling:touch;
  scroll-behavior:smooth;
}
.page-hidden { display:none !important; }

/* ── GLASS CARD ── */
.g {
  background:var(--glass);
  backdrop-filter:blur(40px) saturate(180%);
  -webkit-backdrop-filter:blur(40px) saturate(180%);
  border:1px solid var(--glassB);
  border-radius:24px;
}

/* ── HOME PAGE ── */
.home-hero {
  position:relative; overflow:hidden;
  padding:32px 28px 28px; margin-bottom:14px;
  border-radius:28px; min-height:160px;
  background:var(--glass);
  backdrop-filter:blur(40px) saturate(180%);
  -webkit-backdrop-filter:blur(40px) saturate(180%);
  border:1px solid var(--glassB);
}
.hero-glow {
  position:absolute; top:-40%; right:-20%; width:280px; height:280px;
  border-radius:50%;
  background:${this._isDay()
    ? 'radial-gradient(circle, rgba(100,100,255,0.15) 0%, transparent 70%)'
    : 'radial-gradient(circle, rgba(120,120,255,0.2) 0%, transparent 70%)'};
  pointer-events:none;
}
.time-display {
  font-size:clamp(4rem,18vw,6.5rem); font-weight:100; letter-spacing:-4px;
  color:${C.fg}; line-height:1; font-variant-numeric:tabular-nums;
}
.date-display {
  font-size:.7rem; font-weight:500; letter-spacing:2px; text-transform:uppercase;
  color:var(--fg2); margin-top:10px;
}

.home-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }

.weather-card { padding:20px; }
.w-emoji { font-size:2.5rem; margin-bottom:8px; display:block; }
.w-temp { font-size:2.4rem; font-weight:200; letter-spacing:-1px; color:var(--fg); }
.w-loc { font-size:.65rem; font-weight:500; letter-spacing:1.5px; text-transform:uppercase; color:var(--fg2); margin-top:4px; }

.status-card { padding:20px; display:flex; flex-direction:column; justify-content:center; gap:10px; }
.status-row { display:flex; align-items:center; gap:8px; }
.status-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.status-dot.on { background:#4cd964; box-shadow:0 0 6px #4cd96488; }
.status-dot.off { background:var(--fg3); }
.status-dot.play { background:#4a9eff; animation:pulse 1.8s ease-in-out infinite; }
.status-text { font-size:.78rem; font-weight:500; color:var(--fg2); }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.9)} }

.scene-row { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.scene-tile {
  padding:16px 10px; border-radius:20px; cursor:pointer;
  display:flex; flex-direction:column; align-items:center; gap:8px;
  background:var(--glass); backdrop-filter:blur(32px); -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--glassB); transition:transform .12s, box-shadow .12s;
  user-select:none;
}
.scene-tile:active { transform:scale(.93); }
.scene-tile svg { width:26px; height:26px; }
.scene-tile span { font-size:.62rem; font-weight:600; letter-spacing:.5px; color:var(--fg2); text-align:center; }

/* ── MUSIC PAGE ── */
.now-playing-card {
  padding:28px; margin-bottom:14px; border-radius:28px;
  position:relative; overflow:hidden;
  background:${this._isDay()
    ? 'linear-gradient(135deg,rgba(80,80,220,0.12) 0%,rgba(140,80,200,0.08) 100%)'
    : 'linear-gradient(135deg,rgba(80,80,220,0.18) 0%,rgba(140,80,200,0.12) 100%)'};
  border:1px solid ${this._isDay() ? 'rgba(80,80,220,0.15)' : 'rgba(120,120,255,0.15)'};
  backdrop-filter:blur(40px); -webkit-backdrop-filter:blur(40px);
}
.np-glow {
  position:absolute; width:200px; height:200px; border-radius:50%;
  background:radial-gradient(circle,rgba(100,80,255,0.25) 0%,transparent 70%);
  top:-50px; right:-50px; pointer-events:none;
}
.np-label { font-size:.58rem; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; color:rgba(120,120,255,0.6); margin-bottom:12px; }
.np-title { font-size:1.3rem; font-weight:600; color:var(--fg); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.np-artist { font-size:.82rem; color:var(--fg2); margin-top:4px; }
.np-state-badge {
  display:inline-flex; align-items:center; gap:6px;
  padding:5px 12px; border-radius:20px; margin-top:12px;
  background:rgba(74,158,255,0.15); border:1px solid rgba(74,158,255,0.25);
  font-size:.65rem; font-weight:600; color:#4a9eff;
}
.eq-bars { display:flex; gap:2px; align-items:flex-end; height:14px; }
.eq-bar { width:2.5px; border-radius:2px; background:#4a9eff; }
.eq-bar.a { animation:eq 0.8s ease-in-out infinite; }
.eq-bar.b { animation:eq 1.1s ease-in-out .15s infinite; }
.eq-bar.c { animation:eq 0.9s ease-in-out .3s infinite; }
@keyframes eq { 0%,100%{height:3px} 50%{height:12px} }

.ctrl-row {
  display:flex; align-items:center; justify-content:center; gap:24px; margin:20px 0;
}
.ctrl { background:none; border:none; cursor:pointer; color:var(--fg); transition:transform .1s, opacity .1s; padding:8px; border-radius:50%; }
.ctrl:active { transform:scale(.82); opacity:.7; }
.ctrl-play {
  width:64px; height:64px; border-radius:50%; cursor:pointer; border:none;
  background:${this._isDay() ? '#1a1a2e' : '#e8e8ff'};
  color:${this._isDay() ? '#fff' : '#0a0a18'};
  display:flex; align-items:center; justify-content:center;
  box-shadow:${this._isDay()
    ? '0 8px 24px rgba(26,26,46,0.25)'
    : '0 8px 24px rgba(100,100,255,0.35)'};
  transition:transform .1s, box-shadow .1s;
}
.ctrl-play:active { transform:scale(.88); box-shadow:none; }
.ctrl svg { width:24px; height:24px; }
.ctrl-play svg { width:26px; height:26px; }
.ctrl-sm svg { width:20px; height:20px; color:var(--fg2); }

.vol-row { display:flex; align-items:center; gap:12px; padding:0 4px; }
.vol-icon { color:var(--fg3); flex-shrink:0; }
.vol-icon svg { width:18px; height:18px; }
.vol-slider {
  flex:1; height:4px; -webkit-appearance:none; appearance:none; outline:none;
  border-radius:2px; background:var(--glassB); cursor:pointer; touch-action:pan-x;
}
.vol-slider::-webkit-slider-thumb {
  -webkit-appearance:none; width:20px; height:20px; border-radius:50%;
  background:${this._isDay() ? '#1a1a2e' : '#e8e8ff'};
  box-shadow:0 2px 8px rgba(0,0,0,.3); cursor:pointer;
}
.vol-pct { font-size:.68rem; font-weight:600; color:var(--fg3); min-width:34px; text-align:right; }

.radio-section { margin-bottom:14px; }
.section-label {
  font-size:.58rem; font-weight:700; letter-spacing:2.5px; text-transform:uppercase;
  color:var(--fg3); margin-bottom:12px; padding:0 2px;
}
.radio-pills { display:flex; gap:8px; flex-wrap:wrap; }
.r-pill {
  padding:9px 16px; border-radius:20px; cursor:pointer;
  font-size:.72rem; font-weight:700; letter-spacing:.3px;
  border:1.5px solid transparent; transition:all .15s; user-select:none;
  background:var(--glass); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px);
}
.r-pill:active { transform:scale(.92); }

.spotify-card {
  padding:18px 20px; border-radius:20px; cursor:pointer;
  display:flex; align-items:center; gap:14px; margin-top:14px;
  background:rgba(29,185,84,${this._isDay() ? '.08' : '.07'});
  border:1px solid rgba(29,185,84,${this._isDay() ? '.18' : '.15'});
  backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
  transition:all .15s; user-select:none;
}
.spotify-card:active { transform:scale(.97); background:rgba(29,185,84,.14); }
.spotify-logo svg { width:32px; height:32px; color:#1db954; }
.spotify-info .t { font-size:.88rem; font-weight:600; color:#1db954; }
.spotify-info .s { font-size:.67rem; color:rgba(29,185,84,.55); margin-top:2px; }

/* ── LIGHTS PAGE ── */
.lights-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }
.light-tile {
  padding:20px 16px; border-radius:22px; cursor:pointer; user-select:none;
  background:var(--glass); backdrop-filter:blur(32px); -webkit-backdrop-filter:blur(32px);
  border:1.5px solid var(--glassB);
  display:flex; flex-direction:column; gap:14px;
  transition:all .2s; position:relative; overflow:hidden;
}
.light-tile:active { transform:scale(.96); }
.light-tile.on { border-color:rgba(255,200,60,0.3); }
.lt-glow {
  position:absolute; width:120px; height:120px; border-radius:50%; pointer-events:none;
  top:-30px; right:-30px; transition:opacity .4s;
}
.lt-icon {
  width:46px; height:46px; border-radius:15px;
  display:flex; align-items:center; justify-content:center;
  background:var(--glassB); transition:all .3s;
}
.light-tile.on .lt-icon { background:rgba(255,200,60,0.2); }
.lt-icon svg { width:22px; height:22px; color:var(--fg2); transition:color .3s; }
.light-tile.on .lt-icon svg { color:#ffc040; }
.lt-name { font-size:.82rem; font-weight:600; color:var(--fg); }
.lt-status { font-size:.65rem; color:var(--fg3); }
.light-tile.on .lt-status { color:rgba(255,200,60,0.7); }
.bri-track {
  width:100%; height:3px; border-radius:2px; background:var(--glassB);
  position:relative; overflow:visible;
}
.bri-fill { height:100%; border-radius:2px; background:linear-gradient(90deg,#ffb020,#ffd060); transition:width .3s; }
.bri-slider {
  position:absolute; top:50%; transform:translateY(-50%);
  width:100%; height:22px; opacity:0; cursor:pointer; touch-action:pan-x;
  -webkit-appearance:none; appearance:none;
  margin:0; left:0;
}

.dev-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.dev-tile {
  padding:18px 16px; border-radius:22px; cursor:pointer; user-select:none;
  background:var(--glass); backdrop-filter:blur(32px); -webkit-backdrop-filter:blur(32px);
  border:1.5px solid var(--glassB);
  display:flex; flex-direction:column; gap:10px;
  transition:all .2s;
}
.dev-tile:active { transform:scale(.96); }
.dev-tile.on { border-color:rgba(100,170,255,0.3); background:rgba(100,170,255,0.07); }
.dt-icon { width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:var(--glassB); }
.dev-tile.on .dt-icon { background:rgba(74,158,255,0.15); }
.dt-icon svg { width:22px; height:22px; color:var(--fg2); }
.dev-tile.on .dt-icon svg { color:#4a9eff; }
.dt-name { font-size:.8rem; font-weight:600; }
.dt-st { font-size:.65rem; color:var(--fg3); }

/* ── BOTTOM NAV ── */
.nav {
  display:flex; align-items:center; justify-content:space-around;
  padding:10px 8px 10px;
  padding-bottom:max(10px,env(safe-area-inset-bottom));
  background:${C.navBg};
  backdrop-filter:blur(40px) saturate(180%); -webkit-backdrop-filter:blur(40px) saturate(180%);
  border-top:1px solid ${C.navB};
  flex-shrink:0;
}
.nav-btn {
  display:flex; flex-direction:column; align-items:center; gap:3px;
  padding:6px 20px; border-radius:16px; cursor:pointer;
  border:none; background:none; color:var(--fg3);
  transition:all .18s; min-width:64px; user-select:none;
}
.nav-btn svg { width:23px; height:23px; transition:transform .18s; stroke-width:1.6; }
.nav-btn span { font-size:.56rem; font-weight:600; letter-spacing:.8px; text-transform:uppercase; transition:all .18s; }
.nav-btn.active { color:var(--fg); }
.nav-btn.active svg { transform:scale(1.12); }

/* ── SVG ICONS ── */
svg { overflow:visible; }
    `;
  }

  _icon(n) {
    const icons = {
      home:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12L12 3l9 9"/><path d="M5 10v9a1 1 0 001 1h4v-5h4v5h4a1 1 0 001-1v-9"/></svg>`,
      music:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="18" r="2.5"/><circle cx="18" cy="16" r="2.5"/><path d="M10.5 18V7.5l10-2.5V16"/></svg>`,
      lights: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6M12 3a6 6 0 016 6c0 2.6-1.4 4.8-3 6.2V17a1 1 0 01-1 1H10a1 1 0 01-1-1v-1.8C7.4 13.8 6 11.6 6 9a6 6 0 016-6z"/></svg>`,
      plan:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 9h18M9 21V9"/></svg>`,
      play:   `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5z"/></svg>`,
      pause:  `<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>`,
      stop:   `<svg viewBox="0 0 24 24" fill="currentColor"><rect x="5" y="5" width="14" height="14" rx="2"/></svg>`,
      prev:   `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 20L9 12l10-8v16z"/><rect x="5" y="4" width="2" height="16" rx="1"/></svg>`,
      volL:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/></svg>`,
      volH:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.54 8.46a5 5 0 010 7.07"/><path d="M19.07 4.93a10 10 0 010 14.14"/></svg>`,
      bulb:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6M12 3a6 6 0 016 6c0 2.6-1.4 4.8-3 6.2V17a1 1 0 01-1 1H10a1 1 0 01-1-1v-1.8C7.4 13.8 6 11.6 6 9a6 6 0 016-6z"/></svg>`,
      strip:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="2"/><line x1="6" y1="10" x2="6" y2="7"/><line x1="10" y1="10" x2="10" y2="5"/><line x1="14" y1="10" x2="14" y2="7"/><line x1="18" y1="10" x2="18" y2="5"/></svg>`,
      tv:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="14" rx="2.5"/><path d="M8 20h8M12 18v2"/></svg>`,
      switch: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="9" width="20" height="6" rx="3"/><circle cx="16" cy="12" r="2.5" fill="currentColor"/></svg>`,
      power:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M18.36 6.64a9 9 0 11-12.73 0M12 2v10"/></svg>`,
      moon:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>`,
      film:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M7 4v16M17 4v16M2 12h20M2 8h5M2 16h5M17 8h5M17 16h5"/></svg>`,
      spotify:`<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.586 14.424a.622.622 0 01-.857.207c-2.348-1.435-5.304-1.76-8.785-.964a.623.623 0 01-.277-1.215c3.809-.87 7.077-.496 9.712 1.115a.623.623 0 01.207.857zm1.223-2.722a.779.779 0 01-1.072.257c-2.687-1.652-6.785-2.131-9.965-1.166a.779.779 0 01-.973-.52.779.779 0 01.52-.972c3.632-1.102 8.147-.568 11.233 1.328a.779.779 0 01.257 1.073zm.105-2.835c-3.223-1.914-8.54-2.09-11.618-1.156a.935.935 0 11-.543-1.79c3.532-1.072 9.404-.865 13.115 1.338a.935.935 0 01-.954 1.608z"/></svg>`,
    };
    return icons[n] || '';
  }

  _wIcon(s) {
    return {sunny:'☀️','clear-night':'🌙','partlycloudy':'⛅','cloudy':'☁️',
            fog:'🌫️',rainy:'🌧️',snowy:'❄️',windy:'💨',lightning:'⛈️',pouring:'🌧️'}[s]||'🌤️';
  }

  /* ─── PAGES ─── */
  _pageHome() {
    const now = new Date();
    const time = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
    const days = ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'];
    const months = ['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'];
    const date = `${days[now.getDay()]}, ${now.getDate()}. ${months[now.getMonth()]}`;
    const wState = this._state('weather.forecast_home');
    const temp = this._attr('weather.forecast_home','temperature') ?? '—';
    const almState = this._state(ALM);
    const almTitle = this._attr(ALM,'media_title') || '';
    const lightsOn = LIGHTS.filter(l => this._state(l.id) === 'on').length;

    return `
    <div class="home-hero">
      <div class="hero-glow"></div>
      <div class="time-display" id="wz-clock">${time}</div>
      <div class="date-display">${date}</div>
    </div>
    <div class="home-row">
      <div class="g weather-card">
        <span class="w-emoji">${this._wIcon(wState)}</span>
        <div class="w-temp">${temp}°</div>
        <div class="w-loc">Egg SZ</div>
      </div>
      <div class="g status-card">
        <div class="status-row">
          <div class="status-dot ${lightsOn > 0 ? 'on' : 'off'}"></div>
          <span class="status-text">${lightsOn > 0 ? `${lightsOn} Licht${lightsOn > 1 ? 'er an' : ' an'}` : 'Alles aus'}</span>
        </div>
        <div class="status-row">
          <div class="status-dot ${almState === 'playing' ? 'play' : 'off'}"></div>
          <span class="status-text">${almState === 'playing' ? (almTitle || 'Läuft...') : 'Kein Audio'}</span>
        </div>
      </div>
    </div>
    <div class="section-label">Szenen</div>
    <div class="scene-row">
      <div class="scene-tile" data-scene="abend">
        <svg viewBox="0 0 24 24" fill="none" stroke="#f0a030" stroke-width="1.8" stroke-linecap="round">${this._icon('moon').replace('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round">','').replace('</svg>','')}</svg>
        ${this._icon('moon').replace('currentColor','#f0a030')}
        <span>Abend</span>
      </div>
      <div class="scene-tile" data-scene="film">
        ${this._icon('film').replace('currentColor','#4a9eff')}
        <span>Film</span>
      </div>
      <div class="scene-tile" data-scene="off">
        ${this._icon('power').replace('currentColor','rgba(255,80,80,0.7)')}
        <span>Alles aus</span>
      </div>
    </div>`;
  }

  _pageMusic() {
    const alm = this._hass?.states[ALM];
    const almState = alm?.state || 'off';
    const title = alm?.attributes?.media_title || (almState === 'playing' ? 'Läuft...' : 'Bereit');
    const artist = alm?.attributes?.media_artist || 'Almando';
    const vol = Math.round((alm?.attributes?.volume_level ?? 0.4) * 100);
    const isPlaying = almState === 'playing';
    const spot = this._hass?.states[SPOT];
    const spotTitle = spot?.attributes?.media_title || '';
    const spotArtist = spot?.attributes?.media_artist || '';

    const radioPills = RADIO.map(r => `
      <div class="r-pill${this._activeRadio===r.name?` active`:''}"
           style="${this._activeRadio===r.name
             ? `background:${r.color}22;border-color:${r.color}66;color:${r.color}`
             : `color:var(--fg2)`}"
           data-r-url="${r.url}" data-r-name="${r.name}">${r.name}</div>`).join('');

    return `
    <div class="now-playing-card">
      <div class="np-glow"></div>
      <div class="np-label">Jetzt läuft</div>
      <div class="np-title">${title}</div>
      <div class="np-artist">${artist}</div>
      ${isPlaying ? `<div class="np-state-badge">
        <div class="eq-bars">
          <div class="eq-bar a" style="height:8px"></div>
          <div class="eq-bar b" style="height:4px"></div>
          <div class="eq-bar c" style="height:11px"></div>
          <div class="eq-bar a" style="height:6px"></div>
        </div>
        Live
      </div>` : ''}
    </div>
    <div class="g" style="padding:22px;margin-bottom:14px">
      <div class="ctrl-row">
        <button class="ctrl ctrl-sm" id="btn-prev">${this._icon('prev')}</button>
        <button class="ctrl-play" id="btn-play">${this._icon(isPlaying ? 'pause' : 'play')}</button>
        <button class="ctrl ctrl-sm" id="btn-stop">${this._icon('stop')}</button>
      </div>
      <div class="vol-row">
        <span class="vol-icon">${this._icon('volL')}</span>
        <input type="range" class="vol-slider" id="vol-slider" min="0" max="100" value="${vol}">
        <span class="vol-icon">${this._icon('volH')}</span>
        <span class="vol-pct" id="vol-pct">${vol}%</span>
      </div>
    </div>
    <div class="section-label">Radio</div>
    <div class="radio-pills" style="margin-bottom:14px">${radioPills}</div>
    <div class="spotify-card" id="btn-spotify">
      <span class="spotify-logo">${this._icon('spotify')}</span>
      <div class="spotify-info">
        <div class="t">Spotify${spot?.state==='playing'?' · läuft':''}</div>
        <div class="s">${spotTitle ? `${spotTitle}${spotArtist?' – '+spotArtist:''}` : 'Öffnen'}</div>
      </div>
    </div>`;
  }

  _pageLight() {
    const lightsHTML = LIGHTS.map(l => {
      const on = this._state(l.id) === 'on';
      const bri = Math.round((this._attr(l.id,'brightness') ?? 0) / 2.55);
      const iconName = l.id.includes('h618') ? 'strip' : 'bulb';
      return `
      <div class="light-tile${on?' on':''}" data-lid="${l.id}">
        ${on ? `<div class="lt-glow" style="background:radial-gradient(circle,${l.color}40 0%,transparent 70%)"></div>` : ''}
        <div class="lt-icon">${this._icon(iconName)}</div>
        <div>
          <div class="lt-name">${l.name}</div>
          <div class="lt-status">${on ? (bri ? `${bri}%` : 'An') : 'Aus'}</div>
        </div>
        ${on ? `
        <div class="bri-track">
          <div class="bri-fill" style="width:${bri||100}%"></div>
          <input type="range" class="bri-slider" min="1" max="100" value="${bri||100}" data-bri="${l.id}">
        </div>` : ''}
      </div>`;
    }).join('');

    const tvOn = this._state(TV) === 'on';
    const shellyOn = this._state(SHELLY) === 'on';

    return `
    <div class="section-label">Licht</div>
    <div class="lights-grid">${lightsHTML}</div>
    <div class="section-label">Geräte</div>
    <div class="dev-grid">
      <div class="dev-tile${tvOn?' on':''}" data-dev="${TV}">
        <div class="dt-icon">${this._icon('tv')}</div>
        <div class="dt-name">LG OLED</div>
        <div class="dt-st">${tvOn ? 'An' : 'Aus'}</div>
      </div>
      <div class="dev-tile${shellyOn?' on':''}" data-dev="${SHELLY}" data-domain="switch">
        <div class="dt-icon">${this._icon('switch')}</div>
        <div class="dt-name">Wandlampe</div>
        <div class="dt-st">${shellyOn ? 'An' : 'Aus'}</div>
      </div>
    </div>`;
  }

  _pagePlan() {
    return `<div class="g" style="text-align:center;padding:70px 24px">
      <div style="font-size:3rem;margin-bottom:18px">🗺</div>
      <div style="font-size:1.05rem;font-weight:600;color:var(--fg);margin-bottom:8px">Grundriss</div>
      <div style="font-size:.78rem;color:var(--fg2)">Interaktiver Floor Plan kommt bald</div>
    </div>`;
  }

  _navHTML() {
    const pages = [{id:'home',label:'Home',icon:'home'},{id:'music',label:'Musik',icon:'music'},
                   {id:'lights',label:'Licht',icon:'lights'},{id:'plan',label:'Plan',icon:'plan'}];
    return pages.map(p => `
      <button class="nav-btn${this._page===p.id?' active':''}" data-nav="${p.id}">
        ${this._icon(p.icon)}<span>${p.label}</span>
      </button>`).join('');
  }

  _pageHTML() {
    switch(this._page) {
      case 'home':   return this._pageHome();
      case 'music':  return this._pageMusic();
      case 'lights': return this._pageLight();
      case 'plan':   return this._pagePlan();
    }
  }

  _build() {
    this.shadowRoot.innerHTML = `
      <style>${this._css()}</style>
      <div class="root">
        <div class="page" id="wz-page">${this._pageHTML()}</div>
        <nav class="nav" id="wz-nav">${this._navHTML()}</nav>
      </div>`;
    this._bindAll();
  }

  _update() {
    const pg = this.shadowRoot.getElementById('wz-page');
    const nav = this.shadowRoot.getElementById('wz-nav');
    if (pg) { pg.innerHTML = this._pageHTML(); this._bindPage(); }
    if (nav) { nav.innerHTML = this._navHTML(); this._bindNav(); }
  }

  _bindAll() { this._bindNav(); this._bindPage(); }

  _bindNav() {
    this.shadowRoot.querySelectorAll('.nav-btn').forEach(b => {
      b.addEventListener('click', () => { this._page = b.dataset.nav; this._update(); });
    });
  }

  _bindPage() {
    const r = this.shadowRoot;
    // Radio
    r.querySelectorAll('.r-pill').forEach(p => {
      p.addEventListener('click', () => {
        this._activeRadio = p.dataset.rName;
        this._svc('media_player','play_media',{
          entity_id:ALM, media_content_id:p.dataset.rUrl, media_content_type:'audio/mp4'});
        this._update();
      });
    });
    // Play/Stop/Prev
    r.getElementById('btn-play')?.addEventListener('click', () =>
      this._svc('media_player','media_play_pause',{entity_id:ALM}));
    r.getElementById('btn-stop')?.addEventListener('click', () => {
      this._activeRadio = null;
      this._svc('media_player','media_stop',{entity_id:ALM});
    });
    r.getElementById('btn-prev')?.addEventListener('click', () =>
      this._svc('media_player','media_previous_track',{entity_id:ALM}));
    // Volume
    const vs = r.getElementById('vol-slider');
    if (vs) {
      vs.addEventListener('input', e => {
        const p = r.getElementById('vol-pct'); if (p) p.textContent = e.target.value+'%';
      });
      vs.addEventListener('change', e =>
        this._svc('media_player','volume_set',{entity_id:ALM,volume_level:+e.target.value/100}));
    }
    // Spotify
    r.getElementById('btn-spotify')?.addEventListener('click', () =>
      this.dispatchEvent(new CustomEvent('hass-more-info',{bubbles:true,composed:true,detail:{entityId:SPOT}})));
    // Lights
    r.querySelectorAll('.light-tile').forEach(t => {
      t.addEventListener('click', e => {
        if (e.target.classList.contains('bri-slider')) return;
        this._svc('light','toggle',{entity_id:t.dataset.lid});
      });
    });
    r.querySelectorAll('.bri-slider').forEach(s => {
      s.addEventListener('click', e => e.stopPropagation());
      s.addEventListener('change', e =>
        this._svc('light','turn_on',{entity_id:e.target.dataset.bri,brightness_pct:+e.target.value}));
    });
    // Devices
    r.querySelectorAll('.dev-tile').forEach(t => {
      t.addEventListener('click', () => {
        const id = t.dataset.dev, domain = t.dataset.domain || 'media_player';
        const on = this._state(id) === 'on';
        this._svc(domain, on ? 'turn_off' : 'turn_on', {entity_id:id});
      });
    });
    // Scenes
    r.querySelectorAll('.scene-tile').forEach(t => {
      t.addEventListener('click', () => {
        const s = t.dataset.scene;
        if (s === 'off') {
          ['light.h618a','light.h618a_2','light.hue_play_l'].forEach(id =>
            this._svc('light','turn_off',{entity_id:id}));
          this._svc('switch','turn_off',{entity_id:SHELLY});
          this._svc('media_player','turn_off',{entity_id:ALM});
          this._svc('media_player','turn_off',{entity_id:TV});
        } else if (s === 'abend') {
          this._svc('light','turn_on',{entity_id:'light.h618a',brightness_pct:40,rgb_color:[255,140,40]});
          this._svc('light','turn_on',{entity_id:'light.h618a_2',brightness_pct:25,rgb_color:[255,80,20]});
        } else if (s === 'film') {
          this._svc('light','turn_off',{entity_id:['light.h618a','light.h618a_2','light.hue_play_l']});
          this._svc('media_player','turn_on',{entity_id:TV});
        }
      });
    });
  }

  _tickClock() {
    const el = this.shadowRoot.getElementById('wz-clock');
    if (!el) return;
    const n = new Date();
    el.textContent = `${String(n.getHours()).padStart(2,'0')}:${String(n.getMinutes()).padStart(2,'0')}`;
  }

  getCardSize() { return 15; }
  static getStubConfig() { return {}; }
}

customElements.define('wz-dashboard', WzDashboard);
window.customCards = window.customCards || [];
window.customCards.push({type:'wz-dashboard',name:'WZ Dashboard v3',description:'Premium iOS-style Control Center'});
