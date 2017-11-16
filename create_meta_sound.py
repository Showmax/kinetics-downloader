import argparse, os, random

import lib.config as config
import lib.utils as utils

def get_valid_videos(videos, root):
  """
  Go through a list of videos and find all downloaded videos.
  :param videos:    The list of video metadata.
  :param root:      Video frames root.
  :return:
  """

  valid_videos = {}

  for video_id in videos.keys():
    cls = videos[video_id]["annotations"]["label"]
    cls_path = cls.replace(" ", "_")
    video_path = os.path.join(root, cls_path, "{}.mp3".format(video_id))

    if os.path.isfile(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def split_videos(videos, val_split):
  """
  Split videos into train and valid sets.
  :param videos:        Dictionary of classes in which each class contains a list of corresponding videos.
  :param val_split:     Fraction of validation videos.
  :return:              Train and validation videos dictionary. The same format as the input dictionary.
  """

  train_videos = {}
  valid_videos = {}

  for cls, vids in videos.items():
    random.shuffle(vids)
    count = len(vids)
    val_count = int(round(count * val_split))
    train_count = count - val_count

    train_videos[cls] = vids[:train_count]
    valid_videos[cls] = vids[train_count:]

  return train_videos, valid_videos

def class_keys_to_video_id_keys(videos):
  """
  Transform a dictionary with keys = classes, values = video lists to a dictionary where key = video id, value = class.
  :param videos:    Dictionary with classes as keys.
  :return:          Dictionary with video ids as keys.
  """

  new_videos = {}

  for cls, vids in videos.items():
    for vid in vids:
      new_videos[vid] = cls

  return new_videos

def main(args):

  # load train videos metadata and find downloaded videos
  videos = utils.load_json(config.TRAIN_METADATA_PATH)
  valid_videos = get_valid_videos(videos, config.TRAIN_SOUND_ROOT)

  # create training and validation splits
  train_videos, valid_videos = split_videos(valid_videos, args.val_split)

  # load and validate test videos
  videos = utils.load_json(config.VAL_METADATA_PATH)
  test_videos = get_valid_videos(videos, config.VALID_SOUND_ROOT)

  # validate that all splits contain the same classes
  assert sorted(train_videos.keys()) == sorted(valid_videos.keys()) == sorted(test_videos.keys())

  # create datasets
  datasets = {}
  classes = list(train_videos.keys())
  random.shuffle(classes)

  for num_classes in args.sets:
    set_classes = classes[:num_classes]
    set_train = {cls: videos for cls, videos in train_videos.items() if cls in set_classes}
    set_valid = {cls: videos for cls, videos in valid_videos.items() if cls in set_classes}
    set_test = {cls: videos for cls, videos in test_videos.items() if cls in set_classes}

    set_train = class_keys_to_video_id_keys(set_train)
    set_valid = class_keys_to_video_id_keys(set_valid)
    set_test = class_keys_to_video_id_keys(set_test)

    datasets[num_classes] = {
      "train": set_train,
      "valid": set_valid,
      "test": set_test,
      "classes": set_classes
    }

  # save datasets
  for num_classes, dataset in datasets.items():
    train_path = "{:s}_{:d}_train.json".format(args.save, num_classes)
    val_path = "{:s}_{:d}_val.json".format(args.save, num_classes)
    test_path = "{:s}_{:d}_test.json".format(args.save, num_classes)
    classes_path = "{:s}_{:d}_classes.json".format(args.save, num_classes)

    utils.save_json(train_path, dataset["train"])
    utils.save_json(val_path, dataset["valid"])
    utils.save_json(test_path, dataset["test"])
    utils.save_json(classes_path, dataset["classes"])

parser = argparse.ArgumentParser("Create a train and validation split of specified subsets of Kinetics.")

parser.add_argument("meta_path", help="path to a JSON metadata file containing a list of videos")

parser.add_argument("-s", "--sets", type=int, nargs="+", default=[400, 200, 100, 50, 2])
parser.add_argument("-v", "--val-split", type=float, default=0.0)
parser.add_argument("--save", default="resources/kinetics_sound", help="save path")

parsed = parser.parse_args()
main(parsed)