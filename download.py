import argparse, json, os

import lib.config as config
import lib.downloader as downloader

def maybe_create_dirs():
  for path in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
    if not os.path.exists(path):
      try:
        os.makedirs(path)
      except FileExistsError:
        pass

def download_category(category, compress):

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  labels = categories[category]

  failed_videos = []
  for label in labels:
    failed_videos += download_class(label, compress)

  return failed_videos

def download_class(class_name, compress):

  with open(config.KINETICS_TRAIN_PATH) as file:
    train_data = json.load(file)

  with open(config.KINETICS_VAL_PATH) as file:
    valid_data = json.load(file)

  failed_videos = []

  failed_videos += downloader.download_class(class_name, train_data, config.TRAIN_ROOT, compress=compress)
  failed_videos += downloader.download_class(class_name, valid_data, config.VALID_ROOT, compress=compress)

  return failed_videos

def main(args):

  maybe_create_dirs()

  failed_videos = []

  if args.all:

    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      failed_videos += download_category(category, args.compress)

  else:
    if args.categories:
      for category in args.categories:
        failed_videos += download_category(category, args.compress)

    if args.classes:
      for class_name in args.classes:
        failed_videos += download_class(class_name, args.compress)

  if len(failed_videos) > 0:
    print("Failed videos (in any stage of processing):")

    for video in failed_videos:
      print(video)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--categories", nargs="+", help="categories to download")
  parser.add_argument("--classes", nargs="+", help="classes to download")
  parser.add_argument("--all", action="store_true", help="download the whole dataset")

  # TODO
  #parser.add_argument("--disable-separate", default=False, help="do not create a separate directory for each class;"
  #                                                              " e.g. dataset/train/swimming")
  parser.add_argument("--compress", default=False, action="store_true", help="compress videos using gzip")

  parsed = parser.parse_args()
  main(parsed)