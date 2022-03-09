from fitness_functions import publish, run
from tests import FitnessFunctionsTestBase
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from fitness_functions.publish import normalise
import math


class TestMetricCollection(FitnessFunctionsTestBase):
    mock_project_path = 'mock_code_path'
    mock_python_file = 'mock_code_path/mock_file.py'

    def run_metric_collection(self):
        return run(self.mock_project_path, 'mock_code_path')

    def run_publish_function(self):
        return publish(self.mock_project_path)

    def setUp(self) -> None:
        self.collected_metrics = self.run_metric_collection()
        self.publish_graph = self.run_publish_function()
        self.dummy_metrics_dict = {'dates': ['22/04/2022', '23/04/2022'], 'noqa_occurrences': [12, 24]}

    def test_normalise_function(self):
        array_for_normalisation = self.dummy_metrics_dict['noqa_occurrences']

        # Formula for vector form normalization: x = sqrt(Σ𝑥2𝑖)
        normalised_denominator = 0
        for digit in array_for_normalisation:
            normalised_denominator += (int(digit)**2)
        normalised_denominator = math.sqrt(normalised_denominator)
        normalised_array = []

        # Graph plots on y axis between 0-100 so need to round and convert to whole number
        for digit in array_for_normalisation:
            normalised_array.append(round((int(digit)/normalised_denominator), 2)*100)

        normalise_data = normalise(self.dummy_metrics_dict)

        self.assertEqual(normalise_data['noqa_occurrences'], normalised_array)

