"""LLM client abstraction.

Provides a simple in‑memory cache for LLM responses.
"""
import os
import json
import requests

# API tokens
NVIDIA_KEY = os.getenv('NVIDIA_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')

# Cache dict
_cache: dict[tuple[str, str], str] = {}


def get_llm_response(prompt: str, model: str='LLAMA3-70B') -> str:
    """Return LLM output, using cache if available.

    The key is a tuple of (model, prompt).  Cache size is unbounded for
    simplicity; in production you would add an LRU policy.
    """
    key = (model, prompt)
    if key in _cache:
        return _cache[key]
    if NVIDIA_KEY:
        url = 'https://api.nvidia.com/v1/nim/llm/v1/predictions'
        headers = {
            'Authorization': f'Bearer {NVIDIA_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'input': prompt,
            'parameters': {
                'max_new_tokens': 256,
                'temperature': 0.7
            }
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        text = data.get('outputs', [{}])[0].get('generated_text', '')
    elif HF_TOKEN:
        from huggingface_hub.inference import InferenceClient
        client = InferenceClient(model, token=HF_TOKEN)
        text = client.text_generation(prompt, max_new_tokens=256, temperature=0.7)
    else:
        raise RuntimeError('No LLM key set. Provide NVIDIA_API_KEY or HF_TOKEN')
    _cache[key] = text
    return text
