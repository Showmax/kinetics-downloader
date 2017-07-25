import json, unittest

import lib.config as config

class TestCategories(unittest.TestCase):

  def extract_classes_from_categories(self):

    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    classes = []

    for key in categories.keys():
      classes += categories[key]

    return classes

  def test_all_source_classes_in_categories(self):

    categories_classes = self.extract_classes_from_categories()

    classes_not_present = set()

    for list_path in [config.KINETICS_TRAIN_PATH, config.KINETICS_VAL_PATH]:
      with open(list_path, "r") as file:
        videos_dict = json.load(file)

      for key in videos_dict.keys():
        class_name = videos_dict[key]["annotations"]["label"]

        if class_name not in categories_classes:
          classes_not_present.add(class_name)

    if len(classes_not_present) > 0:
      print("The following classes are not present in categories:")
      for item in classes_not_present:
        print(item)

    self.assertTrue(len(classes_not_present) == 0)

  def test_all_categories_in_source(self):

    categories_classes = self.extract_classes_from_categories()

    with open(config.KINETICS_TRAIN_PATH, "r") as file:
      train_dict = json.load(file)

    with open(config.KINETICS_VAL_PATH, "r") as file:
      valid_dict = json.load(file)

    not_in_train = []
    not_in_valid = []

    for cat_class in categories_classes:
      for source, not_in_list in zip([train_dict, valid_dict], [not_in_train, not_in_valid]):

        flag = False

        for key in source.keys():
          class_name = source[key]["annotations"]["label"]

          if cat_class == class_name:
            flag = True
            break

        if not flag:
          not_in_list.append(cat_class)

    for name, class_list in zip(["train", "valid"], [not_in_train, not_in_valid]):
      if len(class_list) > 0:
        print("The following classes are not present in {} list:".format(name))
        for item in class_list:
          print(item)

    for class_list in [not_in_train, not_in_valid]:
      self.assertTrue(len(class_list) == 0)

  def test_categories_do_not_overlap(self):

    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    classes = set()

    for key in categories.keys():
      for cls in categories[key]:
        if cls in classes:
          print("{} from {} duplicate".format(cls, key))
        else:
          classes.add(cls)