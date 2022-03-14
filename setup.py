from setuptools import find_packages, setup

setup(
    name="fitness-functions",
    version="1.0",
    description="Fitness Functions used to measure and display codebase health",
    author="Christopher Pettinga",
    author_email="chris.pettinga@digital.trade.gov.uk",
    url="https://github.com/uktrade/fitness-functions",
    packages=find_packages(include=["fitness_functions", "fitness_functions.*"]),
    entry_points={
        "console_scripts": [
            "fitness-functions = fitness_functions.__main__:main",
        ],
    },
)
