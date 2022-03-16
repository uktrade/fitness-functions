from fitness_functions import run
from tests import FitnessFunctionsTestBase


class TestMetricCollection(FitnessFunctionsTestBase):
    mock_project_path = None
    mock_python_file = "mock_code_path/mock_file.py"

    def run_metric_collection(self):
        return run(self.mock_project_path, "mock_code_path")

    def setUp(self) -> None:
        self.collected_metrics = self.run_metric_collection()

    def test_noqa_occurrences(self):
        self.assertEqual(self.collected_metrics["noqa_occurrences"], "1")

    def test_line_of_code(self):
        self.assertEqual(self.collected_metrics["lines_of_code"], "3")
