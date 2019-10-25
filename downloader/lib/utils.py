import json

def load_json(path):
  """
  Load a JSON file.
  :param path:    Path to the file.
  :return:        The loaded JSON file.
  """

  with open(path, "r") as file:
    return json.load(file)

def save_json(path, data):
  """
  Save JSON into a file.
  :param path:      Where to save the JSON data.
  :param data:      The JSON data.
  :return:          None.
  """

  with open(path, "w") as file:
    json.dump(data, file, indent=4, sort_keys=True)

def class_name_to_dir_name(class_name):
  """
  Replace all spaces with underscores.
  :param class_name:      Class name string.
  :return:                Modified class name.
  """

  return class_name.replace(" ", "_")

class DiscreteHistogram:

  def __init__(self):
    """
    A histogram for discrete values.
    """
    self.data = {}
    self.nones = 0

  def add(self, value):
    """
    Add a value.
    :param value:   A value to add.
    :return:        None
    """

    if value is None:
      self.nones += 1

    if value in self.data:
      self.data[value] += 1
    else:
      self.data[value] = 1

  def print(self, threshold=None):
    """
    Print histogram contents.
    :param threshold:     Don't print values that occurred less times than the threshold.
    :return:
    """

    for key in sorted(self.data.keys()):
      if threshold is None or self.data[key] > threshold:
        print("{}: {:d}".format(key, self.data[key]))

    if self.nones >= 1:
      print("nones: {:d}".format(self.nones))

  def empty(self):
    """
    Reset the histogram.
    :return:    None.
    """

    self.data = {}
    self.nones = 0

class StreamingAverage:
  """
  Simple streaming average data structure.
  """

  def __init__(self):
    self.avg = 0
    self.count = 0

  def add(self, value):
    """
    Add a value to the streaming average.
    :param value:     A value.
    :return:          None.
    """
    self.avg = (self.avg * self.count + value) / (self.count + 1)
    self.count += 1
