import argparse, os

import lib.parallel_to_frames as parallel

def process_classes(classes, train_root, valid_root, train_frames_root, valid_frames_root, num_workers,
                    failed_save_file):
  """
  Extract video frames for a class.
  :param classes:               List of classes.
  :param num_workers:           Number of worker processes.
  :param failed_save_file:      Path to a log of failed extractions.
  :return:                      None.
  """

  for source_root, target_root in zip([train_root, valid_root],
                                      [train_frames_root, valid_frames_root]):

    pool = parallel.Pool(classes, source_root, target_root, num_workers, failed_save_file)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def main(args):

  train_root = "training"
  valid_root = "validation"

  train_frames_root = "training_frames"
  valid_frames_root = "validation_frames"

  classes = os.listdir("training")

  process_classes(classes, train_root, valid_root, train_frames_root, valid_frames_root, args.num_workers,
                  args.failed_log)

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Extract individual frames from videos for faster loading.")

  parser.add_argument("--num-workers", type=int, default=1, help="number of worker threads")
  parser.add_argument("--failed-log", default="failed_frames.txt", help="where to save list of videos for "
                                                                        "which the frame extraction failed")

  parsed = parser.parse_args()
  main(parsed)
