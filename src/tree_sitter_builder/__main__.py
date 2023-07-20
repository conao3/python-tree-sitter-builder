import logging
import logging.config
import argparse
import pathlib

import platformdirs
import tree_sitter
import yaml

from . import subr


with open(pathlib.Path(__file__).parent / 'logging.conf.yml') as f:
    logging.config.dictConfig(yaml.safe_load(f))


logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', help='Repository specifier in github or git URL.')

    return parser.parse_args()


def main():
    args = parse_args()

    data_dir = pathlib.Path(platformdirs.user_data_dir('tree-sitter-builder'))
    data_dir.mkdir(parents=True, exist_ok=True)

    repo_dir = data_dir / 'repos'
    repo_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f'Clone `{args.repository}` to `{repo_dir}`')
    clone_dir_name = subr.git.get_repo_name(args.repository)
    subr.git.clone(
        url=subr.git.get_repo_url(args.repository),
        dir=repo_dir,
        name=clone_dir_name,
    )

    build_dir = data_dir / 'build'
    build_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f'Build tree-sitter module: {str(build_dir / (clone_dir_name + ".so"))}')
    tree_sitter.Language.build_library(
        str(build_dir / (clone_dir_name + '.so')),
        [str(repo_dir / clone_dir_name)]
    )
