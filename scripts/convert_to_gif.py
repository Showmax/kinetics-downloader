from pathlib import Path
from collections import defaultdict
import json
import subprocess
from multiprocessing import Process, Queue, current_process, cpu_count
import shutil
import os
import glob

DATASET_ROOT = Path("/media/gitumarkk/Seagate Backup Plus Drive//Dancelogue/DATASETS/Kinetics/")
DATA_GIF_ROOT = Path("/home/gitumarkk/Desktop/WORK_DIR/kinetics_gif/")

DATA_GIF_ROOT.mkdir(exist_ok=True, parents=True)


class Pool:
  def __init__(self):
    self.num_workers = cpu_count() * 2
    self.workers = []
    self.videos_queue = Queue(100)

  def start_workers(self):
    for _ in range(self.num_workers):
      worker = Process(
        target=video_worker,
        args=(self.videos_queue,)
      )
      worker.start()
      self.workers.append(worker)

  def stop_workers(self):
    """
    Stop all workers.
    :return:    None.
    """

    # clean_png()

    # send end signal to all download workers
    for _ in range(len(self.workers)):
      self.videos_queue.put(None)

    # wait for the processes to finish
    for worker in self.workers:
      worker.join()

  def feed_videos(self):
    read_files(self.videos_queue)


def video_worker(videos_queue):
  while True:
    request = videos_queue.get(timeout=60)
    if request is None:
      break

    file_path, output_path, index, folder, png_parent = request
    generate_gif(file_path, output_path, index, folder, png_parent)

def generate_gif(filename, output_path, index, folder, png_parent):
  output_gif = output_path / "{}.gif".format(filename.stem)
  if output_gif.exists() or filename.suffix != '.mp4':
    print('iter {} - skipping {} of {} - {}'.format(index, filename.stem, filename.parent.stem, folder))
    return

  png_file = str(png_parent / "{}_%06d.png".format(output_gif.stem))

  subprocess.call([
    'ffmpeg',
    '-i', str(filename),
    '-filter_complex',
    "[0:v] fps=4,scale={scale}:-1".format(scale='180'),
    '-f', 'image2',
    '-loglevel', 'warning',
    '-y',
    png_file
  ])

  subprocess.call([
    'ffmpeg',
    '-i', png_file,
    '-f', 'gif',
    '-framerate', '16',
    '-loglevel', 'warning',
    '-y',
    str(output_gif)
  ])

  print('iter {} - {} - {} - completed of {}'.format(index, filename.stem, filename.parent.stem, folder))

  for png in glob.glob(str(png_parent / "{}_*".format(output_gif.stem))):
    os.remove(png)

def read_files(videos_queue):
  file_dict = defaultdict(dict)
  for f1 in DATASET_ROOT.iterdir():
    if f1.stem in ['train']:
      folder_path = DATA_GIF_ROOT / f1.stem
      folder_path.mkdir(exist_ok=True, parents=True)

      png_parent = folder_path / 'png'
      png_parent.mkdir(exist_ok=True, parents=True)

      for index_1, f2 in enumerate(f1.iterdir()):
        if f2.is_dir():
          f2_folder_path = (folder_path / f2.stem)
          f2_folder_path.mkdir(exist_ok=True, parents=True)


          for index_2, f3 in enumerate(f2.iterdir()):
            videos_queue.put((f3, f2_folder_path, index_2, f1.stem, png_parent))

        else:
          pass
          # videos_queue.put((f2, folder_path, index_1, f1.stem))
          # folder_path = DATA_GIF_ROOT / f2.stem
          # folder_path.mkdir(exist_ok=True, parents=True)

          # file_dict[f2.name]['folder'] = f1.stem
          # file_dict[f2.name]['size'] = f2.stat().st_size

      #
  return file_dict

def clean_png():
  for f1 in DATASET_ROOT.iterdir():
    if f1.stem in ['val']:
      folder_path = DATA_GIF_ROOT / f1.stem
      png_parent = folder_path / 'png'
      if png_parent.is_dir():
        shutil.rmtree(png_parent)


def run():
  pool = Pool()
  pool.start_workers()
  pool.feed_videos()
  pool.stop_workers()

run()
