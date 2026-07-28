import openai

from config import AIPROXY_TOKEN, OPENAI_BASE_URL, MODEL

client = openai.Client(api_key=AIPROXY_TOKEN, base_url=OPENAI_BASE_URL)


SYSTEM_PROMPT = """
You are an expert data analyst.

Answer the user's question accurately.

Rules:
- If the user specifies a JSON shape in their message, you MUST respond with a valid JSON object matching EXACTLY the requested shape for the 'answer' key.
- Do NOT include the 'log_url' key in your response. Only provide the value for the 'answer' key.
- Return ONLY valid JSON if a JSON shape is requested. No markdown backticks, no explanations.
- If no JSON shape is requested, return only the direct answer.
"""


def ask_llm(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
    )

    return response.choices[0].message.content.strip()