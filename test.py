import asyncio
import threading
import time
from dataclasses import dataclass
from beeai_framework.adapters.ollama import OllamaChatModel
from beeai_framework.agents.react import ReActAgent
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.memory.token_memory import TokenMemory

llm = OllamaChatModel(model_id="granite3.3:2b", settings={})


@dataclass
class Context:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def update_context(self, agent_name, output):
        with self.lock:
            self.data[agent_name + " output: "] = output


class Agent:
    def __init__(self, name, context, event):
        self.name = name
        self.context = context
        self.event = event

    async def listen_to_context(self, prompt):
        print('listen_to_context*********************')
        #while True:
        #self.event.wait()
        self.event.clear()
        running_agent_output = self.name + " output: "
        #if running_agent_output not in self.context.data.keys():
        print(f"{self.name} received context update: {self.context.data}")
        print('complete_task*********************')
        agent = ReActAgent(llm=llm, tools=[DuckDuckGoSearchTool()], memory=TokenMemory(llm))
        result = await agent.run(prompt)
        print(f"Result***************************: {result.result.text}")
        time.sleep(2)
        self.context.update_context(self.name, result.result.text)
        print(f"{self.name} completed task")
        self.event.set()  # Notify other agent


    '''
    async def complete_task(self):
        print('complete_task*********************')
        agent = ReActAgent(llm = llm, tools=[DuckDuckGoSearchTool()], memory=TokenMemory(llm))
        result = await agent.run("what is AI?")
        print(f"Result***************************: {result.result.text}")
        time.sleep(2)
        self.context.update_task_status(self.name, "Completed")
        print(f"{self.name} completed task")
        self.event.set()  # Notify other agent
    '''


async def main():
    context = Context()
    event = threading.Event()

    agent1 = Agent("Agent1", context, event)
    agent2 = Agent("Agent2", context, event)

    await agent1.listen_to_context("What is AI?")
    await agent2.listen_to_context("What is Machine Learning?")
    #threading.Thread(target=agent2.listen_to_context, daemon=True).start()

    # Trigger initial task
    event.set()

    # Keep the main thread alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
