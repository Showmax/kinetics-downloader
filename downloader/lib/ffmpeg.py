import json, subprocess, os
from enum import Enum

class Medium:
  """
  Stores metadata for movie and audio files.
  """

  class Type(Enum):
    AUDIO = 1
    VIDEO = 2

  def __init__(self, type):
    """
    :param type: Type of the medium, see the Type enum.
    """

    self.raw_json = None

    self.sample_rate = None
    self.channels = None
    self.audio_duration_sec = None

    self.width = None
    self.height = None
    self.video_duration_sec = None
    self.frame_rate = None

    if type not in self.Type:
      raise ValueError("Invalid medium type")

    self.type = type

  def from_file(self, path):
    """
    Extract metadata from an audio or a movie file.
    :param path:    Path to the file.
    :return:        None.
    """
    self.__load_json(path)

    self.__decode_audio_json()

    if self.type == self.Type.VIDEO:
      self.__decode_video_json()

  def from_json(self, path):
    """
    Load metadata stored in a JSON file.
    :param path:    Path to the JSON file.
    :return:        None.
    """

    if not os.path.isfile(path):
      raise FileNotFoundError("JSON file not found at: %s" % path)

    with open(path, "r") as file:
      json_obj = json.load(file)

    self.sample_rate = json_obj["sample_rate"]
    self.channels = json_obj["channels"]
    self.audio_duration_sec = json_obj["audio_duration_sec"]

    if self.type == self.Type.VIDEO:
      self.width = json_obj["width"]
      self.height = json_obj["height"]
      self.video_duration_sec = json_obj["video_duration_sec"]
      self.frame_rate = json_obj["frame_rate"]

  def to_json(self, path):
    """
    Save metadata to a JSON file.
    :param path:    Path to the JSON file.
    :return:        None.
    """

    json_obj = {
      "sample_rate": self.sample_rate,
      "channels": self.channels,
      "audio_duration_sec": self.audio_duration_sec
    }

    if self.type == self.Type.VIDEO:
      json_obj["width"] = self.width
      json_obj["height"] = self.height
      json_obj["video_duration_sec"] = self.video_duration_sec
      json_obj["frame_rate"] = self.frame_rate

    with open(path, "w") as file:
      json.dump(json_obj, file)

  def to_dict(self):
    """
    Transfer various attributes to a dictionary.
    :return:    The dictionary.
    """

    obj = {}

    if self.sample_rate is not None:
      obj["sample_rate"] = self.sample_rate
    if self.channels is not None:
      obj["channels"] = self.channels
    if self.audio_duration_sec is not None:
      obj["audio_duration_sec"] = self.audio_duration_sec

    if self.width is not None:
      obj["width"] = self.width
    if self.height is not None:
      obj["height"] = self.height
    if self.video_duration_sec is not None:
      obj["video_duration_sec"] = self.video_duration_sec
    if self.frame_rate is not None:
      obj["frame_rate"] = self.frame_rate

    return obj

  def __load_json(self, path):
    """
    Extract FFPROBE JSON for an audio or a video file.
    :param path:      Path to the file.
    :return:          None.
    """

    result = subprocess.check_output(["ffprobe", path, "-print_format", "json", "-show_streams"], stderr=subprocess.DEVNULL)
    result = result.decode()
    obj = json.loads(result)
    self.raw_json = obj

    if "streams" not in self.raw_json:
      raise ValueError("Unexpected JSON format, key streams not found")

  def __find_codec_type(self, type):
    """
    Find a stream with a given codec type.
    :param type:    The codec type to search for.
    :return:        The stream information or None if not found.
    """
    for item in self.raw_json["streams"]:
      if "codec_type" in item and item["codec_type"] == type:
        return item

    return None

  def __decode_audio_json(self):
    """
    Decode audio metadata from FFPROBE JSON output.
    :return:    None.
    """
    audio_json = self.__find_codec_type("audio")

    self.sample_rate = float(audio_json["sample_rate"])
    self.channels = float(audio_json["channels"])

    if "duration" in audio_json.keys():
      self.audio_duration_sec = float(audio_json["duration"])

  def __decode_video_json(self):
    """
    Decode video metadata from FFPROBE JSON output.
    :return:    None.
    """
    video_json = self.__find_codec_type("video")

    self.width = float(video_json["width"])
    self.height = float(video_json["height"])

    if "duration" in video_json.keys():
      self.video_duration_sec = float(video_json["duration"])

    self.frame_rate = self.__decode_frame_rate(video_json["avg_frame_rate"])

  @staticmethod
  def __decode_frame_rate(raw):
    """
    Decode movie frame rate from FFPROBE output.
    :param raw:     Raw frame rate string.
    :return:        Frame rate float.
    """
    split = raw.split("/")
    first = int(split[0])
    second = int(split[1])
    return first / second