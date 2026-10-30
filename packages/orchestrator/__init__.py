"""Orchestrator engine with language‑specific agents.

The orchestrator can schedule a thought (plan) which determines the
appropriate agent to handle the request.
"""
import asyncio
import os
from typing import Dict, Any

# Base agent interface
class Agent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, task: Dict[str, Any]):  # pragma: no cover
        raise NotImplementedError

# Example language agents using OpenAI chat completion
class PythonAgent(Agent):
    async def run(self, task):
        prompt = f"Generate Python code for: {task.get('brief', '')}"
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': prompt}]
            )
            code = response['choices'][0]['message']['content']
            return {'lang': 'python', 'generated': code}
        except Exception as e:
            return {'error': str(e)}

class JavascriptAgent(Agent):
    async def run(self, task):
        prompt = f"Generate JavaScript code for: {task.get('brief', '')}"
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': prompt}]
            )
            code = response['choices'][0]['message']['content']
            return {'lang': 'js', 'generated': code}
        except Exception as e:
            return {'error': str(e)}

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
            agent_name = None
            if task.get('type') == 'codegen':
                lang = task.get('lang')
                if lang == 'python':
                    agent_name = 'python'
                elif lang in ('js', 'javascript', 'node'):
                    agent_name = 'javascript'
            if not agent_name:
                agent_name = 'unknown'
            agent = self.agents.get(agent_name)
            if agent:
                print(f"{agent.name} handling task {task.get('id')} ({task.get('lang')})")
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
