import argparse, cv2, os
import numpy as np

import lib.config as config
import lib.utils as utils

train_metadata = utils.load_json("resources/kinetics_400_train.json")

class Avg:
  """
  Simple streaming average data structure.
  """

  def __init__(self):
    self.avg = 0
    self.count = 0

  def add(self, value):
    self.avg = (self.avg * self.count + value) / (self.count + 1)
    self.count += 1

def main(args):

  r_avg = Avg()
  g_avg = Avg()
  b_avg = Avg()

  for video_id, cls in train_metadata.items():

    video_folder_path = os.path.join(config.TRAIN_FRAMES_ROOT, cls.replace(" ", "_"), video_id)

    frame_paths = [os.path.join(video_folder_path, frame_path) for frame_path in os.listdir(video_folder_path)]

    for frame_path in frame_paths:

      frame = cv2.imread(frame_path)

      assert len(frame.shape) == 3
      assert frame.shape[-1] == 3

      # opencv loads images in BGR
      b = np.mean(frame[..., 0])
      g = np.mean(frame[..., 1])
      r = np.mean(frame[..., 2])

      r_avg.add(r)
      g_avg.add(g)
      b_avg.add(b)

  means = [r_avg.avg, g_avg.avg, b_avg.avg]
  np.save(args.save_path, means)

parser = argparse.ArgumentParser("Compute means over the whole training split (kinetics_400_train) of Kinetics.")

parser.add_argument("save_path", help="where to save a numpy array containing R, G and B channel means")

parsed = parser.parse_args()
main(parsed)