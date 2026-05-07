import unittest
from pathlib import Path

from sandbox.runner import LocalPythonSandbox


class LocalPythonSandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = Path("/tmp/gemma4-test-output")
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.sandbox = LocalPythonSandbox(workspace=self.workspace)

    def test_run_python_success(self):
        result = self.sandbox.run_python("print('ok')")
        self.assertTrue(result.success)
        self.assertIn("ok", result.stdout)

    def test_run_python_failure(self):
        result = self.sandbox.run_python("raise RuntimeError('boom')")
        self.assertFalse(result.success)
        self.assertIn("boom", result.stderr)


if __name__ == "__main__":
    unittest.main()
