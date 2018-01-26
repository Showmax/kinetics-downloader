import argparse, os

import lib.config as config
import lib.utils as utils

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


def main(args):

  # load video classes
  classes = utils.load_json(config.CLASSES_PATH)

  # load lists of videos
  train_metadata = utils.load_json(config.TRAIN_METADATA_PATH)
  val_metadata = utils.load_json(config.VAL_METADATA_PATH)
  test_metadata = utils.load_json(config.TEST_METADATA_PATH)

  num_found = 0
  total = 0

  total_train_present = 0
  total_train_missing = 0

  total_val_present = 0
  total_val_missing = 0

  # load subset
  subset = None
  if args.subset:
    subset = utils.load_json(args.subset)

  # count train and validation videos
  for cls in classes:

    if subset is not None and cls not in subset:
      continue

    total += 1

    cls_train_path = os.path.join(config.TRAIN_ROOT, cls.replace(" ", "_"))
    cls_valid_path = os.path.join(config.VALID_ROOT, cls.replace(" ", "_"))

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

      if args.details:
        print("class {}".format(cls))

        if train_found:
          print("train: {} / {}".format(train_present, train_present + train_missing))

        if valid_found:
          print("valid: {} / {}".format(valid_present, valid_present + valid_missing))

        print()

  # count test videos
  test_present, test_missing = count_present_and_missing(None, config.TEST_ROOT, test_metadata)

  # print
  train_percent_found = 0
  if total_train_present > 0:
    train_percent_found = (total_train_present * 100) / (total_train_present + total_train_missing)

  valid_percent_found = 0
  if total_val_present > 0:
    valid_percent_found = (total_val_present * 100) / (total_val_present + total_val_missing)

  test_percent_found = 0
  if test_present > 0:
    test_percent_found = (test_present * 100) / (test_present + test_missing)

  print("class stats:")
  print("\t{:d} / {:d} classes found".format(num_found, total))

  print()

  print("video stats (only for found classes):")
  print("\t{:d} / {:d} ({:.2f}%) train videos found".format(
    total_train_present, total_train_present + total_train_missing, train_percent_found))
  print("\t{:d} / {:d} ({:.2f}%) valid videos found".format(
    total_val_present, total_val_present + total_val_missing, valid_percent_found))
  print("\t{:d} / {:d} ({:.2f}%) test videos found".format(
    test_present, test_present + test_missing, test_percent_found))

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Print statistics about downloaded videos.")

  parser.add_argument("-d", "--details", action="store_true", default=False, help="detailed stats for each found class")
  parser.add_argument("-s", "--subset", help="path to a JSON file containing a subset of Kinetics classes")

  parsed = parser.parse_args()
  main(parsed)