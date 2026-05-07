import unittest
from pathlib import Path

from agent.orchestrator import AutonomousLabOrchestrator


class OrchestratorTests(unittest.TestCase):
    def test_run_executes_plan_steps(self):
        output_dir = Path("/tmp/gemma4-orchestrator-output")
        output_dir.mkdir(parents=True, exist_ok=True)
        orchestrator = AutonomousLabOrchestrator(output_directory=output_dir)

        result = orchestrator.run("Test query")

        self.assertTrue(result.planner_thought.startswith("<|think|>"))
        self.assertEqual(len(result.steps), 3)
        self.assertTrue(all(step.success for step in result.steps))


if __name__ == "__main__":
    unittest.main()
