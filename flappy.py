import streamlit as st
import json
import random

st.set_page_config(page_title="🐍 Snake", layout="centered")

# ── Embed the entire game as a self-contained HTML/JS widget ──────────────────
GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0a0a0f;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Share Tech Mono', monospace;
    color: #e0e0e0;
  }

  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 0.18em;
    background: linear-gradient(90deg, #00ff88, #00cfff, #ff4fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    text-shadow: none;
  }

  #scoreboard {
    display: flex;
    gap: 2.5rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    letter-spacing: 0.12em;
  }
  .score-item { display: flex; flex-direction: column; align-items: center; }
  .score-label { color: #666; font-size: 0.7rem; text-transform: uppercase; }
  .score-value { color: #00ff88; font-size: 1.4rem; font-weight: bold; }
  #best-value { color: #ffd700; }

  #arena {
    position: relative;
    border: 2px solid #1a1a2e;
    border-radius: 4px;
    box-shadow:
      0 0 0 1px #0d0d1a,
      0 0 40px rgba(0,255,136,0.08),
      inset 0 0 60px rgba(0,0,0,0.6);
    background: #080810;
  }

  canvas { display: block; border-radius: 2px; }

  /* scanline overlay */
  #arena::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.08) 2px,
      rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    border-radius: 2px;
  }

  #overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(8,8,16,0.88);
    border-radius: 2px;
    gap: 1rem;
  }
  #overlay h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    color: #00ff88;
    letter-spacing: 0.15em;
  }
  #overlay p { color: #888; font-size: 0.85rem; letter-spacing: 0.1em; }

  button {
    margin-top: 0.5rem;
    padding: 0.6rem 2rem;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #0a0a0f;
    background: linear-gradient(135deg, #00ff88, #00cfff);
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: transform 0.1s, box-shadow 0.2s;
    box-shadow: 0 0 20px rgba(0,255,136,0.4);
  }
  button:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(0,255,136,0.6); }
  button:active { transform: scale(0.97); }

  #controls {
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #444;
    letter-spacing: 0.08em;
  }
  #controls span { color: #00ff88; }

  /* D-pad for mobile */
  #dpad {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(3, 44px);
    grid-template-rows: repeat(3, 44px);
    gap: 4px;
  }
  .dp {
    background: #111122;
    border: 1px solid #222240;
    border-radius: 6px;
    color: #00ff88;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    user-select: none;
    transition: background 0.1s;
  }
  .dp:active { background: #1a1a3a; }
  .dp-blank { background: transparent; border: none; cursor: default; }
</style>
</head>
<body>

<h1>SNAKE</h1>

<div id="scoreboard">
  <div class="score-item">
    <span class="score-label">Score</span>
    <span class="score-value" id="score-value">0</span>
  </div>
  <div class="score-item">
    <span class="score-label">Level</span>
    <span class="score-value" id="level-value">1</span>
  </div>
  <div class="score-item">
    <span class="score-label">Best</span>
    <span class="score-value" id="best-value">0</span>
  </div>
</div>

<div id="arena">
  <canvas id="c"></canvas>
  <div id="overlay">
    <h2>READY?</h2>
    <p>USE ARROW KEYS OR WASD</p>
    <button id="start-btn">START GAME</button>
  </div>
</div>

<div id="controls">
  <span>↑↓←→</span> or <span>WASD</span> &nbsp;|&nbsp;
  <span>P</span> pause &nbsp;|&nbsp;
  <span>R</span> restart
</div>

<!-- Mobile d-pad -->
<div id="dpad">
  <div class="dp-blank"></div>
  <div class="dp" id="dp-up">▲</div>
  <div class="dp-blank"></div>
  <div class="dp" id="dp-left">◀</div>
  <div class="dp-blank"></div>
  <div class="dp" id="dp-right">▶</div>
  <div class="dp-blank"></div>
  <div class="dp" id="dp-down">▼</div>
  <div class="dp-blank"></div>
</div>

<script>
const COLS = 25, ROWS = 25, CELL = 22;
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
canvas.width  = COLS * CELL;
canvas.height = ROWS * CELL;
document.getElementById('arena').style.width  = canvas.width  + 'px';
document.getElementById('arena').style.height = canvas.height + 'px';

// ── Palette ──────────────────────────────────────────────────────────────────
const SNAKE_PALETTES = [
  ['#00ff88','#00dd70','#00bb58'],
  ['#00cfff','#00aadd','#0088bb'],
  ['#ff4fff','#dd00dd','#aa00aa'],
  ['#ffdd00','#ffbb00','#ff8800'],
];
const FOOD_COLORS  = ['#ff4757','#ff6b81','#ff4fff','#ffd700','#00cfff'];
const BONUS_COLORS = ['#ffd700','#fff176','#ffecb3'];
let palette = SNAKE_PALETTES[0];

// ── State ────────────────────────────────────────────────────────────────────
let snake, dir, nextDir, food, bonus, score, best = 0, level, speed, loop, paused, running;

function rand(n) { return Math.floor(Math.random() * n); }

function newFood(occupied) {
  let pos;
  do { pos = { x: rand(COLS), y: rand(ROWS) }; }
  while (occupied.some(s => s.x === pos.x && s.y === pos.y));
  pos.color = FOOD_COLORS[rand(FOOD_COLORS.length)];
  pos.pulse = 0;
  return pos;
}

function init() {
  clearInterval(loop);
  palette = SNAKE_PALETTES[rand(SNAKE_PALETTES.length)];
  snake = [{ x: 12, y: 12 }, { x: 11, y: 12 }, { x: 10, y: 12 }];
  dir = { x: 1, y: 0 };
  nextDir = { x: 1, y: 0 };
  food = newFood(snake);
  bonus = null;
  score = 0;
  level = 1;
  speed = 145;
  paused = false;
  running = true;
  document.getElementById('overlay').style.display = 'none';
  updateHUD();
  startLoop();
}

function startLoop() {
  clearInterval(loop);
  loop = setInterval(tick, speed);
}

function setSpeed(s) {
  speed = s;
  startLoop();
}

// ── Game tick ────────────────────────────────────────────────────────────────
function tick() {
  if (paused || !running) return;
  dir = { ...nextDir };

  const head = { x: (snake[0].x + dir.x + COLS) % COLS,
                  y: (snake[0].y + dir.y + ROWS) % ROWS };

  // Self-collision
  if (snake.some(s => s.x === head.x && s.y === head.y)) { return gameOver(); }

  snake.unshift(head);

  let grew = false;
  if (head.x === food.x && head.y === food.y) {
    score += level;
    grew = true;
    food = newFood(snake);
    // Spawn bonus every 5 food
    if (score % 5 === 0) {
      bonus = newFood(snake);
      bonus.color = BONUS_COLORS[rand(BONUS_COLORS.length)];
      bonus.isBonus = true;
      bonus.ttl = 60; // ticks
    }
    // Level up every 10 food
    if (score % 10 === 0 && level < 10) {
      level++;
      setSpeed(Math.max(55, speed - 15));
    }
    updateHUD();
  }

  if (bonus) {
    if (head.x === bonus.x && head.y === bonus.y) {
      score += level * 3;
      grew = true;
      bonus = null;
      updateHUD();
    } else {
      bonus.ttl--;
      if (bonus.ttl <= 0) bonus = null;
    }
  }

  if (!grew) snake.pop();
  draw();
}

// ── Draw ─────────────────────────────────────────────────────────────────────
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Grid
  ctx.strokeStyle = 'rgba(255,255,255,0.025)';
  ctx.lineWidth = 0.5;
  for (let x = 0; x <= COLS; x++) {
    ctx.beginPath(); ctx.moveTo(x*CELL,0); ctx.lineTo(x*CELL,canvas.height); ctx.stroke();
  }
  for (let y = 0; y <= ROWS; y++) {
    ctx.beginPath(); ctx.moveTo(0,y*CELL); ctx.lineTo(canvas.width,y*CELL); ctx.stroke();
  }

  // Snake
  snake.forEach((seg, i) => {
    const ratio = i / snake.length;
    const col = lerpColor(palette[0], palette[2], ratio);
    const x = seg.x * CELL, y = seg.y * CELL;
    const r = i === 0 ? 6 : 4;

    // Glow on head
    if (i === 0) {
      ctx.shadowColor = palette[0];
      ctx.shadowBlur = 18;
    } else {
      ctx.shadowBlur = 0;
    }

    roundRect(ctx, x+1, y+1, CELL-2, CELL-2, r, col);

    // Eye on head
    if (i === 0) {
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#0a0a0f';
      const ex = dir.x === 0 ? 0 : dir.x * 5;
      const ey = dir.y === 0 ? 0 : dir.y * 5;
      ctx.beginPath();
      ctx.arc(x + CELL/2 + ex + (dir.y*3), y + CELL/2 + ey - (dir.x*3), 3, 0, Math.PI*2);
      ctx.fill();
      if (dir.x === 0) {
        ctx.beginPath();
        ctx.arc(x + CELL/2 + ex - 4, y + CELL/2 + ey, 3, 0, Math.PI*2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + CELL/2 + ex + 4, y + CELL/2 + ey, 3, 0, Math.PI*2);
        ctx.fill();
      }
    }
  });

  ctx.shadowBlur = 0;

  // Food
  food.pulse = (food.pulse + 0.1) % (Math.PI * 2);
  const fp = 1 + 0.15 * Math.sin(food.pulse);
  drawItem(food, fp, 8);

  // Bonus
  if (bonus) {
    bonus.pulse = ((bonus.pulse || 0) + 0.18) % (Math.PI * 2);
    const bp = 1 + 0.25 * Math.sin(bonus.pulse);
    drawItem(bonus, bp, 10);
    // Flashing TTL warning
    if (bonus.ttl < 20 && Math.floor(bonus.ttl / 4) % 2 === 0) {
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(bonus.x*CELL, bonus.y*CELL, CELL, CELL);
    }
  }
}

