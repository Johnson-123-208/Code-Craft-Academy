"""Runner unit tests including malicious / abusive inputs."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

# Force local subprocess mode for CI / machines without Docker
os.environ["SANDBOX_DISABLED"] = "true"
os.environ.setdefault(
    "CONTENT_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "content")),
)

from app.main import app  # noqa: E402
from app.models.schemas import RunRequest, SubmitRequest  # noqa: E402
from app.services import runner  # noqa: E402

client = TestClient(app)


def test_run_hello() -> None:
    result = runner.run_code(RunRequest(code='print("hi")'))
    assert result.exit_code == 0
    assert "hi" in result.stdout
    assert not result.timed_out


def test_run_stdin() -> None:
    result = runner.run_code(
        RunRequest(code="print(input())", stdin="codecraft\n")
    )
    assert result.exit_code == 0
    assert "codecraft" in result.stdout


def test_infinite_loop_times_out() -> None:
    result = runner.run_code(RunRequest(code="while True:\n    pass\n"))
    assert result.timed_out or result.exit_code != 0


def test_output_cap() -> None:
    code = "print('x' * 200000)"
    result = runner.run_code(RunRequest(code=code))
    assert result.truncated or len(result.stdout) < 200000


def test_file_escape_attempt_does_not_crash_runner() -> None:
    code = "open('/etc/passwd').read()"
    result = runner.run_code(RunRequest(code=code))
    # May error depending on OS; runner must return a structured response
    assert isinstance(result.exit_code, int)


def test_network_attempt() -> None:
    code = (
        "import urllib.request\n"
        "urllib.request.urlopen('http://example.com', timeout=1)\n"
    )
    result = runner.run_code(RunRequest(code=code))
    # Without network isolation in subprocess mode this may succeed;
    # ensure runner still responds.
    assert isinstance(result.stdout, str)


def test_submit_two_sum_reference() -> None:
    from app.services.content import get_problem_raw

    problem = get_problem_raw("two-sum")
    assert problem is not None
    code = problem["reference_solution"]
    response = runner.submit_code(
        SubmitRequest(problem_slug="two-sum", code=code)
    )
    assert response.passed
    assert response.passed_count == response.total


def test_api_run_endpoint() -> None:
    res = client.post("/api/run", json={"code": "print(2+2)", "stdin": ""})
    assert res.status_code == 200
    data = res.json()
    assert "4" in data["stdout"]


def test_fork_bomb_string_does_not_hang() -> None:
    # Soft check: massive process spawn attempts should not hang the test suite
    code = "import os\n[os.fork() for _ in range(100)] if hasattr(os, 'fork') else print('no-fork')\n"
    result = runner.run_code(RunRequest(code=code))
    assert result.execution_time_ms < 15_000
