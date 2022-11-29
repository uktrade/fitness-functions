import datetime
import json
import os
import sqlite3
import subprocess
from pathlib import Path

from setuptools import find_packages

from fitness_functions.utils import check_last_collection


def run(project_path, code_path):
    collected_metrics = {}
    project_fitness_directory = os.path.join(project_path, "fitness")
    if not os.path.isdir(project_fitness_directory):
        os.mkdir(project_fitness_directory)

    connection = sqlite3.connect(
        os.path.join(project_fitness_directory, "fitness_metrics.db")
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS FITNESS_METRICS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            date_collected TEXT NOT NULL,
            metrics TEXT NOT NULL
        );
    """
    )

    if check_last_collection(connection):
        noqa_occurrences = subprocess.run(
            f'grep -R --include="*.py" "# noqa" "{code_path}" | wc -l',
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        )
        collected_metrics["noqa_occurrences"] = noqa_occurrences.stdout.strip()

        lines_of_code = subprocess.run(
            f"find \"{code_path}\" \( -path '*/migrations' \) -prune -o -type f -exec cat {{}} + | wc -l",
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        collected_metrics["lines_of_code"] = lines_of_code.stdout.strip()

        if lines_of_code:
            number_of_files = subprocess.run(
                f"find \"{code_path}\" \( -path '*/migrations' \) -o -type f | wc -l",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            collected_metrics["average_lines_of_code_per_file"] = round(
                int(collected_metrics["lines_of_code"]) / int(number_of_files.stdout.strip()), 2
            )

        package_sizes = []
        for pkg in find_packages(code_path):
            pkgpath = os.path.join(code_path, pkg.replace(".", os.path.sep))
            root_directory = Path(pkgpath)
            package_size = (
                               sum(f.stat().st_size for f in root_directory.glob("**/*") if f.is_file())
                           ) / float(
                1 << 10
            )  # Kb
            package_sizes.append(package_size)

        if package_sizes:
            collected_metrics["average_package_size"] = round(
                sum(package_sizes) / len(package_sizes), 2
            )
            collected_metrics["largest_package_size"] = round(max(package_sizes), 2)


        today_string = datetime.datetime.today().isoformat()

        connection.execute(
            f"""
            INSERT INTO FITNESS_METRICS(date_collected, metrics) VALUES('{today_string}', '{json.dumps(collected_metrics)}')
        """
        )
        connection.commit()
        string_collected_metrics = [
            f"{key} ---- {value}\n" for key, value in collected_metrics.items()
        ]
        print("Fitness Functions have finished:\n\n", *string_collected_metrics)
        return collected_metrics
