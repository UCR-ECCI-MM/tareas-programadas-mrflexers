from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='health_topic_index',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
