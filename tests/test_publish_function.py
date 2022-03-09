import math
import os
import tempfile
from fitness_functions import publish
from tests import FitnessFunctionsTestBase
from fitness_functions.publish import normalise


class TestMetricCollection(FitnessFunctionsTestBase):
    def setUp(self):
        self.dummy_metrics_dict = {'dates': ['22/04/2022', '23/04/2022'], 'noqa_occurrences': [12, 24]}

    def test_normalise_function(self):
        array_for_normalisation = self.dummy_metrics_dict['noqa_occurrences']

        # Formula for vector form normalization: x = sqrt(Σ𝑥2𝑖)
        normalised_denominator = 0
        for digit in array_for_normalisation:
            normalised_denominator += (int(digit) ** 2)
        normalised_denominator = math.sqrt(normalised_denominator)

        # Graph plots on y axis between 0-100 so need to round and convert to whole number
        normalised_array = []
        for digit in array_for_normalisation:
            normalised_array.append(round(int(digit) / normalised_denominator, 2) * 100)

        normalise_data = normalise(self.dummy_metrics_dict)

        self.assertEqual(normalise_data['noqa_occurrences'], normalised_array)

    def test_publish_function(self):
        with tempfile.TemporaryDirectory() as self.mock_project_path:
            mock_project_path = self.mock_project_path
            mock_graph_path = os.path.join(mock_project_path, 'fitness/fitness_metrics_graph.png')
            publish(mock_project_path, mock_project_path)
            assert os.path.isfile(mock_graph_path) and os.access(mock_graph_path, os.R_OK)
