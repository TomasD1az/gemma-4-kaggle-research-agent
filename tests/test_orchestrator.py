import unittest
from tempfile import TemporaryDirectory

from agent.orchestrator import AutonomousLabOrchestrator


class OrchestratorTests(unittest.TestCase):
    def test_run_executes_plan_steps(self):
        with TemporaryDirectory() as output_dir:
            orchestrator = AutonomousLabOrchestrator(output_directory=output_dir)

            result = orchestrator.run("Test query")

            self.assertTrue(result.planner_thought.startswith("<|think|>"))
            self.assertEqual(len(result.steps), 3)
            self.assertTrue(all(step.success for step in result.steps))


if __name__ == "__main__":
    unittest.main()
