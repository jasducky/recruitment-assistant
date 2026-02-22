# Deployment Plan

**Status:** Complete
**Last updated:** 2026-02-22

---

## Deployment Approach

This project is deployed as a **local Python script**. Given that this is a learning exercise (AAMAD mini-project), a local deployment is the simplest and most appropriate approach. Docker containerisation is documented as an optional enhancement but is not required.

### Why local deployment?

- Single-user CLI application — no need for a server or orchestration
- API keys are managed locally via `.env`
- Output is a markdown file written to `output/report.md`
- No persistent storage, web UI, or multi-user access

---

## Required Dependencies

All Python dependencies are listed in `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| crewai[anthropic] | 1.9.3 | CrewAI framework with Anthropic LLM support |
| crewai-tools | 1.9.3 | SerperDevTool and ScrapeWebsiteTool |
| python-dotenv | >=1.0.0 | Load `.env` file into environment |

### System requirements

- Python 3.13+ (tested with 3.13.7)
- pip (for installing dependencies)
- Internet access (required for SerperDev API and Anthropic API calls)

---

## Environment Setup

### API keys (required)

Create a `.env` file in the project root with the following keys:

```
ANTHROPIC_API_KEY=your-anthropic-api-key
SERPER_API_KEY=your-serper-api-key
```

- **ANTHROPIC_API_KEY** — used by all three agents for LLM inference (Claude)
- **SERPER_API_KEY** — used by the Researcher agent for web search (free tier sufficient)

A `.env.example` template is provided. Copy and fill in your keys:

```bash
cp .env.example .env
```

### CrewAI telemetry

The application automatically opts out of CrewAI telemetry by setting `CREWAI_TELEMETRY_OPT_OUT=true` at startup. No action needed.

---

## Step-by-Step Deployment Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd recruitment-assistant
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Check output**
   - The report prints to the terminal
   - A copy is saved to `output/report.md`

### Using the startup script

A convenience script `run.sh` is provided that handles virtual environment activation and pre-flight checks:

```bash
chmod +x run.sh
./run.sh
```

---

## Rollback Procedures

Since this is a git-managed local application, rollback is straightforward:

### Rollback to a previous version

```bash
# View recent commits
git log --oneline -10

# Roll back to a specific commit
git checkout <commit-hash>

# Or revert the last commit while preserving history
git revert HEAD
```

### Rollback dependency changes

```bash
# Reinstall pinned dependencies
pip install -r requirements.txt
```

### If .env is corrupted

```bash
# Restore from the example template
cp .env.example .env
# Re-enter your API keys
```

---

## Optional: Docker Deployment

For environments where Python version management is awkward, a Docker container could be used. This is not implemented but the approach would be:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

This is not a priority for a single-user learning exercise.
