# Solution Architecture Document — Recruitment Assistant

**Product:** Recruitment Assistant (Multi-Agent Candidate Sourcing & Evaluation)
**Framework:** CrewAI 1.9.3
**Author:** System Architect Agent
**Date:** 2026-02-22
**Status:** Draft
**Scope:** Learning exercise (AAMAD Module 06)
**Adapter:** CrewAI

---

## 1. Architecture Philosophy & Principles

### Design Principles

- **Proportionate complexity:** This is a learning exercise. Every architectural decision should be the simplest option that demonstrates the concept. No over-engineering.
- **Config-driven agents:** Agent behaviour defined in YAML, not hardcoded — aligning with CrewAI best practices and enabling iteration without code changes.
- **Observable by default:** Verbose logging on all agents so handoffs and reasoning are visible during development.
- **Fail gracefully:** Handle API failures and empty results without crashing the pipeline.

### Scope Boundaries

**In scope:**
- CLI-only interface (no web UI, no API server)
- 3-agent sequential crew (Researcher, Evaluator, Reporter)
- Local development environment
- Output to terminal and/or markdown file

**Explicitly out of scope:**
- Frontend / web UI (PRD F13, P2)
- Database or persistent storage (PRD F12, P2)
- Deployment infrastructure, CI/CD, containerisation
- Authentication, user management, multi-tenancy
- Communication/outreach agent (PRD F10, P2; decisions.md #2)

---

## 2. Multi-Agent System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────┐
│                  CLI Entry Point                 │
│                   (main.py)                      │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │              CrewAI Crew                     │ │
│  │         (Process.sequential)                 │ │
│  │                                              │ │
│  │  ┌──────────┐   ┌──────────┐   ┌─────────┐  │ │
│  │  │Researcher│──>│Evaluator │──>│Reporter │  │ │
│  │  │  Agent   │   │  Agent   │   │  Agent  │  │ │
│  │  └────┬─────┘   └──────────┘   └────┬────┘  │ │
│  │       │                              │       │ │
│  └───────┼──────────────────────────────┼───────┘ │
│          │                              │         │
│          v                              v         │
│  ┌───────────────┐              ┌──────────────┐  │
│  │  External APIs │              │ File Output  │  │
│  │  (SerperDev)   │              │ (report.md)  │  │
│  └───────────────┘              └──────────────┘  │
└─────────────────────────────────────────────────┘

External Services:
  ┌──────────────┐    ┌──────────────────┐
  │ Anthropic API │    │  SerperDev API   │
  │ (Claude LLM)  │    │  (Web Search)    │
  └──────────────┘    └──────────────────┘
```

### Agent Definitions

All three agents are defined in YAML configuration files and instantiated by CrewAI at runtime. Agent definitions are taken directly from the PRD (Section 3).

#### Agent 1: Researcher

| Property | Value |
|----------|-------|
| **role** | Senior Talent Researcher |
| **goal** | Find the best candidate profiles matching the job requirements by searching the web |
| **tools** | SerperDevTool, ScrapeWebsiteTool |
| **memory** | true |
| **delegation** | false |
| **max_iter** | 5 |
| **verbose** | true |

**Rationale for tools:** SerperDevTool provides web search via the SerperDev API. ScrapeWebsiteTool (CrewAI built-in) extracts structured data from discovered pages. Both are P0 requirements (PRD Section 3). No custom tools are needed for MVP.

#### Agent 2: Evaluator

| Property | Value |
|----------|-------|
| **role** | Candidate Evaluation Specialist |
| **goal** | Evaluate and rank candidates against job requirements using a structured scoring rubric |
| **tools** | None (works with Researcher output) |
| **memory** | true |
| **delegation** | false |
| **max_iter** | 3 |
| **verbose** | true |

**Rationale for no tools:** The Evaluator works entirely with data passed from the Researcher via CrewAI's context-passing mechanism. It applies LLM reasoning to score candidates — no external data sources needed.

#### Agent 3: Reporter

| Property | Value |
|----------|-------|
| **role** | Recruitment Report Analyst |
| **goal** | Produce a clear, well-structured recruitment report ranking candidates with scores and rationale |
| **tools** | None (works with Evaluator output) |
| **memory** | true |
| **delegation** | false |
| **max_iter** | 2 |
| **verbose** | true |

**Rationale for no tools:** The Reporter transforms evaluation data into a formatted report. This is a pure text generation task.

### Task Orchestration

CrewAI's `Process.sequential` ensures tasks execute in order, with each task receiving the output of the previous task as context.

```
Task 1: research_candidates
  Agent: Researcher
  Input: Job requirements (from user input)
  Output: List of candidate profiles with raw data
  Expected output fields per candidate:
    - Name, current role, company
    - Key skills, location
    - Source URL
    - Sourcing note (why they match)

        │ (context passed automatically)
        v

Task 2: evaluate_candidates
  Agent: Evaluator
  Input: Candidate profiles from Task 1
  Output: Scored and ranked candidate list
  Expected output fields per candidate:
    - Score per criterion (1-5): skills match, experience relevance, location fit
    - Total score and tier (e.g. Highly qualified: 12+/15)
    - Written rationale per criterion

        │ (context passed automatically)
        v

Task 3: generate_report
  Agent: Reporter
  Input: Scored candidates from Task 2
  Output: Formatted markdown recruitment report
  Expected structure:
    - Summary (role, count found, count qualified, top pick)
    - Ranked table
    - Per-candidate detail sections
```

**Eval criteria reference:** PRD Section 6b defines quality signals and failure signals for each agent's output. These serve as acceptance criteria during testing.

---

## 3. Technology Stack

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Language** | Python | 3.13+ | PRD requirement; shared venv already configured |
| **Agent framework** | CrewAI | 1.9.3 | Course requirement; installed in shared venv |
| **Agent tools** | crewai-tools | (latest compatible) | Provides SerperDevTool, ScrapeWebsiteTool |
| **LLM provider** | Anthropic (Claude Sonnet) | Via litellm | Project decision — Anthropic API key available |
| **Web search** | SerperDev API | N/A | P0 integration (PRD Section 3) |
| **Configuration** | YAML | N/A | CrewAI config-driven pattern for agents and tasks |
| **Environment vars** | python-dotenv + .env | N/A | API key management (PRD Section 5) |

### CrewAI with Anthropic Configuration

CrewAI uses `litellm` under the hood to route LLM calls. To use Anthropic's Claude instead of the default OpenAI:

**In `.env`:**
```
ANTHROPIC_API_KEY=your-key-here
SERPER_API_KEY=your-key-here
```

**In agent/crew configuration:**
```python
# Option A: Set in crew definition
crew = Crew(
    agents=[researcher, evaluator, reporter],
    tasks=[research_task, evaluate_task, report_task],
    process=Process.sequential,
    verbose=True,
    max_rpm=10,  # Rate limiting (PRD Section 5)
)

# LLM model specified per agent or globally
# CrewAI uses litellm format: "anthropic/claude-sonnet-4-20250514"
```

**In YAML config (agents.yaml):**
```yaml
researcher:
  role: "Senior Talent Researcher"
  goal: "Find the best candidate profiles matching the job requirements..."
  backstory: "You are an experienced talent researcher..."
  llm: anthropic/claude-sonnet-4-20250514
  tools:
    - SerperDevTool
    - ScrapeWebsiteTool
  memory: true
  allow_delegation: false
  max_iter: 5
  verbose: true
```

**Key note:** The `anthropic/` prefix is required — this tells litellm to route to the Anthropic API. Without it, CrewAI defaults to OpenAI. This resolves the open question from the PRD about LLM provider choice.

---

## 4. Data Flow

### End-to-End Pipeline

```
User Input (CLI)
    │
    │  Job title, skills, experience, location
    │
    v
┌─────────────────────────────────────────┐
│            main.py                       │
│                                          │
│  1. Parse/collect job requirements       │
│  2. Instantiate crew from YAML config    │
│  3. crew.kickoff(inputs={...})           │
└──────────────────┬──────────────────────┘
                   │
                   v
┌─────────────────────────────────────────┐
│         CrewAI Sequential Crew           │
│                                          │
│  Task 1: research_candidates             │
│    ├─ SerperDevTool → web search queries │
│    ├─ ScrapeWebsiteTool → page content   │
│    └─ Output: candidate profiles (text)  │
│                   │                      │
│                   v                      │
│  Task 2: evaluate_candidates             │
│    ├─ Receives candidate profiles        │
│    ├─ Applies scoring rubric (LLM)       │
│    └─ Output: scored rankings (text)     │
│                   │                      │
│                   v                      │
│  Task 3: generate_report                 │
│    ├─ Receives scored rankings           │
│    ├─ Formats markdown report            │
│    └─ Output: final report (text)        │
└──────────────────┬──────────────────────┘
                   │
                   v
┌─────────────────────────────────────────┐
│              Output                      │
│                                          │
│  - Print to terminal (stdout)            │
│  - Save to output/report.md             │
└─────────────────────────────────────────┘
```

### Data Formats

All data between agents is passed as **unstructured text** via CrewAI's built-in context mechanism. There are no structured schemas or serialisation formats — each agent receives the previous agent's output as a string in its task context.

This is intentional for MVP. Structured output (e.g. JSON schemas per task) is a post-MVP enhancement that would improve reliability but adds complexity.

---

## 5. Directory Structure

```
recruitment-assistant/
├── CLAUDE.md                    # Project rules and context
├── CHECKLIST.md                 # Module completion tracking
├── README.md                    # Project overview
├── .env                         # API keys (not committed)
├── .env.example                 # Template for required env vars
├── .gitignore                   # Excludes .env, __pycache__, output/
│
├── project-context/             # AAMAD artefacts
│   ├── 1.define/
│   │   ├── mrd.md
│   │   ├── prd.md
│   │   └── decisions.md
│   ├── 2.build/
│   │   ├── sad.md               # This document
│   │   └── architecture-plan.md
│   └── 3.deliver/
│       └── .gitkeep
│
├── src/                         # Application code
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── crew.py                  # Crew definition and orchestration
│   └── tools/                   # Custom tools (if needed post-MVP)
│       └── __init__.py
│
├── config/                      # CrewAI YAML configuration
│   ├── agents.yaml              # Agent definitions (role, goal, backstory, tools)
│   └── tasks.yaml               # Task definitions (description, expected output)
│
├── output/                      # Generated reports (gitignored)
│   └── report.md
│
└── requirements.txt             # Pinned dependencies
```

**Design decisions:**
- `src/` separates application code from project context and configuration
- `config/` holds CrewAI YAML files — separating agent definitions from Python code follows the config-driven pattern
- `output/` is gitignored — generated reports are ephemeral
- `.env.example` documents required environment variables without exposing keys

---

## 6. Configuration Management

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `ANTHROPIC_API_KEY` | LLM provider authentication | Yes |
| `SERPER_API_KEY` | SerperDev web search API | Yes |

### YAML Configuration

CrewAI supports defining agents and tasks in YAML files. This is preferred over hardcoding because:
1. Agent behaviour can be iterated without changing Python code
2. Configuration is readable and auditable
3. It follows CrewAI's recommended config-driven pattern

**agents.yaml** defines: role, goal, backstory, llm model, tools, memory, delegation, max_iter, verbose for each agent.

**tasks.yaml** defines: description, expected_output, agent assignment, and context dependencies for each task.

### Crew-Level Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| `process` | `Process.sequential` | Pipeline pattern — each agent depends on the previous (PRD Section 3) |
| `verbose` | `True` | Observability requirement (PRD Section 5) |
| `max_rpm` | `10` | Rate limiting to avoid API throttling (PRD Section 5) |
| `memory` | `True` | Per-agent memory for within-run context |

---

## 7. Error Handling Strategy

| Scenario | Handling |
|----------|----------|
| SerperDev API returns no results | Researcher agent should note "no candidates found" and pass empty context forward; Reporter generates a "no results" report |
| SerperDev API key missing/invalid | Fail fast at startup with a clear error message before crew kickoff |
| Anthropic API rate limit hit | CrewAI's built-in retry with `max_rpm` throttling; `max_iter` limits prevent runaway loops |
| Web scraping fails on a page | ScrapeWebsiteTool handles gracefully; Researcher continues with available data |
| Agent exceeds max_iter | CrewAI stops the agent and passes its best output forward |

**General principle:** For a learning exercise, "log and continue" is preferred over complex retry logic. The verbose logging makes failures visible.

---

## 8. Assumptions

1. **Anthropic API key is available** with sufficient quota for development and testing (estimated 10-20 runs during build/test).
2. **SerperDev free tier** (100 queries) is sufficient for development. A paid tier is not needed.
3. **CrewAI 1.9.3** supports YAML-based config with Anthropic via litellm. If not, agents will be defined in Python directly.
4. **Publicly available web data** is sufficient for candidate sourcing in this exercise. Real-world accuracy is not the goal.
5. **Python 3.13** and the shared venv at `~/Projects/agentic-architect/.venv/` will be used.
6. **No persistent state** between runs. Each execution is independent.

---

## 9. Open Questions

1. **CrewAI YAML config with Anthropic:** Does CrewAI 1.9.3 support setting `llm: anthropic/claude-sonnet-4-20250514` in YAML config, or must it be set programmatically? Needs verification during build.
2. **SerperDev tool configuration:** Does SerperDevTool pick up `SERPER_API_KEY` from `.env` automatically, or does it need explicit configuration?
3. **Output file writing:** Should `main.py` handle writing the report to `output/report.md`, or can the Reporter agent's task be configured to write to file directly?
4. **Evaluation rubric format:** The PRD suggests criteria weights (skills 40%, experience 25%, location 15%, portfolio 20%) — should these be embedded in the Evaluator's task description or configurable in YAML?
5. **Input method:** Should job requirements be collected interactively (prompts) or via command-line arguments? PRD Section 6 suggests prompts, but CLI args would be simpler for testing.

---

## 10. Architecture Decisions Log

| # | Decision | Rationale | PRD Reference |
|---|----------|-----------|---------------|
| A1 | Anthropic (Claude Sonnet) as LLM provider | Available API key; resolves PRD open question #1 | PRD Assumptions, Open Questions #1 |
| A2 | YAML-based agent configuration | Config-driven pattern recommended by CrewAI; enables iteration without code changes | PRD Section 3 |
| A3 | Single `src/` directory (no packages) | Simplest structure for 3 files; no need for complex packaging in a learning exercise | PRD Section 3 (Infrastructure) |
| A4 | Unstructured text for inter-agent data | CrewAI default; structured output adds complexity without proportionate benefit for MVP | PRD Section 3 (Context passing) |
| A5 | No database, no persistent storage | Out of scope per PRD; output to file is sufficient | PRD F12 (P2, out of scope) |
| A6 | No custom tools for MVP | SerperDevTool and ScrapeWebsiteTool cover all P0 requirements | PRD Section 3 (Integration) |
| A7 | `max_rpm=10` at crew level | Conservative rate limiting to stay within free tier limits | PRD Section 5 (Cost control) |

---

## Traceability Matrix

| PRD Requirement | Architecture Component |
|-----------------|----------------------|
| F1: Job requirements input | `main.py` CLI entry point; inputs passed to `crew.kickoff()` |
| F2: Candidate sourcing | Researcher agent with SerperDevTool + ScrapeWebsiteTool |
| F3: Candidate evaluation | Evaluator agent with scoring rubric in task description |
| F4: Recruitment report | Reporter agent; output to terminal + `output/report.md` |
| F5: End-to-end pipeline | `Process.sequential` crew orchestration |
| NFR: Performance < 5 min | `max_iter` limits on agents; `max_rpm` throttling |
| NFR: Observability | `verbose=True` on all agents and crew |
| NFR: Security | `.env` for keys; `.gitignore` excludes `.env` |
| NFR: Reproducibility | `requirements.txt` with pinned versions |

---

## Sources

- PRD: `project-context/1.define/prd.md`
- MRD: `project-context/1.define/mrd.md`
- Decisions log: `project-context/1.define/decisions.md`
- CrewAI documentation: https://docs.crewai.com/
- CrewAI recruitment example: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
- SAD template (adapted): `.cursor/templates/sad-template.md`
