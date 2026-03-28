# Neue Musik-Seite HTML — kompakt, Radio immer sichtbar
NEW_MUSIK = '''<div class="page" id="pg-musik">
      <!-- Blurred album-art background layer -->
      <div id="album-page-bg" style="position:absolute;inset:0;z-index:0;overflow:hidden;border-radius:0;pointer-events:none">
        <img id="album-page-bg-img" src="" alt="" style="width:100%;height:100%;object-fit:cover;transform:scale(1.15);filter:blur(40px) brightness(.35) saturate(1.8);transition:opacity 1.8s ease">
        <div style="position:absolute;inset:0;background:rgba(0,0,0,.55)"></div>
        <canvas id="spec-cv" style="position:absolute;bottom:0;left:0;width:100%;height:38%;opacity:0;pointer-events:none;transition:opacity 1.2s ease"></canvas>
      </div>

      <!-- ── Compact Now Playing Card ── -->
      <div class="c" id="np-card" style="position:relative;z-index:1;margin:0 0 10px;padding:14px 16px 10px">
        <!-- Top: disc + info -->
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:12px">
          <!-- Vinyl Disc (simple, rotating when playing) -->
          <div id="alb-tilt-wrap" style="position:relative;flex-shrink:0;width:72px;height:72px">
            <div id="alb-disc" style="
              width:72px;height:72px;border-radius:50%;overflow:hidden;position:relative;
              box-shadow:0 4px 18px rgba(0,0,0,.55);
              background:radial-gradient(circle at 50% 50%,#222 28%,transparent 29%),
                         conic-gradient(#1a1a1a 0deg,#2d2d2d 60deg,#1a1a1a 120deg,#2d2d2d 180deg,#1a1a1a 240deg,#2d2d2d 300deg,#1a1a1a 360deg)">
              <!-- Album art covers the disc -->
              <img id="alb-img" src="" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:50%;opacity:0;transition:opacity .8s ease">
              <div id="alb-fallback" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:1">
                <div id="spk-wrap" style="width:32px;height:32px;opacity:.6">
                  <svg viewBox="0 0 32 32" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="1.6" stroke-linecap="round">
                    <ellipse cx="16" cy="16" rx="11" ry="11"/>
                    <ellipse cx="16" cy="16" rx="5" ry="5"/>
                    <circle cx="16" cy="16" r="2" fill="rgba(255,255,255,.7)" stroke="none"/>
                  </svg>
                </div>
              </div>
              <!-- Center hole -->
              <div style="position:absolute;top:50%;left:50%;width:10px;height:10px;background:#111;border-radius:50%;transform:translate(-50%,-50%);z-index:3"></div>
            </div>
            <!-- Glow ring when playing -->
            <div id="alb-glow" style="position:absolute;inset:-3px;border-radius:50%;background:transparent;transition:box-shadow .8s ease;pointer-events:none"></div>
            <!-- Hidden tonearm (kept for JS compat) -->
            <div id="alb-tonearm-wrap" style="display:none"><svg></svg></div>
          </div>

          <!-- Track Info -->
          <div style="flex:1;min-width:0">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px">
              <div id="np-src" style="display:inline-flex;align-items:center;gap:4px;background:rgba(255,255,255,.1);border-radius:20px;padding:2px 8px 2px 6px;font-size:.58rem;font-weight:700;color:rgba(255,255,255,.7);letter-spacing:.2px">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
                <span id="np-src-txt">Almando</span>
              </div>
            </div>
            <div class="nptitle" id="np-t" style="font-size:.92rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;line-height:1.25">Bereit</div>
            <div class="npsub" id="np-s" style="font-size:.7rem;color:rgba(255,255,255,.5);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px">Almando Wohnzimmer</div>
            <!-- EQ Bars -->
            <div class="eq" id="eq" style="margin-top:5px"><i></i><i></i><i></i><i></i><i></i></div>
          </div>
        </div>

        <!-- Track progress (hidden until known) -->
        <div id="track-prog-wrap" style="display:none;margin-bottom:10px">
          <svg id="track-prog-arc-svg" style="display:none"></svg>
          <div style="height:3px;background:rgba(255,255,255,.12);border-radius:2px;overflow:hidden">
            <div id="track-prog-fill" style="height:100%;width:0%;background:linear-gradient(90deg,#0a84ff,rgba(10,132,255,.6));border-radius:2px;transition:width .5s linear"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:4px">
            <span id="track-pos" style="font-size:.55rem;color:rgba(255,255,255,.3)">0:00</span>
            <span id="track-dur" style="font-size:.55rem;color:rgba(255,255,255,.3)">0:00</span>
          </div>
        </div>

        <!-- Controls row -->
        <div class="btns" style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:10px">
          <button class="bsml" id="btn-prev" title="Zurück" style="opacity:0;pointer-events:none;transition:opacity .2s">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="19 20 9 12 19 4 19 20"/><line x1="5" y1="19" x2="5" y2="5"/></svg>
          </button>
          <button class="bplay" id="btn-play">
            <svg id="play-ico" width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          </button>
          <button class="bsml" id="btn-stop" title="Stop">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
          </button>
          <button class="bsml" id="btn-next" title="Weiter" style="opacity:0;pointer-events:none;transition:opacity .2s">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
          </button>
          <!-- Sleep Timer inline -->
          <div id="sleep-timer-row" style="margin-left:4px">
            <button id="sleep-timer-btn" title="Sleep-Timer" class="bsml">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
              <span id="sleep-btn-lbl" style="display:none">Sleep</span>
            </button>
            <div id="sleep-pill" style="display:none;align-items:center;gap:4px;background:rgba(10,132,255,.2);border-radius:20px;padding:3px 8px">
              <div id="sleep-pill-dot" style="width:6px;height:6px;border-radius:50%;background:#0a84ff"></div>
              <span id="sleep-pill-txt" style="font-size:.65rem;color:#0a84ff;font-weight:600">00:00</span>
              <button id="sleep-cancel" title="Abbrechen" style="background:none;border:none;color:rgba(255,255,255,.4);font-size:.7rem;cursor:pointer;padding:0 0 0 2px">✕</button>
            </div>
          </div>
        </div>

        <!-- Volume -->
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="2" stroke-linecap="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          <div style="flex:1;position:relative;height:36px;display:flex;align-items:center">
            <div style="position:absolute;left:0;right:0;height:4px;background:rgba(255,255,255,.12);border-radius:2px">
              <div id="vfill" style="height:100%;width:40%;background:linear-gradient(90deg,#0a84ff,rgba(10,132,255,.6));border-radius:2px;transition:width .08s"></div>
              <div id="vthumb" style="position:absolute;left:40%;top:50%;width:18px;height:18px;background:#fff;border-radius:50%;box-shadow:0 1px 6px rgba(0,0,0,.4);transform:translate(-50%,-50%);pointer-events:none;transition:left .08s"></div>
            </div>
            <input type="range" id="vol-range" min="0" max="100" value="40" style="position:absolute;left:0;width:100%;height:100%;opacity:0;cursor:pointer;margin:0;padding:0;touch-action:none">
          </div>
          <span id="vv-hdr" style="font-size:.65rem;font-weight:600;color:rgba(255,255,255,.45);min-width:30px;text-align:right">40%</span>
        </div>
        <div id="vol-wrap" style="display:none">
          <div style="display:flex;justify-content:space-between;padding:0 2px">
            <span style="font-size:.58rem;color:rgba(255,255,255,.25)">Leise</span>
            <span id="vv" style="font-size:.65rem;font-weight:600;color:rgba(255,255,255,.5)">40%</span>
            <span style="font-size:.58rem;color:rgba(255,255,255,.25)">Laut</span>
          </div>
        </div>
      </div><!-- /np-card -->

      <!-- ── Radio Fallback Card (only when radio playing) ── -->
      <div id="radio-fallback-card" style="position:relative;z-index:1;margin:0 0 8px;display:none;background:rgba(28,28,30,.92);border-radius:16px;border:1px solid rgba(255,255,255,.08);padding:12px 14px;overflow:hidden">
        <div id="rfc-bg"></div>
        <div style="position:relative;z-index:1;display:flex;align-items:center;gap:10px">
          <div id="rfc-antenna-ico" style="width:32px;height:32px;border-radius:10px;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="1.8" stroke-linecap="round"><path d="M12 1v5m0 0c-5.5 0-9 4.5-9 9h18c0-4.5-3.5-9-9-9z"/><path d="M8 23v-4h8v4"/><line x1="12" y1="6" x2="12" y2="15"/></svg>
          </div>
          <div style="flex:1;min-width:0">
            <div id="rfc-type-badge" style="font-size:.58rem;font-weight:700;letter-spacing:.6px;color:rgba(255,255,255,.4)">📻 RADIO</div>
            <div id="rfc-title" style="font-size:.82rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">–</div>
            <div id="rfc-sub" style="font-size:.65rem;color:rgba(255,255,255,.4)">Almando Wohnzimmer</div>
          </div>
          <div id="rfc-freq-row">
            <div id="rfc-wave-bars" style="display:flex;align-items:flex-end;gap:2px;height:14px">
              <span style="width:3px;height:6px;background:rgba(255,255,255,.3);border-radius:2px"></span>
              <span style="width:3px;height:10px;background:rgba(255,255,255,.3);border-radius:2px"></span>
              <span style="width:3px;height:14px;background:rgba(255,255,255,.3);border-radius:2px"></span>
              <span style="width:3px;height:9px;background:rgba(255,255,255,.3);border-radius:2px"></span>
              <span style="width:3px;height:5px;background:rgba(255,255,255,.3);border-radius:2px"></span>
            </div>
            <span id="rfc-cid" style="display:none"></span>
          </div>
        </div>
      </div>

      <!-- Track History (shown when tracks available) -->
      <div id="track-history" style="display:none;flex-direction:column;gap:5px;margin:0 0 10px;position:relative;z-index:1">
        <div id="track-history-lbl" style="font-size:.6rem;font-weight:700;letter-spacing:.7px;color:rgba(255,255,255,.3);text-transform:uppercase;margin-bottom:4px">🎵 Zuletzt gespielt</div>
        <div id="track-history-list"></div>
      </div>

      <!-- ── Radio ── -->
      <span class="lbl" style="position:relative;z-index:1">Radio</span>
      <div class="rg" id="rg" style="position:relative;z-index:1"></div>

      <!-- ── Spotify ── -->
      <div style="position:relative;z-index:1;margin-bottom:0">
        <div class="spotcard c" id="spotcard">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="#1db954"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.586 14.424a.622.622 0 0 1-.857.207c-2.348-1.435-5.304-1.76-8.785-.964a.623.623 0 0 1-.277-1.215c3.809-.87 7.077-.496 9.712 1.115.293.18.387.563.207.857zm1.223-2.723a.78.78 0 0 1-1.072.257c-2.687-1.652-6.785-2.131-9.965-1.166a.78.78 0 0 1-.973-.519.781.781 0 0 1 .519-.972c3.632-1.102 8.147-.568 11.234 1.328a.78.78 0 0 1 .257 1.072zm.105-2.835C14.69 8.956 9.954 8.8 7.034 9.608a.937.937 0 1 1-.543-1.794c3.353-.998 8.936-.792 12.457 1.349a.937.937 0 0 1-.034 1.703z"/></svg>
          <div style="flex:1;min-width:0">
            <div class="spott" id="sp-t">Spotify</div>
            <div class="spots" id="sp-s" style="cursor:pointer" title="Gerät wechseln">–</div>
          </div>
          <select id="sp-dev" style="display:none" title="Spotify-Gerät"></select>
          <div id="sp-arrow" style="color:rgba(255,255,255,.3)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
        <div id="sp-playlists" style="display:none;padding:0 4px 4px">
          <div style="padding:4px 0 4px">
            <div id="sp-pl-list" style="display:flex;flex-direction:column;gap:4px">
              <div style="color:rgba(255,255,255,.4);font-size:.8rem;padding:8px">Lade Playlists…</div>
            </div>
          </div>
        </div>
      </div><!-- /spotify -->
    </div><!-- /pg-musik -->
'''

print(f"New musik HTML: {len(NEW_MUSIK)} chars")
print("Required IDs check:")
required = ['alb-disc','alb-img','alb-fallback','alb-tilt-wrap','alb-tonearm-wrap','album-page-bg-img',
            'spk-wrap','np-t','np-s','np-src-txt','eq','btn-play','btn-stop','btn-prev','btn-next',
            'vfill','vthumb','vol-range','vv','vv-hdr','track-prog-wrap','track-prog-fill',
            'track-pos','track-dur','rfc-title','rfc-sub','rfc-type-badge','rfc-wave-bars',
            'rfc-cid','sleep-timer-btn','sleep-pill','sleep-pill-txt','sleep-cancel',
            'track-history','rg','spotcard','sp-t','sp-s','sp-dev','sp-playlists','sp-pl-list',
            'spec-cv','alb-glow','sleep-timer-row']
for id in required:
    found = f'id="{id}"' in NEW_MUSIK
    print(f"  {'✓' if found else '✗'} {id}")
