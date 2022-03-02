"""Fitness Functions.

Usage:
  fitness-functions run <project_path> <code_path>
  fitness-functions publish <project_path> <code_path>

Options:
  <project_path>     The path of the project directory containing the codebase
  <code_path>        The path of the directory containing the code you would like to run fitness functions on

'run' will analyse the code in the directory defined by the <code_path> variable, and save the metrics to
<project_path>/fitness/fitness_metrics.db (it will create the directory and database if they don't already exist)

'publish' will generate a graph using the <project_path>/fitness/fitness_metrics.db data, save it as a base64 PNG
string in the READ.ME file located in <project_path>
"""
import importlib
import sys
import os
from run import run
from publish import publish


def get_path(path):
    return os.getcwd() if path == '.' else path


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print(__doc__)
    elif args[0] in ['run', 'publish']:
        try:
            project_path = get_path(args[1])
            code_path = get_path(args[2])
            if not os.path.isdir(project_path) or not os.path.isdir(code_path):
                print(f'Please provide valid directory(ies) to run fitness functions on.')
            else:
                if args[0] == 'run':
                    run(project_path, code_path)
                elif args[0] == 'publish':
                    publish(project_path, code_path)
        except IndexError:
            print(f'Not enough arguments were passed, please see:\n{__doc__}')
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