function drawItem(item, scale, baseR) {
  const cx = item.x * CELL + CELL/2;
  const cy = item.y * CELL + CELL/2;
  const s = (CELL/2 - 2) * scale;
  ctx.shadowColor = item.color;
  ctx.shadowBlur = 16;
  ctx.fillStyle = item.color;
  ctx.beginPath();
  ctx.arc(cx, cy, s, 0, Math.PI*2);
  ctx.fill();
  ctx.shadowBlur = 0;
  // Shine
  ctx.fillStyle = 'rgba(255,255,255,0.35)';
  ctx.beginPath();
  ctx.arc(cx - s*0.25, cy - s*0.25, s*0.3, 0, Math.PI*2);
  ctx.fill();
}

function roundRect(ctx, x, y, w, h, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, r);
  ctx.fill();
}

function lerpColor(a, b, t) {
  const ah = parseInt(a.slice(1),16), bh = parseInt(b.slice(1),16);
  const ar = (ah>>16)&0xff, ag = (ah>>8)&0xff, ab = ah&0xff;
  const br = (bh>>16)&0xff, bg = (bh>>8)&0xff, bb = bh&0xff;
  const rr = Math.round(ar + (br-ar)*t);
  const rg = Math.round(ag + (bg-ag)*t);
  const rb = Math.round(ab + (bb-ab)*t);
  return `rgb(${rr},${rg},${rb})`;
}

