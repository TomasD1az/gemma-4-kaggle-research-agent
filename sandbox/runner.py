from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SandboxRunResult:
    success: bool
    stdout: str
    stderr: str
    returncode: int


class LocalPythonSandbox:
    """Executes generated Python in an isolated subprocess."""

    def __init__(self, workspace: Path | str = "output", timeout_seconds: int = 45) -> None:
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.timeout_seconds = timeout_seconds

    def run_python(self, code: str) -> SandboxRunResult:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as script_file:
            script_file.write(code)
            script_path = Path(script_file.name)

        try:
            completed = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.workspace.parent.resolve()),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            return SandboxRunResult(
                success=completed.returncode == 0,
                stdout=completed.stdout,
                stderr=completed.stderr,
                returncode=completed.returncode,
            )
        except subprocess.TimeoutExpired as exc:
            return SandboxRunResult(
                success=False,
                stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + "\nExecution timed out.",
                returncode=124,
            )
        finally:
            script_path.unlink(missing_ok=True)
