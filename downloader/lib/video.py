import cv2, os, subprocess

def video_to_jpgs(video_path, save_path, do_resize=True, shorter_side=256):
  """
  Extract individual frames from a video.
  :param video_path:          Path to the video file.
  :param save_path:           Path to a directory where to save the video frames.
  :param do_resize:           Resize the frames.
  :param shorter_side:        If do_resize, shorter side will be resized to this value.
  :return:                    True if extraction successful, otherwise false.
  """

  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
    return False

  i = 0
  res, frame = cap.read()

  while res:
    if do_resize:
      frame = resize(frame, shorter_side=shorter_side)

    cv2.imwrite(os.path.join(save_path, "frame{:d}.jpg".format(i)), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
    res, frame = cap.read()
    i += 1

  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  num_images = len(os.listdir(save_path))

  return num_frames == num_images

def video_has_sound(source):
  """
  Check if video contains sound.
  :param source:      Path to the video file.
  :return:            True if the video contains sound, otherwise false.
  """

  # check if the video contains sound
  cmd1 = ["ffprobe", "-i", source, "-show_streams", "-select_streams", "a", "-loglevel", "error"]

  try:
    output = subprocess.check_output(cmd1)
  except subprocess.CalledProcessError:
    return False

  if output is None:
    return False

  output = output.decode()
  output = output.split("\n")

  if output[0] != "[STREAM]":
    return False

  return True

def video_to_sound(source, target):
  """
  Extract the sound track from a video.
  :param source:    Path to a video.
  :param target:    Where to save the extracted sound file.
  :return:          True if conversion succeeded, otherwise false.
  """

  # convert video to sound
  cmd2 = ["ffmpeg", "-i", source, target]

  try:
    subprocess.check_call(cmd2)
  except subprocess.CalledProcessError:
    return False

  return True

def resize(frame, shorter_side=256):
  """
  Resize a frame using OpenCV.
  :param frame:           A single video frame.
  :param shorter_side:    Size of the target shorter side, longer side will be computed so that the aspect ratio
                          is preserved.
  :return:                Resized frame.
  """

  if frame.shape[0] > frame.shape[1]:
    long = frame.shape[0]
    short = frame.shape[1]
  else:
    short = frame.shape[0]
    long = frame.shape[1]

  fract = shorter_side / short
  target_long = int(long * fract)

  if frame.shape[0] > frame.shape[1]:
    return cv2.resize(frame, (shorter_side, target_long))
  else:
    return cv2.resize(frame, (target_long, shorter_side))

