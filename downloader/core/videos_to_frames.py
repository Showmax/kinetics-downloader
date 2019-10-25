import argparse, json

import lib.config as config
import lib.parallel_to_frames as parallel

def process_category(category, num_workers, failed_save_file):
  """
  Extract video frames for a category.
  :param category:              Category name.
  :param num_workers:           Number of worker processes.
  :param failed_save_file:      Path to a log of failed extractions.
  :return:                      None.
  """

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  classes = categories[category]
  process_classes(classes, num_workers, failed_save_file)

def process_classes(classes, num_workers, failed_save_file):
  """
  Extract video frames for a class.
  :param classes:               List of classes.
  :param num_workers:           Number of worker processes.
  :param failed_save_file:      Path to a log of failed extractions.
  :return:                      None.
  """

  for source_root, target_root in zip([config.TRAIN_ROOT, config.VALID_ROOT],
                                        [config.TRAIN_FRAMES_ROOT, config.VALID_FRAMES_ROOT]):

    pool = parallel.Pool(classes, source_root, target_root, num_workers, failed_save_file)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def process_test_set(num_workers, failed_save_file):
  """
  Extract video frames for the test set.
  :param num_workers:           Number of worker processes.
  :param failed_save_file:      Path to a log of failed extractions.
  :return:                      None.
  """

  pool = parallel.Pool(None, config.TEST_ROOT, config.TEST_FRAMES_ROOT, num_workers, failed_save_file)
  pool.start_workers()
  pool.feed_videos()
  pool.stop_workers()

def main(args):

  if args.all:
    # extract for all categories => all videos
    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      process_category(category, args.num_workers, args.failed_log)

  else:
    if args.categories:
      # extract for selected categories
      for category in args.categories:
        process_category(category, args.num_workers, args.failed_log)

    if args.classes:
      # extract for selected classes
      process_classes(args.classes, args.num_workers, args.failed_log)

    if args.test:
      # extract for the test set
      process_test_set(args.num_workers, args.failed_log)

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Extract individual frames from videos for faster loading.")

  parser.add_argument("--categories", nargs="+", help="categories to extract")
  parser.add_argument("--classes", nargs="+", help="classes to extract")
  parser.add_argument("--all", action="store_true", help="extract the train and validation subsets")
  parser.add_argument("--test", action="store_true", help="extract the test set")

  parser.add_argument("--num-workers", type=int, default=1, help="number of worker threads")
  parser.add_argument("--failed-log", default="dataset/failed_frames.txt", help="where to save list of videos for "
                                                                                "which the frame extraction failed")

  parsed = parser.parse_args()
  main(parsed)
