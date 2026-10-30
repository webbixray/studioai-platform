"""Security scanning module.

Supports simple static analysis based on language.
For Python it runs Bandit; JavaScript uses a minimal placeholder.
"""
import os
import subprocess
import tempfile
import json

def _run_bandit(code: str) -> list:
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
        f.write(code)
        tmp_path=f.name
    try:
        result=subprocess.run(['bandit','-q','-f','json','-r',tmp_path],capture_output=True,text=True,check=False)
        if result.returncode==0:
            data=json.loads(result.stdout)
            return data.get('results',[])
        else:
            return [{'type':'error','message':result.stderr.strip()}]
    finally:
        os.unlink(tmp_path)


def scan_code(language: str, code: str) -> list:
    language=language.lower()
    if language=='python':
        return _run_bandit(code)
    elif language in ('js','javascript','node'):
        # Placeholder: No linting implemented.
        return []
    elif language=='java':
        return []
    elif language=='go':
        return []
    elif language=='rust':
        return []
    else:
        return []
