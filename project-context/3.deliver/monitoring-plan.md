# Monitoring Plan

**Status:** Complete
**Last updated:** 2026-02-22

---

## Logging Setup

The application uses Python's standard `logging` module with two output handlers:

### Console handler (StreamHandler)

- **Level:** INFO
- **Format:** `[LEVEL] message`
- **Purpose:** Quick visibility during interactive use

### File handler (FileHandler)

- **Level:** INFO
- **Format:** `2026-02-22 14:30:00 [INFO] recruitment_assistant — message`
- **Location:** `logs/app.log`
- **Purpose:** Persistent log for post-run analysis and debugging

### Log levels used

| Level | When used |
|-------|-----------|
| INFO | App startup, config loading, agent/task creation, execution milestones, completion |
| ERROR | Exceptions during crew execution (includes full traceback via `exc_info=True`) |

### What is logged

- Application startup
- Environment variable loading
- API key validation
- Job requirements collected (title, location, experience level)
- Configuration file loading (agents.yaml, tasks.yaml)
- Agent creation (name and role for each)
- Task creation (name and assigned agent for each)
- Crew assembly (agent count, task count, process type)
- Crew execution start and completion
- Report save location
- Any errors with full stack traces

---

## Log file management

Log files are written to `logs/app.log`. The `logs/` directory is created automatically at runtime. Log files are excluded from git (via `.gitignore`) but the directory is preserved with a `.gitkeep` file.

For a learning exercise, no log rotation is configured. If the log file grows large, delete it manually:

```bash
rm logs/app.log
```

---

## CrewAI Tracing

CrewAI provides a built-in tracing dashboard that shows agent execution, tool calls, and token usage.

### How to enable

1. **Log in to CrewAI** (one-time setup):
   ```bash
   crewai login
   ```
   This opens a browser for authentication and stores credentials locally.

2. **Uncomment the tracing parameter** in `src/crew.py`:
   ```python
   crew = Crew(
       ...
       tracing=True,  # uncomment this line
   )
   ```

3. **Run the application** as normal. Traces will appear in the CrewAI dashboard.

### What tracing shows

- Per-agent execution timeline
- Tool calls and their results
- Token usage per agent and per task
- Error details if an agent fails

### Note

Tracing is commented out by default because it requires the `crewai login` step. The application works without it — tracing is purely optional observability.
