import argparse, os, random

import lib.config as config
import lib.utils as utils

FORMAT_VIDEOS = "videos"
FORMAT_FRAMES = "frames"
FORMAT_SOUND = "sound"

def get_valid_videos(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded videos.
  :param videos:    The list of video metadata.
  :param root:      Videos root.
  :return:          List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():

    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, video_id + ".mp4")
    else:
      cls = ""
      video_path = os.path.join(root, video_id + ".mp4")

    if os.path.isfile(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def get_valid_frames(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded video frames.
  :param videos:    The list of video metadata.
  :param root:      Video frames root.
  :return:          List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():
    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, video_id)
    else:
      cls = ""
      video_path = os.path.join(root, video_id)

    if os.path.isdir(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def get_valid_sound(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded video sound tracks.
  :param videos:    The list of video metadata.
  :param root:      Video sounds root.
  :return:          List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():
    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, "{}.mp3".format(video_id))
    else:
      cls = ""
      video_path = os.path.join(root, "{}.mp3".format(video_id))

    if os.path.isfile(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

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

  # validate arguments
  assert args.format in [FORMAT_VIDEOS, FORMAT_FRAMES, FORMAT_SOUND]

  # load and validate training videos
  videos = utils.load_json(config.TRAIN_METADATA_PATH)
  if args.format == FORMAT_VIDEOS:
    train_videos = get_valid_videos(videos, config.TRAIN_ROOT)
  elif args.format == FORMAT_FRAMES:
    train_videos = get_valid_frames(videos, config.TRAIN_FRAMES_ROOT)
  elif args.format == FORMAT_SOUND:
    train_videos = get_valid_sound(videos, config.TRAIN_SOUND_ROOT)

  # load and validate validation videos
  videos = utils.load_json(config.VAL_METADATA_PATH)
  if args.format == FORMAT_VIDEOS:
    validation_videos = get_valid_videos(videos, config.VALID_ROOT)
  elif args.format == FORMAT_FRAMES:
    validation_videos = get_valid_frames(videos, config.VALID_FRAMES_ROOT)
  elif args.format == FORMAT_SOUND:
    validation_videos = get_valid_sound(videos, config.VALID_SOUND_ROOT)

  # load and validate test videos
  videos = utils.load_json(config.TEST_METADATA_PATH)
  if args.format == FORMAT_VIDEOS:
    test_videos = get_valid_videos(videos, config.TEST_ROOT, class_dirs=False)
  elif args.format == FORMAT_FRAMES:
    test_videos = get_valid_frames(videos, config.TEST_FRAMES_ROOT, class_dirs=False)
  elif args.format == FORMAT_SOUND:
    test_videos = get_valid_sound(videos, config.TEST_SOUND_ROOT, class_dirs=False)

  # validate that all splits contain the same classes
  assert sorted(train_videos.keys()) == sorted(validation_videos.keys())

  # create datasets
  datasets = {}
  classes = list(train_videos.keys())
  random.shuffle(classes)

  for num_classes in args.sets:
    set_classes = classes[:num_classes]
    set_train = {cls: videos for cls, videos in train_videos.items() if cls in set_classes}
    set_valid = {cls: videos for cls, videos in validation_videos.items() if cls in set_classes}
    set_test = test_videos

    set_train = class_keys_to_video_id_keys(set_train)
    set_valid = class_keys_to_video_id_keys(set_valid)
    set_test = class_keys_to_video_id_keys(set_test)

    set_classes = list(sorted(set_classes))
    set_classes = {cls: idx for idx, cls in enumerate(set_classes)}

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

parser.add_argument("format", help="{}, {} or {}".format(FORMAT_VIDEOS, FORMAT_FRAMES, FORMAT_SOUND))

parser.add_argument("-s", "--sets", type=int, nargs="+", default=[400], help="list of sets to generate, each integer denotes number of classes in the set")
parser.add_argument("--save", default="resources/kinetics", help="save path")

parsed = parser.parse_args()
main(parsed)
