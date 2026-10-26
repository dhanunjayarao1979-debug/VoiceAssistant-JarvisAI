from Brain.llm import ask
from Config import db_path

SYSTEM_PROMPT = (
    "You are Jarvis, a helpful, concise voice assistant. "
    "Your replies are spoken aloud, so keep them short and conversational."
)
FALLBACK_REPLY = "Sorry sir, I could not reach my brain right now."


def ReplyBrain(question, chat_file=None):
    chat_file = chat_file or db_path("chat_log.txt")

    chat_log = load_chat(chat_file)
    chat_log.append(f"You: {question}")

    try:
        response = generate_response(chat_log)
    except Exception as e:
        print(f"[AIBrain] {e}")
        return FALLBACK_REPLY

    response = response.replace("Jarvis:", "").strip()

    chat_log.append(f"Jarvis: {response}")
    save_chat(chat_log, chat_file)

    return response


def load_chat(chat_file):
    try:
        with open(chat_file, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def save_chat(chat_log, chat_file):
    with open(chat_file, "w") as file:
        for line in chat_log:
            file.write(line + "\n")


def generate_response(chat_log):
    return ask(
        SYSTEM_PROMPT,
        chat_log,
        user_prefix="You:",
        assistant_prefix="Jarvis:",
        max_tokens=150,
        temperature=0.5,
        top_p=0.3,
        frequency_penalty=0.5,
    )
