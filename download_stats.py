import argparse, json, os

import lib.config as config

def count_present_and_missing(cls, directory, metadata):
  """
  Count present and missing videos for a class based on metadata.
  :param cls:           The class. If None, count all videos (used for testing videos - no classes).
  :param directory:     Directory containing the videos.
  :param metadata:      Kinetics metadata json.
  :return:              Tuple: number present videos, number of missing videos
  """

  present = 0
  missing = 0

  for key in metadata:
    if cls is None or metadata[key]["annotations"]["label"] == cls:
      if os.path.isfile(os.path.join(directory, "{}.mp4".format(key))):
        present += 1
      else:
        missing += 1

  return present, missing

def load_json(path):
  """
  Load a JSON file.
  :param path:    Path to the file.
  :return:        The loaded JSON file.
  """

  with open(path, "r") as file:
    return json.load(file)

def main(args):

  # load video classes
  classes = load_json(config.CLASSES_PATH)

  # load lists of videos
  train_metadata = load_json(config.TRAIN_METADATA_PATH)
  val_metadata = load_json(config.VAL_METADATA_PATH)
  test_metadata = load_json(config.TEST_METADATA_PATH)

  num_found = 0
  total = len(classes)

  total_train_present = 0
  total_train_missing = 0

  total_val_present = 0
  total_val_missing = 0

  for cls in classes:
    cls_train_path = os.path.join(config.TRAIN_ROOT, cls)
    cls_valid_path = os.path.join(config.VALID_ROOT, cls)

    train_found = False
    valid_found = False

    if os.path.isdir(cls_train_path):
      train_present, train_missing = count_present_and_missing(cls, cls_train_path, train_metadata)
      train_found = True
      total_train_present += train_present
      total_train_missing += train_missing

    if os.path.isdir(cls_valid_path):
      valid_present, valid_missing = count_present_and_missing(cls, cls_valid_path, val_metadata)
      valid_found = True
      total_val_present += valid_present
      total_val_missing += valid_missing

    if train_found or valid_found:
      num_found += 1

      print("class {}".format(cls))

      if train_found:
        print("train: {} / {}".format(train_present, train_present + train_missing))

      if valid_found:
        print("valid: {} / {}".format(valid_present, valid_present + valid_missing))

      print()

  print("Overall:")
  print("\t{:d} / {:d} classes found".format(num_found, total))
  print("\t{:d} / {:d} ({:.2f}%) train videos found".format(
    total_train_present, total_train_present + total_train_missing,
    total_train_present / (total_train_present + total_train_missing)))
  print("\t{:d} / {:d} ({:.2f}%) valid videos found".format(
    total_val_present, total_val_present + total_val_missing,
    total_val_present / (total_val_present + total_val_missing)))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--classes", nargs="+")
  parser.add_argument("-d", "--details", action="store_true", default=False)

  parsed = parser.parse_args()
  main(parsed)