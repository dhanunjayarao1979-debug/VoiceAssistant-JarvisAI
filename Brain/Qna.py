from Brain.llm import ask
from Config import db_path

SYSTEM_PROMPT = (
    "You are Jarvis, a voice assistant. Answer the question accurately and briefly, "
    "in one or two sentences, since the answer is spoken aloud."
)
FALLBACK_REPLY = "Sorry sir, I could not reach my brain right now."


def QuestionsAnswer(question, chat_file=None):
    chat_file = chat_file or db_path("qna_log.txt")

    chat_log = load_chat(chat_file)
    chat_log.append(f"Question: {question}")

    try:
        response = generate_response(chat_log)
    except Exception as e:
        print(f"[Qna] {e}")
        return FALLBACK_REPLY

    response = response.replace("Answer:", "").strip()

    chat_log.append(f"Answer: {response}")
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
        user_prefix="Question:",
        assistant_prefix="Answer:",
        max_tokens=200,
        temperature=0,
        top_p=1,
    )
