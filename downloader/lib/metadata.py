import os


def get_valid_videos(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded videos.
  :param videos:        The list of video metadata.
  :param root:          Videos root.
  :param class_dirs:    Expect videos to be located in folders named after their classes (e.g. jogging/0123.mp4).
  :return:              List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():

    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, video_id + ".mp4")
    else:
      cls = ""
      video_path = os.path.join(root, video_id + ".mp4")

    if os.path.isfile(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def get_valid_frames(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded video frames.
  :param videos:        The list of video metadata.
  :param root:          Video frames root.
  :param class_dirs:    Expect frames to be located in folders named after their classes
                        (e.g. jogging/0123/frame0.jpg ...).
  :return:              List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():
    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, video_id)
    else:
      cls = ""
      video_path = os.path.join(root, video_id)

    if os.path.isdir(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def get_valid_sound(videos, root, class_dirs=True):
  """
  Go through a list of videos and find all downloaded video sound tracks.
  :param videos:    The list of video metadata.
  :param root:          Video sounds root.
  :param class_dirs:    Expect sounds to be located in folders named after their classes (e.g. jogging/0123.mp3).
  :return:              List of valid video ids for each class.
  """

  valid_videos = {}

  for video_id in videos.keys():
    if class_dirs:
      cls = videos[video_id]["annotations"]["label"]
      cls_path = cls.replace(" ", "_")
      video_path = os.path.join(root, cls_path, "{}.mp3".format(video_id))
    else:
      cls = ""
      video_path = os.path.join(root, "{}.mp3".format(video_id))

    if os.path.isfile(video_path):
      if cls in valid_videos:
        valid_videos[cls].append(video_id)
      else:
        valid_videos[cls] = [video_id]

  return valid_videos

def class_keys_to_video_id_keys(videos):
  """
  Transform a dictionary with keys = classes, values = video lists to a dictionary where key = video id, value = class.
  :param videos:    Dictionary with classes as keys.
  :return:          Dictionary with video ids as keys.
  """

  new_videos = {}

  for cls, vids in videos.items():
    for vid in vids:
      new_videos[vid] = cls

  return new_videos
