---
title: "2026 Flying Star Chart — Annual Feng Shui Energy Map"
description: "Free 2026 Flying Star (Xuan Kong Fei Xing) calculator. See which areas of your home bring wealth, illness, or conflict this year — and what to do about it."
date: "2026-05-26"
type: "tool"
layout: "tool"
slug: "flying-star-chart"
---

<style>
.fs-tool { max-width: 720px; margin: 0 auto; font-family: system-ui, sans-serif; }
.fs-tool .orient-bar { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1.5rem; justify-content: center; }
.fs-tool .orient-bar button {
  padding: 0.5rem 0.8rem; border: 2px solid #2a1f3d; background: #1a1025; 
  color: #a89878; border-radius: 6px; cursor: pointer; transition: all 0.2s;
  font-size: 0.85rem; font-weight: 600;
}
.fs-tool .orient-bar button.active { border-color: #c9a84c; color: #c9a84c; background: #2a1f3d; }
.fs-tool .orient-bar button:hover { border-color: #c9a84c55; }
.fs-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 1rem; }
.fs-cell { 
  padding: 1rem 0.6rem; border-radius: 10px; text-align: center; cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s; min-height: 80px;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  position: relative;
}
.fs-cell:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
.fs-cell .star-num { font-size: 2rem; font-weight: 900; line-height: 1; }
.fs-cell .star-element { font-size: 0.75rem; opacity: 0.8; margin-top: 0.2rem; }
.fs-cell .star-dir { font-size: 0.65rem; opacity: 0.5; position: absolute; top: 4px; right: 6px; }
.fs-cell.lucky { background: linear-gradient(135deg, #1a3020, #0d2010); border: 1px solid #2d8a4e55; }
.fs-cell.lucky .star-num { color: #4caf50; }
.fs-cell.very-lucky { background: linear-gradient(135deg, #1a2a20, #153015); border: 1px solid #c9a84c55; }
.fs-cell.very-lucky .star-num { color: #c9a84c; }
.fs-cell.neutral { background: linear-gradient(135deg, #1a1a25, #15152a); border: 1px solid #3a3a5a55; }
.fs-cell.neutral .star-num { color: #7e8a9a; }
.fs-cell.unlucky { background: linear-gradient(135deg, #2a1515, #1a1010); border: 1px solid #8a2d2d44; }
.fs-cell.unlucky .star-num { color: #f44336; }
.fs-cell.worst { background: linear-gradient(135deg, #301010, #1a0808); border: 1px solid #ff000044; animation: pulse-danger 2s infinite; }
.fs-cell.worst .star-num { color: #ff1744; }
@keyframes pulse-danger { 0%,100%{box-shadow:0 0 5px #f4433644} 50%{box-shadow:0 0 15px #f44336}} 
.fs-detail { 
  display: none; padding: 1.5rem; margin-top: 1rem; border-radius: 10px;
  background: #1a1025; border: 1px solid #c9a84c33; 
}
.fs-detail.show { display: block; }
.fs-detail h3 { color: #c9a84c; margin-top: 0; }
.fs-detail .fs-remedy { 
  margin-top: 0.8rem; padding: 0.8rem; background: #0d0820; border-radius: 6px;
  font-size: 0.9rem; color: #a89878;
}
.cta-box { margin-top: 2rem; padding: 1.2rem; background: #1a1025; border-radius: 8px; border: 1px dashed #c9a84c55; text-align: center; }
.cta-box a { color: #c9a84c; font-weight: 600; }
</style>

<div class="fs-tool">
  <p style="color:#a89878;margin-bottom:1.2rem;">
    The <strong>Xuan Kong Flying Star</strong> chart shows how energy shifts through your home each year. 
    2026 is a <strong>Bing Wu (丙午) Fire Horse</strong> year in <strong>Period 9</strong>.
    Select your home's facing direction to see which areas bring fortune — and which need remedies.
  </p>

  <div class="orient-bar" id="orient-bar">
    <button onclick="rotateFacing('N')">N ↑</button>
    <button onclick="rotateFacing('NE')">NE ↗</button>
    <button onclick="rotateFacing('E')">E →</button>
    <button onclick="rotateFacing('SE')">SE ↘</button>
    <button onclick="rotateFacing('S')" class="active">S ↓</button>
    <button onclick="rotateFacing('SW')">SW ↙</button>
    <button onclick="rotateFacing('W')">W ←</button>
    <button onclick="rotateFacing('NW')">NW ↖</button>
  </div>

  <div id="fs-grid" class="fs-grid"></div>
  <div id="fs-detail" class="fs-detail"></div>

  <div class="cta-box">
    <p style="margin:0 0 0.5rem;">🔮 <strong>Need remedies?</strong> Crystals, Bagua mirrors, and wind chimes for every Flying Star.</p>
    <a href="/best/feng-shui-products-home/">Shop Feng Shui Mall → 10% commission + 180-day cookie, authentic Feng Shui products</a>
  </div>
</div>

<script>
// 2026 Annual Flying Star (Period 9, Bing Wu year)
// Layout: palace positions in compass order (when facing South)
const BASE_CHART = {
  SE: {star:3, element:'Wood', luck:'unlucky', name:'三碧禄存 (Quarrel Star)', 
        advice:'🔥 Use red items, candles, or lamps. Avoid green/wood decor. Fire weakens Wood. Place red rug or red curtain.', 
        aff:'quarrel'},
  S:  {star:2, element:'Earth', luck:'unlucky', name:'二黑巨门 (Illness Star)',
        advice:'🪙 Place 6 metal coins or metal wind chimes here. Metal drains Earth. Avoid red/fire colors. White/gold is protective.',
        aff:'illness'},
  SW: {star:7, element:'Metal', luck:'unlucky', name:'七赤破军 (Robbery Star)',
        advice:'💧 Add water element — blue/black colors, small fountain. Water drains Metal. Avoid sharp metal objects.',
        aff:'robbery'},
  E:  {star:5, element:'Earth', luck:'worst', name:'五黄廉贞 (Five Yellow — Disaster)',
        advice:'🔔 <strong>CRITICAL:</strong> Hang 6-rod metal wind chime. Use white/gold colors. NO renovations here in 2026. Metal drains the 5 Yellow. Salt water cure recommended.',
        aff:'disaster'},
  C:  {star:9, element:'Fire', luck:'very-lucky', name:'九紫右弼 (Joy & Celebration)',
        advice:'🌱 Keep this area bright and active. Purple, red, and green enhance the energy. Perfect for living room or main gathering space.',
        aff:'joy'},
  W:  {star:1, element:'Water', luck:'lucky', name:'一白贪狼 (Future Prosperity)',
        advice:'🌊 Water features, mirrors, and blue/black colors enhance. Good for career and romance in 2026. Avoid messy clutter.',
        aff:'prosperity'},
  NE: {star:6, element:'Metal', luck:'neutral', name:'六白武曲 (Authority Star)',
        advice:'📚 Great for home office. Add crystals (clear quartz, amethyst). Avoid red/fire. Earth tones support Metal.',
        aff:'authority'},
  N:  {star:4, element:'Wood', luck:'neutral', name:'四绿文曲 (Study & Romance)',
        advice:'📖 Perfect study/reading area. Add plants, green, and blue. Wood element supports learning. Place desk facing this direction.',
        aff:'study'},
  NW: {star:8, element:'Earth', luck:'very-lucky', name:'八白左辅 (Wealth Star — BEST)',
        advice:'💰 <strong>BEST AREA OF 2026!</strong> Place wealth ship, citrine, jade plant here. Keep active (not bedroom). Use red/purple to activate Earth. This is your money spot.',
        aff:'wealth'}
};

// Compass ordering for each facing direction
const ROTATIONS = {
  'S':  ['SE','S','SW','E','C','W','NE','N','NW'],
  'N':  ['NW','N','NE','W','C','E','SW','S','SE'],
  'E':  ['NE','E','SE','N','C','S','NW','W','SW'],
  'W':  ['SW','W','NW','S','C','N','SE','E','NE'],
  'SE': ['E','SE','S','NE','C','SW','N','NW','W'],
  'SW': ['S','SW','W','SE','C','NW','E','NE','N'],
  'NE': ['N','NE','E','NW','C','SE','W','SW','S'],
  'NW': ['W','NW','N','SW','C','NE','S','SE','E']
};

let currentFacing = 'S';

function rotateFacing(dir) {
  currentFacing = dir;
  document.querySelectorAll('#orient-bar button').forEach(b => b.classList.remove('active'));
  document.querySelector(`#orient-bar button[onclick="rotateFacing('${dir}')"]`).classList.add('active');
  renderGrid();
  document.getElementById('fs-detail').classList.remove('show');
}

function renderGrid() {
  const grid = document.getElementById('fs-grid');
  const order = ROTATIONS[currentFacing];
  grid.innerHTML = order.map(pos => {
    if (pos === 'C') {
      return `<div class="fs-cell neutral" style="grid-column:2;grid-row:2" onclick="showDetail('C')">
        <div class="star-num">9</div><div class="star-element">Fire</div><div class="star-dir">Center</div></div>`;
    }
    const d = BASE_CHART[pos];
    return `<div class="fs-cell ${d.luck}" onclick="showDetail('${pos}')">
      <div class="star-dir">${pos}</div>
      <div class="star-num">${d.star}</div>
      <div class="star-element">${d.element}</div>
    </div>`;
  }).join('');
}

function showDetail(pos) {
  const d = BASE_CHART[pos];
  if (!d) return;
  const detail = document.getElementById('fs-detail');
  const posName = pos === 'C' ? 'Center' : pos;
  detail.innerHTML = `
    <h3>${posName} — Star ${d.star}: ${d.name}</h3>
    <p style="color:#a89878;margin-bottom:0.5rem">Element: <strong>${d.element}</strong> | Rating: <strong style="color:${d.luck==='very-lucky'?'#c9a84c':d.luck==='lucky'?'#4caf50':d.luck==='worst'?'#ff1744':'#f44336'}">${
      d.luck==='very-lucky'?'⭐⭐⭐⭐⭐':d.luck==='lucky'?'⭐⭐⭐⭐':d.luck==='neutral'?'⭐⭐⭐':d.luck==='unlucky'?'⭐⭐':'⭐'
    }</strong></p>
    <div class="fs-remedy">${d.advice}</div>
    <p style="margin-top:0.8rem;font-size:0.85rem;">
      <a href="/best/feng-shui-products-home/" style="color:#c9a84c;">🛒 Get ${d.aff} remedies at Feng Shui Mall (10% commission + 180-day cookie)</a>
    </p>
  `;
  detail.classList.add('show');
}

// Initial render
renderGrid();
</script>
