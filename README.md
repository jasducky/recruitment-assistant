# Recruitment Assistant

A multi-agent candidate sourcing and evaluation system built with CrewAI. Takes a job description as input, searches the web for matching candidates, scores them against structured criteria, and produces a ranked recruitment report with transparent rationale.

This project is a learning exercise for the [AAMAD](https://github.com/synaptic-ai-consulting/AAMAD) (AI-Assisted Multi-Agent Application Development) methodology, demonstrating the full workflow from market research through requirements to build and test.

---

## Problem Statement

Recruitment teams are losing ground on time-to-hire:

- **60% of companies** saw increased time-to-hire in 2024, up from 44% in 2023
- **90% of organisations** missed their 2026 hiring goals
- **56% of employers** cite "not enough qualified candidates" as their biggest challenge
- **27% of TA teams** report unmanageable workloads

AI adoption in recruitment is near-universal (99.8% of TA teams use or plan to use AI), but current tools focus on scheduling or keyword search. No widely adopted solution automates the full pipeline from candidate discovery through structured evaluation to ranked recommendations with clear reasoning.

*Data points sourced from the [Market Research Document](project-context/1.define/mrd.md).*

---

## Features

The system runs a 3-agent sequential pipeline:

1. **Candidate Sourcing** — Researcher agent discovers candidate profiles via web search (SerperDev API + web scraping), returning structured profiles with name, role, skills, location, and source URLs
2. **Candidate Evaluation** — Evaluator agent scores each candidate against the job criteria (skills match, experience relevance, location fit) using a 1-5 rubric with written rationale per criterion
3. **Recruitment Report** — Reporter agent produces a formatted markdown report with summary, ranked table, per-candidate detail, and recommended next steps

**Explicitly out of scope:** candidate outreach, communication, ATS integration, persistent storage, and web UI.

---

## Architecture Overview

The system uses CrewAI's sequential process orchestration. Each agent receives the output of the previous agent as context input.

```
Job Requirements (user input)
        |
        v
  +-----------+
  | Researcher |  --> Searches web, collects candidate profiles
  +-----------+
        |
        | (candidate profiles with raw data)
        v
  +-----------+
  | Evaluator  |  --> Scores against criteria, ranks with rationale
  +-----------+
        |
        | (scored, ranked candidates)
        v
  +-----------+
  |  Reporter  |  --> Formats final recruitment report
  +-----------+
        |
        v
  Recruitment Report (output)
```

**Agent roles:**

| Agent | Role | Tools |
|-------|------|-------|
| Researcher | Senior Talent Researcher — discovers candidates via crafted search queries | SerperDevTool, ScrapeWebsiteTool |
| Evaluator | Candidate Evaluation Specialist — applies structured scoring rubric | None (works with Researcher output) |
| Reporter | Recruitment Report Analyst — transforms evaluation data into actionable report | None (works with Evaluator output) |

All agents have memory enabled and delegation disabled. Iteration limits are set per agent (5, 3, and 2 respectively) to control cost and runtime.

---

## Getting Started

### Prerequisites

- Python 3.13+
- [CrewAI](https://docs.crewai.com/) and crewai-tools
- API keys for:
  - An LLM provider (OpenAI or Anthropic)
  - [SerperDev](https://serper.dev/) (web search — free tier sufficient for testing)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd recruitment-assistant

# Install dependencies (once build phase is complete)
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Usage

> **Coming soon** — the Build phase has not yet started. Once implemented, usage will be:

```bash
python main.py
```

The system will prompt for job title, required skills, experience level, and location preference, then run the full pipeline and output a recruitment report to the terminal and `output/report.md`.

---

## Project Structure

This project follows the AAMAD directory structure, which separates framework artifacts (reusable across projects) from project-specific context:

```
recruitment-assistant/
├── .cursor/
│   ├── agents/          # AAMAD agent persona definitions
│   ├── prompts/         # Phase-specific prompts
│   ├── rules/           # Architecture, workflow, and adapter rules
│   └── templates/       # MRD, PRD, and SAD generation templates
├── project-context/
│   ├── 1.define/        # Market research, PRD, decisions log
│   │   ├── mrd.md       # Market Research Document
│   │   ├── prd.md       # Product Requirements Document
│   │   └── decisions.md # Scope and design decisions
│   ├── 2.build/         # Build artifacts (architecture, code docs)
│   └── 3.deliver/       # QA logs, deploy configs, release notes
├── CHECKLIST.md          # Step-by-step execution guide
├── CLAUDE.md             # Claude Code project instructions
└── README.md             # This file
```

**Key artifacts to review:**
- [PRD](project-context/1.define/prd.md) — full requirements, agent definitions, success metrics
- [MRD](project-context/1.define/mrd.md) — market research backing the requirements
- [Decisions](project-context/1.define/decisions.md) — scope and design decision log

---

## Development Status

| Phase | Status | Details |
|-------|--------|---------|
| **Define** | Complete | MRD, PRD, and decisions log authored. Requirements traced to market data. |
| **Build** | Not started | Architecture document, agent implementation, CLI, and end-to-end wiring. |
| **Deliver** | Not started | Testing, QA validation, and demo run. |

### What has been completed

- Market research (MRD) with sourced data points on recruitment pain points, AI adoption, and competitive gaps
- Product requirements (PRD) with agent definitions, feature priorities (P0/P1/P2), evaluation criteria, and success metrics
- Scope decisions documented (3-agent pipeline, sequential orchestration, no outreach, CLI-only)
- Per-agent evaluation criteria defined (what "good output" looks like for each agent)

### What is next

1. System architecture document (agent YAML config, task definitions, data flow)
2. CrewAI project scaffolding and dependency setup
3. Agent implementation (Researcher, Evaluator, Reporter)
4. Sequential crew wiring and CLI entry point
5. End-to-end testing with sample job requirement

---

## Development Crew

This project is built using AAMAD agent personas. Each persona owns a specific phase and set of artifacts:

| AAMAD Persona | Phase | Responsibility | Key Output |
|---------------|-------|---------------|------------|
| **Product Manager** | Define | Requirements, scope, success criteria | MRD, PRD |
| **System Architect** | Build | Agent architecture, task definitions, tool selection, data flow | Architecture document, YAML config specs |
| **Backend Engineer** | Build | Implement agents, tasks, tools, crew orchestration | Python code, CrewAI config, CLI entry point |
| **QA/Test Engineer** | Deliver | End-to-end testing, edge cases, output validation | Test results, bug reports |

Frontend Engineer and DevOps personas are not used for this project (CLI only, local development).

---

*This is a learning exercise for the AAMAD methodology. It demonstrates the full artefact trail from market research to product requirements to (eventually) a working multi-agent system. The goal is to learn the process, not to build a production recruitment tool.*
