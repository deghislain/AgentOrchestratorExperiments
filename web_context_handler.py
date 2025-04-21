from typing import Dict
import asyncio
from beeai_framework.agents.react import ReActAgent

import random
from typing import List
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
        self.callbacks = {}
        self.team = team
        self.running_agent = ""
        self.current_step = ""

    async def add_record(self, agent_name: str, output):
        logger.info(f"*************add_record START with input: {agent_name} and: {output}")
        code = random.randrange(100, 200)
        record_id = str(code) + "_" + agent_name + "_" + "Output"
        self.data[record_id] = output
        for agent in self.team.keys():
            logger.info(f"Creating tasks with Agent {agent}-/------//--------////")
            await asyncio.create_task(self._notify_agent(agent))
        logger.info(f"*************add_record END****************")

    async def _notify_agent(self, agent_name: str):
        #while True:
        logger.info(f"Notifying agent: {agent_name} with data: {self.data}................")

        prompt = f"""Having access to the following context: {self.data} and using your memory, your task is to retrieve
        the prompt that match your capabilities then use the tools at your disposal to execute it and returns the results. 
        only execute it if it aligns with your capabilities. YOU MUST ONLY RETURN YOUR FINAL ANSWER NO INTERMEDIARY STEPS OR RESULTS"""
        result = await self.team[agent_name].run(prompt)

        logger.info(f"///////////////////_notify_agent END: Agent {agent_name} output: {result.result.text}")

