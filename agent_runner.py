import re

from agent import ask_llm
from memory import add_message, get_history
from tools import download_file, load_dataframe, dataframe_summary
from dataset_cache import save_dataframe, get_dataframe

URL_PATTERN = r"https?://[^\s]+"


def run_agent(chat_id: int, question: str):

    # -------------------------------------------------
    # Save user message
    # -------------------------------------------------
    add_message(chat_id, "user", question)

    history = get_history(chat_id)

    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in history
    )

    # -------------------------------------------------
    # Download dataset if a URL exists
    # -------------------------------------------------

    urls = re.findall(URL_PATTERN, history_text)

    context = ""

    if urls:

        try:
            path = download_file(urls[-1])

            df = load_dataframe(path)

            save_dataframe(chat_id, df)

            summary = dataframe_summary(df)

            context = f"""
Dataset Summary

{summary}
"""

        except Exception as e:

            context = f"Dataset could not be loaded: {e}"

    # -------------------------------------------------
    # Dataset context if previously loaded
    # -------------------------------------------------

    df = get_dataframe(chat_id)

    print("=" * 60)
    print("DataFrame exists:", df is not None)

    if df is not None:
        print("DataFrame shape:", df.shape)
        if not context:
            summary = dataframe_summary(df)
            context = f"Dataset:\n\n{summary}\n"

    # -------------------------------------------------
    # Gemini fallback
    # -------------------------------------------------

    prompt = f"""
Conversation:

{history_text}

{context}

Based on the above conversation and data, answer the user's latest message.
If the user specifies a JSON shape in their message, return ONLY valid JSON matching the exact shape they requested for the 'answer' key.
If the user does NOT ask a question (e.g., they just provide a dataset link), return exactly this JSON: {{"status": "acknowledged"}}.
Do NOT include the 'log_url' key in your response.
Do NOT wrap the JSON in markdown code blocks.
"""

    print("Using Gemini...")
    import json

    try:
        answer_text = ask_llm(prompt)
        print(f"Raw LLM output: {answer_text}")
        
        # Clean markdown code blocks if any
        if answer_text.startswith("```"):
            lines = answer_text.strip().split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            answer_text = "\n".join(lines).strip()

        try:
            answer = json.loads(answer_text)
            # Some models output {"answer": {"capital": "Paris"}} 
            # instead of just {"capital": "Paris"}. Let's unwrap it if they do!
            if isinstance(answer, dict) and "answer" in answer and len(answer) == 1:
                answer = answer["answer"]
        except json.JSONDecodeError:
            answer = answer_text

    except Exception as e:
        answer = f"LLM temporarily unavailable: {e}"

    add_message(chat_id, "assistant", str(answer))

    # Mark the state as closed logically: if the AI provides a tangible answer 
    # (not just an intermediate acknowledgement), the task is completely finished.
    if isinstance(answer, dict) and answer.get("status") != "acknowledged":
        from memory import clear_history
        from dataset_cache import clear_dataframe
        clear_history(chat_id)
        clear_dataframe(chat_id)

    return answer