from typing import Dict
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import SystemMessage

from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.adapters.ollama import OllamaChatModel
from agent import Agent
from web_app_tools import search_web, scrap_web_page
import logging

llm = OllamaChatModel(model_id="granite3.3:8b", settings={})
logger = logging.getLogger('web_report_writer')
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


async def build_the_team() -> TeamBuilder:
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
    await web_researcher.memory.add(SystemMessage(
        content="""Your name is SeArchAgent. You are a helpful assistant equipped with tools that allows you to search 
        the web and return a list of relevant websites given a user query. Leverage other agents' outputs to build your own 
        tools' inputs as needed to complete your tasks efficiently.
        
        For example, if you need to use the `search_web` tool, please provide a count of 5.
        YOU MUST RETURN WEBSITE LINKS AND NOT THEIR RESPECTIVE CONTENTS"""))

    team.register_agent(name="SearchAgent", agent=web_researcher)

    report_writer = Agent(
        name="WriteReportAgent",
        capabilities=[
            """
                           Extract relevant information, identify key themes and insights, from websites return by 
                           the SearchAgent to  generate a comprehensive, well-structured report.
                        """

        ],
        description="This agent is equipped with tools that given a list of websites, "
                    "it extract its contents and use the information related to a provided topic to write a report.",
        llm=llm,
        tools=[scrap_web_page],
        memory=TokenMemory(llm)
    )
    await report_writer.memory.add(SystemMessage(
        content="""
        Your name is WriteReportAgent. You are a helpful assistant equipped with tools that enables you to extract 
        relevant website contents and generate a comprehensive report based on a list of provided websites. Leverage other 
        agents' outputs to build your own tools' inputs as needed to complete your tasks efficiently.

        Specifically, utilize the `scrap_web_page` tool to extract data from web pages, ensuring a count of 5 is used 
        for optimal results. Alternatively, develop and refine your own techniques for extracting website contents or 
        modify existing tools to suit specific reporting needs.

        To further enhance your capabilities, explore integrating multiple agents' outputs to streamline your workflow 
        and produce high-quality reports. Please document your process and outcomes using relevant metadata, such as 
        report title, source websites, and extraction methods.
        """))

    team.register_agent(name="WriteReportAgent", agent=report_writer)
    logger.info("*****************build_the_team END***************")
    return team
