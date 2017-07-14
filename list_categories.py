import json

import lib.config as config

with open(config.CATEGORIES_PATH, "r") as file:
  categories = json.load(file)

for key in categories.keys():
  print(key)

  for label in categories[key]:
    print("\t{}".format(label))
