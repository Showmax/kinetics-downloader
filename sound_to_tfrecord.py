import librosa

import lib.config as config
import lib.utils as utils

kinetics_sound_400_train = utils.load_json("resources/kinetics_full_sound_400_train.json")
kinetics_sound_400_valid = utils.load_json("resources/kinetics_full_sound_400_val.json")
sampling_rate = 22050

def load_audio(path):
  audio, _ = librosa.load(path, sr=sampling_rate, mono=True)
  return audio

def convert_to_tfrecord(meta):

  for path, cls in meta.items():

  	audio = load_audio(path + ".mp3")
  	print(audio.shape)

convert_to_tfrecord(kinetics_sound_400_train)