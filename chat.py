from openai import OpenAI
client = OpenAI()
TOKEN_BUDGET = 300
messages = [{"role": "system" , "content": "You are a concise assistant."}]
while True:
    user_in = input("you: ").strip()
    if user_in.lower() in ("quit", "exit"):
        break
    if user_in == "/reset":
        messages = [messages[0]]
        continue
    messages.append({"role": "user", "content": user_in})
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("bot:", reply)
    print(f"[tokens so far: {resp.usage.total_tokens}]")
    prompt_tokens = resp.usage.prompt_tokens
    if prompt_tokens > TOKEN_BUDGET :
      print(f"budget Exceeded({prompt_tokens} > {TOKEN_BUDGET}) - Type /reset toclear hystory.")
