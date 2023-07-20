import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', help='Repository specifier in github or git URL.')

    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
