import os
import csv
from multiprocessing import Process, Queue, current_process
from pathlib import Path
import time


import lib.downloader as downloader

class Pool:
  """
  A pool of video downloaders.
  """

  def __init__(self, classes, videos_dict, directory, num_workers, failed_save_file, compress, verbose, skip,
               log_file=None, stats_file=None):
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
    self.stats_file = stats_file

    self.videos_queue = Queue(100)
    self.failed_queue = Queue(100)
    self.stats_queue = Queue(100)

    self.workers = []
    self.failed_save_worker = None
    self.stats_worker = None

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

    # start stats worker
    if self.stats_file is not None:
      self.stats_worker = Process(target=write_stats_worker, args=(self.stats_queue, self.stats_file))
      self.stats_worker.start()

    # start download workers
    for _ in range(self.num_workers):
      worker = Process(
        target=video_worker,
        args=(
          self.videos_queue, self.failed_queue, self.compress,
          self.log_file, self.failed_save_file, self.stats_queue)
      )
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

    # End stats saver
    if self.stats_worker is not None:
      self.stats_queue.put(None)
      self.stats_worker.join()

def video_worker(videos_queue, failed_queue, compress, log_file, failed_log_file, stats_queue):
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
  elapsed = 0
  i = 0
  s = 0
  while True:
    try:
      request = videos_queue.get(timeout=60*5) # Timeout after 5 minutes

      if request is None:
        stats_queue.put(None)
        break

      video_id, directory, start, end = request
      s += 1

      if video_id in failed_ids:
        print('Skipping {} as previously failed'.format(video_id))
        continue

      slice_path = "{}.mp4".format(os.path.join(directory, video_id))
      if os.path.isfile(slice_path):
        print('Exists skipping {}'.format(video_id))
        continue

      start_time = time.time()
      result = downloader.process_video(video_id, directory, start, end, compress=compress, log_file=log_file)
      duration = round(time.time() - start_time, 1)
      elapsed += duration

      current = current_process()
      label = Path(directory).stem

      print("Completed {video_id}: duration={duration}s, download={download_duration}s, ffmpeg={ffmpeg_duration}s, elapsed={elapsed}s, avg={avg}s, i={i}, i+s={s}, id={cp}, pid={pid}, label={label}".format(
        video_id=video_id,
        duration=duration,
        download_duration=result.get("download_duration"),
        ffmpeg_duration=result.get("ffmpeg_duration"),
        elapsed=round(elapsed, 1),
        avg=round(elapsed / (i + 1), 1),
        i=i,
        s=s,
        cp=current.name,
        pid=current.pid,
        label=label)
      )

      result.update({
        'total_duration': duration,
        'elapsed': round(elapsed, 1),
        'average_duration': round(elapsed / (i + 1), 1),
        'iteration': i,
        'skipped_iteration': s,
        'queue_id': current.name,
        'pid': current.pid,
        'label': label
      })

      if result.get('success'):
        stats_queue.put(result)

      i += 1
      if not result.get('success'):
        if result.get('error') and 'HTTP Error 429' in result.get('error'):
          print('Exceeded API Limit, no point in continuing')
          break

        failed_queue.put(result)

    except Exception as e:
      failed_queue.put({ 'video_id': video_id, 'error': str(e) })
      break

def write_failed_worker(failed_queue, failed_save_file):
  """
  Write failed video ids into a file.
  :param failed_queue:        Queue of failed video ids.
  :param failed_save_file:    Where to save the videos.
  :return:                    None.
  """

  while True:
    error = failed_queue.get()

    if error is None:
      break

    with open(failed_save_file, "a") as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow([error.get('video_id'), error.get('label'), error.get('error')])


def write_stats_worker(stats_queue, stats_file):
  """
  Write failed video ids into a file.
  :param failed_queue:        Queue of failed video ids.
  :param failed_save_file:    Where to save the videos.
  :return:                    None.
  """
  fieldnames = [
    "video_id", "label", "status", "download_duration",
    "ffmpeg_duration", "total_duration", "average_duration", "elapsed",
    "iteration", "skipped_iteration", "queue_id", "pid"
  ]
  with open(stats_file, "a") as csv_file:
    writer = csv.DictWriter(
      csv_file,
      fieldnames=fieldnames
    )
    writer.writeheader()

    writer = csv.writer(csv_file)

    while True:
      stats = stats_queue.get()
      if not stats:
        break
      writer.writerow([stats[f] for f in fieldnames])
