# Python ReAct Agent — from scratch

LLM fundamentals, then a raw ReAct agent built from scratch — no framework.

## LLM fundamentals

- `extract.py`: structured-extraction CLI. Reads a job-posting text file
  and emits JSON with exactly five keys (title, company, location, skills
  array, salary) — system-prompt schema, temperature 0, JSON response
  mode, validation that all five keys exist, and one bounded retry feeding
  the validation error back to the model. Test postings in
  `posting1.txt`, `posting2.txt`, `posting3.txt`.
- Smaller experiments: `hello.py` (first LLM call), `tokens.py`,
  `temperature.py`, `few_shot.py`, `system_prompt.py`, `embeddings.py`,
  `json_test.py`, `api.py`, `chat.py`.

## The agent (`agent.py`)

A raw ReAct loop: Thought / Action / Action Input, with tool
observations, max 6 steps. gpt-4o-mini, temperature 0. Three tools:

- Calculator, word count, current time

Four mechanisms built on the loop, each born from a diagnosed failure:

- **Memory across runs** (`memory.json`): the full message list persists
  to disk — load at startup, save at run end, `--fresh` to start clean.
  A second run can only answer from the file.
- **Compaction** (`compact_memory`): rolling summary — old turns
  summarized by a dedicated model call keeping durable facts only, with
  an explicit volatile-fact drop-list (no clock readings or dates kept
  as durable facts, after a staleness failure surfaced in testing).
- **Guardrails**: `validate_question` (rejects empty/non-string input);
  `check_grounding` scans the run's trace for a `get_current_time`
  action on temporal questions and appends one corrective observation
  for a bounded retry; honest fallback on "stopped: max steps reached".
- **Plan-and-execute**: `make_plan` renders the tool registry verbatim
  and emits `[tool]`-bracketed steps with deterministic bracket
  validation; `execute_plan` runs each step through the ReAct loop;
  the bounded replanner returns one temperature-0 verdict
  (CONTINUE/REVISE/DONE), failing open to CONTINUE, `MAX_REPLANS=2`.

Capstone order: validate → plan → execute → verify → persist → compact.

## Run it

python -m venv .venv
source .venv/bin/activate
pip install openai
export OPENAI_API_KEY="..."
python agent.py "count the words in 'the quick brown fox jumps over the lazy dog' and multiply by 3"

## Verified behavior

- First multi-tool chained run: word_count → calculator →
  get_current_time, all genuinely working.
- Week 2 capstone acceptance task → 98, trace-verified.
- Three-way side-by-side (same question as the Java ports): answered 27
  with 0 tool calls — the explicit no-tool rule fired deterministically
  ("you already know: skip the tools").

## Scope note

The Week 4 agentic RAG build (`agent_rag.py`, `memory_rag.json`, and the
`rag/` folder) is deliberately excluded from this repo and will live in
its own repository later.
