import uuid
from typing import Dict
import asyncio
from beeai_framework.agents.react import ReActAgent

import random
import logging

logger = logging.getLogger('web_context')
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


class Context:
    def __init__(self, team: Dict[str, ReActAgent]):
        self.data = {}
        self.team = team

    async def add_record(self, agent_name: str, output):
        logger.info(f"*************add_record START with input: {agent_name} and: {output}")
        record_id = uuid.uuid1()
        self.data[record_id] = agent_name + " output= "+ output
        for agent in self.team.keys():
            logger.info(f"Creating tasks with Agent {agent}-/------//--------////")
            await asyncio.create_task(self._notify_agent(agent))
        logger.info(f"*************add_record END****************")

    def _update_context(self, new_data: str, agent_name: str):
        record_id = uuid.uuid1()
        self.data[record_id] = agent_name + " output= " + new_data

    async def _notify_agent(self, agent_name: str):
        logger.info(f"Notifying agent: {agent_name} with data: {self.data}................")

        prompt = f"""Having access to the following context: {self.data} and using your memory, your task is to retrieve
        the prompt that match your capabilities then use the tools at your disposal to execute it and returns the results. 
        USE OTHER AGENTS OUTPUT VALUE WHENEVER YOU SEE FIT.
        only execute it if it aligns with your capabilities."""

        result = await self.team[agent_name].run(prompt)
        self._update_context(result.result.text, agent_name)

        logger.info(f"///////////////////_notify_agent END: Agent {agent_name} output: {result.result.text}")
