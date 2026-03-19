/**
 * CLAWY MASCOT v2 — Desktop Buddy
 * Cute SVG crab that walks around, talks, and reacts
 */
(function() {
  if (window.__CLAWY_MASCOT__) return;
  window.__CLAWY_MASCOT__ = true;

  const style = document.createElement('style');
  style.textContent = `
    #clawy-wrap { position:fixed; bottom:0; z-index:99999; cursor:pointer; user-select:none; transition:left 0.05s linear; }
    #clawy-svg { display:block; filter:drop-shadow(0 6px 18px rgba(224,64,251,0.55)); transition:filter 0.3s; }
    #clawy-wrap:hover #clawy-svg { filter:drop-shadow(0 6px 28px rgba(224,64,251,0.9)); }
    #clawy-bubble {
      position:absolute; bottom:100%; right:0; margin-bottom:10px;
      background:rgba(6,8,18,0.93); border:1.5px solid rgba(224,64,251,0.55);
      border-radius:18px 18px 4px 18px; padding:10px 15px;
      font-family:-apple-system,BlinkMacSystemFont,sans-serif;
      font-size:13px; color:#eef; line-height:1.5; max-width:210px;
      white-space:pre-wrap; box-shadow:0 0 20px rgba(224,64,251,0.3);
      backdrop-filter:blur(12px); pointer-events:none;
      opacity:0; transform:translateY(6px) scale(0.95);
      transition:opacity 0.25s ease, transform 0.25s ease;
    }
    #clawy-bubble.show { opacity:1; transform:translateY(0) scale(1); }
    #clawy-bubble::after {
      content:''; position:absolute; bottom:-9px; right:20px;
      border:9px solid transparent; border-top-color:rgba(224,64,251,0.55);
      border-bottom:none;
    }
    @keyframes clawyBounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
    @keyframes clawyDance { 0%{transform:rotate(-12deg) translateY(0)} 25%{transform:rotate(12deg) translateY(-8px)} 50%{transform:rotate(-8deg) translateY(-4px)} 75%{transform:rotate(10deg) translateY(-9px)} 100%{transform:rotate(-12deg) translateY(0)} }
    @keyframes clawyAngry { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-5px) rotate(-4deg)} 60%{transform:translateX(5px) rotate(4deg)} }
    #clawy-wrap.bounce #clawy-svg { animation:clawyBounce 0.5s ease-in-out infinite; }
    #clawy-wrap.dance  #clawy-svg { animation:clawyDance  0.4s ease-in-out infinite; }
    #clawy-wrap.angry  #clawy-svg { animation:clawyAngry  0.2s ease-in-out infinite; }
  `;
  document.head.appendChild(style);

  // SVG crab — cute, symmetrical, big eyes
  function makeSVG(mood, dir, legSwing) {
    // dir: 1=right, -1=left (facing direction)
    const flip = dir < 0 ? 'transform="scale(-1,1) translate(-100,0)"' : '';
    const ls = Math.sin(legSwing);
    const ec = mood==='angry' ? '#ff4444' : mood==='happy' ? '#76ff03' : '#e040fb';
    const eyeGlow = `0 0 8px ${ec}`;
    // Mouth shape
    const mouthD = mood==='talk'   ? 'M38,66 Q50,74 62,66'
                 : mood==='angry'  ? 'M38,70 Q50,63 62,70'
                 :                   'M38,66 Q50,72 62,66'; // smile

    return `<svg id="clawy-svg" xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <defs>
    <radialGradient id="cshell" cx="42%" cy="38%">
      <stop offset="0%" stop-color="#e8451a"/>
      <stop offset="100%" stop-color="#9e1500"/>
    </radialGradient>
    <radialGradient id="cbelly" cx="50%" cy="40%">
      <stop offset="0%" stop-color="#ffcc99"/>
      <stop offset="100%" stop-color="#e8965a"/>
    </radialGradient>
    <filter id="eg"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="glow2"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <g ${flip}>

  <!-- SHADOW -->
  <ellipse cx="50" cy="97" rx="30" ry="5" fill="rgba(0,0,0,0.25)"/>

  <!-- BACK LEGS (behind body) -->
  <!-- Left legs -->
  <g stroke="#9e1500" stroke-width="3.5" stroke-linecap="round" fill="none">
    <line x1="28" y1="68" x2="${14 + ls*4}" y2="${82 - ls*2}" />
    <line x1="${14 + ls*4}" y1="${82 - ls*2}" x2="${10 + ls*3}" y2="95"/>
    
    <line x1="23" y1="65" x2="${8 - ls*3}" y2="${76 + ls*2}" />
    <line x1="${8 - ls*3}" y1="${76 + ls*2}" x2="${5 - ls*2}" y2="90"/>
    
    <line x1="20" y1="60" x2="${5 - ls*4}" y2="${70 - ls*2}" />
    <line x1="${5 - ls*4}" y1="${70 - ls*2}" x2="${3 - ls*3}" y2="84"/>
  </g>
  <!-- Right legs -->
  <g stroke="#9e1500" stroke-width="3.5" stroke-linecap="round" fill="none">
    <line x1="72" y1="68" x2="${86 - ls*4}" y2="${82 + ls*2}" />
    <line x1="${86 - ls*4}" y1="${82 + ls*2}" x2="${90 - ls*3}" y2="95"/>
    
    <line x1="77" y1="65" x2="${92 + ls*3}" y2="${76 - ls*2}" />
    <line x1="${92 + ls*3}" y1="${76 - ls*2}" x2="${95 + ls*2}" y2="90"/>
    
    <line x1="80" y1="60" x2="${95 + ls*4}" y2="${70 + ls*2}" />
    <line x1="${95 + ls*4}" y1="${70 + ls*2}" x2="${97 + ls*3}" y2="84"/>
  </g>

  <!-- BELLY -->
  <ellipse cx="50" cy="73" rx="28" ry="18" fill="url(#cbelly)"/>

  <!-- SHELL -->
  <ellipse cx="50" cy="58" rx="34" ry="26" fill="url(#cshell)"/>
  <!-- Shell highlight -->
  <ellipse cx="43" cy="50" rx="13" ry="9" fill="rgba(255,255,255,0.18)" transform="rotate(-18,43,50)"/>
  <!-- Shell ridges -->
  <path d="M22,60 Q50,48 78,60" stroke="rgba(0,0,0,0.12)" stroke-width="1.5" fill="none"/>
  <path d="M28,67 Q50,58 72,67" stroke="rgba(0,0,0,0.09)" stroke-width="1.5" fill="none"/>

  <!-- LEFT CLAW -->
  <g>
    <path d="M20,60 Q4,48 6,35" stroke="#b02000" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="7" cy="31" rx="10" ry="8" fill="#c52500" transform="rotate(-25,7,31)"/>
    <path d="M2,26 Q-2,18 5,20" stroke="#c52500" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M12,25 Q15,17 9,21" stroke="#9e1500" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  </g>

  <!-- RIGHT CLAW -->
  <g>
    <path d="M80,60 Q96,48 94,35" stroke="#b02000" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="93" cy="31" rx="10" ry="8" fill="#c52500" transform="rotate(25,93,31)"/>
    <path d="M98,26 Q102,18 95,20" stroke="#c52500" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M88,25 Q85,17 91,21" stroke="#9e1500" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  </g>

  <!-- EYE STALKS -->
  <line x1="37" y1="40" x2="32" y2="26" stroke="#b02000" stroke-width="4" stroke-linecap="round"/>
  <line x1="63" y1="40" x2="68" y2="26" stroke="#b02000" stroke-width="4" stroke-linecap="round"/>

  <!-- EYES — big and cute -->
  <!-- Glow -->
  <circle cx="32" cy="23" r="11" fill="${ec}" opacity="0.3" filter="url(#glow2)"/>
  <circle cx="68" cy="23" r="11" fill="${ec}" opacity="0.3" filter="url(#glow2)"/>
  <!-- White -->
  <circle cx="32" cy="23" r="11" fill="white"/>
  <circle cx="68" cy="23" r="11" fill="white"/>
  <!-- Iris -->
  <circle cx="32" cy="23" r="9" fill="${ec}" filter="url(#eg)"/>
  <circle cx="68" cy="23" r="9" fill="${ec}" filter="url(#eg)"/>
  <!-- Pupil -->
  <circle cx="33.5" cy="24" r="5" fill="#111"/>
  <circle cx="69.5" cy="24" r="5" fill="#111"/>
  <!-- Shine 1 -->
  <circle cx="30" cy="19" r="2.5" fill="white" opacity="0.95"/>
  <circle cx="66" cy="19" r="2.5" fill="white" opacity="0.95"/>
  <!-- Shine 2 small -->
  <circle cx="35" cy="26" r="1.2" fill="white" opacity="0.6"/>
  <circle cx="71" cy="26" r="1.2" fill="white" opacity="0.6"/>
  <!-- Eye ring glow -->
  <circle cx="32" cy="23" r="10.5" fill="none" stroke="${ec}" stroke-width="1.5" opacity="0.7"/>
  <circle cx="68" cy="23" r="10.5" fill="none" stroke="${ec}" stroke-width="1.5" opacity="0.7"/>

  <!-- MOUTH -->
  <path d="${mouthD}" stroke="#7a1500" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  ${mood==='talk' ? '<ellipse cx="50" cy="70" rx="5" ry="3.5" fill="#7a1500" opacity="0.5"/>' : ''}

  <!-- CHEEK blush -->
  <ellipse cx="24" cy="62" rx="6" ry="4" fill="rgba(255,100,100,0.2)"/>
  <ellipse cx="76" cy="62" rx="6" ry="4" fill="rgba(255,100,100,0.2)"/>

  <!-- Antenna dots -->
  <circle cx="36" cy="14" r="3" fill="#c52500"/>
  <circle cx="64" cy="14" r="3" fill="#c52500"/>

  </g>
</svg>`;
  }

  // DOM
  const wrap = document.createElement('div');
  wrap.id = 'clawy-wrap';
  document.body.appendChild(wrap);

  const bub = document.createElement('div');
  bub.id = 'clawy-bubble';
  wrap.appendChild(bub);

  // State
  let x = window.innerWidth - 130;
  let vx = 0;
  let dir = -1;
  let mood = 'idle';
  let legPhase = 0;
  let bubTimer = null;
  let moodTimer = 0;
  let clicks = 0;
  let frame = 0;

  const SIZE = 100;
  const IDLE_MSGS = [
    'Alles okay? 🦀','Ich passe auf! 👀','System online ✅',
    'Tap mich an 👆','Schön ruhig heute 😌','Hallo! Brauchst du was?',
    'Ich bin immer hier 🦀','Psst — alles gut!','Was gibt\'s Neues?',
    '...ich beobachte dich 👁️','Kleiner Krabben-Check ✔️',
  ];
  const GREET = ['Hey Janis! 👋','Da bist du! 🎉','Willkommen! 🦀','Schön dich zu sehen!'];

  function speak(msg, newMood) {
    bub.textContent = msg;
    bub.classList.add('show');
    clearTimeout(bubTimer);
    if (newMood) setMood(newMood, 3000);
    bubTimer = setTimeout(() => bub.classList.remove('show'), Math.max(2200, msg.length * 65));
  }

  function setMood(m, dur) {
    mood = m;
    moodTimer = dur || 2500;
    wrap.className = '';
    wrap.id = 'clawy-wrap';
    if (m === 'happy') wrap.classList.add('dance');
    if (m === 'angry') wrap.classList.add('angry');
    if (m === 'idle' || m === 'walk') wrap.classList.add('bounce');
  }

  // Greet
  setTimeout(() => speak(GREET[Math.floor(Math.random()*GREET.length)], 'happy'), 900);
  setTimeout(() => setMood('idle', 0), 4000);

  // Click
  wrap.addEventListener('click', e => {
    e.stopPropagation();
    clicks++;
    if (clicks % 8 === 0) speak('Du klickst mich IMMER noch! 🦀❤️', 'happy');
    else if (clicks % 5 === 0) speak('Okay, jetzt reicht\'s! 😤', 'angry');
    else {
      const msgs = ['Hey! 👋','Was los?','Brauchst du was?','Hier! 🦀','Ich höre! 👂'];
      speak(msgs[Math.floor(Math.random()*msgs.length)], 'talk');
    }
  });

  // Random chat
  setInterval(() => {
    if (!bub.classList.contains('show') && Math.random() < 0.35) {
      speak(IDLE_MSGS[Math.floor(Math.random()*IDLE_MSGS.length)]);
    }
  }, 8000);

  // Walk trigger
  setInterval(() => {
    if (Math.random() < 0.5) {
      vx = (Math.random() - 0.5) * 4;
      dir = vx > 0 ? 1 : -1;
      setMood('walk', 2500 + Math.random()*2000);
    } else if (mood === 'walk') {
      vx = 0; setMood('idle', 0);
    }
  }, 3000);

  // Render loop
  function loop() {
    requestAnimationFrame(loop);
    frame++;
    moodTimer -= 16;
    if (moodTimer < 0 && mood !== 'idle') { vx=0; setMood('idle',0); }

    if (mood === 'walk') {
      x += vx;
      legPhase += 0.25;
      if (x < 10) { x=10; vx=Math.abs(vx); dir=1; }
      if (x > window.innerWidth-SIZE-10) { x=window.innerWidth-SIZE-10; vx=-Math.abs(vx); dir=-1; }
    } else {
      legPhase += 0.04; // subtle idle leg movement
    }

    wrap.style.left = x + 'px';
    // Redraw every few frames for perf
    if (frame % 3 === 0) {
      const svgEl = wrap.querySelector('svg');
      const newSvg = document.createElement('div');
      newSvg.innerHTML = makeSVG(mood==='talk'?'talk':mood==='angry'?'angry':mood==='happy'?'happy':'idle', dir, legPhase);
      if (svgEl) svgEl.replaceWith(newSvg.firstElementChild);
      else wrap.insertBefore(newSvg.firstElementChild, bub);
    }
  }

  // Initial draw
  wrap.insertAdjacentHTML('afterbegin', makeSVG('idle', dir, 0));
  loop();

  // Public API
  window.clawy = {
    say: (m) => speak(m, 'talk'),
    happy: () => { speak('🎉', 'happy'); },
    notify: (m) => speak('🔔 '+m, 'talk'),
    angry: () => setMood('angry', 2000),
  };
})();
