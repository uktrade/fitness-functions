"""Fitness Functions.

Usage:
  fitness-functions run <path>
  fitness-functions publish <path>

Options:
  <path>     The path of the directory containing the code you would like to run fitness functions on

'run' will analyse the code in the directory defined by the <path> variable, and save the metrics to
<path>/fitness/fitness_metrics.db (it will create the directory and database if they don't already exist)

'publish' will generate a graph using the <path>/fitness/fitness_metrics.db data, save it as a base64 PNG string in the
READ.ME file located in ../<path>
"""

import sys
import os
from .run import run

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print(__doc__)
    elif args[0] == 'run':
        try:
            path = os.getcwd() if args[1] == '.' else args[1]
            if not os.path.isdir(path):
                print('Please provide a valid directory to run fitness functions on')
            return run(path)
        except IndexError:
            print(f'Not enough arguments were passed, please see:\n\n{__doc__}')
    elif args[1] == 'publish':
        # Generate the PNG image from the database, and save it to the READ.ME as BASE64
        pass
