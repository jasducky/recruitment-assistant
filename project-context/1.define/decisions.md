# Decisions Log — Recruitment Assistant

Tracks all scope and design decisions for traceability. Updated as decisions are made.

## Scope Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| 1 | 3 agents: Researcher, Evaluator, Reporter | Simplified from CrewAI example's 4 agents. Keeps mini-project focused on core sourcing + evaluation flow | 2026-02-22 |
| 2 | Communication/outreach is out of scope | Not core to the learning exercise. Can be added later if needed | 2026-02-22 |
| 3 | IDE: Claude Code, not Cursor | Full feature mapping shows equivalent capability. CLAUDE.md + .claude/agents/ replaces .cursor/ equivalents | 2026-02-22 |

## Architecture Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|

## Design Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| 4 | Define eval criteria per agent BEFORE build | PM thinking: you can't build agents without knowing what good output looks like. Eval-driven development — acceptance criteria for each agent's output shape the design, not just test it afterwards. AAMAD doesn't explicitly call this out in the Define phase, but it belongs here. | 2026-02-22 |
| 5 | CLI is acceptable for learning exercise only | Experience hat review: CLI works for demonstrating the pipeline but would need web UI for production users. Captured as P2 feature. | 2026-02-22 |

## Framework Improvement Notes

| # | Observation | What would need to change |
|---|------------|--------------------------|
| 1 | PRD template has no section for per-agent eval criteria / acceptance criteria | Add a "What Good Looks Like" section to `prd-template.md` requiring output definition per agent (expected fields, quality signals, failure signals) |
| 2 | PM persona prompt (`prompt-phase-1`) doesn't ask for eval criteria | Update prompt to include: "For each agent in the Application Crew, define what good output looks like, including expected data fields, scoring approach, and failure signals" |
| 3 | CLI noted as poor UX in Experience hat review | PRD template could prompt for UX rationale — "Why is this interface appropriate for the target user?" |

## Sources
- CrewAI recruitment example: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
- Module 05 exercise instructions
- AAMAD templates (.cursor/templates/)

## Open Questions
- Does Julia need OpenAI API credits or can she use Anthropic API with CrewAI?
- Capstone project idea — to be selected in Week 1
