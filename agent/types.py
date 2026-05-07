from __future__ import annotations

from typing import List

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - fallback for lightweight environments
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def Field(default: str = "", description: str = "") -> str:
        return default


class PlanStep(BaseModel):
    id: int
    objective: str


class ResearchPlan(BaseModel):
    thought: str = Field(description="Planner internal monologue")
    steps: List[PlanStep]


class StepExecutionResult(BaseModel):
    step_id: int
    objective: str
    code: str
    success: bool
    stdout: str
    stderr: str
    reflection: str = ""
