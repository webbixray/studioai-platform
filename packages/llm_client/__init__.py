"""LLM client abstraction.

Supports NVIDIA NIM and HuggingFace inference via environment keys.
"""
import os
import json
import requests
from typing import Optional

NVIDIA_KEY = os.getenv('NVIDIA_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')

def get_llm_response(prompt: str, model: str='LLAMA3-70B') -> str:
    if NVIDIA_KEY:
        url = f'https://api.nvidia.com/v1/nim/llm/v1/predictions'
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
        return data.get('outputs', [{}])[0].get('generated_text', '')
    elif HF_TOKEN:
        from huggingface_hub.inference import InferenceClient
        client = InferenceClient(model, token=HF_TOKEN)
        return client.text_generation(prompt, max_new_tokens=256, temperature=0.7)
    else:
        raise RuntimeError('No LLM key set. Provide NVIDIA_API_KEY or HF_TOKEN')
