import os, subprocess

def download_video(video_id, download_path, video_format="mp4"):
  """
  Download video from YouTube.
  :param video_id:        YouTube ID of the video.
  :param directory:       Directory where to save the video.
  :param video_format:    Format to download.
  :return:                Tuple: path to the downloaded video and a bool indicating success.
  """

  return_code = subprocess.call(["youtube-dl", "https://youtube.com/watch?v={}".format(video_id),
                   "--quiet", "-f", "bestvideo[ext={}]+bestaudio/best".format(video_format),
                   "--output", download_path, "--no-continue"], stderr=subprocess.DEVNULL)
  success = return_code == 0

  return success

def cut_video(raw_video_path, slice_path, start, end):
  """
  Cut out the section of interest from a video.
  :param raw_video_path:    Path to the whole video.
  :param video_id:          YouTube ID of the video.
  :param directory:         Directory where to save the output.
  :param start:             Start of the section.
  :param end:               End of the section.
  :param video_format:      Format of the output video.
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

def process_video(video_id, directory, start, end, video_format="mp4", compress=False, overwrite=False):
  """
  Process one video for the kinetics dataset.
  :param video_id:        YouTube ID of the video.
  :param directory:       Directory where to save the video.
  :param start:           Start of the section of interest.
  :param end:             End of the section of interest.
  :param compress:        Decides if the video slice should be compressed by gzip.
  :return:                Bool indicating success.
  """

  download_path = "{}_raw.{}".format(os.path.join(directory, video_id), video_format)
  slice_path = "{}.{}".format(os.path.join(directory, video_id), video_format)

  # simply delete residual downloaded videos
  if os.path.isfile(download_path):
    os.remove(download_path)

  # if slices video already exists, decide what to do next
  if os.path.isfile(slice_path):
    if overwrite:
      os.remove(slice_path)
    else:
      return True

  # download video and cut out the section of interest
  success = download_video(video_id, download_path)

  if not success:
    return False

  success = cut_video(download_path, slice_path, start, end)

  if not success:
    return False

  # remove the downloaded video
  os.remove(download_path)

  if compress:
    # compress the video slice
    return compress_video(slice_path)

  return True

def download_class_sequential(class_name, videos_dict, directory, compress=False):
  """
  Download all videos with the given label sequentially.
  :param class_name:      The label.
  :param videos_dict:     Dataset metadata.
  :param directory:       Directory where to save the videos.
  :param compress:        Decides if the video slice should be compressed by gzip.
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

      if not process_video(key, class_dir, start, end, compress=compress):
        failed_videos.append(key)

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

    if annotations["label"].lower() == class_name.lower():
      start = annotations["segment"][0]
      end = annotations["segment"][1]

      videos_queue.put((key, class_dir, start, end))
