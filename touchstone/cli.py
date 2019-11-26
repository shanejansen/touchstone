import os

import click

from touchstone import develop
from touchstone import init
from touchstone import run
from touchstone.lib.configs.touchstone_config import TouchstoneConfig


@click.group()
def cli():
    TouchstoneConfig.instance().set_root(os.getcwd())


@cli.command(name='init', help='Initialize Touchstone in the current directory.')
def init_cmd():
    init.execute()


@cli.command(name='run', help='Runs Touchstone with an exit code.')
def run_cmd():
    run.execute()


@cli.command(name='develop', help='Start a development session of Touchstone.')
def develop_cmd():
    develop.execute()


if __name__ == '__main__':
    cli()
