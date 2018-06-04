import argparse, math, random

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

  # maybe load and validate test videos
  test_videos = None
  if not args.validation_from_training:
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

  # create dataset
  classes = utils.load_json(args.classes)
  num_classes = len(classes)

  set_train = {cls: videos for cls, videos in train_videos.items() if cls in classes}

  # maybe limit the number of training videos
  if args.max_training_videos is not None:
    for cls in classes:
      set_train[cls] = set_train[cls][:args.max_training_videos]

  if args.validation_from_training:

    set_test = {cls: videos for cls, videos in validation_videos.items() if cls in classes}

    # create validation set from the training set
    set_valid = {}

    for cls in classes:
      cls_videos = set_train[cls]
      num_videos = len(cls_videos)
      num_validation_videos = math.ceil(num_videos * args.validation_from_training_fraction)

      random.shuffle(cls_videos)
      set_valid[cls] = cls_videos[:num_validation_videos]
      set_train[cls] = cls_videos[num_validation_videos:]

  else:
    set_valid = {cls: videos for cls, videos in validation_videos.items() if cls in classes}
    set_test = test_videos

  if args.max_testing_videos is not None:
    for cls in classes:
      set_test[cls] = set_test[cls][:args.max_testing_videos]

  set_train = metadata.class_keys_to_video_id_keys(set_train)
  set_valid = metadata.class_keys_to_video_id_keys(set_valid)
  set_test = metadata.class_keys_to_video_id_keys(set_test)

  set_classes = list(sorted(classes))
  set_classes = {cls: idx for idx, cls in enumerate(set_classes)}

  dataset = {
    "train": set_train,
    "valid": set_valid,
    "test": set_test,
    "classes": set_classes
  }

  # save dataset
  train_path = "{:s}_train.json".format(args.save_path, num_classes)
  val_path = "{:s}_val.json".format(args.save_path, num_classes)
  test_path = "{:s}_test.json".format(args.save_path, num_classes)
  classes_path = "{:s}_classes.json".format(args.save_path, num_classes)

  utils.save_json(train_path, dataset["train"])
  utils.save_json(val_path, dataset["valid"])
  utils.save_json(test_path, dataset["test"])
  utils.save_json(classes_path, dataset["classes"])


if __name__ == "__main__":

  parser = argparse.ArgumentParser("Create metadata for all downloaded videos and specify which classes to include.")

  parser.add_argument("format", help="{}, {} or {}".format(constants.FORMAT_VIDEOS, constants.FORMAT_FRAMES,
                                                           constants.FORMAT_SOUND))
  parser.add_argument("classes", help="path to a JSON list of classes to include")
  parser.add_argument("save_path", help="where to save the metadata")

  parser.add_argument("--max-training-videos", default=None, type=int,
                      help="maximum number of training videos per class")
  parser.add_argument("--max-testing-videos", default=None, type=int,
                      help="maximum number of testing videos per class")
  parser.add_argument("--validation-from-training", default=False, action="store_true",
                      help="create the validation set from the training set")
  parser.add_argument("--validation-from-training-fraction", type=float,
                      help="what fraction of training videos to put into the validation set")
  parser.add_argument("-f", "--force", default=False, action="store_true",
                      help="create metadata even if training and validation sets do not contain the same classes")


  parsed = parser.parse_args()
  main(parsed)
