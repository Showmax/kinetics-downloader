import argparse, json, os

import lib.config as config
import lib.parallel_download as parallel

from tqdm import tqdm


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

def download_category(category, num_workers, failed_save_file, compress, verbose, skip, log_file):
  """
  Download all videos that belong to the given category.
  :param category:              The category to download.
  :param num_workers:           Number of downloads in parallel.
  :param failed_save_file:      Where to save failed video ids.
  :param compress:              Decides if the videos should be compressed.
  :param verbose:               Print status.
  :param skip:                  Skip classes that already have folders (i.e. at least one video was downloaded).
  :param log_file:              Path to log file for youtube-dl.
  :return:                      None.
  """

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  classes = categories[category]
  download_classes(classes, num_workers, failed_save_file, compress, verbose, skip, log_file)

def download_classes(classes, num_workers, failed_save_file, compress, verbose, skip, log_file):
  """
  Download all videos of the provided classes.
  :param classes:               List of classes to download.
  :param num_workers:           Number of downloads in parallel.
  :param failed_save_file:      Where to save failed video ids.
  :param compress:              Decides if the videos should be compressed.
  :param verbose:               Print status.
  :param skip:                  Skip classes that already have folders (i.e. at least one video was downloaded).
  :param log_file:              Path to log file for youtube-dl.
  :return:                      None.
  """

  for list_path, save_root in tqdm(zip([config.TRAIN_METADATA_PATH, config.VAL_METADATA_PATH],
                                        [config.TRAIN_ROOT, config.VALID_ROOT])):
    with open(list_path) as file:
      data = json.load(file)

    pool = parallel.Pool(classes, data, save_root, num_workers, failed_save_file, compress, verbose, skip,
                         log_file=log_file)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def download_test_set(num_workers, failed_log, compress, verbose, skip, log_file):
  """
  Download the test set.
  :param num_workers:           Number of downloads in parallel.
  :param failed_log:            Where to save failed video ids.
  :param compress:              Decides if the videos should be compressed.
  :param verbose:               Print status.
  :param skip:                  Skip classes that already have folders (i.e. at least one video was downloaded).
  :param log_file:              Path to log file for youtube-dl.
  :return:
  """

  with open(config.TEST_METADATA_PATH) as file:
    data = json.load(file)

  pool = parallel.Pool(None, data, config.TEST_ROOT, num_workers, failed_log, compress, verbose, skip,
                       log_file=log_file)
  pool.start_workers()
  pool.feed_videos()
  pool.stop_workers()

def main(args):

  maybe_create_dirs()

  if args.all:
    # download all categories => all videos
    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      download_category(category, args.num_workers, args.failed_log, args.compress, args.verbose, args.skip,
                        args.log_file)

  else:
    if args.categories:
      # download selected categories
      for category in args.categories:
        download_category(category, args.num_workers, args.failed_log, args.compress, args.verbose, args.skip,
                          args.log_file)

    if args.classes:
      # download selected classes
      download_classes(args.classes, args.num_workers, args.failed_log, args.compress, args.verbose, args.skip,
                       args.log_file)

    if args.test:
      # download the test set
      download_test_set(args.num_workers, args.failed_log, args.compress, args.verbose, args.skip, args.failed_log)

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Download Kinetics videos in the mp4 format.")

  parser.add_argument("--categories", nargs="+", help="categories to download")
  parser.add_argument("--classes", nargs="+", help="classes to download")
  parser.add_argument("--all", action="store_true", help="download the whole dataset")
  parser.add_argument("--test", action="store_true", help="download the test set")

  parser.add_argument("--num-workers", type=int, default=1, help="number of downloader processes")
  parser.add_argument("--failed-log", default="dataset/failed.txt", help="where to save list of failed videos")
  parser.add_argument("--compress", default=False, action="store_true", help="compress videos using gzip (not recommended)")
  parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print additional info")
  parser.add_argument("-s", "--skip", default=False, action="store_true", help="skip classes that already have folders")
  parser.add_argument("-l", "--log-file", help="log file for youtube-dl (the library used to download YouTube videos)")

  parsed = parser.parse_args()
  main(parsed)