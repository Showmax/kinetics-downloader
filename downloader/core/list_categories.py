import argparse, json

import lib.config as config

def main(args):

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  for key in categories.keys():
    print(key)

    if args.classes:
      for label in categories[key]:
        print("\t{}".format(label))

if __name__ == "__main__":
  parser = argparse.ArgumentParser("List all categories.")

  parser.add_argument("-c", "--classes", help="list classes for each category", action="store_true", default=False)

  parsed = parser.parse_args()
  main(parsed)