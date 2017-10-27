import argparse

import lib.utils as utils

def main(args):

  source = utils.load_json(args.source_path)
  source = sorted(source)

  target = {source[idx]: idx for idx in range(len(source))}
  utils.save_json(args.target_path, target)

parser = argparse.ArgumentParser()
parser.add_argument("source_path")
parser.add_argument("target_path")
parsed = parser.parse_args()
main(parsed)