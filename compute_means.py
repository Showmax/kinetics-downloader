import argparse, cv2, os
import numpy as np

import lib.config as config
import lib.utils as utils

def main(args):

  r_avg = utils.StreamingAverage()
  g_avg = utils.StreamingAverage()
  b_avg = utils.StreamingAverage()

  for video_id, cls in args.train_metadata.items():

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

parser = argparse.ArgumentParser("Compute means over a subset (most likely the training subset) of Kinetics.")

parser.add_argument("train_metadata", help="metadata containing all downloaded videos")
parser.add_argument("save_path", help="where to save a numpy array containing R, G and B channel means")

parsed = parser.parse_args()
main(parsed)