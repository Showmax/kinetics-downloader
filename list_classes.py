import json

import lib.config as config

with open(config.CATEGORIES_PATH, "r") as file:
  categories = json.load(file)

classes = set()

for key in categories.keys():
  for label in categories[key]:
    classes.add(label)

for label in sorted(list(classes)):
  print(label)