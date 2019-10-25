import argparse, random

import lib.config as config
import lib.constants as constants
import lib.metadata as metadata
import lib.utils as utils


def main(args):

  # load and validate training videos
  videos = utils.load_json(config.TRAIN_METADATA_PATH)
  if args.format == constants.FORMAT_VIDEOS:
    train_videos = metadata.get_valid_videos(videos, config.TRAIN_ROOT)
  elif args.format == constants.FORMAT_FRAMES:
    train_videos = metadata.get_valid_frames(videos, config.TRAIN_FRAMES_ROOT)
  elif args.format == constants.FORMAT_SOUND:
    train_videos = metadata.get_valid_sound(videos, config.TRAIN_SOUND_ROOT)
  else:
    raise ValueError("Invalid format type.")

  # load and validate validation videos
  videos = utils.load_json(config.VAL_METADATA_PATH)
  if args.format == constants.FORMAT_VIDEOS:
    validation_videos = metadata.get_valid_videos(videos, config.VALID_ROOT)
  elif args.format == constants.FORMAT_FRAMES:
    validation_videos = metadata.get_valid_frames(videos, config.VALID_FRAMES_ROOT)
  elif args.format == constants.FORMAT_SOUND:
    validation_videos = metadata.get_valid_sound(videos, config.VALID_SOUND_ROOT)
  else:
    raise ValueError("Invalid format type.")

  # load and validate test videos
  videos = utils.load_json(config.TEST_METADATA_PATH)
  if args.format == constants.FORMAT_VIDEOS:
    test_videos = metadata.get_valid_videos(videos, config.TEST_ROOT, class_dirs=False)
  elif args.format == constants.FORMAT_FRAMES:
    test_videos = metadata.get_valid_frames(videos, config.TEST_FRAMES_ROOT, class_dirs=False)
  elif args.format == constants.FORMAT_SOUND:
    test_videos = metadata.get_valid_sound(videos, config.TEST_SOUND_ROOT, class_dirs=False)
  else:
    raise ValueError("Invalid format type.")

  # validate that training and validation sets contain the same classes
  if not args.force:
    if sorted(train_videos.keys()) != sorted(validation_videos.keys()):
      raise ValueError("Training and validation videos do not contain the same classes.")

  # create datasets
  datasets = {}
  classes = list(train_videos.keys())
  random.shuffle(classes)

  for num_classes in args.sets:
    set_classes = classes[:num_classes]
    set_train = {cls: videos for cls, videos in train_videos.items() if cls in set_classes}
    set_valid = {cls: videos for cls, videos in validation_videos.items() if cls in set_classes}
    set_test = test_videos

    set_train = metadata.class_keys_to_video_id_keys(set_train)
    set_valid = metadata.class_keys_to_video_id_keys(set_valid)
    set_test = metadata.class_keys_to_video_id_keys(set_test)

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


if __name__ == "__main__":

  parser = argparse.ArgumentParser("Create metadata for all downloaded videos with the option to limit the number of "
                                   "classes included.")

  parser.add_argument("format", help="{}, {} or {}".format(constants.FORMAT_VIDEOS, constants.FORMAT_FRAMES,
                                                           constants.FORMAT_SOUND))

  parser.add_argument("-s", "--sets", type=int, nargs="+", default=[400], help="list of sets to generate, each integer "
                                                                               "denotes number of classes in the set")
  parser.add_argument("-f", "--force", default=False, action="store_true",
                      help="create metadata even if training and validation sets do not contain the same classes")

  parser.add_argument("--save", default="resources/kinetics", help="save path")

  parsed = parser.parse_args()
  main(parsed)
