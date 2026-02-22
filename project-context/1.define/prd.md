# Product Requirements Document — Recruitment Assistant

**Product:** Recruitment Assistant (Multi-Agent Candidate Sourcing & Evaluation)
**Framework:** CrewAI
**Author:** Product Manager Agent
**Date:** 2026-02-22
**Status:** Complete
**Scope:** Learning exercise (AAMAD Module 05)

---

## 1. Executive Summary

### Problem Statement

Recruitment teams are losing the battle against time-to-hire. 60% of companies saw increased time-to-hire in 2024 (up from 44% in 2023), 90% missed their 2026 hiring goals, and 56% of employers cite "not enough qualified candidates" as their biggest challenge [MRD sources 1-3]. Talent acquisition teams are overloaded — 27% report unmanageable workloads — yet AI adoption remains shallow: 99.8% of TA teams use or plan AI, but current tools focus on scheduling or keyword search, not the full sourcing-to-evaluation pipeline [MRD Section 1].

The gap is clear: no widely adopted solution automates candidate discovery through structured evaluation to ranked recommendations with transparent rationale.

### Solution Overview

A 3-agent sequential crew built with CrewAI that automates the core recruitment pipeline:

1. **Researcher** — discovers candidate profiles via web search
2. **Evaluator** — scores and ranks candidates against structured criteria
3. **Reporter** — produces a formatted recruitment report with rationale

