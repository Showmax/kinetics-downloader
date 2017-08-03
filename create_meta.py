import argparse, os, random

import lib.config as config
import lib.utils as utils

def get_valid_videos(videos, root, classes):
  """
  Go though the list of all Kinetics videos and return videos that were successfully downloaded and segmented into frame jpgs.
  :param videos:        Dictionary of videos.
  :param root:          Frames root.
  :param classes:       List of classes to search for.
  :return:              Dictionary of found videos.
  """

  valid_videos = {}

  for video_id in videos.key():
    cls = videos[video_id]["annotations"]["label"]
    if cls in classes:
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, video_id)

      if os.path.isdir(video_path):
        valid_videos["id"] = cls

  return valid_videos

def main(args):

  # load train videos metadata and find downloaded videos
  classes = utils.load_json(args.meta_path)
  videos = utils.load_json(config.TRAIN_METADATA_PATH)

  valid_videos = get_valid_videos(videos, config.TRAIN_FRAMES_ROOT, classes)
  valid_video_ids = random.shuffle(valid_videos.keys())

  # split training videos into train and valid datasets
  count = len(valid_videos.keys())
  val_count = int(round(count * args.val_split))
  train_count = count - val_count

  train_video_ids = valid_video_ids[:train_count]
  val_video_ids = valid_video_ids[train_count:]

  # create a list of downloaded test videos
  train_videos = {key: valid_videos[key] for key in train_video_ids}
  val_videos = {key: valid_videos[key] for key in val_video_ids}

  videos = utils.load_json(config.VAL_METADATA_PATH)
  test_videos = get_valid_videos(videos, config.VALID_FRAMES_ROOT, classes)

  # save metadata
  train_path = args.save + "_train.json"
  val_path = args.save + "_val.json"
  test_path = args.save + "_test.json"

  utils.save_json(train_path, train_videos)
  utils.save_json(val_path, val_videos)
  utils.save_json(test_path, test_videos)

parser = argparse.ArgumentParser("Create a train and validation split of a given subset of Kinetcs")

parser.add_argument("meta_path", help="path to a JSON file with classes")
parser.add_argument("save", help="save path")

parser.add_argument("-v", "--val-split", type=float, default=0.1)

parsed = parser.parse_args()
main(parsed)