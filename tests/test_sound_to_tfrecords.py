import unittest
import numpy as np

import sound_to_tfrecords
import lib.constants as constants

class TestSoundToTfrecords(unittest.TestCase):

  def test_string_to_bytes_feature(self):

    string = "data/file1.mp3"
    feature = sound_to_tfrecords.bytes_feature(string.encode())

    output_string = feature.bytes_list.value[0].decode()

    self.assertEqual(output_string, string)

  def test_generate_example(self):

    file_path = "data/file1.mp3"
    length = 220500
    audio_raw = np.random.uniform(-1, 1, size=(length, 1)).tostring()
    cls_id = 200

    example = sound_to_tfrecords.generate_example(file_path, length, audio_raw, cls_id)

    file_path_feature = example.features.feature[constants.TFRECORDS_KEY_PATH]
    length_feature = example.features.feature[constants.TFRECORDS_KEY_LENGTH]
    audio_raw_feature = example.features.feature[constants.TFRECORDS_KEY_SOUND_RAW]
    cls_id_feature = example.features.feature[constants.TFRECORDS_KEY_CLS_ID]

    self.assertEqual(file_path_feature.bytes_list.value[0].decode(), file_path)
    self.assertEqual(length_feature.int64_list.value[0], length)
    self.assertEqual(audio_raw_feature.bytes_list.value[0], audio_raw)
    self.assertEqual(cls_id_feature.int64_list.value[0], cls_id)