import re
import pandas as pd

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

CRITICAL RULES:
1. If the user's latest message ONLY provides a dataset link (e.g. "Here is a dataset: ...") and does NOT explicitly ask you to calculate or answer a specific question, you MUST return exactly this JSON and nothing else: {{"status": "acknowledged"}}
2. If the user's message explicitly contains instructions to calculate, count, or provide a JSON object, you MUST provide the final answer!
3. If the message requires calculating or filtering data, you MUST write a Python script to compute the exact answer instead of guessing.
   - The dataset is already loaded in memory as a pandas DataFrame named `df`.
   - You must store your final JSON answer dictionary into a variable named `final_answer`.
   - Output your Python code inside a ```python block. Do not output anything else.
4. Do NOT include the 'log_url' key in your response.
"""

    print("Using Gemini...")
    import json

    try:
        answer_text = ask_llm(prompt)
        print(f"Raw LLM output: {answer_text}")
        
        # Check if the AI wrote a python script to calculate the answer
        python_match = re.search(r"```python(.*?)```", answer_text, re.DOTALL)
        
        if python_match:
            code = python_match.group(1).strip()
            print("Executing AI Python code:\n", code)
            local_vars = {"df": df, "pd": pd}
            try:
                exec(code, local_vars)
                answer = local_vars.get("final_answer", {"error": "final_answer variable not found in code"})
            except Exception as code_e:
                print(f"AI Code Execution Failed: {code_e}")
                answer = {"error": f"Failed to calculate answer: {code_e}"}
        else:
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