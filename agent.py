from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import BaseMemory
from beeai_framework.tools import AnyTool
from web_context_handler import Context
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
