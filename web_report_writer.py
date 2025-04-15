from beeai_framework.memory.token_memory import TokenMemory
from local_model import OllamaAIChatModel
from agent import Agent
from web_app_tools import search_web
from web_team_builder import TeamBuilder
from web_prompt import get_the_team_goal
from web_utils import retrieve_agent_capabilities
import asyncio
import logging

llm = OllamaAIChatModel(model_id="llama3.2:latest", settings={})
logger = logging.getLogger('web_search_report_writer')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def build_the_team() -> TeamBuilder:
    logger.info("*****************build_the_team START***************")
    team = TeamBuilder()
    web_researcher = Agent(
        name="SearchAgent",
        capabilities=[
                        """
                        Conduct a targeted web search for a specified topic and return a curated list of relevant 
                        websites, prioritizing credible sources such as academic journals, research papers, government 
                        websites, and reputable news outlets.
                        """
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
                        """
                            Given a list of curated websites and a specified topic, extract relevant content, 
                            analyze and synthesize the information,and write a well-structured report.
                        """

                    ],
        description="This agent is equipped with tools that given a list of websites, "
                    "it extract its contents and use the information related to a provided topic to write a report.",
        llm=llm,
        tools=[search_web],
        memory=TokenMemory(llm)
    )
    team.register_agent(name="ReportWriterAgent", agent=report_writer)
    logger.info("*****************build_the_team END***************")
    return team


async def main():
    team = build_the_team()
    agent_orchestrator = Agent(
        name="SystemOrchestrator",
        capabilities=[
                        """
                        Decomposes complex goals into smaller, manageable tasks, and orchestrates the workflow between 
                        multiple specialized agents, assigning tailored prompts and integrating their outputs to achieve 
                        the desired outcome.
                        """
        ],
        description="specialized in searching the web",
        llm=llm,
        tools=[],
        memory=TokenMemory(llm))

    details_report = """  Ensure the report has the following structure and information:
                          Definition of Artificial Intelligence (AI). Brief history and development of AI
                          Importance and relevance of AI in modern times
                    """

    agents_capabilities = retrieve_agent_capabilities(team.get_the_team())
    number_agents = len(team.get_the_team())
    complete_prompt = get_the_team_goal(details_report, agents_capabilities, number_agents)
    logger.info(f"*****************complete_prompt= {complete_prompt}***************")
    result = await agent_orchestrator.run(complete_prompt)
    logger.info(f"*****************Agent Orchestrator response= {result.result.text}***************")
    print(result.result.text)


if __name__ == "__main__":
    asyncio.run(main())
