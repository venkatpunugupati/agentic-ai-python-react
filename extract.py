import argparse, json
from openai import OpenAI

client = OpenAI()
SCHEMA = {
    "title": "string or null",
    "company": "string or null",
    "location": "string or null",
    "skills": "array of strings (empty array if none found)",
    "salary": "string or null",
}
REQUIRED_KEYS = list(SCHEMA.keys())
SYSTEM = (
    "You extract structured data from job postings.\n"
    "Return ONLY a JSON object with exactly these keys:\n"
    + "\n".join(f"- {k}: {v}" for k, v in SCHEMA.items())
    + "\nRules: if a field is not present, use null (or [] for skills). Never invent values."
)

def extract(text):
    resp = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content
def extract_validated(text):
    raw = extract(text)
    error = validate(raw)
    if error:
        # retry once, showing the model its mistake
        resp = client.chat.completions.create(
            model="gpt-4o-mini", temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": text},
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"That output failed validation: {error}. Return ONLY a corrected JSON object with exactly these keys: {', '.join(REQUIRED_KEYS)}."},
            ],
        )
        raw = resp.choices[0].message.content
        error = validate(raw)
        if error:
            raise ValueError(f"extraction failed after retry: {error}")
    return raw

def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", help="text file with the job posting")
    args = p.parse_args()
    text = open(args.file).read()
    raw = extract_validated(text)
    print(raw)
   

def validate(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return f"invalid JSON: {e}"
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        return f"missing keys: {missing}"
    return None




if __name__ == "__main__":
    main()
