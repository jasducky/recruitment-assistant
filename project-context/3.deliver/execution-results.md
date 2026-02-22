# Execution Results

**Date:** 2026-02-22
**Phase:** Build phase validation run (Module 06)

---

## Test Run Summary

| Field | Value |
|-------|-------|
| **Input: Job title** | Senior Python Developer |
| **Input: Skills** | Python, FastAPI, PostgreSQL |
| **Input: Experience** | 5+ years |
| **Input: Location** | London, UK |
| **Candidates found** | 5 |
| **Candidates qualified (8+/15)** | 5 |
| **Top recommendation** | Asim Poptani (15/15) |

---

## Input

The test run used the default job requirements built into the CLI prompts:

- **Job title:** Senior Python Developer
- **Required skills:** Python, FastAPI, PostgreSQL
- **Experience level:** 5+ years
- **Location preference:** London, UK

---

## Output

The crew produced a structured recruitment report (`output/report.md`) containing:

1. **Executive summary** — role searched, candidate count, top recommendation
2. **Ranked candidate table** — 5 candidates scored out of 15 with tier labels
3. **Detailed profiles** — per-candidate breakdown across three scoring dimensions (skills match, experience relevance, location fit), each scored 1-5
4. **Recommendations** — prioritised action items for the recruiter

### Candidate Rankings

| Rank | Name | Score | Tier | Key Strength |
|------|------|-------|------|--------------|
| 1 | Asim Poptani | 15/15 | Highly Qualified | Perfect technical match + CTO leadership |
| 2 | Azeez Bello | 12/15 | Highly Qualified | Senior cloud expertise + London location |
| 3 | Annette Alcasabas | 10/15 | Qualified | Fintech Python development + analytical background |
| 4 | Victor Okoye | 9/15 | Qualified | 18+ years backend expertise + Django specialisation |
| 5 | Ada Richmond | 8/15 | Qualified | Met Office senior role + CS foundation |

---

## Observations

### What worked well

- **Structured scoring rubric:** The Evaluator agent applied the 3-dimension scoring (skills, experience, location) consistently across all candidates, producing transparent and comparable results.
- **Clear report format:** The Reporter agent produced a well-organised report with executive summary, ranked table, detailed profiles, and actionable recommendations.
- **Sequential pipeline:** Data flowed cleanly from Researcher (raw profiles) to Evaluator (scored profiles) to Reporter (formatted report) without manual intervention.

### Areas for improvement

- **Location accuracy:** Two candidates (Victor Okoye in Nigeria, Ada Richmond at Met Office) had low location fit scores. The Researcher agent could benefit from stronger location filtering in its search queries to avoid sourcing candidates outside the target area.
- **Skills verification depth:** Several candidates had "needs verification" notes for FastAPI and PostgreSQL. The Researcher agent's web search naturally has limited visibility into specific technical skills that are not prominently listed on profiles.
- **Candidate pool size:** 5 candidates is a reasonable minimum but a production system would benefit from sourcing more candidates to give the Evaluator a larger pool to rank.

### Validation against success criteria

Per the PRD success metrics:

| Criterion | Target | Result | Status |
|-----------|--------|--------|--------|
| Candidates returned | >= 3 | 5 | Pass |
| Scoring dimensions applied | 3 (skills, experience, location) | 3 | Pass |
| Report includes rankings | Yes | Yes | Pass |
| Report includes rationale | Per-candidate | Yes (per criterion) | Pass |
| End-to-end execution | Completes without error | Yes | Pass |

---

## Full Report

The complete report is available at `output/report.md`.
