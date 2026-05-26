---
title: "Bagua Map Overlay — Map Your Home's Energy Zones"
description: "Interactive Bagua Map tool. Overlay the Feng Shui energy map on your floor plan and get personalized zone-by-zone recommendations. Free, no signup."
date: "2026-05-26"
type: "tool"
layout: "tool"
slug: "bagua-map-overlay"
---

<style>
.bagua-tool { max-width: 720px; margin: 0 auto; font-family: system-ui, sans-serif; }
.bagua-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; margin-bottom: 1.5rem; }
.bagua-cell {
  padding: 0.8rem 0.5rem; border-radius: 10px; text-align: center; cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s; min-height: 90px;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  background: #1a1025; border: 2px solid #2a1f3d;
}
.bagua-cell:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(201,168,76,0.2); border-color: #c9a84c55; }
.bagua-cell .zone-name { font-size: 0.9rem; font-weight: 700; color: #c9a84c; margin-bottom: 0.3rem; }
.bagua-cell .zone-dir { font-size: 0.7rem; color: #a89878; }
.bagua-cell .zone-element { font-size: 0.7rem; color: #7e8a9a; margin-top: 0.1rem; }
.bagua-cell .room-select { 
  margin-top: 0.4rem; padding: 0.3rem 0.4rem; background: #0d0820; color: #a89878; 
  border: 1px solid #2a1f3d; border-radius: 4px; font-size: 0.7rem; width: 90%; cursor: pointer;
}
.bagua-cell .room-select:focus { border-color: #c9a84c; outline: none; }

/* Modal */
.bagua-modal-overlay {
  display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.75); z-index: 1000; justify-content: center; align-items: center;
}
.bagua-modal-overlay.show { display: flex; }
.bagua-modal {
  background: linear-gradient(135deg, #1a1025, #2a1f3d); border: 1px solid #c9a84c55;
  border-radius: 12px; padding: 1.5rem; max-width: 500px; width: 90%; max-height: 80vh;
  overflow-y: auto; position: relative;
}
.bagua-modal h3 { color: #c9a84c; margin-top: 0; font-size: 1.2rem; }
.bagua-modal .close-btn {
  position: absolute; top: 8px; right: 12px; background: none; border: none;
  color: #a89878; font-size: 1.5rem; cursor: pointer; padding: 0; line-height: 1;
}
.bagua-modal .close-btn:hover { color: #c9a84c; }
.bagua-modal .do-dont { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-top: 0.8rem; }
.bagua-modal .do-box { padding: 0.6rem; border-radius: 6px; font-size: 0.85rem; }
.bagua-modal .do-box.do { background: #1a3020; border: 1px solid #2d8a4e44; }
.bagua-modal .do-box.do h4 { color: #4caf50; margin: 0 0 0.3rem; font-size: 0.9rem; }
.bagua-modal .do-box.dont { background: #301a1a; border: 1px solid #8a2d2d44; }
.bagua-modal .do-box.dont h4 { color: #f44336; margin: 0 0 0.3rem; font-size: 0.9rem; }
.bagua-modal ul { margin: 0; padding-left: 1.2rem; font-size: 0.82rem; color: #a89878; }
.bagua-modal li { margin-bottom: 0.2rem; }
.bagua-modal .room-warning { 
  margin-top: 0.8rem; padding: 0.6rem; background: #2a1515; border-radius: 6px;
  border-left: 3px solid #f44336; font-size: 0.85rem; color: #f4a4a4; display: none;
}
.cta-box { margin-top: 2rem; padding: 1.2rem; background: #1a1025; border-radius: 8px; border: 1px dashed #c9a84c55; text-align: center; }
.cta-box a { color: #c9a84c; font-weight: 600; }
</style>

<div class="bagua-tool">
  <p style="color:#a89878;margin-bottom:1.2rem;">
    The <strong>Bagua Map</strong> (八卦) divides your space into 9 energy zones — each linked to a life area.
    Stand at your front door looking <strong>inward</strong>. The grid below shows what each zone controls and what to place there.
    <strong>Select room types below each zone for specific advice.</strong>
  </p>

  <div id="bagua-grid" class="bagua-grid"></div>

  <div class="cta-box">
    <p style="margin:0 0 0.5rem;"><strong>Want to activate your Bagua?</strong> Crystals, plants, and mirrors for every zone.</p>
    <a href="/reviews/fengshui-world/">Shop Feng Shui World → 500+ items, 35% commission</a>
  </div>
</div>

<!-- Modal -->
<div id="bagua-modal" class="bagua-modal-overlay" onclick="closeModal(event)">
  <div class="bagua-modal" onclick="event.stopPropagation()">
    <button class="close-btn" onclick="closeModal()">&times;</button>
    <div id="bagua-modal-content"></div>
  </div>
</div>

<script>
const BAGUA = {
  SE: {
    name:'Wealth & Prosperity', cn:'财富', element:'Wood', color:'Purple/Green/Red',
    dir:'Southeast (Far-Left from door)',
    do:['Healthy plants (jade plant, money tree)','Purple items or amethyst crystals','Small water fountain','Citrine or pyrite','Red envelope with coins'],
    dont:['Clutter or storage','Dead/dying plants','Trash can','Broken items','Bathroom in this zone (washes wealth away)'],
    roomWarnings: {
      bathroom:'⚠️ Bathroom in Wealth zone = money going down the drain. Keep door closed + mirror on outside of door.',
      kitchen:'⚠️ Kitchen fire can burn wealth energy. Add water element (blue) between stove and wealth zone.',
      bedroom:'🟡 OK for bedroom but avoid water features in sleeping area.'
    }
  },
  S: {
    name:'Fame & Reputation', cn:'名声', element:'Fire', color:'Red/Orange/Bright',
    dir:'South (Far-Center from door)',
    do:['Red candles or lamps','Awards, diplomas, achievements on display','Bright lighting','Horse or phoenix imagery','Triangular shapes'],
    dont:['Water features (water puts out fire)','Black or dark blue dominance','Mirrors facing the front door','Clutter','Bathroom'],
    roomWarnings: {
      bathroom:'⚠️ Bathroom in Fame zone = reputation being "flushed." Add red accents and keep extremely clean.',
      kitchen:'✅ Kitchen Fire supports Fame! Perfect placement. Add red accents.',
      bedroom:'🟡 Acceptable. Add red throw pillows or a red lamp for activation.'
    }
  },
  SW: {
    name:'Love & Relationships', cn:'爱情', element:'Earth', color:'Pink/Red/White',
    dir:'Southwest (Far-Right from door)',
    do:['Pairs of items (2 candles, 2 pillows)','Rose quartz crystals','Pink or red decor','Photos of happy couples','Round/oval shapes'],
    dont:['Single-person photos','Sharp or pointed objects','Electronics/TV','Exercise equipment','Green plants (Wood weakens Earth)'],
    roomWarnings: {
      bathroom:'⚠️ Bathroom in Love zone drains relationship energy. Keep door closed, add pink towels.',
      kitchen:'⚠️ Fire burns Earth. Add clay/ceramic items to buffer.',
      bedroom:'✅ GREAT placement. This is ideal for master bedroom — enhances intimacy.'
    }
  },
  E: {
    name:'Family & Health', cn:'家庭', element:'Wood', color:'Green/Brown/Blue',
    dir:'East (Middle-Left from door)',
    do:['Wooden furniture','Family photos','Healthy green plants','Blue accent colors','Rectangular shapes'],
    dont:['Too much metal/white decor','Dead plants','Clutter','Sharp objects','Fire elements in excess'],
    roomWarnings: {
      kitchen:'⚠️ Kitchen (Fire) in Family/Health zone — Fire burns Wood. Add green plants to buffer.',
      bathroom:'⚠️ Bathroom = draining family health. Add plants and keep door closed.',
      bedroom:'✅ Good for children\'s bedroom. Use wooden bed frame.'
    }
  },
  C: {
    name:'Health & Center', cn:'健康', element:'Earth', color:'Yellow/Earth tones',
    dir:'Center of home',
    do:['Open space — don\'t block the center','Yellow or earth-tone decor','Ceramic or clay items','Square shapes','Crystal cluster'],
    dont:['Staircase in center (energy rushes up/down)','Bathroom in center','Heavy furniture blocking flow','Dark/unlit center','Too much wood'],
    roomWarnings: {
      bathroom:'⚠️ Bathroom in center = serious health drain. Keep sparkling clean + add earth-colored decor.',
      staircase:'⚠️ Staircase in center disrupts entire home energy. Add crystals at base + hang crystal above.',
    }
  },
  W: {
    name:'Children & Creativity', cn:'子女', element:'Metal', color:'White/Silver/Gold',
    dir:'West (Middle-Right from door)',
    do:['Metal decor (brass, silver, gold)','Circular/round shapes','Art supplies and creative tools','White color scheme','Wind chimes (metal)'],
    dont:['Fire elements (red/orange excessive)','Sharp knives or weapons decor','Clutter','Brown/earth dominance','Broken electronics'],
    roomWarnings: {
      kitchen:'⚠️ Kitchen Fire melts Metal. Add metal utensils display or white accents to balance.',
      bedroom:'✅ Good for children\'s room. Add metal bed frame + creative art supplies.',
    }
  },
  NE: {
    name:'Knowledge & Wisdom', cn:'知识', element:'Earth', color:'Blue/Green/Black',
    dir:'Northeast (Near-Left from door)',
    do:['Books and study materials','Blue or green decor','Quiet meditation corner','Good lighting for reading','Globe or world map'],
    dont:['TV or gaming consoles','Loud speakers','Clutter','Too much white/metal','Distracting decor'],
    roomWarnings: {
      bedroom:'✅ Excellent study-bedroom placement. Desk facing NE boosts concentration.',
      bathroom:'⚠️ Bathroom drains knowledge energy. Add blue decor + keep immaculate.',
    }
  },
  N: {
    name:'Career & Life Path', cn:'事业', element:'Water', color:'Black/Dark Blue',
    dir:'North (Near-Center from door)',
    do:['Water feature or fountain','Black or dark blue decor','Mirrors','Wavy/curvy shapes','Vision board or career goals display'],
    dont:['Earth tones dominance (blocks water)','Clutter blocking flow','Brown/yellow excess','Dead plants','Stagnant water'],
    roomWarnings: {
      bathroom:'✅ Water in Career zone is harmonious! Keep clean and flowing.',
      kitchen:'⚠️ Kitchen Fire vs Career Water = conflict. Add black/blue between them.',
      bedroom:'🟡 Acceptable. Add black throw pillows or a small water feature for activation.'
    }
  },
  NW: {
    name:'Travel & Helpful People', cn:'贵人', element:'Metal', color:'Gray/Silver/White',
    dir:'Northwest (Near-Right from door)',
    do:['Gray or silver decor','Travel souvenirs','World map or globe','Metal picture frames','Photos of mentors'],
    dont:['Red or fire elements excess','Clutter','Broken items','Darkness','Too many plants'],
    roomWarnings: {
      kitchen:'⚠️ Fire weakens Metal. Add gray/silver items + avoid red in this zone.',
      bedroom:'✅ Good for guest room — enhances helpful visitor energy.',
    }
  }
};

const ROOMS = ['-- Room Type --','Bedroom','Living Room','Kitchen','Bathroom','Home Office','Dining Room','Hallway','Storage','Empty/Open'];

const GRID_ORDER = ['SE','S','SW','E','C','W','NE','N','NW'];

function renderGrid() {
  const grid = document.getElementById('bagua-grid');
  grid.innerHTML = GRID_ORDER.map(pos => {
    if (pos === 'C') {
      const d = BAGUA['C'];
      return `<div class="bagua-cell" style="grid-column:2;grid-row:2" onclick="openModal('C')">
        <div class="zone-name">${d.name}</div><div class="zone-dir">Center</div>
        <div class="zone-element">Element: ${d.element}</div>
      </div>`;
    }
    const d = BAGUA[pos];
    return `<div class="bagua-cell" onclick="openModal('${pos}')">
      <div class="zone-name">${d.name}</div><div class="zone-dir">${pos} · ${d.element}</div>
      <select class="room-select" onclick="event.stopPropagation()" onchange="updateRoom('${pos}', this.value)" id="room-${pos}">
        ${ROOMS.map(r => `<option>${r}</option>`).join('')}
      </select>
    </div>`;
  }).join('');
}

function openModal(pos) {
  const d = BAGUA[pos];
  const posName = pos === 'C' ? 'Center' : pos;
  const room = document.getElementById(`room-${pos}`)?.value || '';

  let roomWarning = '';
  if (room && room !== '-- Room Type --' && room !== 'Empty/Open') {
    const w = d.roomWarnings?.[room.toLowerCase().replace(' ','')];
    if (w) roomWarning = w;
    else if (room === 'Bathroom') roomWarning = '⚠️ Bathroom in this zone may need extra remedies. Keep door closed and space immaculate.';
  }

  document.getElementById('bagua-modal-content').innerHTML = `
    <h3>${posName} — ${d.name} (${d.cn})</h3>
    <p style="color:#a89878;font-size:0.9rem;margin:0.3rem 0">📍 ${d.dir} | 🎨 Colors: ${d.color} | Element: ${d.element}</p>
    
    <div class="do-dont">
      <div class="do-box do">
        <h4>✅ Place Here</h4>
        <ul>${d.do.map(i => `<li>${i}</li>`).join('')}</ul>
      </div>
      <div class="do-box dont">
        <h4>❌ Avoid</h4>
        <ul>${d.dont.map(i => `<li>${i}</li>`).join('')}</ul>
      </div>
    </div>
    ${roomWarning ? `<div class="room-warning" style="display:block">${roomWarning}</div>` : ''}
    <p style="margin-top:1rem;font-size:0.85rem;"><a href="/reviews/fengshui-world/" style="color:#c9a84c;">🛒 Get ${d.element} element items at Feng Shui World</a></p>
  `;
  document.getElementById('bagua-modal').classList.add('show');
}

function updateRoom(pos, room) {
  if (room !== '-- Room Type --') {
    openModal(pos);
  }
}

function closeModal(e) {
  if (e && e.target !== document.getElementById('bagua-modal')) return;
  document.getElementById('bagua-modal').classList.remove('show');
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.getElementById('bagua-modal').classList.remove('show');
  }
});

renderGrid();
</script>
