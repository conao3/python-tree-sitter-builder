import logging
import logging.config
import argparse
import pathlib

import tree_sitter
import yaml

from . import subr
from . import lib


with open(pathlib.Path(__file__).parent / 'logging.conf.yml') as f:
    logging.config.dictConfig(yaml.safe_load(f))


logger = logging.getLogger(__name__)


def main_build(args: argparse.Namespace):
    data_dir = lib.dir.get_data_dir()
    repo_dir = lib.dir.get_repo_dir(data_dir)
    build_dir = lib.dir.get_build_dir(data_dir)

    logger.info(f'Clone `{args.repository}` to `{repo_dir}`')
    clone_dir_name = subr.git.get_repo_name(args.repository)
    subr.git.clone(
        url=subr.git.get_repo_url(args.repository),
        dir=repo_dir,
        name=clone_dir_name,
    )

    logger.info(f'Build tree-sitter module: {str(build_dir / (clone_dir_name + ".so"))}')
    tree_sitter.Language.build_library(
        str(build_dir / (clone_dir_name + '.so')),
        [str(repo_dir / clone_dir_name)]
    )


def main_update(args: argparse.Namespace):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_build = subparsers.add_parser('build', help='Build tree-sitter module.')
    parser_build.add_argument('repository', help='Repository specifier in github or git URL.')
    parser_build.set_defaults(handler=main_build)

    parser_update = subparsers.add_parser('update', help='Update tree-sitter module.')
    parser_update.set_defaults(handler=main_update)

    return parser.parse_args()


def main():
    args = parse_args()
    args.handler(args)
