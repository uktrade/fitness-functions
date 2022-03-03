import os
import sqlite3

from fitness_functions import run
from . import FitnessFunctionsTestBase


class TestSetup(FitnessFunctionsTestBase):

    def test_fitness_directory_created(self):
        self.assertFalse(os.path.exists(os.path.join(self.mock_project_path, 'fitness')))
        run(self.mock_project_path, self.mock_code_path)
        self.assertTrue(os.path.exists(os.path.join(self.mock_project_path, 'fitness')))

    def test_database_created(self):
        self.assertFalse(os.path.exists(os.path.join(self.mock_project_path, 'fitness', 'fitness_metrics.db')))
        run(self.mock_project_path, self.mock_code_path)
        self.assertTrue(os.path.exists(os.path.join(self.mock_project_path, 'fitness', 'fitness_metrics.db')))

    def test_database_correct(self):
        run(self.mock_project_path, self.mock_code_path)
        connection = sqlite3.connect(os.path.join(self.mock_project_path, 'fitness', 'fitness_metrics.db'))
        result = connection.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='FITNESS_METRICS';""")
        self.assertEqual(len(result.fetchone()), 1)

        columns = ['date_collected', 'metrics']
        for column in columns:
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute(f'ALTER TABLE FITNESS_METRICS ADD COLUMN {column};')
