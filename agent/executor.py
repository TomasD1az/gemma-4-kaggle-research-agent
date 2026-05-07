from __future__ import annotations

from typing import Dict


class PythonCodeExecutor:
    """Code-focused executor that emits native function-call payloads."""

    def generate_function_call(self, step_objective: str, query: str) -> Dict[str, object]:
        code = (
            "from pathlib import Path\n"
            "output_dir = Path('output')\n"
            "output_dir.mkdir(parents=True, exist_ok=True)\n"
            f"print('Executing step:', {step_objective!r})\n"
            f"print('Query context:', {query!r})\n"
        )
        return {"name": "run_python", "arguments": {"code": code}}

    def generate_fix_function_call(self, reflection: str, step_objective: str) -> Dict[str, object]:
        code = (
            "from pathlib import Path\n"
            "output_dir = Path('output')\n"
            "output_dir.mkdir(parents=True, exist_ok=True)\n"
            "with (output_dir / 'summary.txt').open('a', encoding='utf-8') as handle:\n"
            f"    handle.write('Recovered step: {step_objective}\\n')\n"
            f"print({reflection!r})\n"
            "print('Recovery execution completed.')\n"
        )
        return {"name": "run_python", "arguments": {"code": code}}
