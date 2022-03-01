from setuptools import setup, find_packages

setup(
    name='fitness-functions',
    version='1.0',
    description='Fitness Functions used to measure and display codebase health',
    author='Christopher Pettinga',
    author_email='chris.pettinga@digital.trade.gov.uk',
    packages=find_packages(include=['fitness-functions', 'fitness-functions.*'])
)
