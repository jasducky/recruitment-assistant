# Architecture Plan — Recruitment Assistant

**Author:** System Architect Agent
**Date:** 2026-02-22
**Status:** Planned
**SAD Reference:** `project-context/2.build/sad.md`

---

## Implementation Order

The build follows a bottom-up approach: configuration and scaffolding first, then agents, then orchestration, then the CLI entry point. This ensures each layer is testable before the next is added.

### Phase 1: Project Scaffolding

| # | Task | Description | Status | Dependencies |
|---|------|-------------|--------|--------------|
| 1.1 | Create directory structure | Set up `src/`, `config/`, `output/` directories per SAD Section 5 | Planned | None |
| 1.2 | Create `requirements.txt` | Pin crewai, crewai-tools, python-dotenv versions | Planned | None |
| 1.3 | Create `.env.example` | Document required env vars (ANTHROPIC_API_KEY, SERPER_API_KEY) | Planned | None |
| 1.4 | Update `.gitignore` | Add `.env`, `output/`, `__pycache__/` | Planned | None |

### Phase 2: Configuration Files

| # | Task | Description | Status | Dependencies |
|---|------|-------------|--------|--------------|
| 2.1 | Create `config/agents.yaml` | Define all 3 agents with roles, goals, backstories, tools, LLM config | Planned | 1.1 |
| 2.2 | Create `config/tasks.yaml` | Define all 3 tasks with descriptions, expected outputs, context chains | Planned | 2.1 |

### Phase 3: Core Application Code

| # | Task | Description | Status | Dependencies |
|---|------|-------------|--------|--------------|
| 3.1 | Create `src/crew.py` | Crew definition: load YAML config, instantiate agents/tasks, configure Process.sequential | Planned | 2.1, 2.2 |
| 3.2 | Create `src/main.py` | CLI entry point: collect job requirements, run crew, handle output | Planned | 3.1 |

### Phase 4: Testing & Validation

| # | Task | Description | Status | Dependencies |
|---|------|-------------|--------|--------------|
| 4.1 | Verify API connectivity | Confirm Anthropic and SerperDev keys work; test a single agent in isolation | Planned | 3.1 |
| 4.2 | End-to-end test run | Run full pipeline with sample input: "Senior Python Developer, London, 5+ years" | Planned | 3.2, 4.1 |
| 4.3 | Validate output quality | Check report against eval criteria in PRD Section 6b | Planned | 4.2 |
| 4.4 | Error handling test | Test with missing API key, empty search results | Planned | 4.2 |

---

## Build Dependencies Graph

```
1.1 (directories)
 │
 ├──> 1.2 (requirements.txt)
 ├──> 1.3 (.env.example)
 ├──> 1.4 (.gitignore)
 │
 └──> 2.1 (agents.yaml)
       │
       └──> 2.2 (tasks.yaml)
             │
             └──> 3.1 (crew.py)
                   │
                   └──> 3.2 (main.py)
                         │
                         └──> 4.1 → 4.2 → 4.3
                                         → 4.4
```

---

## Key Implementation Notes

1. **Start with YAML config, not Python code.** Getting agent definitions right in YAML first means `crew.py` is a thin orchestration layer. Most iteration will happen in config files.

2. **Test one agent before wiring the crew.** Verify the Researcher agent can call SerperDev and return results before building the full pipeline. This catches API configuration issues early.

3. **The Evaluator's task description is critical.** The scoring rubric (skills match, experience relevance, location fit — each scored 1-5) must be explicitly stated in the task description. Vague instructions produce vague scores.

4. **Output handling is the last step.** Get the crew running end-to-end first, then add file output. Terminal output is sufficient for initial testing.

5. **Anthropic model string:** Use `anthropic/claude-sonnet-4-20250514` (litellm format). Verify this works with CrewAI 1.9.3 during task 4.1. Fallback: set model programmatically in `crew.py` if YAML config does not support it.

---

## Sources

- SAD: `project-context/2.build/sad.md`
- PRD: `project-context/1.define/prd.md` (Sections 3, 6b, 8)
- Decisions log: `project-context/1.define/decisions.md`
