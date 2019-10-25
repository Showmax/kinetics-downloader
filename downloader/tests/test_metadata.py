import unittest

import lib.config as config
import lib.utils as utils

class TestMetadata(unittest.TestCase):

  def test_no_overlap(self):

    train_meta = utils.load_json(config.TRAIN_METADATA_PATH)
    valid_meta = utils.load_json(config.VAL_METADATA_PATH)
    test_meta = utils.load_json(config.TEST_METADATA_PATH)

    train_videos = list(train_meta.keys())
    valid_videos = list(valid_meta.keys())
    test_videos = list(test_meta.keys())

    self.assertFalse(not set(train_videos).isdisjoint(valid_videos))
    self.assertFalse(not set(train_videos).isdisjoint(test_videos))
    self.assertFalse(not set(valid_videos).isdisjoint(test_videos))