from openai import OpenAI
client = OpenAI()
systems = [
    "You are a terse assistant. Answer in at most 10 words.",
    "You are a pirate. Answer like a pirate.",
    "You are a senior Java architect explaining to a junior developer.",
]
for s in systems :
    resp = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role" : "system","content" : s},
            {"role" : "user", "content" : "What is an API"},
        ],
    )
print(f"sytem: {s}\n-> {resp.choices[0].message.content}\n")
