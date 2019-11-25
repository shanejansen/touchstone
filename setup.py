from setuptools import setup, find_packages

setup(
    name='touchstone',
    version='0.1.0',
    description='Component and end-to-end testing made easy.',
    url='https://github.com/shane-jansen/touchstone',
    author='Shane Jansen',
    author_email='shanejjansen@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pyfiglet', 'click'],
    entry_points={
        'console_scripts': [
            'touchstone = touchstone.cli:cli'
        ]
    },

    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
