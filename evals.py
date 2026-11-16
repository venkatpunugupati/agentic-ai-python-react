# evals.py — eval harness for agent.py and agent_rag.py
# Run:  python evals.py
# Shape: golden data (CASES) -> runner (run_pipeline + main)
#        -> scoring (check functions) -> report (pass/fail summary)

import agent as plain_agent
import agent_rag as rag_agent
from datetime import datetime


# ---------- Scoring: check functions ----------
# A check takes the final answer string and returns True/False.

def exact(expected):
    """True when the final answer equals `expected` exactly (after stripping)."""
    def check(answer):
        return answer.strip() == expected
    return check


def contains(substring):
    """True when the final answer contains `substring`."""
    def check(answer):
        return substring in answer
    return check


def startswith(prefix):
    """True when the final answer starts with `prefix`."""
    def check(answer):
        return answer.startswith(prefix)
    return check


def contains_today():
    """True when the final answer contains today's date, ISO or long form."""
    now = datetime.now()
    iso = now.strftime("%Y-%m-%d")                              # 2026-11-09
    long_form = f"{now.strftime('%B')} {now.day}, {now.year}"   # November 9, 2026
    def check(answer):
        return iso in answer or long_form in answer
    return check


# ---------- Golden data: (name, question, check, agent module) ----------
CASES = [
    ("fox x3",
     "Count the words in 'the quick brown fox jumps over the lazy dog' and multiply by 3",
     exact("27"), plain_agent),
    ("15 percent",
     "What is 15% of 240?",
     exact("36.0"), plain_agent),
    ("current time",
     "What time is it now?",
     contains_today(), plain_agent),
    ("refusal (RAG)",
     "What is the capital of the USA?",
     exact("I don't have that in the documents."), rag_agent),
    ("empty question",
     "",
     startswith("Invalid input"), plain_agent),
    # The ambiguous "the quick brown fox sentence" case is deliberately left out:
    # an ambiguous question is a bad eval — don't grade what you can't define.
]


# ---------- Runner ----------
def run_pipeline(module, question):
    """Run one question through the full pipeline (validate -> plan -> execute)
    with FRESH history. Returns the final answer string."""
    messages = [module.build_system_message()]  # fresh every case, never load_memory()
    valid, reason = module.validate_question(question)
    if not valid:
        return f"Invalid input: {reason}"
    messages.append({"role": "user", "content": question})
    plan = module.make_plan(question)
    results, final_answer = module.execute_plan(question, plan, messages)
    # NOTE: no save_memory() here — evals must not write to the agent's memory file.
    return final_answer


def main():
    passed = 0
    for name, question, check, module in CASES:
        answer = run_pipeline(module, question)
        ok = check(answer)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {answer!r}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
