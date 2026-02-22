# Market Research Document — Recruitment Assistant

**Primary Focus:** Automated candidate sourcing and evaluation system using CrewAI framework for recruitment teams
**Author:** Product Manager Agent
**Date:** 2026-02-22
**Status:** Complete (learning exercise scope)

---

## Executive Summary

**Market Opportunity:** The recruitment technology market faces a compounding problem. 60% of companies saw increased time-to-hire in 2024 — up from 44% in 2023 — and 90% of companies missed their 2026 hiring goals [1]. Talent acquisition teams are stretched thin: 27% of TA leaders report unmanageable workloads, 28% cite skills misalignment as their top challenge, and 56% of employers say "not enough qualified candidates" is their biggest issue [1][2][3]. AI adoption in recruitment is near-universal (99.8% of TA teams use, pilot, or plan AI agents), yet current tools focus narrowly on scheduling or keyword search rather than the full sourcing-to-evaluation pipeline [1]. There is a clear gap for intelligent, multi-stage automation.

**Technical Feasibility:** CrewAI provides a mature framework for multi-agent systems with sequential orchestration, config-driven agent definitions, and built-in tool integration. A 3-agent sequential pattern (Researcher, Evaluator, Reporter) maps cleanly to the existing human recruitment workflow and keeps complexity proportionate to a learning exercise. The CrewAI recruitment example [4] demonstrates the pattern with 4 agents; we simplify to 3 by dropping the Communicator agent (outreach is out of scope) and combining Matcher responsibilities into Evaluator.

