import tempfile
import unittest


class FitnessFunctionsTestBase(unittest.TestCase):
    def run(self, result=None):
        with tempfile.TemporaryDirectory() as mock_project_path:
            with tempfile.TemporaryDirectory() as mock_code_path:
                self.mock_project_path = mock_project_path
                self.mock_code_path = mock_code_path
                super().run(result)
