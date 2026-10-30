"""Simple Orchestrator Engine"""

import asyncio
from typing import Callable, Dict, Any

class Agent:
    """Base class for agent units. Each agent implements run() asynchronously."""
    def __init__(self, name: str):
        self.name = name

    async def run(self, task: Dict[str, Any]):  # pragma: no cover – interface
        """Execute the given task. Override in subclasses."""
        raise NotImplementedError

class Orchestrator:
    """Manages agent lifecycle and task delegation."""
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()

    def register(self, agent: Agent):
        self.agents[agent.name] = agent

    async def schedule(self, task: Dict[str, Any]):
        await self.task_queue.put(task)

    async def _worker(self):
        while True:
            task = await self.task_queue.get()
            target = task.get("agent")
            agent = self.agents.get(target)
            if agent:
                print(f"{agent.name} handling task {task['id']}")
                await agent.run(task)
            else:
                print(f"No agent found for {target}")
            self.task_queue.task_done()

    def run(self, n_workers: int = 1):
        for _ in range(n_workers):
            self.loop.create_task(self._worker())
        self.loop.run_forever()

# placeholder agent for code generation
class CodegenAgent(Agent):
    async def run(self, task):
        print(f"Generating code for {task.get('brief')}")
        # Placeholder: sleep and return dummy
        await asyncio.sleep(1)
        return {"status": "done"}

# example usage
if __name__ == "__main__":
    orch = Orchestrator()
    orch.register(CodegenAgent("codegen"))
    orch.run()
