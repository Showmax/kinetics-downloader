import argparse, json, random

import lib.config as config

def main(args):
  with open(config.CLASSES_PATH, "r") as file:
    classes = json.load(file)

  sampled = random.sample(classes, k=args.num_classes)

  if args.json:
    print("[")

  for cls in sorted(sampled):
    if args.json:
      print("\"{}\",".format(cls))
    else:
      print(cls)

  if args.json:
    print("]")

if __name__ == "__main__":
  parser = argparse.ArgumentParser("Sample N classes from Kinetics randomly.")

  parser.add_argument("num_classes", type=int, help="number of classes to sample")
  parser.add_argument("--json", action="store_true", help="output in JSON format")

  parsed = parser.parse_args()
  main(parsed)