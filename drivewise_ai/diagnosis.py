import json
import os

import requests
import streamlit as st


OLLAMA_BASE_URL = "http://localhost:11434"

OLLAMA_MODEL = "llama3.2:3b"

GROQ_API_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

# Groq returns 404 for models the account cannot access (e.g. free-tier
# keys), so try models in order until one is available.
GROQ_MODELS = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
)

TIMEOUT_SECONDS = 120


def get_groq_api_key():
    """Return the configured Groq API key, or None."""

    for name in ("GROQ_API_KEY", "groq_api_key"):

        try:
            value = st.secrets[name]

        except Exception:
            continue

        if value:
            return str(value).strip()

    env_value = os.environ.get("GROQ_API_KEY", "").strip()

    return env_value or None


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


def get_ai_provider():
    """Return the best available provider: "groq", "ollama", or None."""

    if get_groq_api_key():
        return "groq"

    if check_ollama():
        return "ollama"

    return None


def stream_ollama_diagnosis(prompt):
    """Yield diagnosis text chunks from the local model as they are generated."""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
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


def stream_groq_diagnosis(prompt, api_key):
    """Yield diagnosis text chunks from the Groq API as they are generated."""

    last_error = None

    for model in GROQ_MODELS:

        try:

            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": True,
                },
                stream=True,
                timeout=TIMEOUT_SECONDS,
            )

            response.raise_for_status()

        except requests.exceptions.HTTPError as exc:

            status = (
                exc.response.status_code
                if exc.response is not None
                else None
            )

            if status == 404:
                last_error = exc
                continue

            raise

        for line in response.iter_lines():

            if not line:
                continue

            text = line.decode("utf-8")

            if not text.startswith("data:"):
                continue

            payload = text[len("data:"):].strip()

            if payload == "[DONE]":
                break

            chunk = json.loads(payload)

            choices = chunk.get("choices") or [{}]

            piece = choices[0].get("delta", {}).get(
                "content", ""
            )

            if piece:
                yield piece

        return

    if last_error is not None:
        raise last_error


def stream_ai_diagnosis(prompt):
    """Yield diagnosis chunks from Groq when configured, else Ollama."""

    api_key = get_groq_api_key()

    if api_key:
        yield from stream_groq_diagnosis(prompt, api_key)

    else:
        yield from stream_ollama_diagnosis(prompt)
