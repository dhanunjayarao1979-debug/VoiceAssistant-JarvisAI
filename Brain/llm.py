"""Shared OpenAI chat helper used by AIBrain.py and Qna.py.

The old code called the retired `text-davinci-003` completion model. This uses the
chat completions API instead (available in openai==0.28.1).

Configuration:
  - API key: OPENAI_API_KEY environment variable (or a .env file), falling back to Data/Api.txt
  - Model:   OPENAI_MODEL environment variable, default "gpt-4o-mini"
"""
import os

import openai
from dotenv import load_dotenv

from Config import data_path

load_dotenv()

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
MAX_HISTORY_LINES = 20


def load_api_key():
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    try:
        with open(data_path("Api.txt"), "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def lines_to_messages(lines, user_prefix, assistant_prefix):
    """Turn log lines like 'You: hi' / 'Jarvis: hello' into chat messages.

    Lines without a prefix are continuations of the previous message.
    """
    messages = []
    for line in lines:
        if line.startswith(user_prefix):
            messages.append({"role": "user", "content": line[len(user_prefix):].strip()})
        elif line.startswith(assistant_prefix):
            messages.append({"role": "assistant", "content": line[len(assistant_prefix):].strip()})
        elif messages and line.strip():
            messages[-1]["content"] += "\n" + line.strip()
    return messages


def ask(system_prompt, lines, user_prefix, assistant_prefix, max_tokens, temperature, **extra):
    key = load_api_key()
    if not key:
        raise RuntimeError(
            "No OpenAI API key found. Set OPENAI_API_KEY or paste the key into Data/Api.txt."
        )

    messages = [{"role": "system", "content": system_prompt}]
    messages += lines_to_messages(lines[-MAX_HISTORY_LINES:], user_prefix, assistant_prefix)

    openai.api_key = key
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        **extra,
    )
    return response.choices[0].message["content"].strip()
