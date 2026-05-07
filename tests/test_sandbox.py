import unittest
from tempfile import TemporaryDirectory

from sandbox.runner import LocalPythonSandbox


class LocalPythonSandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.sandbox = LocalPythonSandbox(workspace=self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

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
