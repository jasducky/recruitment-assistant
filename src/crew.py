"""
Crew definition for the Recruitment Assistant.

Loads agent and task definitions from YAML configuration files and
assembles a sequential CrewAI crew: Researcher -> Evaluator -> Reporter.

Source: SAD Sections 2-3, architecture-plan.md Phase 3
"""

import logging
import os
from pathlib import Path

import yaml
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

logger = logging.getLogger("recruitment_assistant.crew")


# Project root is one level up from src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


def _load_yaml(filename: str) -> dict:
    """Load and parse a YAML configuration file from the config directory."""
    filepath = CONFIG_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    logger.info("Loading configuration from %s", filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_tools(agent_name: str) -> list:
    """
    Return the tool instances for a given agent.

    Only the Researcher agent uses external tools (SerperDevTool for web
    search, ScrapeWebsiteTool for extracting page content). The Evaluator
    and Reporter work purely with context passed from previous agents.
    """
    if agent_name == "researcher":
        return [SerperDevTool(), ScrapeWebsiteTool()]
    return []


def _create_agents(agents_config: dict) -> dict[str, Agent]:
    """
    Create Agent instances from YAML configuration.

    Each agent is configured with its role, goal, backstory, LLM model,
    tools, and behavioural settings as defined in agents.yaml.
    """
    agents = {}
    for name, config in agents_config.items():
        logger.info("Creating agent: %s (role: %s)", name, config["role"])
        agents[name] = Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=config.get("llm", "anthropic/claude-sonnet-4-20250514"),
            tools=_build_tools(name),
            memory=config.get("memory", True),
            allow_delegation=config.get("allow_delegation", False),
            max_iter=config.get("max_iter", 5),
            verbose=config.get("verbose", True),
        )
    logger.info("All %d agents created successfully", len(agents))
    return agents


def _create_tasks(
    tasks_config: dict,
    agents: dict[str, Agent],
    inputs: dict[str, str],
) -> list[Task]:
    """
    Create Task instances from YAML configuration.

    Tasks are created in the order defined in tasks.yaml. Context
    dependencies (which previous tasks feed into each task) are wired
    up based on the 'context' field in the YAML.

    The task descriptions use {placeholders} which are interpolated
    with the job requirements provided at runtime.
    """
    tasks_by_name: dict[str, Task] = {}
    task_list: list[Task] = []

    for name, config in tasks_config.items():
        logger.info("Creating task: %s (agent: %s)", name, config["agent"])
        # Interpolate job requirement placeholders in description
        description = config["description"].format(**inputs)
        expected_output = config["expected_output"].format(**inputs)

        # Resolve context dependencies (previous tasks whose output
        # feeds into this task)
        context_tasks = []
        if "context" in config:
            for ctx_name in config["context"]:
                if ctx_name in tasks_by_name:
                    context_tasks.append(tasks_by_name[ctx_name])

        # Look up the agent by name
        agent_name = config["agent"]
        if agent_name not in agents:
            raise ValueError(
                f"Task '{name}' references unknown agent '{agent_name}'. "
                f"Available agents: {list(agents.keys())}"
            )

        task = Task(
            description=description,
            expected_output=expected_output,
            agent=agents[agent_name],
            context=context_tasks if context_tasks else None,
        )
        tasks_by_name[name] = task
        task_list.append(task)

    logger.info("All %d tasks created successfully", len(task_list))
    return task_list


def build_crew(inputs: dict[str, str]) -> Crew:
    """
    Build and return the Recruitment Assistant crew.

    Loads agent and task definitions from YAML configuration,
    creates all instances, and assembles a sequential crew.

    Args:
        inputs: Job requirement fields —
            job_title, skills, experience_level, location

    Returns:
        A configured Crew ready to be kicked off.
    """
    logger.info("Loading agent and task configuration")
    agents_config = _load_yaml("agents.yaml")
    tasks_config = _load_yaml("tasks.yaml")

    agents = _create_agents(agents_config)
    tasks = _create_tasks(tasks_config, agents, inputs)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        max_rpm=10,
        # To enable CrewAI tracing (requires `crewai login` first):
        # tracing=True,
    )

    logger.info("Crew built successfully (%d agents, %d tasks, sequential process)",
                len(agents), len(tasks))
    return crew
