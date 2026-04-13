# MiniLab: Markdown Header Extractor

[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Package Tool](https://img.shields.io/badge/package%20tool-uv-DE5FE9)](https://docs.astral.sh/uv/)
[![TDD](https://img.shields.io/badge/workflow-red%20%E2%86%92%20green-success)](https://en.wikipedia.org/wiki/Test-driven_development)

> Small, focused Python utility that extracts Markdown headers with a strict red/green TDD workflow.

---

## Prompts

> "Build a Python function to extract headers from a markdown string. Use red/green TDD."

> "write the prompt you received from me into a Readme file and publish a public github repo, public, with a naming scheme that matches my style. make sure the readme is fancy and the github repo is well decorated. include the tools we used such as the model and agent with links to them. come up only after you've run gh repo view --web. make sure we have no secrets to leak."

## What it does

`extract_headers(markdown: str) -> list[str]` parses a Markdown string and returns header text in order.

### Supported header styles

- ATX headers (`# Title`, `## Section`, etc.)
- Setext headers:
  - `Title` + `===`
  - `Subtitle` + `---`
- Ignores headers inside fenced code blocks (````` / `~~~`)

## Example

```python
from minilab.markdown import extract_headers

markdown = """\
# Title
Intro paragraph.

## Section ###

Subheading
----------

```python
# not a header
```
"""

print(extract_headers(markdown))
# ['Title', 'Section', 'Subheading']
```

## Run locally

```bash
uv sync
uv run pytest
```

## Red/Green TDD notes

- Red: Added failing tests for ATX, Setext, and fenced-code behavior.
- Green: Implemented parser logic with regex + line scanning to make tests pass.
- Verify: `3 passed` with `uv run pytest`.

## Tools used

- Agent: [OpenCode](https://github.com/sst/opencode)
- Model: [`openai/gpt-5.3-codex`](https://openrouter.ai/openai/gpt-5.3-codex)
- Test runner: [pytest](https://docs.pytest.org/)
- Python project manager: [uv](https://docs.astral.sh/uv/)

## Claude Code park mode hook

A `PostToolUse` hook that puts Claude in park mode after writing `.ts` or `.py` files — Claude stops and waits for user instructions before continuing.

```bash
# .ts file → parks Claude (exit 2)
$ echo '{"tool_name":"Write","tool_input":{"file_path":"src/main.ts"}}' \
    | npx tsx .claude/hooks/park-mode.ts
PARK MODE: Written file "src/main.ts" matches .ts, .py. Stop and wait for user instructions before taking any further action.
# exit code: 2

# .py file → parks Claude (exit 2)
$ echo '{"tool_name":"Write","tool_input":{"file_path":"src/app.py"}}' \
    | npx tsx .claude/hooks/park-mode.ts
PARK MODE: Written file "src/app.py" matches .ts, .py. Stop and wait for user instructions before taking any further action.
# exit code: 2

# .md file → passes through (exit 0)
$ echo '{"tool_name":"Write","tool_input":{"file_path":"README.md"}}' \
    | npx tsx .claude/hooks/park-mode.ts
# exit code: 0
```

## Project layout

```text
.
├── .claude/
│   ├── hooks/park-mode.ts
│   └── settings.json
├── src/minilab/markdown.py
├── tests/test_markdown_headers.py
└── pyproject.toml
```
