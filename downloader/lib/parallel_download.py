import os
import csv
from multiprocessing import Process, Queue
from pathlib import Path


import lib.downloader as downloader

class Pool:
  """
  A pool of video downloaders.
  """

  def __init__(self, classes, videos_dict, directory, num_workers, failed_save_file, compress, verbose, skip,
               log_file=None):
    """
    :param classes:               List of classes to download.
    :param videos_dict:           Dictionary of all videos.
    :param directory:             Where to download to videos.
    :param num_workers:           How many videos to download in parallel.
    :param failed_save_file:      Where to save the failed videos ids.
    :param compress:              Whether to compress the videos using gzip.
    """

    self.classes = classes
    self.videos_dict = videos_dict
    self.directory = directory
    self.num_workers = num_workers
    self.failed_save_file = failed_save_file
    self.compress = compress
    self.verbose = verbose
    self.skip = skip
    self.log_file = log_file

    self.videos_queue = Queue(100)
    self.failed_queue = Queue(100)

    self.workers = []
    self.failed_save_worker = None

    if verbose:
      print("downloading:")
      if self.classes is not None:
        for cls in self.classes:
          print(cls)
        print()

  def feed_videos(self):
    """
    Feed video ids into the download queue.
    :return:    None.
    """

    if self.classes is None:
      downloader.download_class_parallel(None, self.videos_dict, self.directory, self.videos_queue)
    else:
      for class_name in self.classes:

        if self.verbose:
          print(class_name)

        class_path = os.path.join(self.directory, class_name.replace(" ", "_"))

        if not self.skip or not os.path.isdir(class_path):
          downloader.download_class_parallel(class_name, self.videos_dict, self.directory, self.videos_queue)

      if self.verbose:
        print("done")

  def start_workers(self):
    """
    Start all workers.
    :return:    None.
    """

    # start failed videos saver
    if self.failed_save_file is not None:
      self.failed_save_worker = Process(target=write_failed_worker, args=(self.failed_queue, self.failed_save_file))
      self.failed_save_worker.start()

    # start download workers
    for _ in range(self.num_workers):
      worker = Process(target=video_worker, args=(self.videos_queue, self.failed_queue, self.compress, self.log_file, self.failed_save_file))
      worker.start()
      self.workers.append(worker)

  def stop_workers(self):
    """
    Stop all workers.
    :return:    None.
    """

    # send end signal to all download workers
    for _ in range(len(self.workers)):
      self.videos_queue.put(None)

    # wait for the processes to finish
    for worker in self.workers:
      worker.join()

    # end failed videos saver
    if self.failed_save_worker is not None:
      self.failed_queue.put(None)
      self.failed_save_worker.join()

def video_worker(videos_queue, failed_queue, compress, log_file, failed_log_file):
  """
  Downloads videos pass in the videos queue.
  :param videos_queue:      Queue for metadata of videos to be download.
  :param failed_queue:      Queue of failed video ids.
  :param compress:          Whether to compress the videos using gzip.
  :param log_file:          Path to a log file for youtube-dl.
  :return:                  None.
  """
  failed_ids = []

  lf_path = Path(failed_log_file)

  if lf_path.exists():
    with lf_path.open(mode='r') as lf:
      csv_reader = csv.reader(lf, delimiter=',')
      for row in csv_reader:
        failed_ids.append(row[0])

  # keep_going = True
  while True:
    try:
      request = videos_queue.get(timeout=60*5) # Timeout after 5 minutes

      if request is None:
        break

      video_id, directory, start, end = request

      if video_id in failed_ids:
        print('Skipping {} as previously failed'.format(video_id))
        continue

      success, error = downloader.process_video(video_id, directory, start, end, compress=compress, log_file=log_file)
      if not success:
        if error and 'HTTP Error 429' in str(error):
          print('Exceeded API Limit, no point in continuing')
          break

        failed_queue.put({ video_id: error })

    except Exception as e:
      failed_queue.put({ video_id: str(e) })
      break

def write_failed_worker(failed_queue, failed_save_file):
  """
  Write failed video ids into a file.
  :param failed_queue:        Queue of failed video ids.
  :param failed_save_file:    Where to save the videos.
  :return:                    None.
  """

  while True:
    error_dict = failed_queue.get()

    if error_dict is None:
      break

    with open(failed_save_file, "a") as csv_file:
      writer = csv.writer(csv_file)
      for key, value in error_dict.items():
        writer.writerow([key, value])