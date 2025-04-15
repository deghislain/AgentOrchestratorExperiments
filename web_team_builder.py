from typing import Dict
from beeai_framework.agents.react import ReActAgent


class TeamBuilder:
    def __init__(self):
        self.team: Dict[str, ReActAgent] = {}

    def register_agent(self, name: str, agent: ReActAgent):
        """Register a new agent"""
        self.team[name] = agent

    def get(self, name: str) -> ReActAgent:
        """Get an agent."""
        if name not in self.team:
            raise ValueError(f"This agent {name} is not part of the team")
        return self.team[name]

    def has(self, name: str) -> bool:
        """Check if an agent is part of the team"""
        return name in self.team

    def get_the_team(self):
        """Return the list of registered agents"""
        return self.team
