
class DiscreteHistogram:

  def __init__(self):
    self.data = {}
    self.nones = 0

  def add(self, value):
    if value is None:
      self.nones += 1

    if value in self.data:
      self.data[value] += 1
    else:
      self.data[value] = 1

  def print(self, threshold=None):
    for key in sorted(self.data.keys()):
      if threshold is None or self.data[key] > threshold:
        print("{}: {:d}".format(key, self.data[key]))

    print("nones: {:d}".format(self.nones))

  def empty(self):
    self.data = {}
    self.nones = 0