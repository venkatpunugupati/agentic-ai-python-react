from openai import OpenAI

client = OpenAI()  # picks up OPENAI_API_KEY from the environment

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "In the context of large language models, explain what a token is in one sentence."}],
)
print(resp.choices[0].message.content)
print("tokens used:", resp.usage.total_tokens)
