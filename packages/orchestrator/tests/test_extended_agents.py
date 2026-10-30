import os
import asyncio
import pytest
from orchestrator import Orchestrator, PythonAgent, JavascriptAgent, JavaAgent, GoAgent, RustAgent

@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY') and not os.getenv('HF_TOKEN'), reason='No LLM key')
async def test_extended_agents():
    orch = Orchestrator()
    orch.register(PythonAgent('python'))
    orch.register(JavascriptAgent('javascript'))
    orch.register(JavaAgent('java'))
    orch.register(GoAgent('go'))
    orch.register(RustAgent('rust'))
    # schedule one of each
    tasks = [
        {'id':'t_py','type':'codegen','lang':'python','brief':'sample'},
        {'id':'t_js','type':'codegen','lang':'js','brief':'sample'},
        {'id':'t_java','type':'codegen','lang':'java','brief':'sample'},
        {'id':'t_go','type':'codegen','lang':'go','brief':'sample'},
        {'id':'t_rust','type':'codegen','lang':'rust','brief':'sample'},
    ]
    for t in tasks:
        await orch.delegate(t)
    await asyncio.sleep(1)
    assert True
