from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from sandbox.runner import LocalPythonSandbox, SandboxRunResult

from .executor import PythonCodeExecutor
from .planner import Planner31B
from .security import monitor_external_calls
from .types import StepExecutionResult


@dataclass
class LabRunResult:
    query: str
    planner_thought: str
    steps: List[StepExecutionResult]
    output_directory: Path
    external_api_attempts: int


class AutonomousLabOrchestrator:
    def __init__(self, output_directory: Path | str = "output") -> None:
        self.output_directory = Path(output_directory)
        self.planner = Planner31B()
        self.executor = PythonCodeExecutor()
        self.sandbox = LocalPythonSandbox(workspace=self.output_directory)

    def _execute_call(self, function_call: dict) -> SandboxRunResult:
        if function_call.get("name") != "run_python":
            raise ValueError("Executor must call run_python for local sandbox execution.")
        arguments = function_call.get("arguments") or {}
        code = arguments.get("code")
        if not isinstance(code, str) or not code.strip():
            raise ValueError("run_python requires non-empty code.")
        return self.sandbox.run_python(code)

    def run(self, query: str) -> LabRunResult:
        plan = self.planner.create_plan(query)
        step_results: List[StepExecutionResult] = []

        with monitor_external_calls() as network_monitor:
            for step in plan.steps:
                function_call = self.executor.generate_function_call(step.objective, query)
                run_result = self._execute_call(function_call)
                reflection = ""
                used_code = function_call["arguments"]["code"]

                if not run_result.success:
                    reflection = self.planner.reflect_on_failure(step.objective, used_code, run_result.stderr)
                    fix_call = self.executor.generate_fix_function_call(reflection, step.objective)
                    used_code = fix_call["arguments"]["code"]
                    run_result = self._execute_call(fix_call)

                step_results.append(
                    StepExecutionResult(
                        step_id=step.id,
                        objective=step.objective,
                        code=used_code,
                        success=run_result.success,
                        stdout=run_result.stdout,
                        stderr=run_result.stderr,
                        reflection=reflection,
                    )
                )

        return LabRunResult(
            query=query,
            planner_thought=plan.thought,
            steps=step_results,
            output_directory=self.output_directory,
            external_api_attempts=network_monitor.attempts,
        )
