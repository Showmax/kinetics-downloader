import os
from multiprocessing import Process, Queue

import lib.video as video

class Pool:
  """
  A pool of video downloaders.
  """

  def __init__(self, classes, source_directory, target_directory, num_workers, failed_save_file):
    self.classes = classes
    self.source_directory = source_directory
    self.target_directory = target_directory
    self.num_workers = num_workers
    self.failed_save_file = failed_save_file

    self.videos_queue = Queue(100)
    self.failed_queue = Queue(100)

    self.workers = []
    self.failed_save_worker = None

  def feed_videos(self):
    """
    Feed videos to a queue for workers.
    :return:      None.
    """

    if self.classes is None:
      videos = os.listdir(self.source_directory)

      for filename in videos:
        video_path = os.path.join(self.source_directory, filename)
        video_id = ".".join(filename.split(".")[:-1])
        target_dir_path = os.path.join(self.target_directory, video_id)
        self.videos_queue.put((video_id, video_path, target_dir_path))
    else:
      for class_name in self.classes:
        source_class_dir = os.path.join(self.source_directory, class_name.replace(" ", "_"))
        target_class_dir = os.path.join(self.target_directory, class_name.replace(" ", "_"))

        if os.path.isdir(source_class_dir):

          if not os.path.isdir(target_class_dir):
            # when using multiple processes, the folder might have been already created (after the if was evaluated)
            try:
              os.makedirs(target_class_dir)
            except FileExistsError:
              pass

          videos = os.listdir(source_class_dir)

          for filename in videos:
            video_path = os.path.join(source_class_dir, filename)
            video_id = ".".join(filename.split(".")[:-1])
            target_dir_path = os.path.join(target_class_dir, video_id)
            self.videos_queue.put((video_id, video_path, target_dir_path))

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
      worker = Process(target=video_worker, args=(self.videos_queue, self.failed_queue))
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

def video_worker(videos_queue, failed_queue):
  """
  Process video files.
  :param videos_queue:      Queue of video paths.
  :param failed_queue:      Queue for failed videos.
  :return:                  None.
  """

  while True:
    request = videos_queue.get()

    if request is None:
      break

    video_id, video_path, target_dir = request

    if os.path.isdir(target_dir):
      continue

    os.makedirs(target_dir)

    if not video.video_to_jpgs(video_path, target_dir):
      failed_queue.put(video_id)

def write_failed_worker(failed_queue, failed_save_file):
  """
  Write failed video ids into a file.
  :param failed_queue:        Queue of failed video ids.
  :param failed_save_file:    Where to save the videos.
  :return:                    None.
  """

  file = open(failed_save_file, "a")

  while True:
    video_id = failed_queue.get()

    if video_id is None:
      break

    file.write("{}\n".format(video_id))

  file.close()
