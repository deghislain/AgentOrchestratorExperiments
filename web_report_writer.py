from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.adapters.ollama import OllamaChatModel
from web_team_builder import build_the_team
from agent import Agent, Context
from web_prompt import get_the_team_goal
from web_utils import retrieve_agent_capabilities
import asyncio
import logging

llm = OllamaChatModel(model_id="granite3.3:2b", settings={})
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


async def main():
    #event = threading.Event()
    agent_orchestrator = Agent(
        name="SystemOrchestrator",
        capabilities=[
            """
                        Decomposes complex goals into smaller, manageable tasks, and orchestrates the workflow between 
                        multiple specialized agents, assigning tailored prompts and integrating their outputs to achieve 
                        the desired outcome.
                        """
        ],
        description="specialized decomposing complex tasks into smaller manageable tasks",
        llm=llm,
        tools=[],
        memory=TokenMemory(llm),
    )

    details_report = """  Ensure the report has the following structure and information:
                          Definition of Artificial Intelligence (AI). Brief history and development of AI
                          Importance and relevance of AI in modern times
                    """

    team = await build_the_team()
    agents = team.get_the_team()
    agents_capabilities = retrieve_agent_capabilities(agents)
    number_agents = len(agents)
    complete_prompt = get_the_team_goal(details_report, agents_capabilities, number_agents)
    logger.info(f"*****************complete_prompt= {complete_prompt}***************")
    result = await agent_orchestrator.run(complete_prompt)
    logger.info(f"*****************Agent Orchestrator response= {result.result.text}***************")

    context = Context(team=agents)
    #context.data[agent_orchestrator.name + " Output: "] = result.result.text
    await context.add_record(agent_orchestrator.name, result.result.text)


if __name__ == "__main__":
    asyncio.run(main())
