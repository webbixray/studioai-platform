"""Orchestrator engine with language specific agents.

Now each agent performs a security scan after code generation.
"""
import asyncio
import os
from typing import Dict, Any

# Base agent
class Agent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, task: Dict[str, Any]):  # pragma: no cover
        raise NotImplementedError

# Helper import for LLM client
from llm_client import get_llm_response
# Security scan module
from security_scan import scan_code

# Python agent
class PythonAgent(Agent):
    async def run(self, task):
        prompt = f"Generate Python code for: {task.get('brief', '')}"
        try:
            code = get_llm_response(prompt, model='gpt-4o-mini')
            findings = scan_code('python', code)
            return {'lang': 'python', 'generated': code, 'findings': findings}
        except Exception as e:
            return {'error': str(e)}

# Javascript agent
class JavascriptAgent(Agent):
    async def run(self, task):
        prompt = f"Generate JavaScript code for: {task.get('brief', '')}"
        try:
            code = get_llm_response(prompt, model='gpt-4o-mini')
            findings = scan_code('js', code)
            return {'lang': 'js', 'generated': code, 'findings': findings}
        except Exception as e:
            return {'error': str(e)}

# Java agent
class JavaAgent(Agent):
    async def run(self, task):
        prompt = f"Generate Java code for: {task.get('brief', '')}"
        code = get_llm_response(prompt, model='gpt-4o-mini')
        findings = scan_code('java', code)
        return {'lang': 'java', 'generated': code, 'findings': findings}

# Go agent
class GoAgent(Agent):
    async def run(self, task):
        prompt = f"Generate Go code for: {task.get('brief', '')}"
        code = get_llm_response(prompt, model='gpt-4o-mini')
        findings = scan_code('go', code)
        return {'lang': 'go', 'generated': code, 'findings': findings}

# Rust agent
class RustAgent(Agent):
    async def run(self, task):
        prompt = f"Generate Rust code for: {task.get('brief', '')}"
        code = get_llm_response(prompt, model='gpt-4o-mini')
        findings = scan_code('rust', code)
        return {'lang': 'rust', 'generated': code, 'findings': findings}

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
                elif lang == 'java':
                    agent_name = 'java'
                elif lang == 'go':
                    agent_name = 'go'
                elif lang == 'rust':
                    agent_name = 'rust'
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
    orch.register(PythonAgent('python'))
    orch.register(JavascriptAgent('javascript'))
    orch.register(JavaAgent('java'))
    orch.register(GoAgent('go'))
    orch.register(RustAgent('rust'))
    # schedule a dummy task
    orch.loop.create_task(orch.delegate({'id': 't100', 'type': 'codegen', 'lang': 'python', 'brief': 'create sample class'}))
    orch.run()
