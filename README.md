AgentOrchestratorExperiments

This project explores the utilization of context in orchestrating a multi-agent system, focusing on the decomposition of goals into tasks 
and distribution among specialized agents.
Functionality & Workflow

    Upon receiving a goal, the Agent Orchestrator generates a set of sub-tasks (prompts).
    These tasks are added to a shared context, accessible by all agents.
    Each agent retrieves its assigned task/prompt from the shared context.
    The agent performs the task using its specific capabilities.
    The result is returned to the shared context, where other agents can leverage it for their tasks.

Agents

    Agent Orchestrator: Central entity responsible for goal decomposition, task generation, and managing the shared context.
    Search Agent: Gathers information from various sources.
    Write Agent: Generates well-structured report based on the data fetched by the Search Agent.

Modules

    web_app_tools: Contains utilities needed to set up and manage the web application.
    web_context_handler: Manages the shared context where tasks and results are stored and retrieved by agents.
    web_team_builder: Facilitates the formation of agent teams, considering agents' capabilities and available tasks.
