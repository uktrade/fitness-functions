import json
import os
import sqlite3
from collections import defaultdict
from datetime import datetime
from itertools import islice

import matplotlib.pyplot as plt

colours = {
    0: "red",
    1: "green",
    2: "blue",
    3: "brown",
    4: "orange",
    5: "black",
    6: "pink",
    7: "purple"
}


def publish(project_path):
    project_fitness_directory = os.path.join(project_path, "fitness")
    connection = sqlite3.connect(
        os.path.join(project_fitness_directory, "fitness_metrics.db")
    )
    cur = connection.cursor()

    print(f"Publishing fitness functions in {project_fitness_directory}")
    with connection:
        cur.execute("SELECT * FROM FITNESS_METRICS")
        fitness_metrics_array = cur.fetchall()

    # Initialise empty dictionary
    fitness_metrics_dict = {"dates": []}
    new_fitness_metrics_dict = defaultdict(lambda: defaultdict(list))
    for record in fitness_metrics_array:
        literal_metrics_dict = json.loads(record[2])
        for key, value in literal_metrics_dict.items():
            new_fitness_metrics_dict[key]["date_values"].append(
                datetime.strptime(record[1], "%Y-%m-%dT%H:%M:%S.%f"))
            new_fitness_metrics_dict[key]["data_values"].append(int(value))
    number_of_plots = len(new_fitness_metrics_dict)
    fig, axs = plt.subplots(number_of_plots, constrained_layout=True, figsize=(10, 10))

    for index, (key, value) in enumerate(new_fitness_metrics_dict.items()):
        ax = axs[index]
        ax.set_title(key)
        ax.plot(
            value["date_values"],
            value["data_values"],
            color=colours.get(index, "black")
        )

        my_xticks = ax.get_xticks()
        my_yticks = ax.get_yticks()
        ax.set_xticks([my_xticks[0], my_xticks[-1]])
        ax.set_yticks([my_yticks[0], my_yticks[-1]])

    # Save graph to fitness folder in project
    return fig.savefig(
        os.path.join(project_fitness_directory, "fitness_metrics_graph.png")
    ), print(
        "Metrics published:\n",
        *[f"{key}\n" for key, value in islice(fitness_metrics_dict.items(), 1, None)],
        f'\nUpdated fitness metrics graph published to {os.path.join(project_fitness_directory, "fitness_metrics_graph.png")}',
    )
