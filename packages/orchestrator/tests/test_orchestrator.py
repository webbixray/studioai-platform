import asyncio
import pytest
from orchestrator import Orchestrator, CodegenAgent

async def test_orchestrator_basic():
    orch = Orchestrator()
    orch.register(CodegenAgent("codegen"))
    # schedule a dummy task
    await orch.schedule({"id": "t1", "agent": "codegen", "brief": "create sample endpoint"})
    # run only one worker for test
    async def win():
        await orch.task_queue.join()
    await asyncio.wait([win()], timeout=3)

    assert orch.task_queue.empty()
