import os
import ast
import sqlite3
from datetime import datetime
from itertools import islice
import matplotlib.pyplot as plt
from sklearn import preprocessing
from fitness_functions.run import run


# Function to normalise the graph data
def normalise(fitness_dictionary):
    for key, value in islice(fitness_dictionary.items(), 1, None):
        fitness_dictionary[key] = [round(n * 100, 0) for n in preprocessing.normalize([value])[0]]
    return fitness_dictionary


def publish(project_path, code_path):
    project_fitness_directory = os.path.join(project_path, 'fitness')

    try:
        connection = sqlite3.connect(os.path.join(project_fitness_directory, 'fitness_metrics.db'))
        cur = connection.cursor()
    except:
        run(project_path, code_path)
        connection = sqlite3.connect(os.path.join(project_fitness_directory, 'fitness_metrics.db'))
        cur = connection.cursor()

    with connection:
        cur.execute("SELECT * FROM FITNESS_METRICS")
        fitness_metrics_array = cur.fetchall()

    # Intialise empty dictionary
    fitness_metrics_dict = {"dates": []}
    for record in fitness_metrics_array:
        literal_metrics_dict = ast.literal_eval(record[2])
        fitness_metrics_keys = {key: [] for key in literal_metrics_dict.keys()}
        fitness_metrics_dict.update(fitness_metrics_keys)

    # Populate dictionary with applicable data
    for record in fitness_metrics_array:
        literal_metrics_dict = ast.literal_eval(record[2])
        fitness_metrics_dict["dates"].append(datetime.strptime(record[1], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d/%m/%Y"))
        for key, value in literal_metrics_dict.items():
            fitness_metrics_dict[key].append((int(value)))

    fitness_metrics_dict = normalise(fitness_metrics_dict)

    # Plot graph data points
    for key, value in islice(fitness_metrics_dict.items(), 1, None):
        plt.plot(fitness_metrics_dict["dates"], value, label=key.replace("_", " ").capitalize())

    # Stylise graph
    plt.title('Fitness metrics')
    plt.xlabel('Date')
    plt.ylabel('Normalised value')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', prop={'size': 6})
    plt.tight_layout()

    # Save graph to fitness folder in project
    return plt.savefig(os.path.join(project_fitness_directory, 'fitness_metrics_graph.png'))
