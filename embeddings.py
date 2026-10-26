from openai import OpenAI
import math

client = OpenAI()

sentences = [
    "The cat sits on the mat.",
    "A feline rests on the rug.",
    "The stock market crashed today.",
]

def embed(text):
    r = client.embeddings.create(model="text-embedding-3-small", input=text)
    return r.data[0].embedding

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

vecs = [embed(s) for s in sentences]
print("vector dimension:", len(vecs[0]))
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        print(f"{cosine(vecs[i], vecs[j]):.3f}  '{sentences[i]}' <-> '{sentences[j]}'")
