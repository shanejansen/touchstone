from setuptools import setup

setup(
    name='touchstone',
    version='0.1.0',
    description='End-to-end and exploratory testing made easy.',
    url='https://github.com/shane-jansen/touchstone',
    author='Shane Jansen',
    author_email='shanejjansen@gmail.com',
    license='MIT',
    packages=['touchstone'],
    install_requires=['pyfiglet', 'click', 'pika', 'pyyaml', 'pymongo', 'pymysql'],
    entry_points={
        'console_scripts': [
            'touchstone = touchstone.cli:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
