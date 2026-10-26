from openai import OpenAI

client = OpenAI()
prompt = "Give me a person's name and age."

print("--- without response_format ---")
r1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt + " Respond in JSON with keys 'name' and 'age'."}],
)
print(r1.choices[0].message.content)

print("--- with response_format ---")
r2 = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[{"role": "user", "content": prompt + " Respond in JSON with keys 'name' and 'age'."}],
)
print(r2.choices[0].message.content)