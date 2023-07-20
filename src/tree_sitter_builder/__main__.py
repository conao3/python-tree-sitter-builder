import argparse
import pathlib

import platformdirs

from . import subr

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', help='Repository specifier in github or git URL.')

    return parser.parse_args()

def main():
    args = parse_args()
    print(args)

    data_dir = pathlib.Path(platformdirs.user_data_dir('tree-sitter-builder'))
    data_dir.mkdir(parents=True, exist_ok=True)

    repo_dir = data_dir / 'repos'
    repo_dir.mkdir(parents=True, exist_ok=True)

    subr.git.clone(
        url=subr.git.get_repo_url(args.repository),
        dir=repo_dir,
        name=subr.git.get_repo_name(args.repository),
    )
