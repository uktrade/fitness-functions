import json
import os
import sqlite3
from datetime import datetime
from itertools import islice
import matplotlib.pyplot as plt


# Function to normalise the graph data
def normalise(fitness_dictionary):
    for key, value in islice(fitness_dictionary.items(), 1, None):
        norm_range = max(value) - min(value)
        norm_array = []
        for n in value:
            if norm_range != 0:
                norm_array.append(((n-min(value))/norm_range)*100)
            else:
                norm_array.append((1/len(value))*100)
        fitness_dictionary[key] = norm_array
    return fitness_dictionary


def publish(project_path):
    project_fitness_directory = os.path.join(project_path, "fitness")

    connection = sqlite3.connect(
        os.path.join(project_fitness_directory, "fitness_metrics.db")
    )
    cur = connection.cursor()

    with connection:
        cur.execute("SELECT * FROM FITNESS_METRICS")
        fitness_metrics_array = cur.fetchall()

    # Intialise empty dictionary
    fitness_metrics_dict = {"dates": []}
    for record in fitness_metrics_array:
        literal_metrics_dict = json.loads(record[2])
        fitness_metrics_keys = {key: [] for key in literal_metrics_dict.keys()}
        fitness_metrics_dict.update(fitness_metrics_keys)

    # Update each record with the same metric keys
    metric_keys_dict = {}
    for record in fitness_metrics_array:
        for key in json.loads(record[2]).keys():
            if key not in metric_keys_dict.keys():
                metric_keys_dict = json.loads(record[2])

    for record in fitness_metrics_array:
        literal_metrics_dict = json.loads(record[2])
        for key in metric_keys_dict.keys():
            if key not in literal_metrics_dict.keys():
                literal_metrics_dict[key] = 0

        # Populate dictionary with applicable data
        fitness_metrics_dict["dates"].append(
            datetime.strptime(record[1], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y")
        )
        for key, value in literal_metrics_dict.items():
            fitness_metrics_dict[key].append((int(value)))

    fitness_metrics_dict = normalise(fitness_metrics_dict)

    # Plot graph data points
    for key, value in islice(fitness_metrics_dict.items(), 1, None):
        plt.plot(
            fitness_metrics_dict["dates"],
            value,
            label=key.replace("_", " ").capitalize(),
            marker='2'
        )

    # Stylise graph
    plt.title("Fitness metrics")
    plt.xlabel("Date")
    plt.ylabel("Normalised value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left", prop={"size": 6})
    plt.tight_layout()
    plt.gca().axes.get_xaxis().set_ticks([fitness_metrics_dict["dates"][0], fitness_metrics_dict["dates"][-1]])

    # Save graph to fitness folder in project
    return plt.savefig(
        os.path.join(project_fitness_directory, "fitness_metrics_graph.png")
    ), print(
        "Metrics published:\n",
        *[f"{key}\n" for key, value in islice(fitness_metrics_dict.items(), 1, None)],
        f'\nUpdated fitness metrics graph published to {os.path.join(project_fitness_directory, "fitness_metrics_graph.png")}',
    )
