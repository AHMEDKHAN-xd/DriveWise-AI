import json

import requests


OLLAMA_BASE_URL = "http://localhost:11434"

MODEL = "llama3.2:3b"

TIMEOUT_SECONDS = 120


def check_ollama(timeout=2):
    """Return True if the local Ollama server responds."""

    try:

        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=timeout,
        )

        return response.ok

    except requests.exceptions.RequestException:
        return False


def stream_ai_diagnosis(prompt):
    """Yield diagnosis text chunks from the local model as they are generated."""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True,
        },
        stream=True,
        timeout=TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    for line in response.iter_lines():

        if not line:
            continue

        chunk = json.loads(line)

        piece = chunk.get("response", "")

        if piece:
            yield piece

        if chunk.get("done"):
            break
