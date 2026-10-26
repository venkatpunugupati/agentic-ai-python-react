from openai import OpenAI

client = OpenAI()
messages = []

remarks = [
    "My name is Venkat.",
    "I am learning Agentic AI over the next 8 weeks.",
    "My background is 20 years of Java backend engineering.",
    "What is my name, and what is my background?",
]

for remark in remarks:
    messages.append({"role": "user", "content": remark})
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("you:", remark)
    print("model:", reply)
    print("prompt_tokens:", resp.usage.prompt_tokens)
    print()