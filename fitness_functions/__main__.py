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
import argparse
import os


class PathAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == '.':
            values = os.getcwd()
        else:
            if not os.path.isdir(values):
                raise argparse.ArgumentTypeError(f"{values} is not a valid directory.")
        setattr(namespace, self.dest, values)


def main():
    from .publish import publish
    from .run import run

    my_parser = argparse.ArgumentParser(
        prog='fitness-functions',
        description='Collect and display code quality metrics for your application.',
    )
    my_parser.add_argument(
        'action',
        choices=['run', 'publish'],
        type=str,
        help="What you would like to do, 'run' (collect metrics) or 'publish' (graph and save to READ.ME."
    )
    my_parser.add_argument(
        'project_path',
        metavar='project_path',
        type=str,
        help='The path of the project directory containing the codebase',
        action=PathAction
    )
    my_parser.add_argument(
        'code_path',
        metavar='code_path',
        type=str,
        help='The path of the directory containing the code you would like to run fitness functions on',
        action=PathAction,
    )
    args = my_parser.parse_args()
    if args.action == 'run':
        run(args.project_path, args.code_path)
    if args.action == 'publish':
        publish(args.project_path)
