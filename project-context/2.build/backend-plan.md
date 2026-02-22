# Backend Plan — Recruitment Assistant

**Author:** Backend Engineer Agent
**Date:** 2026-02-22
**Branch:** `feature/backend`
**SAD Reference:** `project-context/2.build/sad.md`

---

## What We're Building

A CLI-based recruitment assistant using CrewAI 1.9.3 with 3 sequential agents:

1. **Researcher** — searches the web for candidate profiles using SerperDevTool and ScrapeWebsiteTool
2. **Evaluator** — scores candidates against a structured rubric (skills match, experience relevance, location fit, each 1-5)
3. **Reporter** — produces a formatted markdown recruitment report

The application loads agent/task definitions from YAML config, collects job requirements via CLI prompts, runs the crew, and saves the output to `output/report.md`.

---

## Implementation Order & Status

### Phase 1: Project Scaffolding

| # | Task | Status |
|---|------|--------|
| 1.1 | Create `src/`, `config/`, `output/` directories | Done |
| 1.2 | Create `requirements.txt` (crewai[anthropic]==1.9.3, crewai-tools, python-dotenv) | Done |
| 1.3 | Create `output/.gitkeep` and `src/__init__.py` | Done |
| 1.4 | Update `.gitignore` to exclude `output/*` (keep `.gitkeep`) | Done |

### Phase 2: Configuration Files

| # | Task | Status |
|---|------|--------|
| 2.1 | Create `config/agents.yaml` — 3 agents with roles, goals, backstories, LLM config | Done |
| 2.2 | Create `config/tasks.yaml` — 3 tasks with descriptions, scoring rubric, context chains | Done |

### Phase 3: Core Application Code

| # | Task | Status |
|---|------|--------|
| 3.1 | Create `src/crew.py` — loads YAML, builds agents/tasks, assembles sequential crew | Done |
| 3.2 | Create `src/main.py` — CLI entry point, env validation, interactive prompts, output saving | Done |

### Phase 4: Verification

| # | Task | Status |
|---|------|--------|
| 4.1 | Verify all imports succeed (no runtime errors) | Done |
| 4.2 | Verify crew builds correctly (3 agents, 3 tasks, sequential, context chains) | Done |
| 4.3 | Verify API key validation catches missing keys | Done |

---

## Key Implementation Decisions

1. **No `@CrewBase` decorator** — CrewAI 1.9.3 does not export `CrewBase`. Agents and tasks are created programmatically from YAML config using the standard `Agent`, `Task`, `Crew` classes.

2. **`crewai[anthropic]` extra required** — The Anthropic provider needs the `anthropic` package installed. Using `crewai[anthropic]==1.9.3` in requirements.txt handles this.

3. **YAML placeholder interpolation** — Task descriptions use `{job_title}`, `{skills}`, etc. which are interpolated with user input at runtime via Python string formatting, before passing to CrewAI.

4. **Context wiring** — Task 2 receives Task 1's output via the `context` parameter. Task 3 receives Task 2's output. This matches CrewAI's sequential context-passing mechanism.

5. **Fail-fast API key check** — `main.py` validates `ANTHROPIC_API_KEY` and `SERPER_API_KEY` are present before building the crew, so the user gets a clear error rather than a mid-execution failure.

---

## Files Created

| File | Purpose |
|------|---------|
| `requirements.txt` | Pinned dependencies (crewai[anthropic], crewai-tools, python-dotenv) |
| `config/agents.yaml` | 3 agent definitions (Researcher, Evaluator, Reporter) with roles, goals, backstories |
| `config/tasks.yaml` | 3 task definitions with descriptions, scoring rubric, expected outputs, context chains |
| `src/__init__.py` | Empty init file for the src package |
| `src/crew.py` | Crew definition — loads YAML config, creates agents/tasks, assembles sequential crew |
| `src/main.py` | CLI entry point — env validation, interactive prompts, crew execution, report saving |
| `output/.gitkeep` | Keeps the output directory in git (contents are gitignored) |

---

## How to Run

```bash
source ~/Projects/agentic-architect/.venv/bin/activate
cd ~/Projects/agentic-architect/recruitment-assistant
python src/main.py
```

The system will prompt for job title, skills, experience level, and location. Press Enter to accept defaults (Senior Python Developer, London, UK).
