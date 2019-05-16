import json

import lib.config as config

with open(config.CLASSES_PATH, "r") as file:
  classes = json.load(file)

for cls in classes:
  print(cls)