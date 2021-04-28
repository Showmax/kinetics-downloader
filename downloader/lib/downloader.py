import os, subprocess
from pathlib import Path
import time


def download_video(video_id, download_path, video_format="mp4", log_file=None):
  """
  Download video from YouTube.
  :param video_id:        YouTube ID of the video.
  :param download_path:   Where to save the video.
  :param video_format:    Format to download.
  :param log_file:        Path to a log file for youtube-dl.
  :return:                Tuple: path to the downloaded video and a bool indicating success.
  """

  error = None

  if log_file is None:
    stderr = subprocess.DEVNULL
  else:
    stderr = open(log_file, "a")
  try:
    # print("Downloading = {}".format(video_id))
    process_command = " ".join([
      "youtube-dl",
      "https://youtube.com/watch?v={}".format(video_id),
      "-f", '"bestvideo[ext={},height<=360]/best"'.format(video_format),
      "--output", '"{}"'.format(download_path),
      "--no-continue"
    ])

    # print(process_command)
    subprocess.check_output(
      process_command,
      stderr=subprocess.STDOUT,
      shell=True
    )
    success = True

  except Exception as e:
    print("\n {} Failed with error \n {}".format(video_id, e.stdout))
    success = False
    error = e.stdout

  if log_file is not None:
    stderr.close()

  return success, error

def cut_video(raw_video_path, slice_path, start, end):
  """
  Cut out the section of interest from a video.
  :param raw_video_path:    Path to the whole video.
  :param slice_path:        Where to save the slice.
  :param start:             Start of the section.
  :param end:               End of the section.
  :return:                  Tuple: Path to the video slice and a bool indicating success.
  """

  return_code = subprocess.call(["ffmpeg", "-loglevel", "quiet", "-i", raw_video_path, "-strict", "-2",
                                 "-ss", str(start), "-to", str(end), slice_path])
  success = return_code == 0

  return success

def compress_video(video_path):
  """
  Compress video.
  :param video_path:    Path to the video.
  :return:              None.
  """
  return subprocess.call(["gzip", video_path]) == 0

def process_video(video_id, directory, start, end, video_format="mp4", compress=False, overwrite=False, log_file=None):
  """
  Process one video for the kinetics dataset.
  :param video_id:        YouTube ID of the video.
  :param directory:       Directory where to save the video.
  :param start:           Start of the section of interest.
  :param end:             End of the section of interest.
  :param video_format:    Format of the processed video.
  :param compress:        Decides if the video slice should be compressed by gzip.
  :param overwrite:       Overwrite processed videos.
  :param log_file:        Path to a log file for youtube-dl.
  :return:                Bool indicating success.
  """

  download_path = "{}_raw.{}".format(os.path.join(directory, video_id), video_format)
  mkv_download_path = "{}_raw.mkv".format(os.path.join(directory, video_id))
  slice_path = "{}.{}".format(os.path.join(directory, video_id), video_format)

  # simply delete residual downloaded videos
  if os.path.isfile(download_path):
    os.remove(download_path)

  # if sliced video already exists, decide what to do next
  if os.path.isfile(slice_path):
    if overwrite:
      os.remove(slice_path)
    else:
      print('Exists skipping {}'.format(video_id))
      return {'success': True, 'video_id': video_id, 'status': 'Exists'}

  # sometimes videos are downloaded as mkv
  if not os.path.isfile(mkv_download_path):
    # download video and cut out the section of interest

    download_start_time = time.time()
    success, error = download_video(video_id, download_path, log_file=log_file)
    download_duration = time.time() - download_start_time

    if not success:
      return {'success': False, 'video_id': video_id, 'error': str(error)}

  # video was downloaded as mkv instead of mp4
  if not os.path.isfile(download_path) and os.path.isfile(mkv_download_path):
    download_path = mkv_download_path

  ffmpeg_start_time = time.time()
  success = cut_video(download_path, slice_path, start, end)
  ffmpeg_duration = time.time() - ffmpeg_start_time

  if not success:
    return {'success': False, 'video_id': video_id, 'error': 'Cutting the video failed'}

  # remove the downloaded video
  os.remove(download_path)

  return {
    'success': True,
    'video_id': video_id,
    'status': 'Completed',
    'download_duration': round(download_duration, 1),
    'ffmpeg_duration': round(ffmpeg_duration, 1)
  }

def download_class_sequential(class_name, videos_dict, directory, compress=False, log_file=None):
  """
  Download all videos with the given label sequentially.
  :param class_name:      The label.
  :param videos_dict:     Dataset metadata.
  :param directory:       Directory where to save the videos.
  :param compress:        Decides if the video slice should be compressed by gzip.
  :param log_file:        Path to a log file for youtube-dl.
  :return:                List of videos could not be processed.
  """

  class_dir = os.path.join(directory, class_name.replace(" ", "_"))
  failed_videos = []

  if not os.path.isdir(class_dir):
    # when using multiple processes, the folder might have been already created (after the if was evaluated)
    try:
      os.mkdir(class_dir)
    except FileExistsError:
      pass

  for key in videos_dict.keys():
    metadata = videos_dict[key]
    annotations = metadata["annotations"]

    if annotations["label"].lower() == class_name.lower():
      start = annotations["segment"][0]
      end = annotations["segment"][1]

      success, error = process_video(key, class_dir, start, end, compress=compress, log_file=log_file)
      if not success:
        if 'HTTP Error 429' in error:
          raise Exception('Exceeded API Limit, no point in continuing')
        failed_videos.append({"key": key, "error": error})

  return failed_videos

def download_class_parallel(class_name, videos_dict, directory, videos_queue):
  """
  Download all videos of the given class in parallel.
  :param class_name:        Name of the class.
  :param videos_dict:       Dictionary of all videos.
  :param directory:         Where to save the videos.
  :param videos_queue:      Videos queue for parallel download.
  :return:                  None.
  """

  if class_name is None:
    class_dir = directory
  else:
    class_dir = os.path.join(directory, class_name.replace(" ", "_"))

  if not os.path.isdir(class_dir):
    # when using multiple processes, the folder might have been already created (after the if was evaluated)
    try:
      os.mkdir(class_dir)
    except FileExistsError:
      pass

  for key in videos_dict.keys():
    metadata = videos_dict[key]
    annotations = metadata["annotations"]
    # if class_name is None or annotations["label"].lower() == class_name.lower():
    start = annotations["segment"][0]
    end = annotations["segment"][1]

    videos_queue.put((key, class_dir, start, end))
