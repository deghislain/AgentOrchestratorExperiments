from beeai_framework.memory.token_memory import TokenMemory
from local_model import OllamaAIChatModel
from agent import Agent
from web_app_tools import search_web
from web_team_builder import TeamBuilder
from web_prompt import get_the_team_goal
import asyncio

llm = OllamaAIChatModel(model_id="llama3.2:latest", settings={})


def build_the_team() -> TeamBuilder:
    team = TeamBuilder()
    web_researcher = Agent(
        name="SearchAgent",
        capabilities=[
            {
                "id": "web_researcher",
                "name": "Web Search",
                "description": "Search the web for the given topic and returns a list of websites",
                "confidence": 0.9
            },
        ],
        description="This agents is equipped with tools that allows him to "
                    "search the web and return a list of websites given a topic.",
        llm=llm,
        tools=[search_web],
        memory=TokenMemory(llm)
    )
    team.register_agent(name="SearchAgent", agent=web_researcher)

    report_writer = Agent(
        name="ReportWriterAgent",
        capabilities=[

                    ],
        description="This agent is equipped with tools that given a list of websites, "
                    "it extract its contents and use the information related to a provided topic to write a report.",
        llm=llm,
        tools=[search_web],
        memory=TokenMemory(llm)
    )
    team.register_agent(name="ReportWriterAgent", agent=report_writer)

    return team


async def main():
    team = build_the_team()
    agent_orchestrator = Agent(
        name="SystemOrchestrator",
        capabilities=[
            {
                "id": "orchestrator",
                "name": "System Orchestrator",
                "description": "Given a list of websites, extract its contents "
                               "and use the information related to a provided topic to write a report.",
                "confidence": 0.9
            },
        ],
        description="specialized in searching the web",
        llm=llm,
        tools=[search_web],
        memory=TokenMemory(llm))

    result = await agent_orchestrator.run(get_the_team_goal())
    print(result.result.text)


if __name__ == "__main__":
    asyncio.run(main())
