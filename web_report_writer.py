from beeai_framework.memory.token_memory import TokenMemory
from beeai_framework.adapters.ollama import OllamaChatModel
from beeai_framework.agents.react import ReActAgent
from web_team_builder import build_the_team
from web_context_handler import Context
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
    details_report = """  Ensure the report has the following structure and information:
                             1.Definition of Artificial Intelligence (AI). 
                             2.Brief history and development of AI
                             3.Importance and relevance of AI in modern times.
                            THE FINAL REPORT MUST BE IN MARKDOWN FORMAT.
                       """
    agent_orchestrator = ReActAgent(llm=llm, tools=[], memory=TokenMemory(llm))

    team = await build_the_team()
    agents = team.get_the_team()
    agents_capabilities = retrieve_agent_capabilities(agents)
    number_agents = len(agents)
    complete_prompt = get_the_team_goal(details_report, agents_capabilities, number_agents)
    logger.info(f"*****************complete_prompt= {complete_prompt}***************")
    result = await agent_orchestrator.run(complete_prompt)
    logger.info(f"*****************Agent Orchestrator response= {result.result.text}***************")

    context = Context(team=agents)

    await context.add_record("SystemOrchestrator", result.result.text)


if __name__ == "__main__":
    asyncio.run(main())
