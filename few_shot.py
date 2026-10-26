from openai import OpenAI
client = OpenAI()

print("--- zero-shot ---")
resp1 = client.chat.completions.create(
    model="gpt-4o-mini", temperature=0,
    messages=[{"role": "user", "content": "Classify sentiment as POSITIVE or NEGATIVE or NEUTRAL: 'The package arrived two days late, but the customer support team was helpful.'"}],
)
print(resp1.choices[0].message.content)
print("--- few-shot ---")
resp2 = client.chat.completions.create(
    model="gpt-4o-mini", temperature=0,
    messages=[{"role": "user", "content":
        "Classify sentiment as POSITIVE or NEGATIVE or NEUTRAL.\n\n"
        "Review: 'Loved it, works perfectly.'\nSentiment: POSITIVE\n\n"
        "Review: 'Arrived broken and late.'\nSentiment: NEGATIVE\n\n"
        "Review: 'The package arrived two days late, but the customer support team was helpful.'\nSentiment:"}],
)
print(resp2.choices[0].message.content)
