"""Secure code execution: Docker sandbox with subprocess fallback for tests."""

from __future__ import annotations

import json
import shutil
import tempfile
import textwrap
import time
from pathlib import Path

import structlog

from app.config import get_settings
from app.models.schemas import (
    RunRequest,
    RunResponse,
    SubmitRequest,
    SubmitResponse,
    TestResult,
)
from app.services.content import get_problem_raw

logger = structlog.get_logger(__name__)


class RunnerUnavailableError(RuntimeError):
    """Raised when the sandbox cannot execute code."""


def _truncate(text: str, limit: int) -> tuple[str, bool]:
    if len(text.encode("utf-8")) <= limit:
        return text, False
    # Truncate by characters approximating byte limit
    cut = text.encode("utf-8")[:limit].decode("utf-8", errors="ignore")
    return cut + "\n…[truncated]", True


def run_in_docker(code: str, stdin: str = "") -> RunResponse:
    settings = get_settings()
    start = time.perf_counter()

    try:
        import docker  # type: ignore
        from docker.errors import DockerException, ImageNotFound  # type: ignore
    except ImportError as exc:
        raise RunnerUnavailableError("docker SDK not installed") from exc

    try:
        client = docker.from_env()
        client.ping()
    except Exception as exc:  # noqa: BLE001
        raise RunnerUnavailableError(f"Docker unavailable: {exc}") from exc

    work = Path(tempfile.mkdtemp(prefix="codecraft-"))
    try:
        script = work / "main.py"
        script.write_text(code, encoding="utf-8")
        stdin_file = work / "stdin.txt"
        stdin_file.write_text(stdin, encoding="utf-8")

        wrapper = textwrap.dedent(
            """\
            import base64, runpy, sys, traceback
            from io import BytesIO
            images = []
            try:
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                def _show(*a, **k):
                    buf = BytesIO()
                    plt.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    images.append(base64.b64encode(buf.read()).decode("ascii"))
                    plt.close("all")
                plt.show = _show
            except Exception:
                pass
            sys.stdin = open("/workspace/stdin.txt", "r", encoding="utf-8")
            try:
                runpy.run_path("/workspace/main.py", run_name="__main__")
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
                sys.exit(code)
            except Exception:
                traceback.print_exc()
                sys.exit(1)
            if images:
                print("\\n__CODECRAFT_IMAGES__=" + json.dumps(images), file=sys.stderr)
            """
        ).replace("json.dumps", "__import__('json').dumps")
        (work / "wrapper.py").write_text(wrapper, encoding="utf-8")

        try:
            container = client.containers.run(
                image=settings.sandbox_image,
                command=["python", "/workspace/wrapper.py"],
                volumes={str(work): {"bind": "/workspace", "mode": "ro"}},
                network_mode=settings.sandbox_network,
                mem_limit=f"{settings.sandbox_memory_mb}m",
                nano_cpus=1_000_000_000,  # 1 CPU
                pids_limit=settings.sandbox_pids_limit,
                read_only=True,
                user="1000:1000",
                working_dir="/workspace",
                detach=True,
                stdout=True,
                stderr=True,
                tmpfs={"/tmp": "size=16m,uid=1000"},
            )
        except ImageNotFound as exc:
            raise RunnerUnavailableError(
                f"Sandbox image missing: {settings.sandbox_image}. Run: make sandbox"
            ) from exc
        except DockerException as exc:
            raise RunnerUnavailableError(str(exc)) from exc

        timed_out = False
        try:
            result = container.wait(timeout=settings.sandbox_timeout_seconds)
            exit_code = int(result.get("StatusCode", 1))
        except Exception:  # noqa: BLE001
            timed_out = True
            exit_code = 124
            try:
                container.kill()
            except Exception:  # noqa: BLE001
                pass

        raw_out = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
        raw_err = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")
        try:
            container.remove(force=True)
        except Exception:  # noqa: BLE001
            pass

        images: list[str] = []
        if "__CODECRAFT_IMAGES__=" in raw_err:
            marker = "__CODECRAFT_IMAGES__="
            line = [ln for ln in raw_err.splitlines() if marker in ln][-1]
            payload = line.split(marker, 1)[1]
            try:
                images = list(json.loads(payload))
            except json.JSONDecodeError:
                images = []
            raw_err = "\n".join(
                ln for ln in raw_err.splitlines() if marker not in ln
            )

        out, out_trunc = _truncate(raw_out, settings.sandbox_output_limit_bytes)
        err, err_trunc = _truncate(raw_err, settings.sandbox_output_limit_bytes)
        elapsed = (time.perf_counter() - start) * 1000
        return RunResponse(
            stdout=out,
            stderr=err if not timed_out else (err + "\nTimed out").strip(),
            exit_code=exit_code,
            timed_out=timed_out,
            execution_time_ms=elapsed,
            images=images,
            truncated=out_trunc or err_trunc,
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run_in_subprocess(code: str, stdin: str = "") -> RunResponse:
    """Local fallback used in unit tests when Docker is disabled/unavailable.

    Still applies wall-clock timeout and output caps. NOT safe for untrusted
    multi-tenant production — production must use Docker.
    """
    import subprocess
    import sys

    settings = get_settings()
    start = time.perf_counter()
    work = Path(tempfile.mkdtemp(prefix="codecraft-local-"))
    try:
        script = work / "main.py"
        script.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=settings.sandbox_timeout_seconds,
                cwd=str(work),
            )
            out, out_t = _truncate(proc.stdout, settings.sandbox_output_limit_bytes)
            err, err_t = _truncate(proc.stderr, settings.sandbox_output_limit_bytes)
            return RunResponse(
                stdout=out,
                stderr=err,
                exit_code=proc.returncode,
                timed_out=False,
                execution_time_ms=(time.perf_counter() - start) * 1000,
                truncated=out_t or err_t,
            )
        except subprocess.TimeoutExpired as exc:
            out = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            err = (exc.stderr or "") if isinstance(exc.stderr, str) else "Timed out"
            out, out_t = _truncate(out, settings.sandbox_output_limit_bytes)
            err, err_t = _truncate(err, settings.sandbox_output_limit_bytes)
            return RunResponse(
                stdout=out,
                stderr=err or "Timed out",
                exit_code=124,
                timed_out=True,
                execution_time_ms=(time.perf_counter() - start) * 1000,
                truncated=out_t or err_t,
            )
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run_code(request: RunRequest) -> RunResponse:
    settings = get_settings()
    logger.info("run_requested", code_bytes=len(request.code), sandbox_disabled=settings.sandbox_disabled)

    if settings.sandbox_disabled:
        # Prefer subprocess local mode for CI/dev without Docker
        return run_in_subprocess(request.code, request.stdin)

    try:
        return run_in_docker(request.code, request.stdin)
    except RunnerUnavailableError as exc:
        logger.warning("docker_unavailable_fallback", error=str(exc))
        return RunResponse(
            stdout="",
            stderr=(
                f"{exc}. Set SANDBOX_DISABLED=true for local subprocess mode, "
                "or NEXT_PUBLIC_USE_PYODIDE=true for browser execution."
            ),
            exit_code=1,
            timed_out=False,
            execution_time_ms=0,
        )


