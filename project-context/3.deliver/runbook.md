# Runbook — Recruitment Assistant

**Version:** 1.0
**Last updated:** 2026-02-22

---

## Application Overview

The Recruitment Assistant is a CLI-based multi-agent system built with CrewAI. It takes job requirements as input, searches the web for matching candidates, evaluates them against structured criteria, and produces a ranked recruitment report.

**Pipeline:** Researcher -> Evaluator -> Reporter (sequential)

**Runtime:** Typically 2-5 minutes depending on web search results and LLM response times.

---

## Prerequisites

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Python | 3.8+ (tested on 3.13.7) | Must be on PATH |
| pip | Latest | For installing dependencies |
| Internet | Required | API calls to Anthropic and SerperDev |
| API keys | 2 required | ANTHROPIC_API_KEY, SERPER_API_KEY |

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd recruitment-assistant

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
#   ANTHROPIC_API_KEY=sk-ant-...
#   SERPER_API_KEY=...
```

### Verify installation

```bash
python -c "from crewai import Crew; print('CrewAI imported successfully')"
```

---

## How to Run

### Option A: Direct Python

```bash
source .venv/bin/activate
python src/main.py
```

### Option B: Startup script

```bash
./run.sh
```

### What happens

1. The app loads `.env` and validates API keys
2. You are prompted for job requirements (title, skills, experience, location)
3. Press Enter on any prompt to use the default value
4. The 3-agent pipeline executes sequentially
5. The final report prints to the terminal
6. A copy is saved to `output/report.md`

### Expected output

- Terminal: full recruitment report with candidate rankings
- File: `output/report.md` (overwritten each run)
- Log: `logs/app.log` (appended each run)

---

## How to Monitor

### During execution

- CrewAI prints verbose agent output to the terminal (tool calls, reasoning, intermediate results)
- Application-level log messages appear with `[INFO]` prefix

### After execution

- **Log file:** `logs/app.log` — timestamped entries for startup, config loading, agent creation, execution, and errors
- **Output file:** `output/report.md` — the final recruitment report

### CrewAI tracing dashboard (optional)

If you have run `crewai login` and enabled `tracing=True` in `src/crew.py`, execution traces appear in the CrewAI web dashboard showing per-agent timelines, tool calls, and token usage.

---

## Common Issues and Troubleshooting

### "Missing required API keys"

**Cause:** `.env` file is missing or does not contain the required keys.

**Fix:**
```bash
cp .env.example .env
# Add your actual API keys
```

### "Configuration file not found"

**Cause:** Running from the wrong directory, or config files are missing.

**Fix:** Ensure you are in the project root directory (`recruitment-assistant/`) and that `config/agents.yaml` and `config/tasks.yaml` exist.

### CrewAI agent fails mid-execution

**Cause:** Typically a rate limit from the LLM provider or SerperDev API, or a network timeout.

**Fix:**
- Check `logs/app.log` for the error traceback
- Verify your API keys have sufficient credits/quota
- The crew has `max_rpm=10` to avoid rate limiting — wait a moment and retry
- If a specific agent consistently fails, check its `max_iter` setting in `config/agents.yaml`

### "ModuleNotFoundError: No module named 'crewai'"

**Cause:** Virtual environment not activated or dependencies not installed.

**Fix:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Web scraping returns empty results

**Cause:** The target website may block scraping, or SerperDev returned no results for the search query.

**Fix:** This is expected for some queries. The Researcher agent will attempt multiple search strategies. Try broadening the job requirements (e.g. remove location constraint).

---

## How to Stop

- **During input prompts:** Press `Ctrl+C` to exit
- **During execution:** Press `Ctrl+C` — the process will terminate. No cleanup is needed (no persistent state or open connections)

---

## How to Restart

Simply run the application again. Each run is independent — there is no persistent state between runs. The output file is overwritten and the log file is appended to.

```bash
python src/main.py
# or
./run.sh
```
