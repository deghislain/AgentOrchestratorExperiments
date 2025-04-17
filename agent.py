from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import BaseMemory
from beeai_framework.tools import AnyTool
from web_context_handler import Context, update_context
from web_utils import AgentOutput
from pydantic import Field
from typing import List
import logging

logger = logging.getLogger('agent')
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


class Agent(ReActAgent):
    name: str = Field(description="Agent name")
    capabilities: List[str] = Field(description="Agent capabilities")
    description: str = Field(description="Agent description")

    def __init__(self, name: str, capabilities: List[str], description: str, llm: ChatModel, tools: list[AnyTool],
                 memory: BaseMemory):
        super().__init__(llm, tools, memory)
        self.name = name
        self.capabilities = capabilities
        self.description = description

    async def update_context(self, context: Context, agent_data: AgentOutput, current_step: str):
        logger.info(f"*************Agent updating the context********** with input: {agent_data.agent_name} and  {agent_data.agent_output}")
        update_context(current_step, context)

        await context.add_record(current_step, agent_data)
