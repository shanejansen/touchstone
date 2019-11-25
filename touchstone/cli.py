import os

import click

import develop_cmd
import init_cmd
import run_cmd
from lib.configs.touchstone_config import TouchstoneConfig


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
