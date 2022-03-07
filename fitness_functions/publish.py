import os
import ast
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

from sklearn import preprocessing


def normalise(fitness_array):
    normalised_array = preprocessing.normalize([fitness_array])
    digestible_array = [round(int(n), 2)*100 for n in normalised_array[0]]
    return digestible_array


def publish(project_path, code_path):
    project_fitness_directory = os.path.join(project_path, 'fitness')

    connection = sqlite3.connect(os.path.join(project_fitness_directory, 'fitness_metrics.db'))
    cur = connection.cursor()

    with connection:
        cur.execute("SELECT * FROM FITNESS_METRICS")
        fitness_metrics_array = cur.fetchall()

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

        noqa_occurrences.append(float(literal_metrics_dict.get("noqa_occurrences")))
        lines_of_code.append(float(literal_metrics_dict.get("lines_of_code")))
        average_package_size.append(float(literal_metrics_dict.get("average_package_size")))
        largest_package_size.append(float(literal_metrics_dict.get("largest_package_size")))
        average_coverage.append(float(literal_metrics_dict.get("average_coverage")) if literal_metrics_dict.get("average_coverage") else 0)
        covered_lines.append(float(literal_metrics_dict.get("covered_lines")) if literal_metrics_dict.get("covered_lines") else 0)

    plt.plot(dates, normalise(average_package_size), label='Average package size')
    plt.plot(dates, normalise(largest_package_size), label='Largest package size')
    plt.plot(dates, normalise(average_coverage), label='Average coverage')
    plt.plot(dates, normalise(noqa_occurrences), label='noqa occurrences')
    plt.plot(dates, normalise(covered_lines), label='Covered lines')

    plt.xlabel('Date')
    plt.ylabel('Normalised value')

    plt.legend()
    plt.show()

    plt.savefig(os.path.join(project_fitness_directory, 'fitness_metrics_graph.png'))
