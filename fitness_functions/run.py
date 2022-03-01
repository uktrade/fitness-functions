import datetime
import json
import os
import sqlite3
import subprocess


def run(project_directory):
    collected_metrics = {}
    project_fitness_directory = os.path.join(project_directory, 'fitness')
    if not os.path.isdir(project_fitness_directory):
        os.mkdir(project_fitness_directory)
        # create default config file

    connection = sqlite3.connect(os.path.join(project_fitness_directory, 'fitness_metrics.db'))
    connection.execute("""
        CREATE TABLE IF NOT EXISTS FITNESS_METRICS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            date_collected TEXT NOT NULL,
            metrics TEXT NOT NULL
        );
    """)

    noqa_occurrences = subprocess.run(
        f"grep -R --include=\"*.py\" \"# noqa\" \"{project_directory}\" | wc -l",
        capture_output=True,
        text=True,
        shell=True,
        check=True
    )
    collected_metrics['noqa_occurrences'] = noqa_occurrences.stdout.strip()

    lines_of_code = subprocess.run(
        f"find \"{project_directory}\" \( -path '*/migrations' \) -prune -o -type f -exec cat {{}} + | wc -l",
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
    collected_metrics['lines_of_code'] = lines_of_code.stdout.strip()

    '''init_file = os.path.join(project_directory, '__init__.py')
    if not os.path.exists(init_file):
        open(init_file, 'w').close()

    pylint_output = StringIO()  # Custom open stream
    reporter = JSONReporter(pylint_output)
    pylint.lint.Run(
        ['--disable=C0114', '--disable=C0116', '--disable=C0115', '--disable=E0401', project_directory],
        reporter=reporter,
        do_exit=False
    )

    os.remove(init_file)'''

    today_string = datetime.datetime.today().isoformat()

    connection.execute(f"""
        INSERT INTO FITNESS_METRICS(date_collected, metrics) VALUES('{today_string}', '{json.dumps(collected_metrics)}')
    """)
    connection.commit()
