import argparse, os, librosa
import tensorflow as tf

import lib.config as config
import lib.utils as utils

kinetics_sound_400_train = utils.load_json("resources/kinetics_full_sound_400_train.json")
kinetics_sound_400_valid = utils.load_json("resources/kinetics_full_sound_400_val.json")
kinetics_classes = utils.load_json("resources/kinetics_full_sound_400_classes.json")
sampling_rate = 22050

def load_audio(path):
  audio, _ = librosa.load(path, sr=sampling_rate, mono=True)
  return audio

def bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def convert_to_tfrecord(meta, classes, root, records_path, class_dirs=True):

  writer = tf.python_io.TFRecordWriter(records_path)

  i = 0
  for path, cls_name in meta.items():

    if i > 0 and i % 100 == 0:
      print(i)

    if class_dirs:
      cls_id = classes[cls_name]
      file_path = os.path.join(root, cls_name.replace(" ", "_"), path + ".mp3")
    else:
      cls_id = 0
      file_path = os.path.join(root, path + ".mp3")

    audio = load_audio(file_path)
    audio_raw = audio.tostring()

    length = audio.shape[0]

    example = tf.train.Example(features=tf.train.Features(feature={
      "path": bytes_feature(file_path),
      "length": int64_feature(length),
      "sound_raw": bytes_feature(audio_raw),
      "cls_id": int64_feature(cls_id)}))

    writer.write(example.SerializeToString())
    i += 1

  writer.close()

def main(args):

  if args.subset == "train":
    root = config.TRAIN_SOUND_ROOT
    cls_dirs = True
  elif args.subset == "valid":
    root = config.VALID_SOUND_ROOT
    cls_dirs = True
  elif args.subset == "test":
    root = config.TEST_SOUND_ROOT
    cls_dirs = False

  convert_to_tfrecord(utils.load_json(args.meta_path), utils.load_json(args.classes_path), root, args.save_path, class_dirs=cls_dirs)

parser = argparse.ArgumentParser()
parser.add_argument("subset", help="train, valid or test")
parser.add_argument("meta_path", help="metadata path")
parser.add_argument("classes_path", help="classes path")
parser.add_argument("save_path", help="tfrecords file save path")
parsed = parser.parse_args()
main(parsed)
