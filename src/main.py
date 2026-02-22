"""
CLI entry point for the Recruitment Assistant.

Collects job requirements, runs the 3-agent sequential crew
(Researcher -> Evaluator -> Reporter), and outputs the final
recruitment report to the terminal and to output/report.md.

Usage:
    source ~/Projects/agentic-architect/.venv/bin/activate
    cd <project-root>
    python src/main.py

Source: SAD Section 4, architecture-plan.md Phase 3
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ensure the project root is on the Python path so we can import src.crew
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def _check_api_keys() -> None:
    """
    Validate that required API keys are present in the environment.

    Fails fast with a clear message if any key is missing, rather than
    letting the crew start and fail mid-execution.
    """
    missing = []
    if not os.getenv("ANTHROPIC_API_KEY"):
        missing.append("ANTHROPIC_API_KEY")
    if not os.getenv("SERPER_API_KEY"):
        missing.append("SERPER_API_KEY")

    if missing:
        print("ERROR: Missing required API keys in .env file:")
        for key in missing:
            print(f"  - {key}")
        print(f"\nCopy .env.example to .env and add your keys:")
        print(f"  cp .env.example .env")
        sys.exit(1)


def _collect_job_requirements() -> dict[str, str]:
    """
    Collect job requirements from the user via interactive prompts.

    Returns a dictionary with keys: job_title, skills, experience_level, location.
    """
    print("=" * 60)
    print("  RECRUITMENT ASSISTANT — Job Requirements Input")
    print("=" * 60)
    print()

    job_title = input("Job title (e.g. Senior Python Developer): ").strip()
    if not job_title:
        job_title = "Senior Python Developer"
        print(f"  Using default: {job_title}")

    skills = input("Required skills (comma-separated, e.g. Python, FastAPI, PostgreSQL): ").strip()
    if not skills:
        skills = "Python, FastAPI, PostgreSQL"
        print(f"  Using default: {skills}")

    experience_level = input("Experience level (e.g. 5+ years): ").strip()
    if not experience_level:
        experience_level = "5+ years"
        print(f"  Using default: {experience_level}")

    location = input("Location preference (e.g. London, UK): ").strip()
    if not location:
        location = "London, UK"
        print(f"  Using default: {location}")

    print()
    print("-" * 60)
    print(f"  Searching for: {job_title}")
    print(f"  Skills: {skills}")
    print(f"  Experience: {experience_level}")
    print(f"  Location: {location}")
    print("-" * 60)
    print()

    return {
        "job_title": job_title,
        "skills": skills,
        "experience_level": experience_level,
        "location": location,
    }


def _save_report(report: str) -> Path:
    """
    Save the final report to output/report.md.

    Creates the output directory if it does not exist.
    Returns the path to the saved file.
    """
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "report.md"
    output_path.write_text(str(report), encoding="utf-8")
    return output_path


def main() -> None:
    """Main entry point: load config, collect input, run crew, save output."""

    # Load environment variables from .env
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)

    # Opt out of CrewAI telemetry
    os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")

    # Validate API keys before doing anything else
    _check_api_keys()

    # Collect job requirements from the user
    inputs = _collect_job_requirements()

    # Build and run the crew
    from src.crew import build_crew

    print("Building crew...")
    crew = build_crew(inputs)

    print("Kicking off the recruitment pipeline...\n")
    result = crew.kickoff()

    # Display the final report
    print("\n" + "=" * 60)
    print("  RECRUITMENT REPORT")
    print("=" * 60 + "\n")
    print(result)

    # Save to file
    output_path = _save_report(result)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
