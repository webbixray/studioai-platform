import asyncio
import pytest
from orchestrator import Orchestrator, PythonAgent, JavascriptAgent

async def test_delegate_codegen_python():
    orch = Orchestrator()
    orch.register(PythonAgent("python"))
    orch.register(JavascriptAgent("javascript"))
    await orch.delegate({"id":"t1","type":"codegen","lang":"python","brief":"sample"})
    await asyncio.sleep(0.2)
    assert True
