# ⚖️ Legal Contract Review Environment

> **OpenEnv-compliant RL environment** — Train AI agents to review legal contracts like a professional attorney.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-v1.0-gold)](https://github.com/openenv)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 🎯 What Is This?

This environment simulates **real-world legal contract review** — a $10B+ industry task performed daily by lawyers, paralegals, and legal-tech platforms like LexisNexis and ContractPodAi.

An AI agent receives a realistic legal contract and must demonstrate legal reasoning through **3 tasks of increasing difficulty**, scored with nuanced graders that reward precision and penalize careless answers.

**Why it matters for RL:**
- Legal review is a high-stakes sequential decision task
- Graders provide rich partial credit signals for learning
- Tasks mirror real attorney workflows (not synthetic toy problems)
- Failure modes are meaningful (missing a termination clause ≠ missing IP clause)

---

## 🏗️ Architecture

```
Agent
  │
  ├─ POST /reset ──► receives contract + task description + clauses
  │
  ├─ POST /step  ──► submits legal analysis ──► receives reward (0.0–1.0) + feedback
  │
  └─ POST /step  ──► improves based on feedback (if steps remain) ──► final score
```

**Core components:**

| File | Purpose |
|------|---------|
| `app.py` | FastAPI server — `/reset`, `/step`, `/state` endpoints + interactive dashboard |
| `env.py` | Episode state management, task selection, step execution |
| `models.py` | Typed Pydantic models (action + observation) |
| `graders.py` | Task-specific graders with partial credit logic |
| `contracts.py` | 9 synthetic legal contracts (3 per task) |
| `inference.py` | AI agent using Groq LLaMA-3.3-70B via OpenAI client |

---

## 📋 Tasks

### Task 1: Find Missing Clauses — **Easy** (3 steps)

Agent reviews a contract and identifies which standard clause types are absent.

**Standard clauses:** `termination` · `confidentiality` · `indemnification` · `dispute_resolution` · `payment_terms` · `intellectual_property` · `limitation_of_liability` · `governing_law`

**Reward formula:**
```
score = (correctly_identified / total_missing) - (0.1 × false_positives)
```
- Perfect score: identify all missing clauses with zero false positives → 1.0
- Partial credit for each correct clause found
- Penalty for claiming present clauses are missing

---

### Task 2: Identify Risky Party — **Medium** (2 steps)

A specific clause is flagged. Agent identifies which party bears disproportionate risk.

**Valid answers:** `"Party A"` · `"Party B"` · `"Both equally"` · `"Neither"`

**Reward formula:**
```
base  = 1.0 if correct party, else 0.0
bonus = min(0.2, count(legal_keywords_in_reasoning) × 0.05)
score = min(1.0, base + bonus)
```
Legal keywords that trigger bonus: *unilateral, one-sided, disproportionate, no recourse, imbalance, sole discretion, bears all risk...*

---

### Task 3: Rewrite Ambiguous Clause — **Hard** (1 step)

Agent rewrites a legally vague clause to be precise and enforceable.

**Scoring (5 components):**

| Component | Weight | What it checks |
|-----------|--------|----------------|
| Length adequacy | 0.10 | Meets minimum word count |
| Specificity | 0.30 | Numbers, percentages, durations, dates |
| Legal vocabulary | 0.30 | Domain-specific keywords present |
| Carve-outs / exceptions | 0.20 | Exception clauses (provided that, except, notwithstanding) |
| Enforceability markers | 0.10 | Formal language (shall, in writing, binding) |

---

## 🔌 Action Space

### Task 1 — Find Missing Clauses

```json
{
  "task": "find_missing_clauses",
  "find_missing": {
    "missing_clauses": ["termination", "governing_law", "dispute_resolution"]
  }
}
```

### Task 2 — Identify Risky Party

```json
{
  "task": "identify_risky_party",
  "identify_risky": {
    "clause_id": "clause_6",
    "disadvantaged_party": "Party B",
    "reasoning": "Clause 6 grants Client unilateral termination rights with no obligation to pay work-in-progress, creating severe financial exposure for Freelancer with no recourse or remedy."
  }
}
```

### Task 3 — Rewrite Ambiguous Clause

```json
{
  "task": "rewrite_ambiguous",
  "rewrite": {
    "clause_id": "clause_1",
    "rewritten_clause": "Net profits shall be distributed 60% to Partner A and 40% to Partner B, calculated quarterly on net revenue by a certified public accountant within 30 days of quarter end. Distributions shall be made within 15 days of the accountant's report. Disputes shall be resolved through binding arbitration within 60 days, costs shared equally. Extraordinary distributions require 14 days written notice. This obligation is binding and enforceable, provided that distributions shall not include reserved operating capital as defined in Schedule A."
  }
}
```

---

## 👁️ Observation Space

```json
{
  "contract_id": "FM-001",
  "contract_title": "Software Development Services Agreement",
  "contract_text": "...(full contract text)...",
  "clauses": [
    {
      "clause_id": "clause_3",
      "title": "Confidentiality",
      "text": "Each party maintains confidence of received information for 3 years post-termination.",
      "clause_type": "confidentiality",
      "is_ambiguous": false,
      "flagged_for_analysis": false
    }
  ],
  "task": "find_missing_clauses",
  "task_description": "Identify all missing standard clause types...",
  "step_number": 1,
  "max_steps": 3,
  "last_action_feedback": "✅ Correctly identified: termination | ❌ Missed: governing_law",
  "score_so_far": 0.667
}
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/legal-contract-review
cd legal-contract-review

pip install -r requirements.txt
```

### 2. Start the Environment Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

Open **http://localhost:7860** for the interactive dashboard.

### 3. Run the Inference Script

```bash
# Set your Groq API key (free, ultra-fast)
export GROQ_API_KEY="gsk_your_groq_key_here"

# Run on a specific task
export TASK_NAME="find_missing_clauses"
python inference.py

# Run on all tasks
for task in find_missing_clauses identify_risky_party rewrite_ambiguous; do
    TASK_NAME=$task python inference.py
done
```

**Expected output:**
```
[START] task=find_missing_clauses env=legal_contract_review model=llama-3.3-70b-versatile
[STEP] step=1 action=task=find_missing_clauses,step=1,score=0.750 reward=0.75 done=false error=null
[STEP] step=2 action=task=find_missing_clauses,step=2,score=1.000 reward=1.00 done=true error=null
[END] success=true steps=2 score=1.000 rewards=0.75,1.00
```

---

## 🐳 Docker Deployment

### Build & Run Locally

```bash
docker build -t legal-contract-review .
docker run -p 7860:7860 legal-contract-review
```

### Run Inference Against Docker Container

```bash
# Terminal 1: Start server
docker run -p 7860:7860 legal-contract-review

# Terminal 2: Run inference
export GROQ_API_KEY="gsk_your_key"
export ENV_BASE_URL="http://localhost:7860"
python inference.py
```

---

## 🤗 Hugging Face Spaces Deployment

### Step 1: Create a new Space

Go to [huggingface.co/new-space](https://huggingface.co/new-space) and select:
- **SDK**: Docker
- **Hardware**: CPU Basic (free)

### Step 2: Push your code

```bash
# Initialize git and push to HF Spaces
git init
git add .
git commit -m "Initial commit"

# Add HF Spaces remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/legal-contract-review
git push hf main
```

### Step 3: Verify deployment

Once deployed, your Space URL will be:
`https://YOUR_USERNAME-legal-contract-review.hf.space`

Test it:
```bash
curl https://YOUR_USERNAME-legal-contract-review.hf.space/health
# {"status":"ok","env":"legal-contract-review","version":"1.0.0"}

curl -X POST https://YOUR_USERNAME-legal-contract-review.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "find_missing_clauses"}'
```

### Step 4: Run inference against HF Space

```bash
export GROQ_API_KEY="gsk_your_key"
export ENV_BASE_URL="https://YOUR_USERNAME-legal-contract-review.hf.space"
python inference.py
```

---

## 🔧 Environment Variables

### Server

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `7860` | Server port (HF Spaces standard) |

### Inference Script

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes* | — | Groq API key (fastest, recommended) |
| `HF_TOKEN` | Yes* | — | HuggingFace API key (fallback) |
| `API_KEY` | Yes* | — | Generic API key fallback |
| `API_BASE_URL` | No | `https://api.groq.com/openai/v1` | LLM endpoint |
| `MODEL_NAME` | No | `llama-3.3-70b-versatile` | Model identifier |
| `ENV_BASE_URL` | No | `http://localhost:7860` | Environment server URL |
| `TASK_NAME` | No | `find_missing_clauses` | Task to run |

*One of GROQ_API_KEY, HF_TOKEN, or API_KEY is required.

### Groq Model Options (all free tier)

| Model | Speed | Context | Best For |
|-------|-------|---------|---------|
| `llama-3.3-70b-versatile` | ~500 tok/s | 128k | **Recommended — best quality** |
| `llama3-70b-8192` | ~500 tok/s | 8k | Fast, smaller context |
| `mixtral-8x7b-32768` | ~450 tok/s | 32k | Good balance |

---

## 📊 Baseline Scores

| Model | find_missing | identify_risky | rewrite_ambiguous |
|-------|-------------|---------------|-----------------|
| LLaMA 3.3 70B (Groq) | ~0.85 | ~0.90 | ~0.65 |
| Qwen2.5-72B | ~0.75 | ~0.85 | ~0.55 |
| Random baseline | ~0.15 | ~0.25 | ~0.05 |

---

## 🧪 Testing the Environment

### Manual API Test

```bash
# 1. Start a new episode
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "find_missing_clauses"}' | python3 -m json.tool

# 2. Submit an action
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "task": "find_missing_clauses",
    "find_missing": {
      "missing_clauses": ["termination", "governing_law", "dispute_resolution"]
    }
  }' | python3 -m json.tool

# 3. Check current state
curl http://localhost:7860/state | python3 -m json.tool

# 4. List all tasks
curl http://localhost:7860/tasks | python3 -m json.tool

# 5. Health check
curl http://localhost:7860/health
```

### Run Pre-validation Script

```bash
# From hackathon dashboard — run before submission
python pre_validate.py --url http://localhost:7860
```

---

## 📁 Project Structure

```
legal-contract-review/
├── inference.py          # AI agent — mandatory root location, [START]/[STEP]/[END] logs
├── app.py                # FastAPI server: /reset, /step, /state + dashboard UI
├── env.py                # Episode state management
├── models.py             # Pydantic typed models (action + observation)
├── graders.py            # Task-specific graders with partial credit
├── contracts.py          # 9 synthetic contracts (3 per task)
├── requirements.txt      # fastapi, uvicorn, pydantic, httpx, openai
├── Dockerfile            # Container for HF Spaces deployment
├── openenv.yaml          # OpenEnv specification
└── README.md             # This file
```

---

## 🎓 Real-World Impact

Legal contract review is one of the most cognitively demanding and error-prone tasks in law:

- **$10B+ market** — Contract analysis software used by every major law firm
- **High stakes** — Missing a termination clause can cost millions in disputes
- **Measurable quality** — Unlike creative writing, legal precision has objective criteria
- **Scalable benchmark** — 3 task types × multiple contracts = hundreds of evaluation episodes

This environment creates a **reproducible, graded benchmark** for evaluating LLM legal reasoning — filling a gap in current RL evaluation suites that focus on code or math.

---

## 📜 License

MIT License — free to use for research and commercial applications.

---

## 🙏 Acknowledgments

Built for the **Codorra 2026 Submission – AI-Powered Legal Contract Review, Risk Detection & Clause Optimization**.  
Powered by [Groq](https://groq.com) for ultra-fast LLaMA inference.  
Framework: [OpenEnv](https://github.com/openenv) · [FastAPI](https://fastapi.tiangolo.com) · [Pydantic](https://pydantic.dev)
