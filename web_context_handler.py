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

    async def add_record(self, record_id: str, agent_data: AgentOutput):
        logger.info(f"**************add_record START with input: {record_id} and: {agent_data.agent_name}")
        self.data[record_id] = agent_data
        if record_id in self.callbacks:
            await self.callbacks[record_id](record_id, agent_data)
        logger.info(f"**************add_record END******************")

    def register_callback(self, record_id, callback):
        self.callbacks[record_id] = callback

    def get_next_step(self, current_step: str):
        try:
            index_next_step = self.process_steps.index(current_step)+1
            return self.process_steps[index_next_step]
        except ValueError:
            return None


def update_context(current_step, context):
    async def handle_context_update(current_step, agent_data: AgentOutput):
        previous_step_output = agent_data.agent_output
        logger.info(f"************** handle_context_update with input: {previous_step_output} and: {agent_data.agent_name}")
        next_step = context.get_next_step(current_step)
        for key in context.team.keys():
            if key.startswith(next_step):
                agent = context.team[key]
                logger.info(f" From context running {agent.name}")
                result = await agent.run(previous_step_output)
                logger.info(f" From context {agent.name} output: {result.result.text}")
                await context.add_record(next_step, agent_data)

    context.register_callback(current_step, handle_context_update)