// ── HUD ──────────────────────────────────────────────────────────────────────
function updateHUD() {
  document.getElementById('score-value').textContent = score;
  document.getElementById('level-value').textContent = level;
  if (score > best) best = score;
  document.getElementById('best-value').textContent = best;
}

// ── Game Over ────────────────────────────────────────────────────────────────
function gameOver() {
  running = false;
  clearInterval(loop);
  if (score > best) best = score;
  updateHUD();
  const ov = document.getElementById('overlay');
  ov.innerHTML = `
    <h2>GAME OVER</h2>
    <p>SCORE: ${score} &nbsp;|&nbsp; BEST: ${best}</p>
    <button id="start-btn">PLAY AGAIN</button>
  `;
  ov.style.display = 'flex';
  document.getElementById('start-btn').onclick = init;
}

// ── Controls ─────────────────────────────────────────────────────────────────
const DIRS = {
  ArrowUp:    {x:0,y:-1}, w:{x:0,y:-1},
  ArrowDown:  {x:0,y:1},  s:{x:0,y:1},
  ArrowLeft:  {x:-1,y:0}, a:{x:-1,y:0},
  ArrowRight: {x:1,y:0},  d:{x:1,y:0},
};

document.addEventListener('keydown', e => {
  const k = e.key === e.key.toUpperCase() ? e.key.toLowerCase() : e.key;
  if (DIRS[k]) {
    e.preventDefault();
    const nd = DIRS[k];
    if (nd.x !== -dir.x || nd.y !== -dir.y) nextDir = nd;
  }
  if (k === 'p') { paused = !paused; }
  if (k === 'r') { init(); }
});

document.getElementById('dp-up').onclick    = () => { if (!(-dir.y)) nextDir={x:0,y:-1}; };
document.getElementById('dp-down').onclick  = () => { if (!(dir.y))  nextDir={x:0,y:1};  };
document.getElementById('dp-left').onclick  = () => { if (!(-dir.x)) nextDir={x:-1,y:0}; };
document.getElementById('dp-right').onclick = () => { if (!(dir.x))  nextDir={x:1,y:0};  };

document.getElementById('start-btn').onclick = init;

// Initial draw (empty grid)
ctx.clearRect(0,0,canvas.width,canvas.height);
</script>
</body>
</html>
"""

st.components.v1.html(GAME_HTML, height=720, scrolling=False)

st.markdown(
    "<p style='text-align:center; color:#333; font-size:0.75rem; font-family:monospace; margin-top:0.5rem'>"
    "Arrow keys / WASD to move &nbsp;·&nbsp; P to pause &nbsp;·&nbsp; R to restart"
    "</p>",
    unsafe_allow_html=True,
)