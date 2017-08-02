import argparse, json, os

import lib.config as config
import lib.parallel_download as parallel

def maybe_create_dirs():
  """
  Create directories for training, validation and testing videos if they do not exist.
  :return:    None.
  """
  for path in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
    if not os.path.exists(path):
      try:
        os.makedirs(path)
      except FileExistsError:
        pass

def download_category(category, num_workers, failed_save_file, compress, verbose):
  """
  Download all videos that belong to the given category.
  :param category:              The category to download.
  :param num_workers:           Number of downloads in parallel.
  :param failed_save_file:      Where to save failed video ids.
  :param compress:              Decides if the videos should be compressed.
  :return:
  """

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  classes = categories[category]
  download_classes(classes, num_workers, failed_save_file, compress, verbose)

def download_classes(classes, num_workers, failed_save_file, compress, verbose):
  """
  Download all videos of the provided classes.
  :param classes:               List of classes to download.
  :param num_workers:           Number of downloads in parallel.
  :param failed_save_file:      Where to save failed video ids.
  :param compress:              Decides if the videos should be compressed.
  :return:                      None.
  """

  for list_path, save_root in zip([config.TRAIN_METADATA_PATH, config.VAL_METADATA_PATH],
                                        [config.TRAIN_ROOT, config.VALID_ROOT]):
    with open(list_path) as file:
      data = json.load(file)

    pool = parallel.Pool(classes, data, save_root, num_workers, failed_save_file, compress, verbose)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def main(args):

  maybe_create_dirs()

  if args.all:
    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      download_category(category, args.num_workers, args.failed_log, args.compress, args.varbose)

  else:
    if args.categories:
      for category in args.categories:
        download_category(category, args.num_workers, args.failed_log, args.compress, args.varbose)

    if args.classes:
      download_classes(args.classes, args.num_workers, args.failed_log, args.compress, args.varbose)

    if args.json_classes:
      with open(args.json_classes, "r") as file:
        classes = json.load(file)

      download_classes(classes, args.num_workers, args.failed_log, args.compress, args.verbose)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--categories", nargs="+", help="categories to download")
  parser.add_argument("--classes", nargs="+", help="classes to download")
  parser.add_argument("--json-classes", help="path to a JSON file with a list of classes")
  parser.add_argument("--all", action="store_true", help="download the whole dataset")

  parser.add_argument("--num-workers", type=int, default=1)
  parser.add_argument("--failed-log", default="dataset/failed.txt", help="where to save list of failed videos")
  parser.add_argument("--compress", default=False, action="store_true", help="compress videos using gzip")
  parser.add_argument("--overwrite", default=False, action="store_true", help="overwrite downloaded videos")
  parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print additional info")

  parsed = parser.parse_args()
  main(parsed)