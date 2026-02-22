# Lessons Learned

## Project: Recruitment Assistant

### What Went Well

- **AAMAD structure gave clear phases** — Define → Build → Deliver meant I always knew what to do next and what artefacts were expected
- **Eval-driven development** — Defining per-agent evaluation criteria in the PRD before building meant I could validate output quality against clear benchmarks
- **Worktree-based persona isolation** — Using git worktrees for each AAMAD persona (System Architect, Backend Engineer) kept each session focused on its own scope
- **Config-driven agents** — YAML configuration for agents and tasks made the system easy to modify without touching Python code
- **Sequential pipeline worked first time** — The Researcher → Evaluator → Reporter chain produced a coherent end-to-end result on the first real test run

### Challenges Encountered

- **Claude Code vs Cursor adaptation** — Course materials assume Cursor. Had to create a translation layer (cursor-vs-claude-code.md) and adapt persona invocation patterns
- **CrewAI + Anthropic setup** — Needed the `crewai[anthropic]` extra and `anthropic/` prefix for model names via litellm. Not obvious from docs alone
- **Persona scope boundaries** — The Backend Engineer occasionally tried to make architecture decisions. Separate worktrees helped enforce boundaries

### Key Insights

#### Define Phase
- The MRD and PRD aren't bureaucracy — they're the context engineering that makes the Build phase work. Without them, AI personas invent requirements
- The Agentic Architect's review (Experience + Business hats) caught gaps the PM persona couldn't: CLI being wrong for recruiters, missing per-agent eval criteria

#### Build Phase
- Planning documents (SAD, architecture plan, backend plan) before code saved significant rework
- YAML-based agent config is the right abstraction level for a three-agent system — enough flexibility without over-engineering

#### Deliver Phase

- Writing the runbook forced me to think about the application from a user's perspective rather than a builder's — similar to writing release notes in a product team
- Logging is more important for agentic apps than traditional software because you can't predict what the agents will do — you need the trail to understand what happened
- The Deliver phase felt familiar from PM work: you don't ship a feature without documentation, monitoring, and a way for support to troubleshoot
- Keeping deployment proportionate matters — Docker would have been over-engineering for a CLI learning exercise



### AAMAD Framework Observations

- The three-hat model (Technical, Experience, Business) maps well to how senior PMs already think — you're always switching between "can we build it," "will users want it," and "does it make business sense"
- AAMAD's gap: no explicit guidance on per-agent evaluation criteria in the Define phase. This should be standard — you can't build agents without knowing how you'll judge their output
- The persona-per-session pattern works better in Claude Code with worktrees than with Cursor's chat sessions, because worktrees give true file-level isolation

### Agentic Architect Reflections

- The Agentic Architect role is essentially a tech lead who orchestrates AI personas instead of human developers. The skills transfer directly from PM experience
- The three hats prevent tunnel vision — without the Business hat check, I might have over-engineered a Docker deployment for a learning exercise
- Knowing when to skip personas (I dropped Frontend and Integration Engineers) is as important as knowing when to use them

### Recommendations for Future Projects

- Start with per-agent eval criteria in the Define phase — make it a standard PRD section
- Use worktrees for persona isolation from the start, not as an afterthought
- Keep deployment proportionate to the project's actual needs — don't Docker everything
- Add CrewAI tracing early in Build, not just in Deliver — it helps debug agent behaviour during development

### Skills Developed

- Multi-agent system design with CrewAI (YAML config, sequential orchestration, tool assignment)
- AAMAD framework application (Define-Build-Deliver with persona orchestration)
- Context engineering for AI development workflows
- Operational documentation for agentic applications (deployment plans, monitoring, runbooks)
