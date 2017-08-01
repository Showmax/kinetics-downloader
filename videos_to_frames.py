import argparse, json

import lib.config as config
import lib.parallel_to_frames as parallel

def download_category(category, num_workers, failed_save_file):

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  classes = categories[category]
  download_classes(classes, num_workers, failed_save_file)

def download_classes(classes, num_workers, failed_save_file):

  for list_path, save_root in zip([config.TRAIN_METADATA_PATH, config.VAL_METADATA_PATH],
                                        [config.TRAIN_ROOT, config.VALID_ROOT]):
    with open(list_path) as file:
      data = json.load(file)

    pool = parallel.Pool(classes, data, save_root, num_workers, failed_save_file)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def main(args):

  if args.all:
    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      download_category(category, args.num_workers, args.failed_log)

  else:
    if args.categories:
      for category in args.categories:
        download_category(category, args.num_workers, args.failed_log)

    if args.classes:
      download_classes(args.classes, args.num_workers, args.failed_log)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--categories", nargs="+", help="categories to download")
  parser.add_argument("--classes", nargs="+", help="classes to download")
  parser.add_argument("--all", action="store_true", help="download the whole dataset")

  parser.add_argument("--num-workers", type=int, default=1)
  parser.add_argument("--failed-log", default="dataset/failed.txt", help="where to save list of failed videos")

  parsed = parser.parse_args()
  main(parsed)