def _compare(actual: object, expected: object) -> bool:
    return json.dumps(actual, sort_keys=True, default=str) == json.dumps(
        expected, sort_keys=True, default=str
    )


def _harness_script(user_code: str, function_name: str, tests: list[dict]) -> str:
    return textwrap.dedent(
        f"""\
        import json, traceback
        USER_CODE = {user_code!r}
        FUNCTION_NAME = {function_name!r}
        TESTS = {json.dumps(tests)}

        ns = {{}}
        try:
            exec(compile(USER_CODE, "<user>", "exec"), ns)
        except Exception as e:
            print(json.dumps([{{"name": "compile", "ok": False, "error": traceback.format_exc()}}]))
            raise SystemExit(0)

        fn = ns.get(FUNCTION_NAME)
        if fn is None:
            print(json.dumps([{{"name": "compile", "ok": False, "error": f"Missing function {{FUNCTION_NAME}}"}}]))
            raise SystemExit(0)

        results = []
        for t in TESTS:
            name = t.get("name", "test")
            args = t.get("args", {{}})
            expected = t.get("expected")
            try:
                actual = fn(**args)
                ok = json.dumps(actual, sort_keys=True, default=str) == json.dumps(expected, sort_keys=True, default=str)
                results.append({{
                    "name": name,
                    "ok": ok,
                    "expected": expected,
                    "actual": actual,
                    "error": None if ok else "Output mismatch",
                }})
            except Exception:
                results.append({{
                    "name": name,
                    "ok": False,
                    "expected": expected,
                    "actual": None,
                    "error": traceback.format_exc(),
                }})
        print(json.dumps(results, default=str))
        """
    )


def submit_code(request: SubmitRequest) -> SubmitResponse:
    problem = get_problem_raw(request.problem_slug)
    if problem is None:
        return SubmitResponse(
            passed=False,
            results=[
                TestResult(
                    name="problem",
                    passed=False,
                    visible=True,
                    error=f"Unknown problem: {request.problem_slug}",
                )
            ],
            total=1,
            passed_count=0,
        )

    function_name = str(problem.get("function_name") or "solve")
    visible_tests = list(problem.get("visible_tests") or [])
    hidden_tests = list(problem.get("hidden_tests") or [])
    all_tests = [
        *[ {**t, "_visible": True} for t in visible_tests ],
        *[ {**t, "_visible": False} for t in hidden_tests ],
    ]
    if not all_tests:
        return SubmitResponse(passed=False, results=[], total=0, passed_count=0)

    harness = _harness_script(request.code, function_name, all_tests)
    run = run_code(RunRequest(code=harness, stdin=""))
    results: list[TestResult] = []

    if run.timed_out:
        return SubmitResponse(
            passed=False,
            results=[
                TestResult(
                    name="timeout",
                    passed=False,
                    visible=True,
                    error="Execution timed out",
                )
            ],
            total=len(all_tests),
            passed_count=0,
        )

    try:
        payload = json.loads(run.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return SubmitResponse(
            passed=False,
            results=[
                TestResult(
                    name="runner",
                    passed=False,
                    visible=True,
                    error=run.stderr or run.stdout or "Failed to parse harness output",
                )
            ],
            total=len(all_tests),
            passed_count=0,
        )

    for item, meta in zip(payload, all_tests):
        visible = bool(meta.get("_visible", True))
        passed = bool(item.get("ok"))
        results.append(
            TestResult(
                name=str(item.get("name", meta.get("name", "test"))),
                passed=passed,
                visible=visible,
                runtime_ms=0,
                expected=json.dumps(item.get("expected"), default=str) if visible else None,
                actual=(
                    json.dumps(item.get("actual"), default=str)
                    if visible and not passed
                    else (json.dumps(item.get("actual"), default=str) if visible else None)
                ),
                error=(
                    None
                    if passed
                    else (str(item.get("error")) if visible else "Hidden test failed")
                ),
            )
        )

    passed_count = sum(1 for r in results if r.passed)
    return SubmitResponse(
        passed=passed_count == len(results) and len(results) > 0,
        results=results,
        total=len(results),
        passed_count=passed_count,
    )
