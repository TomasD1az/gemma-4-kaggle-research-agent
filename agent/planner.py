from __future__ import annotations

from .types import PlanStep, ResearchPlan


class Planner31B:
    """High-level planner for think/code/verify workflows."""

    def create_plan(self, query: str) -> ResearchPlan:
        thought = (
            "<|think|>Break the request into ingestion, analysis, and reporting tasks. "
            "Generate code step-by-step and validate each result locally."
        )
        steps = [
            PlanStep(id=1, objective=f"Parse and inspect input data for: {query}"),
            PlanStep(id=2, objective="Run quantitative analysis and produce core metrics."),
            PlanStep(id=3, objective="Generate a concise research summary and save artifacts."),
        ]
        return ResearchPlan(thought=thought, steps=steps)

    def reflect_on_failure(self, step_objective: str, failed_code: str, error: str) -> str:
        return (
            "<|think|>The previous code failed. "
            f"Step: {step_objective}. "
            f"Observed error: {error.strip() or 'unknown error'}. "
            "Generate a safer fix with explicit imports and defensive checks."
        )
