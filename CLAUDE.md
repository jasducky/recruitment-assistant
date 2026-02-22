# Recruitment Assistant — AAMAD Project

## Overview

Mini-project for the Agentic Architect course. Building a recruitment assistant using the AAMAD framework (AI-Assisted Multi-Agent Application Development) with CrewAI.

## AAMAD Core Rules (adapted from .cursor/rules/)

### Context-First Engineering
- All outputs must trace to PRD, SAD, or user stories. Do not invent requirements.
- Every artifact includes Sources, Assumptions, and Open Questions sections.
- Store artifacts in the correct phase folder:
  - `project-context/1.define/` — MRD, PRD
  - `project-context/2.build/` — SAD, backend.md, frontend.md
  - `project-context/3.deliver/` — runbook, deployment docs

### Persona-Based Development
- Each persona has defined inputs, outputs, and prohibited actions.
- Persona files are in `.cursor/agents/` (AAMAD originals) and `.claude/agents/` (Claude Code copies).
- When the course says `@product-mgr`, read and adopt the persona from `.claude/agents/product-mgr.md`.
- When invoking other personas, copy them to `.claude/agents/` first.

### Development Workflow
- Work in modules with focused scope. Do not attempt end-to-end development in a single session.
- Complete each module fully before proceeding to the next.
- Reference previous module outputs via files, not conversation history.

### Templates
- Use AAMAD templates from `.cursor/templates/` when creating MRD, PRD, or SAD.
- Follow template headings exactly.

### Two Crews — Don't Confuse Them
- **Development Crew** (temporary): AI personas that build the app (Product Manager, System Architect, Backend Engineer, etc.)
- **Application Crew** (permanent): The agents that run in production (Researcher, Evaluator, Recommender)

## Cursor → Claude Code Translation

| Course instruction | Claude Code equivalent |
|---|---|
| `@product-mgr` | Read `.claude/agents/product-mgr.md` and adopt persona |
| `@system-arch` | Read `.claude/agents/system-arch.md` and adopt persona |
| `.cursor/rules/` | This CLAUDE.md (auto-loaded) |
| `.cursor/templates/` | Same location, read when needed |
| "Open a new Cursor chat" | Start a new Claude Code session or use a subagent |
| "Check your rules panel" | Rules are in this CLAUDE.md, always auto-loaded |

## Key Files

| File | Purpose |
|------|---------|
| `.cursor/templates/mr-template.md` | Market Research template |
| `.cursor/templates/prd-template.md` | PRD template |
| `.cursor/templates/sad-template.md` | SAD template |
| `.cursor/agents/` | All AAMAD persona definitions |
| `.cursor/prompts/prompt-phase-1` | Define phase prompt |
| `project-context/` | All phase artifacts |
