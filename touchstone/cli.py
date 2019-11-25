import os

import click

from touchstone import develop_cmd
from touchstone import init_cmd
from touchstone import run_cmd
from touchstone.lib.configs.touchstone_config import TouchstoneConfig


@click.group()
def cli():
    TouchstoneConfig.instance().set_root(os.getcwd())


@cli.command()
def init():
    init_cmd.execute()


@cli.command()
def run():
    run_cmd.execute()


@cli.command()
def develop():
    develop_cmd.execute()


if __name__ == '__main__':
    cli()
