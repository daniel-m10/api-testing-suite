# AGENTS.md
> **Tool:** OpenAI Codex CLI
> **How to use:** place this file at the root of each project repo. Codex CLI reads it automatically when you run `codex` inside the repo directory.
> **Important:** Codex CLI usage draws from your ChatGPT Plus plan quota ($20/month), shared with ChatGPT chat. Avoid running heavy Codex sessions on the same days you use ChatGPT chat intensively.
> **Authentication:** run `codex` and select "Sign in with ChatGPT". Do NOT use an API key — that would bypass your plan quota and charge per token.

---

## How to Start a Codex Session

Paste this block at the beginning of each session to give Codex immediate context:

```
Context: I am an SDET building a Python portfolio focused on AI-applied testing.
Current repo: api-testing-suite
Task: [DESCRIBE WHAT TO IMPLEMENT — be specific]
Stack: Python 3.13, pytest 9+, uv, ruff, GitHub Actions.
Standards: type hints everywhere, Google docstrings, AAA pattern in tests,
test naming convention: test_{method}_{condition}_{expected_result}.
Show full diff before applying any change. Do not proceed without my confirmation.
Active MCP servers: none
```

---

## Project Context

```
Plan week:           Week 2
Current feature:     CRUD tests with pydantic models — /posts endpoint
Last commit:         feat: add scaffolding, api_client fixture, and smoke parametrized test
CI status:           green
```

---

## Repo Purpose

**Project A — api-testing-suite:**
API testing suite over JSONPlaceholder (`jsonplaceholder.typicode.com`).
Stack: Python 3.13, pytest, requests, pydantic v2, GitHub Actions.
Goal: demonstrate advanced fixtures, parametrize, pydantic validation models, and AI failure analysis module.
Target: 20+ tests covering full CRUD operations with edge cases.

---

## Stack and Exact Versions

```toml
[project]
name = "api-testing-suite"
requires-python = ">=3.13"
dependencies = [
    "pytest>=9.0.3",
    "requests",
    "pydantic>=2.0",
    "anthropic",
    "pytest-html",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/api_testing_suite"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--html=report.html --self-contained-html"

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I"]

[dependency-groups]
dev = [
    "ruff>=0.15.12",
]
```

---

## Expected Folder Structure

```
api-testing-suite/
├── src/
│   └── api_testing_suite/
│       ├── __init__.py
│       ├── client.py          # APIClient — wraps requests.Session
│       ├── models.py          # Pydantic models for response validation
│       └── ai_analyzer.py     # AI module — Claude Haiku integration (Week 6)
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # All shared fixtures
│   ├── test_posts.py          # CRUD tests — /posts endpoint
│   ├── test_users.py          # GET tests — /users endpoint
│   └── test_comments.py       # GET + filter tests — /comments endpoint
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── AGENTS.md
├── pyproject.toml
└── README.md
```

---

## Code Standards — Non-Negotiable

### Test naming convention
```python
# Pattern: test_{method}_{condition}_{expected_result}
def test_get_post_with_valid_id_returns_200(): ...
def test_get_post_with_invalid_id_returns_404(): ...
def test_create_post_with_valid_payload_returns_201(): ...
def test_create_post_with_missing_title_returns_422(): ...
def test_delete_post_with_valid_id_returns_200(): ...
```

### Required test structure — AAA pattern
```python
def test_create_post_with_valid_payload_returns_201(api_client: APIClient) -> None:
    """Verify that creating a post with valid data returns HTTP 201.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    payload = PostCreate(title="Test post", body="Content", user_id=1)

    # Act
    response = api_client.post("/posts", json=payload.model_dump(by_alias=True))

    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == payload.title
```

### Fixture rules
```python
# Always declare return type
@pytest.fixture(scope="session")
def base_url() -> str:
    """Provide the base URL for JSONPlaceholder API."""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def api_client(base_url: str) -> APIClient:
    """Provide a shared API client for the entire test session."""
    return APIClient(base_url=base_url)

# Scope reference:
# function  → default, fresh instance per test
# class     → shared across tests in the same class
# module    → shared across tests in the same file
# session   → shared across the entire test run (use for clients, browsers, auth)
```

### AI module pattern (Week 6 — do not implement before then)
```python
import anthropic
import logging

logger = logging.getLogger(__name__)


def call_haiku(prompt: str) -> str:
    """Call Claude Haiku and return the text response.

    Args:
        prompt: The full prompt to send to the model.

    Returns:
        The model's text response as a string.

    Raises:
        anthropic.APIError: If the API call fails.
    """
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    cost = (input_tokens / 1_000_000 * 1.00) + (output_tokens / 1_000_000 * 5.00)
    logger.debug(
        "Haiku call | tokens: %d in / %d out | cost: $%.6f",
        input_tokens, output_tokens, cost
    )
    return response.content[0].text
```

### General rules
- Type hints on ALL functions and methods — no exceptions, including `__init__`
- Google-style docstrings on all classes and public functions
- Never use `print()` in tests or source code — use `logging`
- Maximum 1 logical assertion per test — multiple assert lines on the same object are allowed
- Imports ordered by ruff: stdlib → third-party → local

---

## GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Run linter
        run: uv run ruff check src/ tests/

      - name: Run tests
        run: uv run pytest --junitxml=results.xml

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-report-${{ github.run_number }}
          path: |
            report.html
            results.xml

      # Uncomment in Week 6 when ai_analyzer.py is implemented
      # - name: Analyze failures with AI
      #   if: failure()
      #   env:
      #     ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      #   run: uv run python analyze.py --report results.xml --output ai-report.html
      #
      # - name: Upload AI analysis report
      #   if: failure()
      #   uses: actions/upload-artifact@v4
      #   with:
      #     name: ai-failure-analysis-${{ github.run_number }}
      #     path: ai-report.html
```

---

## Commit Convention

Format: `type: short description in English (max 72 chars)`

| Type        | When to use                                |
|-------------|--------------------------------------------|
| `feat:`     | new feature, new test, new module          |
| `fix:`      | fix a failing test, bug in source code     |
| `refactor:` | restructure without changing behavior      |
| `test:`     | improve coverage on existing functionality |
| `ci:`       | GitHub Actions workflow changes            |
| `docs:`     | README, docstrings                         |
| `chore:`    | dependencies, pyproject.toml, .gitignore   |

```
# Examples for this repo
feat: add APIClient with session-scoped fixture
feat: add parametrized GET tests for /posts endpoint
feat: implement pydantic Post model for response validation
fix: correct base_url fixture scope to session
refactor: extract APIClient to src module
ci: add HTML report artifact upload
chore: add pyproject.toml with hatchling build backend
```

---

## Codex Behavior Rules

- **Always show the full diff** before applying any file change — no exceptions
- **Never proceed** to the next task without explicit confirmation from the user
- **Never modify** files outside the explicit scope of the current task
- **Ask before implementing** if the request is ambiguous or could have multiple valid approaches
- **Every task must end** with green CI or a documented plan to get it green
- **Report but do not fix** issues found outside the current task scope — let the user decide
- **Never use API key mode** — always authenticate with ChatGPT account to use plan quota
- **Respect AGENTS.md scope** — this file applies only to the repo where it lives

---

## Environment Variables Reference

```bash
# Required for AI module — add in Week 6
ANTHROPIC_API_KEY=your_key_here

# Add to .bashrc or .zshrc — never commit the actual value
# Add to GitHub repo Secrets for CI usage
```

```
# .env.example — commit this file, not .env
ANTHROPIC_API_KEY=
```

```
# .gitignore additions — verify these are present
.env
__pycache__/
.pytest_cache/
report.html
results.xml
```