The system takes a job description as input and produces a ranked candidate report as output. Communication and outreach are explicitly out of scope [decisions.md #2].

### Strategic Rationale

- **Why multi-agent?** Each recruitment stage (sourcing, evaluation, reporting) requires different skills and context. Specialised agents mirror how human recruitment teams divide labour — and CrewAI's sequential orchestration maps cleanly to this pipeline.
- **Why this scope?** A 3-agent sequential pattern is the simplest valid multi-agent architecture that demonstrates meaningful agent collaboration. It is proportionate to a learning exercise whilst covering the core CrewAI concepts: agent definition, task chaining, tool integration, and context passing.
- **Learning value:** Demonstrates AAMAD methodology end-to-end — from market research through requirements to build and test.

---

## 2. Market Context & User Analysis

### Target Personas

*Note: These personas describe the production use case. For this exercise, the "user" is the developer testing the CLI.*

| Persona | Pain Point | What They Need |
|---------|-----------|----------------|
| **In-house recruiter** (high-volume) | Hours spent on manual sourcing and screening | Automated candidate discovery and ranking |
| **Hiring manager** | Receives poorly matched shortlists | Candidates evaluated against explicit criteria with clear rationale |
| **Recruitment agency** | Managing multiple client requisitions | Scalable pipeline across roles |

### User Needs (from MRD)

- Reduce manual effort in the research-heavy, repetitive parts of the pipeline
- Structured evaluation against explicit criteria (not keyword matching)
- Transparent reasoning — an audit trail the recruiter can review
- Configurable criteria per role

### Competitive Landscape

| Category | Gap Our System Addresses |
|----------|------------------------|
| ATS platforms (Greenhouse, Lever) | Tracking-focused, not intelligent sourcing |
| Search tools (LinkedIn Recruiter) | Search but no automated evaluation |
| AI scheduling (GoodTime) | Coordination only, sourcing untouched |
| Sourcing bots | Low trust — high performers 40% less likely to use them [MRD] |

---

## 3. Technical Requirements & Architecture

### CrewAI Framework Specifications

- **Orchestration pattern:** Sequential (Researcher -> Evaluator -> Reporter)
- **Agent configuration:** YAML-based (CrewAI config-driven pattern)
- **Context passing:** Each agent receives the output of the previous agent as input
- **Process:** `Process.sequential`

### Core Agent Definitions

#### Agent 1: Researcher

- **role:** "Senior Talent Researcher"
- **goal:** "Find the best candidate profiles matching the job requirements by searching the web for relevant professional profiles, portfolios, and public information"
- **backstory:** "You are an experienced talent researcher who specialises in discovering hidden talent. You know how to craft effective search queries to find candidates across the web, including professional profiles, open-source contributions, blog posts, and public portfolios. You focus on finding candidates who match the specific technical skills, experience level, and location preferences provided."
- **tools:** [SerperDevTool, ScrapeWebsiteTool]
- **memory:** true
- **delegation:** false
- **max_iter:** 5
- **verbose:** true

#### Agent 2: Evaluator

- **role:** "Candidate Evaluation Specialist"
- **goal:** "Evaluate and rank candidates against the job requirements using a structured scoring rubric, providing clear rationale for each assessment"
- **backstory:** "You are a meticulous talent evaluator with deep expertise in skills assessment. You analyse candidate profiles against specific job criteria — technical skills, experience level, cultural indicators, and role fit. You use a structured scoring rubric to ensure consistency and always document your reasoning so recruiters can understand and trust your recommendations."
- **tools:** [] (works with data passed from Researcher)
- **memory:** true
- **delegation:** false
- **max_iter:** 3
- **verbose:** true

#### Agent 3: Reporter

- **role:** "Recruitment Report Analyst"
- **goal:** "Produce a clear, well-structured recruitment report that ranks candidates with scores, rationale, and recommended next steps for the recruiter"
- **backstory:** "You are a skilled recruitment analyst who transforms raw evaluation data into actionable reports. You present information clearly, highlight key strengths and concerns for each candidate, and structure the report so a busy recruiter can quickly identify the top candidates and understand why they were ranked that way."
- **tools:** [] (works with data passed from Evaluator)
- **memory:** true
- **delegation:** false
- **max_iter:** 2
- **verbose:** true

### Integration Requirements

| Integration | Purpose | Required? |
|-------------|---------|-----------|
| SerperDev API | Web search for candidate discovery | Yes (P0) |
| LLM provider (OpenAI or Anthropic) | Agent reasoning | Yes (P0) |
| ScrapeWebsiteTool (CrewAI built-in) | Extract candidate data from web pages | Yes (P0) |
| Job board APIs | Structured candidate data | No (P2, out of MVP scope) |

### Infrastructure (Learning Exercise Scope)

- **Environment:** Local development only
- **Dependencies:** Python 3.13+, CrewAI, crewai-tools
- **Storage:** No persistent storage; output to stdout/file
- **Configuration:** `.env` file for API keys, YAML for agent/task config

---

## 4. Functional Requirements

### P0 — Core Features (MVP)

| ID | Feature | User Story | Acceptance Criteria |
|----|---------|-----------|-------------------|
| F1 | Job requirements input | As a user, I can provide job requirements (title, skills, experience, location) so the system knows what to search for | CLI accepts structured input; crew receives requirements as context |
| F2 | Candidate sourcing | As a user, I want the system to find relevant candidate profiles online | Researcher agent returns a list of candidate profiles with name, source URL, and key details |
| F3 | Candidate evaluation | As a user, I want candidates scored against my criteria with clear rationale | Evaluator agent returns scored candidates with per-criterion ratings and written rationale |
| F4 | Recruitment report | As a user, I want a formatted report ranking candidates | Reporter agent produces a structured markdown report with rankings, scores, and recommendations |
| F5 | End-to-end pipeline | As a user, I can run the full pipeline with one command | `python main.py` (or equivalent) runs all 3 agents sequentially and outputs the final report |

### P1 — Enhanced Features (Post-MVP)

| ID | Feature | Description |
|----|---------|-------------|
| F6 | Configurable evaluation rubric | User can specify custom scoring criteria and weightings per search |
| F7 | Multiple output formats | Export report as markdown, JSON, or PDF |
| F8 | Search refinement | User can adjust search parameters and re-run with modified criteria |
| F9 | Cost tracking | Log and display token usage and API costs per run |

### P2 — Future Features (Out of Scope)

| ID | Feature | Description |
|----|---------|-------------|
| F10 | Communication agent | Draft personalised outreach messages to top candidates [decisions.md #2] |
| F11 | ATS integration | Push shortlisted candidates to Greenhouse, Lever, etc. |
| F12 | Persistent candidate database | Store and query previous search results |
| F13 | Web UI | Browser-based interface for non-technical users |

---

## 5. Non-Functional Requirements

*Kept brief — this is a learning exercise, not a production system.*

| Category | Requirement |
|----------|-------------|
| **Performance** | End-to-end pipeline completes in under 5 minutes for a typical search |
| **Reliability** | Graceful error handling if web search returns no results or API calls fail |
| **Observability** | Verbose logging enabled for all agents to observe handoffs and reasoning |
| **Cost control** | max_iter limits on all agents; max_rpm configurable at crew level |
| **Reproducibility** | Pinned dependency versions; consistent agent definitions via YAML config |
| **Security** | API keys stored in `.env` (not committed to version control) |

---

## 6. User Experience Design

### CLI Interface

The MVP interface is a command-line tool. The user interaction flow:

```
1. User runs the crew from terminal:
   $ python main.py

2. System prompts for (or reads from config):
   - Job title (e.g. "Senior Python Developer")
   - Required skills (e.g. "Python, FastAPI, PostgreSQL")
   - Experience level (e.g. "5+ years")
   - Location preference (e.g. "London, UK")

3. System displays progress:
   [Researcher] Searching for candidates...
   [Researcher] Found 8 candidate profiles
   [Evaluator] Evaluating candidates against criteria...
   [Evaluator] Scoring complete — 8 candidates ranked
   [Reporter] Generating recruitment report...

4. System outputs final report to terminal and/or file
```

### Agent Interaction Flow

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

### Transparency & Explainability

- Each agent's reasoning is logged (verbose mode)
- Evaluator provides per-criterion scores and written rationale
- Reporter includes source URLs so the recruiter can verify candidate information
- The sequential pattern makes the pipeline easy to follow and debug

### Agentic Architect Review Notes

*Experience hat (CLI): CLI is acceptable for this learning exercise where the "user" is the developer. For production, a web UI is needed — captured as P2 feature F13.*

*Experience hat (Evals): AAMAD's PRD template doesn't explicitly require per-agent eval criteria in the Define phase. This is a gap — you can't build agents without knowing what good output looks like. The criteria below were added during Agentic Architect review.*

---

## 6b. Per-Agent Eval Criteria (Added by Agentic Architect Review)

*Defines what "good output" looks like for each agent. These serve as acceptance criteria during the Build phase.*

### Researcher Agent

| Field | Requirement |
|---|---|
| Candidate count | 5-10 per search |
| Per candidate | Name, current role, company, key skills, location, source URL |
| Nice to have | Experience level, portfolio/GitHub links |
| Quality signal | Each candidate has a sourcing note explaining why they match |
| Failure signal | Missing basic info, vague skills, no match rationale, or 50+ generic results |

### Evaluator Agent

| Field | Requirement |
|---|---|
| Scoring scale | 1-5 per criterion |
| Criteria (MVP) | Skills match, experience relevance, location fit |
| Per candidate | Score per criterion + written evidence/rationale |
| Output | Ranked list with total score and tier (e.g. Highly qualified: 12+/15) |
| Quality signal | Rationale is clear — you can understand why a candidate scored high or low |
| Failure signal | Scores with no reasoning, all candidates getting the same score |

### Reporter Agent

| Field | Requirement |
|---|---|
| Structure | Summary at top, ranked table, then per-candidate detail |
| Summary | Role searched, number found, number qualified, top recommendation |
| Per candidate | Name, score, tier, key strengths, key gaps, source URL |
| Quality signal | A recruiter could read this and take action without re-doing the research |
| Failure signal | Wall of text with no structure, missing evaluation rationale |

---

## 7. Success Metrics

*Traced from MRD Section 3 — User Experience and Workflow Analysis.*

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pipeline completes end-to-end | Yes | Crew runs without errors from input to report output |
| Report contains relevant candidates | Qualitative review | At least 3 candidates in the report are plausibly relevant to the job requirements |
| Evaluation rationale is clear and traceable | Qualitative review | Each candidate has per-criterion scores and written reasoning |
| Time from input to report | < 5 minutes | Wall-clock time for a single run |
| Agent handoffs work correctly | Yes | Each agent receives and uses context from the previous agent |
| AAMAD methodology demonstrated | Yes | Full artefact trail from MRD -> PRD -> architecture -> build -> test |

---

## 8. Implementation Strategy

### MVP Scope (This Exercise)

**Phase 1 — Core Pipeline:**

1. Set up CrewAI project structure with YAML agent/task config
2. Implement Researcher agent with SerperDevTool
3. Implement Evaluator agent with structured scoring rubric
4. Implement Reporter agent with markdown report output
5. Wire up sequential crew (Researcher -> Evaluator -> Reporter)
6. Create CLI entry point
7. End-to-end test with a sample job requirement

**What is NOT in MVP:**

- Custom evaluation rubrics (fixed criteria for MVP)
- Multiple output formats (markdown only)
- Persistent storage
- Web UI
- Communication/outreach agent

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Web search returns irrelevant candidates | Clear, specific search queries in Researcher agent prompt; test with known roles |
| Evaluation inconsistency | Structured scoring rubric baked into Evaluator backstory/task description |
| API rate limiting | Configure max_rpm at crew level; use max_iter limits |
| Token cost overrun | Set max_iter limits; monitor during testing |
| CrewAI breaking changes | Pin dependency versions in requirements.txt |

---

## 9. Launch & Go-to-Market

*This is a learning exercise, not a product launch. This section is minimal by design.*

- **"Launch"** = successful end-to-end run with a sample job requirement
- **Success criteria:** Pipeline runs, produces a coherent report, demonstrates all 3 agents collaborating sequentially
- **Demo scenario:** Search for "Senior Python Developer, London, 5+ years experience" and review the output report
- **Sharing:** Completed project serves as a portfolio piece and AAMAD methodology demonstration

---

## Development Crew Mapping

*Which AAMAD personas are needed for the Build phase, and what each produces.*

| AAMAD Persona | Responsibility | Key Output |
|---------------|---------------|------------|
| **Product Manager** | Requirements, scope, success criteria | MRD, PRD (this document) |
| **System Architect** | Agent architecture, task definitions, tool selection, data flow | Architecture document, YAML config specs |
| **Backend Engineer** | Implement agents, tasks, tools, crew orchestration | Python code, CrewAI config files, CLI entry point |
| **QA/Test Engineer** | End-to-end testing, edge cases, output validation | Test results, bug reports |

*Note: For this mini-project, Frontend Engineer and DevOps personas are not needed (CLI only, local dev).*

---

## Quality Assurance Checklist

- [x] All requirements traceable to MRD findings
- [x] Technical specifications feasible with CrewAI
- [x] Success metrics aligned with learning exercise objectives
- [x] Scope decisions respected (3 agents, no comms, sequential)
- [x] Risk mitigation documented for all medium-severity risks
- [x] Agent definitions include role, goal, backstory, tools, memory, delegation

---

## Sources

1. GoodTime — 2026 Hiring Statistics: https://goodtime.io/blog/talent-operations/hiring-statistics/
2. Select Software Reviews — Recruiting Statistics: https://www.selectsoftwarereviews.com/blog/recruiting-statistics
3. PR Newswire — HR Leaders Survey 2024: https://www.prnewswire.com/news-releases/survey-hr-leaders-say-recruiting-and-retaining-workers-is-getting-easier-but-challenges-remain-302169813.html
4. CrewAI Recruitment Example: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
5. CrewAI Documentation: https://docs.crewai.com/
6. MRD: `project-context/1.define/mrd.md`
7. Decisions Log: `project-context/1.define/decisions.md`

## Assumptions

- This is a learning exercise for AAMAD methodology, not a production recruitment tool
- SerperDev or equivalent web search API will be available (free tier sufficient for testing)
- CrewAI framework is stable enough for the exercise (pin versions)
- LLM provider choice (OpenAI vs Anthropic) to be confirmed — CrewAI supports both
- The focus is on demonstrating multi-agent orchestration patterns, not production-grade accuracy
- Publicly available web data is sufficient for candidate sourcing in this exercise

## Open Questions

1. **LLM provider:** OpenAI or Anthropic? CrewAI supports both, but default examples use OpenAI. Confirm based on available API credits.
2. **Test scenario:** Which specific job role for the demo run? Recommendation: "Senior Python Developer, London, 5+ years" — specific enough to get relevant results, broad enough to find candidates.
3. **Evaluation criteria:** Fixed rubric for MVP — but what criteria? Recommended starting set: technical skills match (40%), experience level (25%), location fit (15%), portfolio/evidence quality (20%).
4. **SerperDev free tier:** Sufficient API calls for development and testing? (100 free queries should be enough.)
5. **Output destination:** Print to terminal, save to file, or both? Recommendation: both (terminal + `output/report.md`).
