from openai import OpenAI

client = OpenAI()

for temp in (0, 1):
    print(f"--- temperature={temp} ---")
    for _ in range(3):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=temp,
            messages=[{"role": "user", "content": "Invent a startup name for an AI compamy."}],
        )
        print(resp.choices[0].message.content)
    print()