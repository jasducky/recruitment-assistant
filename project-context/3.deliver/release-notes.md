# Release Notes — v1.0.0

**Release date:** 2026-02-22

---

## Summary

Initial release of the Recruitment Assistant, a multi-agent candidate sourcing and evaluation system built with CrewAI as an AAMAD methodology learning exercise.

---

## Features

- **3-agent sequential pipeline:** Researcher, Evaluator, and Reporter agents working in sequence
- **Web-based candidate sourcing:** Researcher agent uses SerperDev API and web scraping to discover candidate profiles
- **Structured evaluation:** Evaluator agent scores candidates across three dimensions (skills match, experience relevance, location fit) using a 1-5 rubric
- **Formatted recruitment report:** Reporter agent produces a markdown report with executive summary, ranked table, detailed profiles, and recommendations
- **CLI interface:** Interactive prompts for job title, skills, experience level, and location (with sensible defaults)
- **Application logging:** INFO and ERROR level logging to console and `logs/app.log`
- **Startup script:** `run.sh` with virtual environment activation and pre-flight checks

---

## Deployment Method

Local Python script. See [deployment plan](deployment-plan.md) and [runbook](runbook.md) for full instructions.

```bash
python src/main.py
# or
./run.sh
```

---

## Known Limitations

- **No persistent storage** — each run is independent; previous results are overwritten
- **Web scraping reliability** — some target websites may block scraping, leading to incomplete candidate data
- **Location filtering** — the Researcher agent may return candidates outside the target location; filtering happens at the evaluation stage rather than at search time
- **Single LLM provider** — currently configured for Anthropic (Claude); switching providers requires code changes
- **No retry logic** — if an API call fails, the agent iteration limit controls retries but there is no dedicated retry/backoff mechanism
- **CLI only** — no web UI or API endpoint

---

## Next Steps (potential enhancements)

- Add location-aware search queries to improve Researcher accuracy
- Implement configurable LLM provider (support OpenAI alongside Anthropic)
- Add retry logic with exponential backoff for API calls
- Support batch processing (multiple job descriptions in one run)
- Add output format options (JSON, CSV alongside markdown)
- Enable CrewAI tracing by default for production monitoring
