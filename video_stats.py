import argparse, os

import lib.config as config
from lib.ffmpeg import Medium
from lib.utils import DiscreteHistogram

def scan_video(path, frame_rate_hist, video_duration_hist, resolution_hist):

  vid = Medium(Medium.Type.VIDEO)
  vid.from_file(path)

  frame_rate_hist.add(round(vid.frame_rate))
  resolution_hist.add("{:d}x{:d}".format(round(vid.width), round(vid.height)))

  if vid.video_duration_sec is not None:
    video_duration_hist.add(round(vid.video_duration_sec))
  else:
    video_duration_hist.add(round(vid.audio_duration_sec))

def main(args):

  frame_rate_hist = DiscreteHistogram()
  video_duration_hist = DiscreteHistogram()
  resolution_hist = DiscreteHistogram()

  for root in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
    for cls_dir in os.listdir(root):
      for vid_path in os.listdir(os.path.join(root, cls_dir)):
        scan_video(os.path.join(root, cls_dir, vid_path), frame_rate_hist, video_duration_hist, resolution_hist)

  print("frame rate:")
  frame_rate_hist.print(threshold=args.threshold)
  print()

  print("duration:")
  video_duration_hist.print(threshold=args.threshold)
  print()

  print("resolution:")
  resolution_hist.print(threshold=args.threshold)
  print()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("-t", "--threshold", default=None)

  parsed = parser.parse_args()
  main(parsed)