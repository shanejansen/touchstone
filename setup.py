from setuptools import setup, find_packages

from touchstone import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='touchstone-testing',
    version=__version__,
    description='Touchstone is a testing framework for your services that focuses on end-to-end and exploratory testing.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shane-jansen/touchstone',
    author='Shane Jansen',
    author_email='shanejjansen@gmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyfiglet~=0.8',
        'click~=7.0',
        'pika~=1.1',
        'pyyaml~=5.2',
        'pymongo~=3.10',
        'pymysql~=0.9.3',
        'minio~=5.0.7'
    ],
    entry_points={
        'console_scripts': [
            'touchstone = touchstone.cli:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)
