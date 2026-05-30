---
title: "Kua Number Calculator — Find Your Lucky Directions"
description: "Free Kua Number calculator based on your birth date and gender. Discover your personal lucky directions, best sleeping position, and compatible colors. Updated 2026."
date: "2026-05-26"
type: "tool"
layout: "tool"
slug: "kua-number-calculator"
---

<style>
.kua-tool { max-width: 680px; margin: 0 auto; font-family: system-ui, -apple-system, sans-serif; }
.kua-tool .input-group { margin-bottom: 1.2rem; }
.kua-tool label { display: block; font-weight: 600; margin-bottom: 0.3rem; color: #c9a84c; }
.kua-tool select, .kua-tool input { 
  width: 100%; padding: 0.7rem; border: 2px solid #2a1f3d; 
  background: #1a1025; color: #e8d5b7; border-radius: 8px; font-size: 1rem; 
}
.kua-tool select:focus, .kua-tool input:focus { border-color: #c9a84c; outline: none; }
.kua-tool button {
  width: 100%; padding: 0.9rem; background: linear-gradient(135deg, #c9a84c, #8b6914);
  color: #0d0820; border: none; border-radius: 8px; font-size: 1.1rem; font-weight: 700;
  cursor: pointer; transition: transform 0.15s;
}
.kua-tool button:hover { transform: translateY(-2px); }
.kua-result { display: none; margin-top: 2rem; padding: 1.5rem; 
  background: linear-gradient(135deg, #1a1025, #2a1f3d); border-radius: 12px; 
  border: 1px solid #c9a84c33; }
.kua-result.show { display: block; }
.kua-number { 
  text-align: center; font-size: 3rem; font-weight: 900; color: #c9a84c;
  text-shadow: 0 0 20px #c9a84c66; margin: 0.5rem 0; 
}
.kua-group { text-align: center; color: #a89878; margin-bottom: 1.2rem; font-size: 1.1rem; }
.kua-group strong { color: #c9a84c; }
.dir-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-top: 1rem; }
.dir-card { padding: 0.7rem; border-radius: 8px; text-align: center; }
.dir-card.lucky { background: #1a3020; border: 1px solid #2d8a4e44; }
.dir-card.unlucky { background: #301a1a; border: 1px solid #8a2d2d44; }
.dir-card .dir-name { font-weight: 700; font-size: 1.05rem; }
.dir-card .dir-type { font-size: 0.8rem; opacity: 0.7; margin-top: 0.2rem; }
.lucky .dir-name { color: #4caf50; }
.unlucky .dir-name { color: #f44336; }
.cta-box { margin-top: 2rem; padding: 1.2rem; background: #1a1025; border-radius: 8px; 
  border: 1px dashed #c9a84c55; text-align: center; }
.cta-box a { color: #c9a84c; font-weight: 600; }
.error-msg { color: #f44336; font-size: 0.85rem; display: none; margin-top: 0.3rem; }
</style>

<div class="kua-tool">
  <p style="color:#a89878;margin-bottom:1.5rem;">
    Your Kua Number (Gua Number) reveals your personal lucky directions — which way your bed should face, 
    which direction to work towards, and which colors bring you the most harmony. 
    <strong>No email required. Instant result.</strong>
  </p>

  <div class="input-group">
    <label for="kua-year">Birth Year</label>
    <input type="number" id="kua-year" placeholder="e.g. 1990" min="1900" max="2030" value="1990">
  </div>

  <div class="input-group">
    <label for="kua-gender">Gender (sex at birth, used in traditional Feng Shui)</label>
    <select id="kua-gender">
      <option value="">-- Select --</option>
      <option value="male">Male</option>
      <option value="female">Female</option>
    </select>
  </div>

  <div id="kua-error" class="error-msg"></div>

  <button onclick="calcKua()">🔮 Calculate My Kua Number</button>

  <div id="kua-result" class="kua-result"></div>

  <div class="cta-box" style="margin-top:2rem;">
    <p style="margin:0;font-size:0.9rem;">
      📿 <a href="/best/feng-shui-products-home/">Get Kua-compatible crystals & compasses</a> — 
      Feng Shui Mall pays <strong>10% commission + 180-day cookie</strong>
    </p>
  </div>
</div>

<script>
const KUA_DATA = {
  1: {
    name: "Kan (坎) — Water",
    group: "East Group",
    lucky: [
      {dir:"Southeast", type:"Sheng Chi (Best Wealth)"},
      {dir:"East", type:"Tian Yi (Health)"},
      {dir:"South", type:"Nian Yan (Relationships)"},
      {dir:"North", type:"Fu Wei (Peace)"}
    ],
    unlucky: [
      {dir:"Southwest", type:"Huo Hai (Misfortune)"},
      {dir:"Northeast", type:"Wu Gui (5 Ghosts)"},
      {dir:"Northwest", type:"Liu Sha (6 Killings)"},
      {dir:"West", type:"Jue Ming (Total Loss)"}
    ]
  },
  2: {
    name: "Kun (坤) — Earth",
    group: "West Group",
    lucky: [
      {dir:"Northeast", type:"Sheng Chi"},
      {dir:"West", type:"Tian Yi"},
      {dir:"Northwest", type:"Nian Yan"},
      {dir:"Southwest", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"East", type:"Huo Hai"},
      {dir:"Southeast", type:"Wu Gui"},
      {dir:"South", type:"Liu Sha"},
      {dir:"North", type:"Jue Ming"}
    ]
  },
  3: {
    name: "Zhen (震) — Thunder",
    group: "East Group",
    lucky: [
      {dir:"South", type:"Sheng Chi"},
      {dir:"North", type:"Tian Yi"},
      {dir:"Southeast", type:"Nian Yan"},
      {dir:"East", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"Southwest", type:"Huo Hai"},
      {dir:"Northwest", type:"Wu Gui"},
      {dir:"Northeast", type:"Liu Sha"},
      {dir:"West", type:"Jue Ming"}
    ]
  },
  4: {
    name: "Xun (巽) — Wind",
    group: "East Group",
    lucky: [
      {dir:"North", type:"Sheng Chi"},
      {dir:"South", type:"Tian Yi"},
      {dir:"East", type:"Nian Yan"},
      {dir:"Southeast", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"Northwest", type:"Huo Hai"},
      {dir:"Southwest", type:"Wu Gui"},
      {dir:"West", type:"Liu Sha"},
      {dir:"Northeast", type:"Jue Ming"}
    ]
  },
  6: {
    name: "Qian (乾) — Heaven",
    group: "West Group",
    lucky: [
      {dir:"West", type:"Sheng Chi"},
      {dir:"Northeast", type:"Tian Yi"},
      {dir:"Southwest", type:"Nian Yan"},
      {dir:"Northwest", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"Southeast", type:"Huo Hai"},
      {dir:"East", type:"Wu Gui"},
      {dir:"North", type:"Liu Sha"},
      {dir:"South", type:"Jue Ming"}
    ]
  },
  7: {
    name: "Dui (兑) — Lake",
    group: "West Group",
    lucky: [
      {dir:"Northwest", type:"Sheng Chi"},
      {dir:"Southwest", type:"Tian Yi"},
      {dir:"Northeast", type:"Nian Yan"},
      {dir:"West", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"North", type:"Huo Hai"},
      {dir:"South", type:"Wu Gui"},
      {dir:"Southeast", type:"Liu Sha"},
      {dir:"East", type:"Jue Ming"}
    ]
  },
  8: {
    name: "Gen (艮) — Mountain",
    group: "West Group",
    lucky: [
      {dir:"Southwest", type:"Sheng Chi"},
      {dir:"Northwest", type:"Tian Yi"},
      {dir:"West", type:"Nian Yan"},
      {dir:"Northeast", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"South", type:"Huo Hai"},
      {dir:"North", type:"Wu Gui"},
      {dir:"East", type:"Liu Sha"},
      {dir:"Southeast", type:"Jue Ming"}
    ]
  },
  9: {
    name: "Li (离) — Fire",
    group: "East Group",
    lucky: [
      {dir:"East", type:"Sheng Chi"},
      {dir:"Southeast", type:"Tian Yi"},
      {dir:"North", type:"Nian Yan"},
      {dir:"South", type:"Fu Wei"}
    ],
    unlucky: [
      {dir:"Northeast", type:"Huo Hai"},
      {dir:"West", type:"Wu Gui"},
      {dir:"Southwest", type:"Liu Sha"},
      {dir:"Northwest", type:"Jue Ming"}
    ]
  }
};

function calcKua() {
  const errEl = document.getElementById('kua-error');
  const resultEl = document.getElementById('kua-result');
  errEl.style.display = 'none';
  resultEl.classList.remove('show');

  const year = parseInt(document.getElementById('kua-year').value);
  const gender = document.getElementById('kua-gender').value;

  if (!year || year < 1900 || year > 2030) {
    errEl.textContent = 'Please enter a valid birth year (1900-2030).';
    errEl.style.display = 'block';
    return;
  }
  if (!gender) {
    errEl.textContent = 'Please select your gender.';
    errEl.style.display = 'block';
    return;
  }

  // Sum digits until single digit
  let sum = year.toString().split('').reduce((a,b) => a + parseInt(b), 0);
  while (sum > 9) {
    sum = sum.toString().split('').reduce((a,b) => a + parseInt(b), 0);
  }

  let kua;
  if (gender === 'male') {
    kua = year >= 2000 ? (9 - sum === 0 ? 9 : 9 - sum) : (11 - sum === 0 ? 9 : 11 - sum);
  } else {
    kua = year >= 2000 ? (6 + sum > 9 ? (6 + sum) % 9 : 6 + sum) : (4 + sum > 9 ? (4 + sum) % 9 : 4 + sum);
  }

  // Kua 5 → 2 for male, 8 for female
  if (kua === 5) kua = gender === 'male' ? 2 : 8;
  if (kua === 0) kua = 9;

  const data = KUA_DATA[kua];
  if (!data) {
    errEl.textContent = 'Calculation error. Please try again.';
    errEl.style.display = 'block';
    return;
  }

  resultEl.innerHTML = `
    <div class="kua-number">${kua}</div>
    <div class="kua-group"><strong>${data.name}</strong> · ${data.group}</div>

    <h4 style="color:#4caf50;margin:1rem 0 0.5rem;">🍀 Your Lucky Directions</h4>
    <div class="dir-grid">
      ${data.lucky.map(d => 
        `<div class="dir-card lucky">
          <div class="dir-name">${d.dir}</div>
          <div class="dir-type">${d.type}</div>
        </div>`
      ).join('')}
    </div>

    <h4 style="color:#f44336;margin:1.2rem 0 0.5rem;">⚠️ Your Unlucky Directions</h4>
    <div class="dir-grid">
      ${data.unlucky.map(d => 
        `<div class="dir-card unlucky">
          <div class="dir-name">${d.dir}</div>
          <div class="dir-type">${d.type}</div>
        </div>`
      ).join('')}
    </div>

    <div style="margin-top:1.2rem;padding:0.8rem;background:#1a1025;border-radius:8px;font-size:0.9rem;color:#a89878;">
      <strong>💡 How to use this:</strong> Face your <span style="color:#4caf50;">Sheng Chi</span> direction when working or sleeping. 
      Avoid facing your <span style="color:#f44336;">Jue Ming</span> direction.
      Place your bed's headboard toward your best direction.
    </div>
  `;
  resultEl.classList.add('show');
}

// Enter key support
document.getElementById('kua-year').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') calcKua();
});
</script>
