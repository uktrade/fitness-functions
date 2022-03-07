import os
import ast
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def publish(project_path, code_path):
    project_fitness_directory = os.path.join(project_path, 'fitness')

    connection = sqlite3.connect(os.path.join(project_fitness_directory, 'fitness_metrics.db'))
    cur = connection.cursor()

    with connection:
        cur.execute("SELECT * FROM FITNESS_METRICS")
        fitness_metrics_array = cur.fetchall()

    plt.ylabel('Value')
    plt.xlabel('Date')

    dates = []
    noqa_occurrences = []
    lines_of_code = []
    average_package_size = []
    largest_package_size = []
    average_coverage = []
    covered_lines = []

    for record in fitness_metrics_array:
        dates.append(datetime.strptime(record[1], '%Y-%m-%dT%H:%M:%S.%f'))

        literal_metrics_dict = ast.literal_eval(record[2])
        noqa_occurrences.append(literal_metrics_dict.get("noqa_occurrences"))
        lines_of_code.append(literal_metrics_dict.get("lines_of_code"))
        average_package_size.append(literal_metrics_dict.get("average_package_size"))
        largest_package_size.append(literal_metrics_dict.get("largest_package_size"))
        average_coverage.append(literal_metrics_dict.get("average_coverage"))
        covered_lines.append(literal_metrics_dict.get("covered_lines"))

    plt.plot(dates, noqa_occurrences, label='#noqa occurrences')
    plt.plot(dates, lines_of_code, label='Lines of code')
    plt.plot(dates, average_package_size, label='Average package size')
    plt.plot(dates, largest_package_size, label='Largest package size')
    plt.plot(dates, average_coverage, label='Average coverage')
    plt.plot(dates, covered_lines, label='Covered lines')
    plt.legend()

    plt.savefig(os.path.join(project_fitness_directory, 'fitness_metrics_graph.png'))


publish('/Users/dituser/Documents/GitHub/trade-remedies-api', '/Users/dituser/Documents/GitHub/trade-remedies-api/trade_remedies_api')
