import argparse, os

import lib.config as config
import lib.utils as utils

def main(args):

  meta = utils.load_json(args.path)

  list_file = open(args.save, "w")

  for video_id, cls in meta.items():

    video_path_frames = os.path.join(config.TRAIN_FRAMES_ROOT, cls.replace(" ", "_"), video_id)
    video_path_flow = os.path.join(config.TRAIN_FLOW_FLOWNET_CSS_FT_SD, cls.replace(" ", "_"), video_id)

    num_frames = len(os.listdir(video_path_frames))

    for frame_idx in range(num_frames - 1):

      frame_1_path = os.path.join(video_path_frames, "frame{:d}.jpg".format(frame_idx))
      frame_2_path = os.path.join(video_path_frames, "frame{:d}.jpg".format(frame_idx + 1))
      flow_path = os.path.join(video_path_flow, "flow{:d}.flo".format(frame_idx))

      list_file.write("{:s} {:s} {:s}\n".format(frame_1_path, frame_2_path, flow_path))

parser = argparse.ArgumentParser()

parser.add_argument("path", help="path to the metadata")
parser.add_argument("save", help="where to save the list")

parsed = parser.parse_args()
main(parsed)