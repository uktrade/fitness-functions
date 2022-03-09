from fitness_functions import run
from tests import FitnessFunctionsTestBase


class TestMetricCollection(FitnessFunctionsTestBase):
    mock_project_path = 'tests/mock_code_path'
    mock_python_file = 'tests/mock_code_path/mock_file.py'

    def run_metric_collection(self):
        return run(self.mock_project_path, self.mock_python_file)

    def setUp(self) -> None:
        self.collected_metrics = self.run_metric_collection()

    def test_noqa_occurrences(self):
        self.assertEqual(self.collected_metrics['noqa_occurrences'], '1')

    def test_line_of_code(self):
        self.assertEqual(self.collected_metrics['lines_of_code'], '3')
