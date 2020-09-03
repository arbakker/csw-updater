# -*- coding: utf-8 -*-
"""TODO Docstring."""
import argparse
import logging
import sys

import click
import click_log

# Setup logging before package imports.
logger = logging.getLogger(__name__)
click_log.basic_config(logger)


from csw_updater.error import AppError
from csw_updater.core import update_metadata, get_password_from_env, get_username_from_env

#
# def parse_args(args):
#     parser = argparse.ArgumentParser()
#     parser.add_argument('ngr_base_url', type=str)
#     parser.add_argument('metadata_file', type=argparse.FileType(mode='r'))
#     parser.add_argument('--csw-user', type=str, help="CSW user, overrules environment variable CSW_USER", default="")
#     parser.add_argument('--csw-password', type=str, help="CSW password, overrules environment variable CSW_PASSWORD", default="")
#     parser.set_defaults(include=True)
#     return parser.parse_args()

@click.group()
def cli():
    pass

@cli.command(name="csw_updater")
@click.argument("csw_base_url", type=str)
@click.argument("metadata_file", type=click.File())
@click.option('-u', '--csw-user', type=str)
@click.option('-p', '--csw-password', type=str)
@click_log.simple_verbosity_option(logger)
def csw_updater_command(csw_base_url, metadata_file, csw_user="", csw_password=""):
    """
    TODO Docstring.
    """
    try:
        if not csw_user:
            csw_user = get_username_from_env()
        if not csw_password:
            csw_password = get_password_from_env()
        update_metadata(csw_base_url, metadata_file, csw_user, csw_password)
    except AppError:
        logger.exception("csw_updater failed:")
        sys.exit(1)


if __name__ == "__main__":
    cli()
