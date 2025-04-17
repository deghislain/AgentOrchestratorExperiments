import logging
from typing import List, Dict
from beeai_framework.agents.react import ReActAgent
from web_utils import AgentOutput

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
    def __init__(self, process_steps: List[str], team: Dict[str, ReActAgent]):
        self.data = {}
        self.callbacks = {}
        self.process_steps = process_steps
        self.team = team
        self.running_agent = ""
        self.current_step = ""

    async def add_record(self, record_id: str, data):
        logger.info(f"**************add_record START with input: {record_id} and: {data}")
        self.data[record_id] = data
        if record_id in self.callbacks:
            await self.callbacks[record_id](data)
        logger.info(f"**************add_record END******************")

    def register_callback(self, record_id, callback):
        self.callbacks[record_id] = callback

    def get_next_step(self, current_step: str):
        try:
            index_next_step = self.process_steps.index(current_step) + 1
            if index_next_step < len( self.process_steps):
                return self.process_steps[index_next_step]
            else: return None

        except ValueError:
            return None


def update_context(context):
    async def handle_context_update(data):
        for key in context.team.keys():
            logger.info(f"handle_context_update//////////////////////////////////////////// {key}")
            agent = context.team[key]
            context.running_agent = key
            next_step = context.get_next_step(context.current_step)
            if next_step is not None:
                context.current_step = next_step
                logger.info(f"************** handle_context_update with input: {data}. Current agent: {key}--------")
                prompt = f""" You are an AI agent with access to {data}. Your task is to follow the provided process steps as ordered in
                in the following list: {context.process_steps}. 
                This is the current step {next_step},  only execute it if it aligns with your capabilities."""

                result = await agent.run(prompt)
                logger.info(f"************** handle_context_update Current agent: {agent.name} //***- output: {result.result.text}")
                await agent.update_context(context, result.result.text, agent.name)
            else:
                logger.info(f"**************----------------------------------------- Process completed")

    context.register_callback(f"{context.running_agent} : output", handle_context_update)


