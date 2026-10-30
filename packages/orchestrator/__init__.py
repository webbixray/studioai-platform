"""Orchestrator engine with language‑specific agents.

The orchestrator can schedule a thought (plan) which determines the
appropriate agent to handle the request.
"""
import asyncio
from typing import Dict, Any, Callable, Awaitable

# Base agent interface
class Agent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, task: Dict[str, Any]):  # pragma: no cover
        raise NotImplementedError

# Example language agents
class PythonAgent(Agent):
    async def run(self, task):
        prompt = task.get("brief", "")
        # Simulate generation
        await asyncio.sleep(0.1)
        return {"lang": "python", "generated": f"# Python code for: {prompt}
print('Hello')"}

class JavascriptAgent(Agent):
    async def run(self, task):
        prompt = task.get("brief", "")
        await asyncio.sleep(0.1)
        return {"lang": "js", "generated": f"// JS code for: {prompt}
console.log('Hello');"}

# Orchestrator core
class Orchestrator:
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
            # Plan: determine appropriate agent based on task type & language
            task_type = task.get("type")
            lang = task.get("lang")
            agent_name = None
            if task_type == "codegen":
                if lang == "python":
                    agent_name = "python"
                elif lang in ("js", "javascript", "node"):
                    agent_name = "javascript"
            if not agent_name:
                agent_name = "unknown"
            agent = self.agents.get(agent_name)
            if agent:
                print(f"{agent.name} handling task {task.get('id')} ({lang})")
                result = await agent.run(task)
                task['result'] = result
            else:
                print(f"No agent found for {agent_name}")
            self.task_queue.task_done()

    def run(self, n_workers: int = 1):
        for _ in range(n_workers):
            self.loop.create_task(self._worker())
        self.loop.run_forever()

    async def delegate(self, task: Dict[str, Any]):
        await self.schedule(task)

# Example usage
if __name__ == "__main__":
    orch = Orchestrator()
    orch.register(PythonAgent("python"))
    orch.register(JavascriptAgent("javascript"))
    # schedule a dummy codegen task
    orch.loop.create_task(orch.delegate({"id": "t100", "type": "codegen", "lang": "python", "brief": "create sample class"}))
    orch.run()
