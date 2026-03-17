/* ═══════════════════════════════════════════════════════════════
   WZ Dashboard — Custom Lovelace Card
   Vollständig selbst gestaltet, Apple/iOS Control Center Stil
   by autoflow-lab / Clawy 🦀
═══════════════════════════════════════════════════════════════ */
class WzDashboard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._activeRadio = null;
    this._built = false;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._built) { this._build(); this._built = true; }
    else this._update();
  }

  // ── Stunde → Day/Night ──
  _isDaytime() {
    const h = new Date().getHours();
    return h >= 7 && h < 21;
  }

  _colors() {
    return this._isDaytime() ? {
      bg:   'linear-gradient(160deg,#e8eef8 0%,#f0f4fb 50%,#eaf0fa 100%)',
      card: 'rgba(255,255,255,0.72)',
      cardBorder: 'rgba(0,0,0,0.07)',
      text: '#1d1d1f',
      sub:  'rgba(0,0,0,0.42)',
      glow: 'rgba(0,113,227,0.08)',
    } : {
      bg:   'radial-gradient(ellipse at 10% 90%,#1a0838 0%,transparent 55%),radial-gradient(ellipse at 88% 12%,#061830 0%,transparent 50%),linear-gradient(160deg,#0b0b1d 0%,#060610 100%)',
      card: 'rgba(255,255,255,0.05)',
      cardBorder: 'rgba(255,255,255,0.09)',
      text: '#f0f0f5',
      sub:  'rgba(255,255,255,0.38)',
      glow: 'rgba(80,120,255,0.10)',
    };
  }

  _css(c) {
    return `
      :host { display:block; width:100%; min-height:100vh; }
      * { box-sizing:border-box; font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif; margin:0; padding:0; -webkit-tap-highlight-color:transparent; }
      .root {
        min-height:100vh; width:100%;
        background:${c.bg};
        padding:clamp(16px,4vw,36px);
        display:grid;
        grid-template-rows:auto 1fr auto auto;
        gap:clamp(12px,2.5vw,22px);
      }

      /* ── GLASS CARD ── */
      .card {
        background:${c.card};
        backdrop-filter:blur(28px);
        -webkit-backdrop-filter:blur(28px);
        border:1px solid ${c.cardBorder};
        border-radius:22px;
        padding:clamp(14px,3vw,24px);
        transition:background .4s,border .4s;
      }

      /* ── TOP ROW ── */
      .top { display:grid; grid-template-columns:1fr 1fr; gap:clamp(12px,2vw,18px); align-items:start; }
      .clock-num {
        font-size:clamp(3rem,10vw,5.5rem);
        font-weight:100;
        color:${c.text};
        letter-spacing:-3px;
        line-height:1;
      }
      .clock-date { font-size:.72rem; color:${c.sub}; letter-spacing:1.8px; text-transform:uppercase; margin-top:6px; }
      .weather-row { display:flex; align-items:center; gap:10px; }
      .weather-icon { font-size:2.6rem; }
      .weather-temp { font-size:clamp(2rem,6vw,3.2rem); font-weight:100; color:${c.text}; letter-spacing:-1px; }
      .weather-loc { font-size:.7rem; color:${c.sub}; margin-top:3px; }
      .weather-cond { font-size:.68rem; color:${c.sub}; margin-top:1px; letter-spacing:.5px; }

      /* ── SECTION LABEL ── */
      .sec-lbl { font-size:.58rem; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; color:${c.sub}; margin-bottom:10px; }

      /* ── RADIO ── */
      .radio-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; }
      .radio-btn {
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        gap:7px; padding:14px 4px; border-radius:18px; cursor:pointer;
        border:1.5px solid transparent;
        background:${c.card};
        backdrop-filter:blur(16px);
        -webkit-backdrop-filter:blur(16px);
        border-color:${c.cardBorder};
        transition:all .18s;
        -webkit-user-select:none; user-select:none;
      }
      .radio-btn:active { transform:scale(.93); }
      .radio-btn.active { border-width:1.5px; }
      .radio-icon { font-size:1.5rem; }
      .radio-name { font-size:.6rem; font-weight:600; letter-spacing:.3px; color:${c.sub}; text-align:center; }
      .radio-btn.active .radio-name { font-weight:700; }

      /* ── PLAYER ── */
      .player-wrap { display:flex; flex-direction:column; gap:14px; }
      .player-title {
        font-size:clamp(.9rem,2.5vw,1.1rem);
        font-weight:500;
        color:${c.text};
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
        min-height:1.4em;
      }
      .player-sub { font-size:.72rem; color:${c.sub}; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
      .controls-row { display:flex; align-items:center; gap:clamp(10px,3vw,24px); }
      .ctrl-btn {
        display:flex; align-items:center; justify-content:center;
        border:none; background:none; cursor:pointer; border-radius:50%;
        color:${c.text}; transition:all .15s; padding:6px;
        -webkit-user-select:none; user-select:none;
      }
      .ctrl-btn:active { transform:scale(.85); opacity:.7; }
      .ctrl-btn.play {
        background:${c.text};
        color:${c._isDaytime ? '#fff' : '#000'};
        width:52px; height:52px;
        box-shadow:0 4px 20px rgba(0,0,0,.22);
      }
      .ctrl-btn.play svg { fill: ${this._isDaytime() ? '#1d1d1f' : '#f0f0f5'}; }
      .vol-row { display:flex; align-items:center; gap:10px; }
      .vol-icon { font-size:1rem; color:${c.sub}; flex-shrink:0; }
      .vol-slider {
        flex:1; height:5px; border-radius:3px;
        -webkit-appearance:none; appearance:none;
        background:${c.cardBorder};
        outline:none; cursor:pointer;
        touch-action:pan-x;
      }
      .vol-slider::-webkit-slider-thumb {
        -webkit-appearance:none;
        width:20px; height:20px; border-radius:50%;
        background:${c.text};
        box-shadow:0 2px 8px rgba(0,0,0,.25);
        cursor:pointer;
      }
      .vol-val { font-size:.7rem; color:${c.sub}; min-width:32px; text-align:right; }

      /* ── SPOTIFY ── */
      .spotify-btn {
        display:flex; align-items:center; gap:10px;
        padding:12px 16px; border-radius:14px; cursor:pointer;
        background:rgba(29,185,84,.09);
        border:1.5px solid rgba(29,185,84,.22);
        transition:all .15s;
        -webkit-user-select:none; user-select:none;
      }
      .spotify-btn:active { transform:scale(.97); background:rgba(29,185,84,.18); }
      .spotify-logo { font-size:1.3rem; }
      .spotify-text { font-size:.82rem; font-weight:600; color:#1db954; }
      .spotify-sub { font-size:.65rem; color:rgba(29,185,84,.65); margin-top:1px; }

      /* ── LIGHTS ── */
      .lights-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
      .light-btn {
        display:flex; flex-direction:column; align-items:center;
        gap:8px; padding:16px 8px 12px;
        border-radius:18px; cursor:pointer;
        background:${c.card};
        border:1.5px solid ${c.cardBorder};
        backdrop-filter:blur(16px);
        -webkit-backdrop-filter:blur(16px);
        transition:all .18s;
        -webkit-user-select:none; user-select:none;
      }
      .light-btn:active { transform:scale(.93); }
      .light-btn.on { background:${c.glow}; border-color:rgba(255,200,60,.3); }
      .light-icon { font-size:1.5rem; transition:filter .3s; }
      .light-btn.on .light-icon { filter:drop-shadow(0 0 6px rgba(255,200,60,.6)); }
      .light-name { font-size:.62rem; color:${c.sub}; text-align:center; line-height:1.3; font-weight:500; }
      .light-btn.on .light-name { color:${c.text}; }

      /* ── BOTTOM BAR ── */
      .bottom-bar { display:flex; align-items:center; justify-content:space-between; gap:10px; }
      .mac-battery { display:flex; align-items:center; gap:5px; font-size:.72rem; color:${c.sub}; }
      .off-btn {
        display:flex; align-items:center; gap:6px;
        padding:9px 16px; border-radius:12px; cursor:pointer;
        background:rgba(255,60,60,.07);
        border:1.5px solid rgba(255,60,60,.18);
        font-size:.75rem; font-weight:600; color:rgba(255,80,80,.8);
        transition:all .15s; -webkit-user-select:none; user-select:none;
      }
      .off-btn:active { background:rgba(255,60,60,.18); transform:scale(.95); }
      .mode-pill {
        display:flex; align-items:center; gap:5px;
        padding:7px 14px; border-radius:20px; cursor:pointer;
        background:${c.card}; border:1px solid ${c.cardBorder};
        font-size:.7rem; color:${c.sub};
        transition:all .2s; -webkit-user-select:none; user-select:none;
      }
    `;
  }

  _weatherIcon(state) {
    const map = {
      'sunny':'☀️','clear-night':'🌙','partlycloudy':'⛅','cloudy':'☁️',
      'fog':'🌫️','rainy':'🌧️','snowy':'❄️','windy':'💨','lightning':'⛈️',
      'pouring':'🌧️','hail':'🌨️','exceptional':'🌡️'
    };
    return map[state] || '🌤️';
  }

  _callService(domain, service, data) {
    if (this._hass) this._hass.callService(domain, service, data);
  }

  _playRadio(url, name) {
    this._activeRadio = name;
    this._callService('media_player','play_media',{
      entity_id:'media_player.wohnzimmer_alm',
      media_content_id: url,
      media_content_type:'audio/mp4'
    });
    this._update();
  }

  _build() {
    const c = this._colors();
    const day = this._isDaytime();

    const RADIO = [
      {name:'SRF 1',  icon:'1️⃣',  color:'#4a9eff', url:'http://stream.srg-ssr.ch/m/drs1/mp3_128'},
      {name:'SRF 3',  icon:'3️⃣',  color:'#ff6b35', url:'http://stream.srg-ssr.ch/m/drs3/mp3_128'},
      {name:'Swiss Pop',icon:'💙',color:'#ff3b8a', url:'http://stream.srg-ssr.ch/m/rsp/mp3_128'},
      {name:'Energy', icon:'⚡',  color:'#f7c948', url:'https://energyzurich.ice.infomaniak.ch/energyzurich-high.mp3'},
      {name:'Radio 24',icon:'📻', color:'#a855f7', url:'https://radio24.ice.infomaniak.ch/radio24-high.mp3'},
    ];

    const LIGHTS = [
      {id:'light.deckenlampe', name:'Decke',    icon:'💡'},
      {id:'light.h618a',       name:'Sofa LED', icon:'🟡'},
      {id:'light.h618a_2',     name:'Küche',    icon:'🟠'},
      {id:'media_player.lg_webos_tv_oled65g49ls_2', name:'LG TV', icon:'📺'},
    ];

    const h = this._hass || {};
    const st = (id) => h.states?.[id];
    const alm = st('media_player.wohnzimmer_alm');
    const spot = st('media_player.spotify_janisss');
    const weather = st('weather.forecast_home');
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
    const dateStr = now.toLocaleDateString('de-CH',{weekday:'long',day:'numeric',month:'long'});
    const mac = st('sensor.macbook_air_von_janis_internal_battery_level');

    const almState = alm?.state || 'off';
    const almTitle = alm?.attributes?.media_title || (almState === 'off' ? 'Ausgeschaltet' : almState === 'playing' ? 'Läuft...' : 'Bereit');
    const almArtist = alm?.attributes?.media_artist || '';
    const almVol = Math.round((alm?.attributes?.volume_level || 0.5) * 100);
    const spotState = spot?.state || 'idle';
    const spotTitle = spot?.attributes?.media_title || '';
    const spotArtist = spot?.attributes?.media_artist || '';
    const wState = weather?.state || '';
    const wTemp = weather?.attributes?.temperature ?? '—';
    const wCond = wState.replace(/-/g,' ');

    // Radio buttons
    const radioHTML = RADIO.map(r => `
      <div class="radio-btn${this._activeRadio===r.name?' active':''}"
           style="${this._activeRadio===r.name?`border-color:${r.color}44;background:${r.color}15;`:''}"
           data-radio-url="${r.url}" data-radio-name="${r.name}">
        <span class="radio-icon">${r.icon}</span>
        <span class="radio-name" style="${this._activeRadio===r.name?`color:${r.color}`:''}">
          ${r.name}
        </span>
      </div>`).join('');

    // Light buttons
    const lightsHTML = LIGHTS.map(l => {
      const on = st(l.id)?.state === 'on';
      return `<div class="light-btn${on?' on':''}" data-toggle-id="${l.id}">
        <span class="light-icon">${l.icon}</span>
        <span class="light-name">${l.name}</span>
      </div>`;
    }).join('');

    // Play icon SVG
    const playIcon = almState === 'playing'
      ? `<svg width="22" height="22" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" fill="${c.text}"/></svg>`
      : `<svg width="22" height="22" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="${c.text}"/></svg>`;

    this.shadowRoot.innerHTML = `
      <style>${this._css(c)}</style>
      <div class="root">

        <!-- TOP ROW: CLOCK + WEATHER -->
        <div class="top">
          <div class="card">
            <div class="clock-num">${timeStr}</div>
            <div class="clock-date">${dateStr}</div>
          </div>
          <div class="card">
            <div class="weather-row">
              <span class="weather-icon">${this._weatherIcon(wState)}</span>
              <div>
                <div class="weather-temp">${wTemp}°</div>
                <div class="weather-loc">Egg SZ · Schweiz</div>
                <div class="weather-cond">${wCond}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- RADIO -->
        <div class="card">
          <div class="sec-lbl">📻 &nbsp;Radio</div>
          <div class="radio-grid">${radioHTML}</div>
        </div>

        <!-- PLAYER -->
        <div class="card">
          <div class="player-wrap">
            <div>
              <div class="player-title">${almTitle}</div>
              <div class="player-sub">${almArtist || 'Almando Wohnzimmer'}</div>
            </div>
            <div class="controls-row">
              <button class="ctrl-btn" id="btn-prev" title="Zurück">
                <svg width="26" height="26" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6 8.5 6V6z" fill="${c.text}"/></svg>
              </button>
              <button class="ctrl-btn play" id="btn-play">${playIcon}</button>
              <button class="ctrl-btn" id="btn-stop" title="Stop">
                <svg width="22" height="22" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" fill="${c.sub}"/></svg>
              </button>
              <button class="ctrl-btn" id="btn-next" title="Weiter">
                <svg width="26" height="26" viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zm2-12v12h2V6H8z" fill="${c.text}"/></svg>
              </button>
              <div style="flex:1"></div>
              <div class="spotify-btn" id="btn-spotify">
                <span class="spotify-logo">🎵</span>
                <div>
                  <div class="spotify-text">Spotify</div>
                  <div class="spotify-sub">${spotTitle || (spotState==='playing'?'Läuft...':'Bereit')}</div>
                </div>
              </div>
            </div>
            <div class="vol-row">
              <span class="vol-icon">🔈</span>
              <input type="range" class="vol-slider" id="vol-slider"
                     min="0" max="100" value="${almVol}"
                     style="--vol:${almVol}%">
              <span class="vol-icon">🔊</span>
              <span class="vol-val">${almVol}%</span>
            </div>
          </div>
        </div>

        <!-- LIGHTS -->
        <div class="card">
          <div class="sec-lbl">💡 &nbsp;Licht & Geräte</div>
          <div class="lights-grid">${lightsHTML}</div>
        </div>

        <!-- BOTTOM BAR -->
        <div class="bottom-bar">
          <div class="off-btn" id="btn-off">⏻ Alles aus</div>
          <div class="mac-battery">💻 ${mac?.state ?? '—'}%</div>
          <div class="mode-pill" id="btn-mode">${day?'☀️ Tag':'🌙 Nacht'}</div>
        </div>

      </div>
    `;

    this._bindEvents(RADIO, LIGHTS, c);
  }

  _bindEvents(RADIO, LIGHTS, c) {
    const root = this.shadowRoot;

    // Radio buttons
    root.querySelectorAll('.radio-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this._playRadio(btn.dataset.radioUrl, btn.dataset.radioName);
      });
    });

    // Play/Pause
    root.getElementById('btn-play')?.addEventListener('click', () => {
      this._callService('media_player','media_play_pause',{entity_id:'media_player.wohnzimmer_alm'});
    });
    root.getElementById('btn-stop')?.addEventListener('click', () => {
      this._activeRadio = null;
      this._callService('media_player','media_stop',{entity_id:'media_player.wohnzimmer_alm'});
    });
    root.getElementById('btn-prev')?.addEventListener('click', () => {
      this._callService('media_player','media_previous_track',{entity_id:'media_player.wohnzimmer_alm'});
    });
    root.getElementById('btn-next')?.addEventListener('click', () => {
      this._callService('media_player','media_next_track',{entity_id:'media_player.wohnzimmer_alm'});
    });

    // Volume slider
    const volSlider = root.getElementById('vol-slider');
    if (volSlider) {
      volSlider.addEventListener('change', (e) => {
        const vol = parseInt(e.target.value) / 100;
        this._callService('media_player','volume_set',{entity_id:'media_player.wohnzimmer_alm',volume_level:vol});
      });
      volSlider.addEventListener('input', (e) => {
        const val = root.querySelector('.vol-val');
        if (val) val.textContent = e.target.value + '%';
      });
    }

    // Spotify more-info
    root.getElementById('btn-spotify')?.addEventListener('click', () => {
      const event = new CustomEvent('hass-more-info',{
        bubbles:true, composed:true,
        detail:{entityId:'media_player.spotify_janisss'}
      });
      this.dispatchEvent(event);
    });

    // Light toggles
    root.querySelectorAll('.light-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.toggleId;
        const domain = id.startsWith('light.') ? 'light' : 'media_player';
        const service = domain === 'light' ? 'toggle' : (this._hass?.states?.[id]?.state==='on'?'turn_off':'turn_on');
        this._callService(domain, service, {entity_id:id});
      });
    });

    // All off
    root.getElementById('btn-off')?.addEventListener('click', () => {
      this._callService('media_player','turn_off',{entity_id:'media_player.wohnzimmer_alm'});
      this._callService('light','turn_off',{entity_id:['light.deckenlampe','light.h618a','light.h618a_2']});
    });

    // Mode toggle (force day/night override)
    root.getElementById('btn-mode')?.addEventListener('click', () => {
      this._forceDark = !this._forceDark;
      this._built = false;
      this._build();
      this._built = true;
    });
  }

  _update() {
    if (!this._hass || !this._built) return;
    // Rebuild on state change (efficient enough for a dashboard)
    this._built = false;
    this._build();
    this._built = true;
  }

  getCardSize() { return 15; }

  static getConfigElement() { return document.createElement('div'); }
  static getStubConfig() { return {}; }
}

customElements.define('wz-dashboard', WzDashboard);
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'wz-dashboard',
  name: 'Wohnzimmer Dashboard',
  description: 'Custom Apple-style Wohnzimmer Control Center'
});