**Recommended Approach:** Build a 3-agent sequential crew that automates candidate sourcing and evaluation, producing ranked candidate reports for recruiter review. Communication and outreach are explicitly out of scope per project decisions [decisions.md #1, #2].

---

## Detailed Findings

### 1. Market Analysis and Opportunity Assessment

**Key Insights:**

- **Time-to-hire is worsening.** 60% of companies saw increased time-to-hire in 2024, up from 44% in 2023. Only 6% reduced it [1]. This is a trend accelerating in the wrong direction.
- **Hiring goals are being missed at scale.** 90% of companies missed 2026 hiring goals; 1 in 3 missed by a wide margin [1].
- **Candidate quality is the top pain point.** 56% of employers say "not enough qualified candidates" is their biggest challenge [3]. 28% of TA leaders cite skills misalignment specifically [2].
- **TA teams are overloaded.** 27% of TA leaders report unmanageable workloads [1], creating a clear need for automation that handles the research-heavy, repetitive parts of the pipeline.
- **AI adoption is near-universal but shallow.** 99.8% of TA teams use, pilot, or plan AI agents [1]. However, high performers are 40% less likely to use sourcing bots [1], suggesting current automated sourcing tools lack the quality needed to be trusted.

**Target Audience (for a production version — noted for context):**

| Persona | Pain Point | Need |
|---------|-----------|------|
| In-house recruiter (high-volume) | Spends hours on manual sourcing | Automated candidate discovery and ranking |
| Hiring manager | Receives poorly matched shortlists | Candidates evaluated against explicit criteria with rationale |
| Recruitment agency | Managing multiple client requisitions | Scalable pipeline across roles |

**Competitive Landscape:**

| Category | Examples | Gap |
|----------|----------|-----|
| ATS platforms | Greenhouse, Lever, Workday | Tracking-focused, not intelligent sourcing |
| Search tools | LinkedIn Recruiter | Search but no automated evaluation or ranking |
| AI scheduling | GoodTime | Coordination only — users are 1.6x more likely to hit hiring goals [1], but sourcing untouched |
| Sourcing bots | Various | Low trust — high performers are 40% less likely to use them [1] |

**Market Gap:** No widely adopted solution automates the full pipeline from candidate sourcing through structured evaluation to ranked recommendations with transparent rationale.

### 2. Technical Feasibility and Requirements Analysis

**CrewAI Capabilities:**

- Sequential, hierarchical, and concurrent orchestration patterns supported
- Config-driven agent and task definitions via YAML
- Built-in tool integration (SerperDev web search, scraping, custom tools)
- Context passing between sequential tasks enables the pipeline pattern
- Active open-source community and documented examples [4][5]

**Agent Architecture (decided):**

| Agent | Role | Inputs | Outputs |
|-------|------|--------|---------|
| Researcher | Find candidate profiles matching job requirements | Job description, skills, location | List of candidate profiles with raw data |
| Evaluator | Score and rank candidates against criteria | Candidate profiles, evaluation rubric | Scored and ranked candidate list with rationale |
| Reporter | Produce structured report for recruiter review | Ranked candidates with scores | Formatted recruitment report |

- Sequential orchestration: Researcher → Evaluator → Reporter
- Each agent has clear inputs/outputs with no circular dependencies
- Simplified from CrewAI example's 4 agents (Researcher, Matcher, Communicator, Reporter) [4]

**Integration Requirements:**

- Web search API (SerperDev or similar) for candidate discovery
- LLM provider for agent reasoning (OpenAI or Anthropic via CrewAI)
- Optional: job board APIs, LinkedIn data (with ToS considerations)

**Technical Risks:**

| Risk | Severity | Mitigation |
|------|----------|------------|
| Web search returns irrelevant candidates | Medium | Clear search criteria and filtering logic in Researcher agent |
| Evaluation inconsistency across runs | Medium | Structured scoring rubric in Evaluator prompt |
| Web scraping reliability (incomplete/stale data) | Medium | Accept limitations for learning exercise; note for production |
| API rate limiting | Low | Configure max_rpm in CrewAI crew settings |
| Token cost overrun | Low | Set max_iter limits per agent |

### 3. User Experience and Workflow Analysis

**User Journey:**

1. Recruiter inputs job requirements (role title, required skills, experience level, location preferences)
2. Researcher agent discovers candidate profiles via web search
3. Evaluator agent scores candidates against requirements using structured criteria
4. Reporter agent produces a ranked report with evaluation rationale
5. Recruiter reviews report and decides next steps (outreach, interviews, etc.)

**Human-in-the-Loop Design:**

- **Input gate:** Recruiter defines job requirements before pipeline runs
- **Output gate:** Recruiter reviews final report before taking action
- **During processing:** Fully automated, no human intervention required

**Success Metrics (for this learning exercise):**

| Metric | Target |
|--------|--------|
| Pipeline completes end-to-end | Yes/No |
| Report contains relevant candidates | Subjective review |
| Evaluation rationale is clear and traceable | Subjective review |
| Time from input to report | Minutes, not hours |

### 4. Production and Operations Requirements

**For this mini-project (in scope):**

- Local development environment only
- CLI interface for running the crew
- No persistent storage required
- Logging for debugging agent behaviour and observing handoffs

**For production (out of scope — noted for awareness):**

- Cloud deployment, API endpoints, frontend integration
- Monitoring and observability for agent performance
- Cost tracking per search (LLM token usage)
- Data privacy and compliance considerations

### 5. Innovation and Differentiation Analysis

**What makes this approach different from existing tools:**

- **Multi-agent collaboration** — Specialised agents for each stage rather than one monolithic model doing everything
- **Structured evaluation** — Candidates scored against explicit criteria, not keyword matching
- **Transparent reasoning** — Each agent documents its process, creating an audit trail the recruiter can review
- **Configurable** — Agents defined in YAML; roles, goals, and criteria adjustable without code changes

**Honest limitations:**

- Relies on publicly available candidate data (no proprietary database access)
- LLM evaluation is probabilistic, not deterministic — results may vary between runs
- Cannot and should not replace human judgement for final hiring decisions
- This is a learning exercise, not a production-grade system

---

## Critical Decision Points

| Decision | Recommendation | Rationale | Reference |
|----------|---------------|-----------|-----------|
| Number of agents | 3 (Researcher, Evaluator, Reporter) | Covers core pipeline; Communicator dropped, Matcher merged into Evaluator | decisions.md #1 |
| Orchestration pattern | Sequential | Each step depends on previous output; simplest valid pattern | decisions.md #1 |
| Communication/outreach | Out of scope | Not core to sourcing and evaluation; can be added later | decisions.md #2 |
| Search tooling | SerperDev web search | Supported by CrewAI, avoids LinkedIn ToS issues | CrewAI docs [5] |

---

## Risk Assessment

| Level | Risk | Mitigation |
|-------|------|------------|
| **Medium** | Search returns irrelevant candidates | Clear search criteria, filtering in Researcher agent |
| **Medium** | Evaluation inconsistency across runs | Structured scoring rubric in Evaluator prompt |
| **Medium** | Incomplete candidate data from web sources | Accept for learning exercise; document limitation |
| **Low** | API rate limiting | Configure max_rpm in CrewAI crew settings |
| **Low** | Token cost overrun | Set max_iter limits per agent |
| **Low** | CrewAI framework breaking changes | Pin dependency versions |

---

## Actionable Recommendations

**Immediate (this exercise):**

- Create PRD based on these findings
- Define agent roles, goals, and backstories in detail
- Specify evaluation criteria and scoring rubric for the Evaluator agent
- Confirm LLM provider choice (OpenAI vs Anthropic with CrewAI)

**Short-term (Build phase):**

- Implement 3-agent crew with sequential pattern
- Set up SerperDev tool integration
- Create CLI interface for testing
- Run end-to-end test with a sample job requirement

---

## Sources

1. GoodTime — 2026 Hiring Statistics: https://goodtime.io/blog/talent-operations/hiring-statistics/
2. Select Software Reviews — Recruiting Statistics: https://www.selectsoftwarereviews.com/blog/recruiting-statistics
3. PR Newswire — HR Leaders Survey 2024: https://www.prnewswire.com/news-releases/survey-hr-leaders-say-recruiting-and-retaining-workers-is-getting-easier-but-challenges-remain-302169813.html
4. CrewAI Recruitment Example: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
5. CrewAI Documentation: https://docs.crewai.com/

## Assumptions

- This is a learning exercise for the AAMAD methodology, not a production recruitment tool
- The mini-project will use publicly available web data for candidate sourcing
- SerperDev or equivalent web search API will be available
- CrewAI framework is stable enough for the exercise (pin versions)
- The focus is on demonstrating multi-agent orchestration patterns, not production-grade accuracy

## Open Questions

- Which LLM provider will be used? (OpenAI vs Anthropic — CrewAI supports both)
- What specific job role will be used for testing? (e.g. "Senior Python Developer in London")
- Should evaluation criteria be configurable per search, or fixed for the MVP?
- Does the SerperDev free tier provide sufficient API calls for development and testing?
