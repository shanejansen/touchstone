import os

import click

from commands import init_command, run_command, develop_command, common
from configs.touchstone_config import TouchstoneConfig


@click.group()
def cli():
    pass


@cli.command()
def init():
    init_command.execute()


@cli.command()
def run():
    prep_run()
    run_command.execute()


@cli.command()
def develop():
    prep_run()
    develop_command.execute()


def prep_run():
    if not common.sanity_check_passes():
        print('touchstone.json and dev-defaults could not be found. '
              'If touchstone has not been initialized, run \'touchstone init\'.')
        exit(1)
    common.load_config()


TouchstoneConfig.instance().set_root(os.getcwd())
cli()
