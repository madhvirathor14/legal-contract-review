"""
FastAPI application — Legal Contract Review Environment.
OpenEnv-compliant endpoints: /reset, /step, /state
Plus a stunning visual dashboard at GET /
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from models import (
    ResetRequest, ContractAction, StepResult, StateResponse,
    TaskName, ContractObservation
)
from env import LegalContractEnv

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────

app = FastAPI(
    title="Legal Contract Review — OpenEnv",
    description=(
        "An OpenEnv-compliant RL environment where AI agents review legal contracts. "
        "Agents identify missing clauses, detect one-sided terms, and rewrite ambiguous language."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single global environment instance
env = LegalContractEnv()


# ─────────────────────────────────────────────
# OpenEnv Required Endpoints
# ─────────────────────────────────────────────

@app.post("/reset", response_model=StepResult)
async def reset(request: ResetRequest = None):
    """Start a new episode. Optionally specify task and seed."""
    if request is None:
        request = ResetRequest()
    return env.reset(request)


@app.post("/step", response_model=StepResult)
async def step(action: ContractAction):
    """Submit an agent action and receive reward + new observation."""
    try:
        return env.step(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state", response_model=StepResult)
async def state():
    """Get current environment state without advancing."""
    return env.get_state()


@app.get("/tasks")
async def list_tasks():
    """List all available tasks with metadata."""
    return {
        "tasks": [
            {
                "name": TaskName.FIND_MISSING_CLAUSES.value,
                "difficulty": "easy",
                "description": "Find all missing standard clauses in a contract",
                "max_steps": 3,
                "reward_type": "partial_credit",
            },
            {
                "name": TaskName.IDENTIFY_RISKY_PARTY.value,
                "difficulty": "medium",
                "description": "Identify which party is disadvantaged by a flagged clause",
                "max_steps": 2,
                "reward_type": "binary_with_bonus",
            },
            {
                "name": TaskName.REWRITE_AMBIGUOUS.value,
                "difficulty": "hard",
                "description": "Rewrite an ambiguous clause to be legally sound and enforceable",
                "max_steps": 1,
                "reward_type": "multi_criteria",
            },
        ]
    }


@app.get("/health")
async def health():
    return {"status": "ok", "env": "legal-contract-review", "version": "1.0.0"}


# ─────────────────────────────────────────────
# Dashboard UI
# ─────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚖️ Legal Contract Review — OpenEnv</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=JetBrains+Mono:wght@300;400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg:       #08090e;
  --surface:  #0e1018;
  --surface2: #13151f;
  --border:   #1e2133;
  --border2:  #2a2d40;
  --gold:     #c9a84c;
  --gold2:    #e8c96a;
  --gold-dim: rgba(201,168,76,0.12);
  --text:     #e8e8ee;
  --muted:    #6b6e87;
  --green:    #3ddc84;
  --green-dim:rgba(61,220,132,0.1);
  --red:      #ff4d6d;
  --red-dim:  rgba(255,77,109,0.1);
  --blue:     #5b8af5;
  --blue-dim: rgba(91,138,245,0.1);
  --amber:    #f5a623;
  --amber-dim:rgba(245,166,35,0.1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Noise texture overlay ── */
body::after {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
  pointer-events: none; z-index: 999; opacity: 0.6;
}

/* ── Top glow line ── */
body::before {
  content: '';
  position: fixed; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  z-index: 100;
}

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 40px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  position: sticky; top: 0; z-index: 50;
  backdrop-filter: blur(12px);
}

.header-left {
  display: flex; align-items: center; gap: 16px;
}

.logo-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  box-shadow: 0 0 20px rgba(201,168,76,0.25);
  animation: logoGlow 3s ease-in-out infinite;
}

@keyframes logoGlow {
  0%, 100% { box-shadow: 0 0 20px rgba(201,168,76,0.25); }
  50% { box-shadow: 0 0 30px rgba(201,168,76,0.45); }
}

.logo-text h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--text);
}

.logo-text .tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--gold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.header-right {
  display: flex; align-items: center; gap: 20px;
}

.status-live {
  display: flex; align-items: center; gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--green);
}

.pulse-dot {
  width: 7px; height: 7px;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--green);
  animation: livePulse 1.8s ease-in-out infinite;
}

@keyframes livePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 3px;
  border: 1px solid;
}

.badge-gold { color: var(--gold); border-color: rgba(201,168,76,0.4); background: var(--gold-dim); }
.badge-blue { color: var(--blue); border-color: rgba(91,138,245,0.3); background: var(--blue-dim); }

/* ══════════════════════════════════════
   HERO
══════════════════════════════════════ */
.hero {
  padding: 60px 40px 48px;
  border-bottom: 1px solid var(--border);
  position: relative; overflow: hidden;
}

.hero-bg {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 10% 50%, rgba(201,168,76,0.04) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 20%, rgba(91,138,245,0.04) 0%, transparent 60%);
  pointer-events: none;
}

.hero-grid {
  display: grid; grid-template-columns: 1fr auto; gap: 48px;
  align-items: center; position: relative; z-index: 1;
  max-width: 1200px; margin: 0 auto;
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2.2rem, 4vw, 3.6rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 16px;
}

.hero-title em {
  font-style: italic;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 0.95rem;
  color: var(--muted);
  line-height: 1.8;
  max-width: 540px;
  margin-bottom: 28px;
}

.hero-stats {
  display: flex; gap: 32px;
}

.hero-stat-val {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: var(--gold);
  display: block; line-height: 1;
}

.hero-stat-lbl {
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 4px;
}

/* Score ring */
.score-ring-wrap {
  display: flex; flex-direction: column; align-items: center; gap: 12px;
}

.score-ring {
  position: relative; width: 120px; height: 120px;
}

.score-ring svg { transform: rotate(-90deg); }

.score-ring circle {
  fill: none;
  stroke-width: 6;
  stroke-linecap: round;
}

.ring-bg { stroke: var(--border2); }

.ring-fg {
  stroke: var(--gold);
  stroke-dasharray: 339.3;
  stroke-dashoffset: 339.3;
  transition: stroke-dashoffset 0.6s ease;
  filter: drop-shadow(0 0 6px rgba(201,168,76,0.5));
}

.ring-label {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}

.ring-score {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem; font-weight: 700;
  color: var(--gold); line-height: 1;
  transition: all 0.3s;
}

.ring-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.ring-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.1em;
}

/* ══════════════════════════════════════
   TASK CARDS
══════════════════════════════════════ */
.tasks-section {
  padding: 40px;
  border-bottom: 1px solid var(--border);
  max-width: 1200px; margin: 0 auto;
}

.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: 20px;
  display: flex; align-items: center; gap: 10px;
}

.section-label::after {
  content: '';
  flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}

.task-cards {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
}

.task-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  position: relative; overflow: hidden;
  transition: transform 0.2s, border-color 0.2s;
  cursor: pointer;
}

.task-card:hover { transform: translateY(-2px); }

.task-card.easy:hover  { border-color: rgba(61,220,132,0.4); }
.task-card.medium:hover { border-color: rgba(245,166,35,0.4); }
.task-card.hard:hover  { border-color: rgba(255,77,109,0.4); }

.task-card-glow {
  position: absolute; top: -40px; right: -40px;
  width: 120px; height: 120px;
  border-radius: 50%;
  opacity: 0.08;
}

.easy   .task-card-glow { background: var(--green); }
.medium .task-card-glow { background: var(--amber); }
.hard   .task-card-glow { background: var(--red); }

.task-top {
  display: flex; align-items: flex-start;
  justify-content: space-between; margin-bottom: 12px;
}

.task-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}

.easy   .task-icon { background: var(--green-dim); }
.medium .task-icon { background: var(--amber-dim); }
.hard   .task-icon { background: var(--red-dim); }

.diff-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.1em;
  padding: 3px 8px; border-radius: 4px;
}

.easy   .diff-badge { color: var(--green); background: var(--green-dim); border: 1px solid rgba(61,220,132,0.2); }
.medium .diff-badge { color: var(--amber); background: var(--amber-dim); border: 1px solid rgba(245,166,35,0.2); }
.hard   .diff-badge { color: var(--red);   background: var(--red-dim);   border: 1px solid rgba(255,77,109,0.2); }

.task-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem; font-weight: 500;
  color: var(--text); margin-bottom: 8px;
}

.task-desc {
  font-size: 0.82rem; color: var(--muted);
  line-height: 1.6; margin-bottom: 16px;
}

.task-meta {
  display: flex; gap: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: var(--muted);
}

.task-meta span { display: flex; align-items: center; gap: 4px; }

/* ══════════════════════════════════════
   MAIN LAYOUT
══════════════════════════════════════ */
main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 0;
  max-width: 1200px; margin: 0 auto;
  padding: 0 40px 40px;
  margin-top: 32px;
}

.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.panel:nth-child(odd) { margin-right: 10px; }
.panel:nth-child(even) { margin-left: 10px; }
.panel.full-width { grid-column: 1 / -1; margin-right: 0; margin-left: 0; }

.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.01);
}

.panel-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text);
  display: flex; align-items: center; gap: 8px;
}

.panel-title::before {
  content: '';
  width: 3px; height: 14px;
  background: var(--gold);
  border-radius: 2px;
}

.panel-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: var(--muted);
}

.panel-body { padding: 20px; }

/* ── Selector ── */
.form-group { margin-bottom: 16px; }

.form-label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; text-transform: uppercase;
  letter-spacing: 0.1em; color: var(--muted);
  margin-bottom: 6px;
}

select {
  width: 100%;
  background: var(--surface2);
  color: var(--text);
  border: 1px solid var(--border2);
  border-radius: 8px;
  padding: 10px 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b6e87' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

select:focus { border-color: var(--gold); }

/* ── Buttons ── */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 8px; width: 100%; padding: 11px 18px;
  border: none; border-radius: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem; font-weight: 500;
  cursor: pointer; transition: all 0.2s;
  letter-spacing: 0.05em;
  position: relative; overflow: hidden;
}

.btn::after {
  content: '';
  position: absolute; inset: 0;
  background: white;
  opacity: 0;
  transition: opacity 0.2s;
}

.btn:hover::after { opacity: 0.05; }
.btn:active { transform: scale(0.98); }

.btn-gold {
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  color: #0a0a0a;
  box-shadow: 0 4px 16px rgba(201,168,76,0.2);
}

.btn-gold:hover { box-shadow: 0 4px 24px rgba(201,168,76,0.35); }

.btn-green {
  background: var(--green-dim);
  color: var(--green);
  border: 1px solid rgba(61,220,132,0.3);
}

.btn-green:hover { background: rgba(61,220,132,0.18); border-color: rgba(61,220,132,0.5); }

.btn-ghost {
  background: var(--surface2);
  color: var(--muted);
  border: 1px solid var(--border2);
}

.btn-ghost:hover { color: var(--text); border-color: var(--border2); }

.btn-sm {
  font-size: 0.65rem; padding: 5px 12px; width: auto;
}

.btn-gap { height: 10px; }

/* ── Response box ── */
.response-box {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  line-height: 1.7;
  color: var(--muted);
  max-height: 280px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  transition: border-color 0.3s;
}

.response-box.success { border-color: rgba(61,220,132,0.4); color: var(--text); }
.response-box.error   { border-color: rgba(255,77,109,0.4); color: var(--red); }

.response-box::-webkit-scrollbar { width: 4px; }
.response-box::-webkit-scrollbar-track { background: transparent; }
.response-box::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── Episode log ── */
.log-scroll {
  max-height: 220px; overflow-y: auto;
  display: flex; flex-direction: column; gap: 4px;
}

.log-scroll::-webkit-scrollbar { width: 3px; }
.log-scroll::-webkit-scrollbar-thumb { background: var(--border2); }

.log-entry {
  display: flex; gap: 10px; align-items: flex-start;
  padding: 6px 10px;
  border-radius: 6px;
  background: var(--surface2);
  animation: logSlide 0.3s ease;
}

@keyframes logSlide {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

.log-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; font-weight: 500;
  padding: 1px 6px; border-radius: 3px;
  flex-shrink: 0; margin-top: 1px;
}

.tag-reset  { background: var(--blue-dim); color: var(--blue); }
.tag-step   { background: var(--green-dim); color: var(--green); }
.tag-end    { background: var(--gold-dim); color: var(--gold); }
.tag-warn   { background: var(--amber-dim); color: var(--amber); }
.tag-init   { background: rgba(255,255,255,0.04); color: var(--muted); }
.tag-error  { background: var(--red-dim); color: var(--red); }

.log-msg {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem; color: var(--muted);
  line-height: 1.5;
}

/* ── Stats grid ── */
.stats-row {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 12px; margin-bottom: 16px;
}

.stat-box {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  text-align: center;
}

.stat-val {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem; font-weight: 600;
  color: var(--gold); line-height: 1;
  transition: all 0.3s;
  display: block;
}

.stat-lbl {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-top: 4px; display: block;
}

/* ── Endpoints table ── */
.endpoint-list { display: flex; flex-direction: column; gap: 8px; }

.endpoint-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: border-color 0.2s;
}

.endpoint-row:hover { border-color: var(--border2); }

.method-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem; font-weight: 500;
  padding: 2px 8px; border-radius: 3px;
  flex-shrink: 0; min-width: 46px; text-align: center;
}

.m-post { background: var(--blue-dim); color: var(--blue); border: 1px solid rgba(91,138,245,0.25); }
.m-get  { background: var(--green-dim); color: var(--green); border: 1px solid rgba(61,220,132,0.25); }

.ep-path {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem; color: var(--text);
  flex: 1;
}

.ep-desc {
  font-size: 0.75rem; color: var(--muted); flex: 1.5;
}

/* ── Reward bar ── */
.reward-bar-wrap {
  margin: 12px 0;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  height: 6px;
}

.reward-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--gold), var(--gold2));
  width: 0%;
  transition: width 0.5s ease;
  border-radius: 6px;
  box-shadow: 0 0 8px rgba(201,168,76,0.4);
}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
footer {
  border-top: 1px solid var(--border);
  padding: 20px 40px;
  display: flex; align-items: center; justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: var(--muted);
}

.footer-links { display: flex; gap: 24px; }
.footer-links a { color: var(--muted); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: var(--gold); }

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@media (max-width: 900px) {
  .hero-grid  { grid-template-columns: 1fr; }
  .task-cards { grid-template-columns: 1fr; }
  main { grid-template-columns: 1fr; padding: 0 20px 40px; }
  .panel:nth-child(odd), .panel:nth-child(even) { margin: 0 0 16px; }
  header { padding: 14px 20px; }
  .hero  { padding: 40px 20px 32px; }
  .tasks-section { padding: 24px 20px; }
}
</style>
</head>

<body>

<!-- ═══════════ HEADER ═══════════ -->
<header>
  <div class="header-left">
    <div class="logo-icon">⚖️</div>
    <div class="logo-text">
      <h1>Legal Contract Review</h1>
      <div class="tagline">OpenEnv · RL Benchmark · v1.0</div>
    </div>
  </div>
  <div class="header-right">
    <div class="status-live">
      <div class="pulse-dot"></div>
      LIVE
    </div>
    <span class="badge badge-gold">Meta × HuggingFace</span>
    <span class="badge badge-blue">Hackathon 2025</span>
  </div>
</header>

<!-- ═══════════ HERO ═══════════ -->
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-grid">
    <div class="hero-content">
      <h2 class="hero-title">
        AI Agents That<br>
        Think Like <em>Lawyers</em>
      </h2>
      <p class="hero-desc">
        An OpenEnv-compliant reinforcement learning environment for legal contract analysis.
        Agents review real-world contracts, identify missing clauses, detect one-sided terms,
        and rewrite ambiguous language — scored with partial credit graders.
      </p>
      <div class="hero-stats">
        <div>
          <span class="hero-stat-val">3</span>
          <div class="hero-stat-lbl">Tasks</div>
        </div>
        <div>
          <span class="hero-stat-val">9</span>
          <div class="hero-stat-lbl">Contracts</div>
        </div>
        <div>
          <span class="hero-stat-val">0–1</span>
          <div class="hero-stat-lbl">Reward Range</div>
        </div>
        <div>
          <span class="hero-stat-val">∂</span>
          <div class="hero-stat-lbl">Partial Credit</div>
        </div>
      </div>
    </div>
    <div class="score-ring-wrap">
      <div class="score-ring">
        <svg viewBox="0 0 120 120" width="120" height="120">
          <circle class="ring-bg" cx="60" cy="60" r="54"/>
          <circle class="ring-fg" id="score-ring" cx="60" cy="60" r="54"/>
        </svg>
        <div class="ring-label">
          <span class="ring-score" id="ring-score-val">—</span>
          <span class="ring-sub">score</span>
        </div>
      </div>
      <div class="ring-title" id="ring-task-label">No episode</div>
    </div>
  </div>
</section>

<!-- ═══════════ TASKS ═══════════ -->
<section style="padding: 40px; max-width: 1200px; margin: 0 auto; border-bottom: 1px solid var(--border);">
  <div class="section-label">Task Difficulty Progression</div>
  <div class="task-cards">
    <div class="task-card easy" onclick="selectTask('find_missing_clauses')">
      <div class="task-card-glow"></div>
      <div class="task-top">
        <div class="task-icon">🔍</div>
        <span class="diff-badge">Easy · 3 steps</span>
      </div>
      <div class="task-name">find_missing_clauses</div>
      <div class="task-desc">Identify all standard clause types absent from a contract. Partial credit per correct answer with false-positive penalty.</div>
      <div class="task-meta">
        <span>🎯 Partial credit</span>
        <span>📋 8 clause types</span>
      </div>
    </div>
    <div class="task-card medium" onclick="selectTask('identify_risky_party')">
      <div class="task-card-glow"></div>
      <div class="task-top">
        <div class="task-icon">⚠️</div>
        <span class="diff-badge">Medium · 2 steps</span>
      </div>
      <div class="task-name">identify_risky_party</div>
      <div class="task-desc">Determine which party bears disproportionate risk from a flagged clause. Bonus for quality legal reasoning.</div>
      <div class="task-meta">
        <span>🎯 Binary + bonus</span>
        <span>👥 4 party options</span>
      </div>
    </div>
    <div class="task-card hard" onclick="selectTask('rewrite_ambiguous')">
      <div class="task-card-glow"></div>
      <div class="task-top">
        <div class="task-icon">✍️</div>
        <span class="diff-badge">Hard · 1 step</span>
      </div>
      <div class="task-name">rewrite_ambiguous</div>
      <div class="task-desc">Rewrite a legally vague clause to be precise and enforceable. Scored across 5 legal criteria.</div>
      <div class="task-meta">
        <span>🎯 5-component score</span>
        <span>⚖️ Multi-criteria</span>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════ MAIN ═══════════ -->
<main>

  <!-- Panel 1: API Tester -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">Live API Tester</div>
      <span class="panel-sub" id="last-call-label">—</span>
    </div>
    <div class="panel-body">
      <div class="form-group">
        <label class="form-label">Select Task</label>
        <select id="task-select" onchange="currentTask = this.value; updateSelectStyle()">
          <option value="find_missing_clauses">🔍 find_missing_clauses (Easy)</option>
          <option value="identify_risky_party">⚠️ identify_risky_party (Medium)</option>
          <option value="rewrite_ambiguous">✍️ rewrite_ambiguous (Hard)</option>
        </select>
      </div>
      <button class="btn btn-gold" onclick="doReset()">
        ▶ POST /reset — Start New Episode
      </button>
      <div class="btn-gap"></div>
      <button class="btn btn-green" onclick="doStep()">
        ⚡ POST /step — Submit Sample Action
      </button>
    </div>
  </div>

  <!-- Panel 2: Response Viewer -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">Response</div>
      <span class="panel-sub" id="reward-label" style="color: var(--gold)">reward: —</span>
    </div>
    <div class="panel-body">
      <div class="reward-bar-wrap">
        <div class="reward-bar" id="reward-bar"></div>
      </div>
      <div id="response-box" class="response-box">// Click "POST /reset" to start an episode...</div>
    </div>
  </div>

  <!-- Panel 3: Episode Stats -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">Episode Log</div>
      <button class="btn btn-ghost btn-sm" onclick="clearLog()">Clear</button>
    </div>
    <div class="panel-body">
      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-val" id="stat-steps">0</span>
          <span class="stat-lbl">Steps</span>
        </div>
        <div class="stat-box">
          <span class="stat-val" id="stat-score">0.00</span>
          <span class="stat-lbl">Best Score</span>
        </div>
        <div class="stat-box">
          <span class="stat-val" id="stat-done">—</span>
          <span class="stat-lbl">Status</span>
        </div>
      </div>
      <div class="log-scroll" id="log-container">
        <div class="log-entry">
          <span class="log-tag tag-init">[INIT]</span>
          <span class="log-msg">Environment ready. Click Reset to begin an episode.</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Panel 4: API Reference -->
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">API Reference</div>
      <a href="/docs" target="_blank" class="btn btn-ghost btn-sm" style="text-decoration:none">Swagger UI ↗</a>
    </div>
    <div class="panel-body">
      <div class="endpoint-list">
        <div class="endpoint-row">
          <span class="method-tag m-post">POST</span>
          <span class="ep-path">/reset</span>
          <span class="ep-desc">Start new episode</span>
          <button class="btn btn-ghost btn-sm" onclick="doReset()">Try</button>
        </div>
        <div class="endpoint-row">
          <span class="method-tag m-post">POST</span>
          <span class="ep-path">/step</span>
          <span class="ep-desc">Submit agent action</span>
          <button class="btn btn-ghost btn-sm" onclick="doStep()">Try</button>
        </div>
        <div class="endpoint-row">
          <span class="method-tag m-get">GET</span>
          <span class="ep-path">/state</span>
          <span class="ep-desc">Current env state</span>
          <button class="btn btn-ghost btn-sm" onclick="doState()">Try</button>
        </div>
        <div class="endpoint-row">
          <span class="method-tag m-get">GET</span>
          <span class="ep-path">/tasks</span>
          <span class="ep-desc">List all tasks</span>
          <button class="btn btn-ghost btn-sm" onclick="doTasks()">Try</button>
        </div>
        <div class="endpoint-row">
          <span class="method-tag m-get">GET</span>
          <span class="ep-path">/health</span>
          <span class="ep-desc">Health check</span>
          <button class="btn btn-ghost btn-sm" onclick="doHealth()">Try</button>
        </div>
        <div class="endpoint-row">
          <span class="method-tag m-get">GET</span>
          <span class="ep-path">/docs</span>
          <span class="ep-desc">Interactive Swagger</span>
          <button class="btn btn-ghost btn-sm" onclick="window.open('/docs','_blank')">Open</button>
        </div>
      </div>
    </div>
  </div>

</main>

<footer>
  <span>⚖️ Legal Contract Review Environment · OpenEnv v1.0 · MIT License</span>
  <div class="footer-links">
    <a href="/docs">API Docs</a>
    <a href="/tasks">Tasks</a>
    <a href="/health">Health</a>
  </div>
  <span>Meta × Hugging Face Hackathon 2025</span>
</footer>

<script>
// ── State ──
let currentTask = 'find_missing_clauses';
let episodeActive = false;

// ── Helpers ──
function setResponse(data, status) {
  const box = document.getElementById('response-box');
  box.textContent = JSON.stringify(data, null, 2);
  box.className = 'response-box' + (status === 'error' ? ' error' : status === 'success' ? ' success' : '');
}

function addLog(tag, tagClass, msg) {
  const container = document.getElementById('log-container');
  const entry = document.createElement('div');
  entry.className = 'log-entry';
  entry.innerHTML = `<span class="log-tag ${tagClass}">[${tag}]</span><span class="log-msg">${msg}</span>`;
  container.insertBefore(entry, container.firstChild);
  while (container.children.length > 15) container.removeChild(container.lastChild);
}

function clearLog() {
  document.getElementById('log-container').innerHTML =
    '<div class="log-entry"><span class="log-tag tag-init">[INIT]</span><span class="log-msg">Log cleared.</span></div>';
}

function updateStats(result) {
  if (!result) return;
  const obs = result.observation || {};
  const score = obs.score_so_far || result.reward || 0;
  const steps = obs.step_number || 0;

  document.getElementById('stat-steps').textContent = steps;
  document.getElementById('stat-score').textContent = score.toFixed(3);
  document.getElementById('stat-done').textContent = result.done ? '✓ Done' : '…';
  document.getElementById('reward-label').textContent = 'reward: ' + (result.reward || 0).toFixed(3);

  // Update reward bar
  document.getElementById('reward-bar').style.width = (score * 100) + '%';

  // Update ring
  const pct = score;
  const circ = 339.3;
  document.getElementById('score-ring').style.strokeDashoffset = circ - (pct * circ);
  document.getElementById('ring-score-val').textContent = score.toFixed(2);
  document.getElementById('ring-task-label').textContent = obs.task || currentTask;
}

function updateSelectStyle() {
  const sel = document.getElementById('task-select');
  const colors = { find_missing_clauses: '#3ddc84', identify_risky_party: '#f5a623', rewrite_ambiguous: '#ff4d6d' };
  sel.style.color = colors[currentTask] || 'var(--text)';
}

function selectTask(task) {
  currentTask = task;
  document.getElementById('task-select').value = task;
  updateSelectStyle();
  addLog('SELECT', 'tag-init', `Task set to: ${task}`);
}

// ── API Calls ──
async function doReset() {
  document.getElementById('last-call-label').textContent = 'POST /reset';
  try {
    const res = await fetch('/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: currentTask })
    });
    const data = await res.json();
    setResponse(data, 'success');
    updateStats(data);
    episodeActive = true;
    const cid = data.observation?.contract_id || '?';
    addLog('RESET', 'tag-reset', `task=${currentTask} contract=${cid} steps_max=${data.observation?.max_steps}`);
  } catch(e) {
    setResponse({ error: e.message }, 'error');
    addLog('ERROR', 'tag-error', e.message);
  }
}

async function doStep() {
  if (!episodeActive) {
    addLog('WARN', 'tag-warn', 'Call /reset first to start an episode.');
    return;
  }
  document.getElementById('last-call-label').textContent = 'POST /step';

  const sampleActions = {
    find_missing_clauses: {
      task: 'find_missing_clauses',
      find_missing: { missing_clauses: ['termination', 'governing_law', 'dispute_resolution'] }
    },
    identify_risky_party: {
      task: 'identify_risky_party',
      identify_risky: {
        clause_id: 'clause_6',
        disadvantaged_party: 'Party B',
        reasoning: 'This clause gives Client unilateral termination rights with no obligation to pay work in progress, creating severe financial exposure and disproportionate disadvantage for Party B with no recourse.'
      }
    },
    rewrite_ambiguous: {
      task: 'rewrite_ambiguous',
      rewrite: {
        clause_id: 'clause_1',
        rewritten_clause: 'Net profits shall be distributed 60% to Partner A and 40% to Partner B, calculated quarterly on net revenue by a certified public accountant within 30 days of each quarter end. Each distribution shall be made within 15 days of the accountant\'s report. Disputes regarding profit calculations shall be resolved through binding arbitration within 60 days, with costs shared equally. Extraordinary distributions require 14 days written notice to all partners. This obligation is binding and enforceable against both parties.'
      }
    }
  };

  const action = sampleActions[currentTask];
  try {
    const res = await fetch('/step', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(action)
    });
    const data = await res.json();
    setResponse(data, data.reward > 0.5 ? 'success' : '');
    updateStats(data);
    const fb = (data.observation?.last_action_feedback || '').substring(0, 80);
    addLog('STEP', 'tag-step', `reward=${data.reward?.toFixed(3)} done=${data.done} | ${fb}`);
    if (data.done) {
      episodeActive = false;
      addLog('END', 'tag-end', `Episode complete. Final score: ${data.observation?.score_so_far?.toFixed(3)}`);
    }
  } catch(e) {
    setResponse({ error: e.message }, 'error');
    addLog('ERROR', 'tag-error', e.message);
  }
}

async function doState() {
  document.getElementById('last-call-label').textContent = 'GET /state';
  try {
    const res = await fetch('/state');
    const data = await res.json();
    setResponse(data, 'success');
    updateStats(data);
    addLog('STATE', 'tag-init', `score=${data.observation?.score_so_far} done=${data.done}`);
  } catch(e) {
    setResponse({ error: e.message }, 'error');
  }
}

async function doTasks() {
  document.getElementById('last-call-label').textContent = 'GET /tasks';
  try {
    const res = await fetch('/tasks');
    setResponse(await res.json(), 'success');
    addLog('TASKS', 'tag-init', '3 tasks loaded');
  } catch(e) {
    setResponse({ error: e.message }, 'error');
  }
}

async function doHealth() {
  document.getElementById('last-call-label').textContent = 'GET /health';
  try {
    const res = await fetch('/health');
    const data = await res.json();
    setResponse(data, 'success');
    addLog('HEALTH', 'tag-init', `status=${data.status} env=${data.env}`);
  } catch(e) {
    setResponse({ error: e.message }, 'error');
  }
}

// ── Init ──
updateSelectStyle();
</script>
</body>
</html>"""
