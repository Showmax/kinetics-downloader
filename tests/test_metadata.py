import os, unittest
import lib.utils as utils

class TestMetadata(unittest.TestCase):

  def test_no_overlap(self):

    resources = "resources"
    datasets = ["kinetics_2", "kinetics_50_old", "kinetics_50", "kinetics_100", "kinetics_200", "kinetics_400"]

    for dataset in datasets:

      train_path = os.path.join(resources, "{:s}_train.json".format(dataset))
      valid_path = os.path.join(resources, "{:s}_val.json".format(dataset))
      test_path = os.path.join(resources, "{:s}_test.json".format(dataset))

      train_meta = utils.load_json(train_path)
      valid_meta = utils.load_json(valid_path)
      test_meta = utils.load_json(test_path)

      train_videos = list(train_meta.keys())
      valid_videos = list(valid_meta.keys())
      test_videos = list(test_meta.keys())

      self.assertFalse(not set(train_videos).isdisjoint(valid_videos))
      self.assertFalse(not set(train_videos).isdisjoint(test_videos))
      self.assertFalse(not set(valid_videos).isdisjoint(test_videos))