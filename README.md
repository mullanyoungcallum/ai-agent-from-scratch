# Build an AI Agent from Scratch — my implementation

This is my own implementation, built chapter by chapter while reading Manning's
[*Build an AI Agent from Scratch*](https://www.manning.com/books/build-an-ai-agent-from-scratch).

The book's companion repo ships a finished package (`scratch_agents/`) alongside notebooks that
reproduce every listing. Reading finished code doesn't teach you to write it, so on this branch
(`learning`) the finished package is gone. `main` still has the original, intact, if you ever want
to compare the full thing. What's left here:

```text
notebooks/    # the book's chapter notebooks, kept as spec + narrative — unmodified
agents/       # my implementation, built one chapter at a time, starting empty
tests/        # my tests, plus tests/fakes.py (fake LLM/sandbox/etc. services, no API keys needed)
```

## Why the notebooks are broken

Every notebook from CH02 onward imports `scratch_agents`, which no longer exists on this branch.
That's intentional: an `ImportError` naming a module I haven't written yet *is* the next thing to
build. The notebook prose, listing numbers, and explanations are all still there — only the
reference implementation is gone.

## Working agreement (with Claude)

- Claude writes module skeletons — signatures, type hints, docstrings stating the contract, bodies
  left as `NotImplementedError` — plus failing tests. I write the bodies.
- Layout and design are mine. Claude only flags a choice when it will hurt a later chapter.
- I compare against the book's original only *after* attempting a piece:
  `git show main:scratch_agents/<file>.py`.
- The loop, per chapter: read the chapter → run its notebook → Claude scaffolds → I implement →
  review and diff against `main`.

## Setup

```bash
uv sync
cp .env.example .env   # add API keys as each chapter needs them
uv run jupyter lab
```

`pyproject.toml` starts with no dependencies — they get added one at a time
(`uv add openai`, `uv add litellm`, …) as each chapter actually needs them, instead of installing
everything the finished book needs on day one.

## API keys

Add keys to `.env` as chapters require them:

| Chapters | Keys / prerequisites |
| --- | --- |
| CH02 | `OPENAI_API_KEY`; `ANTHROPIC_API_KEY` for the Anthropic examples; a Hugging Face account with accepted GAIA access and `HF_TOKEN` for the benchmark |
| CH03–CH04 | `TAVILY_API_KEY`; Node.js/npm (`npx`) for the Tavily MCP server |
| CH05 | `TAVILY_API_KEY` and GAIA access/downloads for attachment exercises |
| CH06 | `OPENAI_API_KEY` for model calls and embeddings |
| CH07 | `TAVILY_API_KEY` for search examples |
| CH08 | `E2B_API_KEY`; `TAVILY_API_KEY` only for sandbox tools that use it |
| CH09 | `E2B_API_KEY`/`TAVILY_API_KEY` when running specialist agents that use those services |
| CH10 | `OPENAI_API_KEY` |

## Tests

```bash
uv sync --extra test
uv run --extra test pytest -q
```

Tests must never require API keys — `tests/fakes.py` has fake external services (LLM completion,
embeddings, sandbox) to monkeypatch instead of calling a real provider.

## Attribution

Notebooks are from Manning's companion repo for *Build an AI Agent from Scratch*, MIT-licensed —
see `LICENSE`. Everything in `agents/` and `tests/` (other than `tests/fakes.py`, adapted from the
same source) is my own.
