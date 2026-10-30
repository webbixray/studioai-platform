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


# Additional helpers
import shutil
import tempfile

# ESLint for JavaScript

def _run_eslint(code: str) -> list:
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js') as f:
        f.write(code)
        tmp_path=f.name
    try:
        eslint_cmd = shutil.which('eslint') or shutil.which('node_modules/.bin/eslint')
        if not eslint_cmd:
            return [{'type':'warning', 'message':'eslint not installed'}]
        result = subprocess.run([eslint_cmd, tmp_path, '--format', 'json'], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data if isinstance(data, list) else []
        else:
            return [{'type':'error','message':result.stderr.strip()}]
    finally:
        os.unlink(tmp_path)

# SpotBugs for Java

def _run_spotbugs(code: str) -> list:
    """Run SpotBugs on compiled Java code.
    Uses javac to compile, then spotbugs command (expects SpotBugs installed).
    Returns list of findings e.g. {"type":"error", "message":...}.
    If javac or spotbugs are missing, returns a warning.
    """
    try:
        import tempfile, shutil, textwrap
        import os
        with tempfile.TemporaryDirectory() as td:
            java_file=os.path.join(td,'Temp.java')
            with open(java_file,'w') as f:
                f.write(code)
            # compile
            javac_cmd=shutil.which('javac')
            if not javac_cmd:
                return [{"type":"warning","message":"javac not found in PATH"}]
            compile_res=subprocess.run([javac_cmd,'-d',td,java_file],capture_output=True,text=True)
            if compile_res.returncode!=0:
                return [{"type":"error","message":compile_res.stderr.strip()}]
            # find class file
            java_class=None
            for root,_,files in os.walk(td):
                for f in files:
                    if f.endswith('.class'):
                        java_class=os.path.join(root,f)
                        break
            if not java_class:
                return [{"type":"error","message":"No class file produced"}]
            # run SpotBugs
            spotbugs_cmd=shutil.which('spotbugs')
            if not spotbugs_cmd:
                return [{"type":"warning","message":"spotbugs command not found"}]
            # SpotBugs requires classpath and directory
            spotbugs_res=subprocess.run([spotbugs_cmd,'-textui','-effort:max','-plugin','-file',td],capture_output=True,text=True)
            if spotbugs_res.returncode==0:
                # Spotbugs outputs findings to stdout
                lines=spotbugs_res.stdout.strip().split('
')
                findings=[{"type":"info","message":l} for l in lines if l]
                return findings
            else:
                return [{"type":"error","message":spotbugs_res.stderr.strip()}]
    except Exception as e:
        return [{"type":"error","message":str(e)}]def _run_govet(code: str) -> list:
    with tempfile.TemporaryDirectory() as d:
        file_path = os.path.join(d, 'temp.go')
        with open(file_path, 'w') as f:
            f.write(code)
        go_cmd = shutil.which('go')
        if not go_cmd:
            return [{'type':'warning', 'message':'go not installed'}]
        result = subprocess.run([go_cmd, 'vet', file_path], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return []
        else:
            return [{'type':'error','message':result.stderr.strip()}]

# Rust clippy

def _run_clippy(code: str) -> list:
    with tempfile.TemporaryDirectory() as d:
        file_path = os.path.join(d, 'main.rs')
        with open(file_path, 'w') as f:
            f.write(code)
        cargo_cmd = shutil.which('cargo')
        if not cargo_cmd:
            return [{'type':'warning', 'message':'cargo not installed'}]
        # Setup minimal Cargo.toml
        cargo_toml = os.path.join(d, 'Cargo.toml')
        with open(cargo_toml, 'w') as f:
            f.write('[package]
name = "tmp"
version = "0.1.0"
edition = "2021"

[dependencies]')
        result = subprocess.run([cargo_cmd, 'clippy', '--manifest-path', cargo_toml, '--quiet'], cwd=d, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return []
        else:
            return [{'type':'error','message':result.stderr.strip()}]

# Main dispatcher

def scan_code(language: str, code: str) -> list:
    language=language.lower()
    if language=='python':
        return _run_bandit(code)
    elif language in ('js','javascript','node'):
        return _run_eslint(code)
    elif language=='java':
        return _run_spotbugs(code)
    elif language=='go':
        return _run_govet(code)
    elif language=='rust':
        return _run_clippy(code)
    else:
        return []
