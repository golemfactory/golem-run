import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name", nargs="?", default="unknown")
args = parser.parse_args()

print(f"Hello {args.name}!")